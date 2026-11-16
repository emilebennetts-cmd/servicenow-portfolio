'use strict';
const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const model=require('../diagnostic-lineage-review.js');
const html=fs.readFileSync(path.join(__dirname,'..','diagnostic-coverage-explorer.html'),'utf8');

test('module-pack and Knowledge Intelligence catalogues remain different source inventories',()=>{
 assert.equal(model.tracks.length,2);
 const a=model.getTrack('module'),b=model.getTrack('knowledge');
 assert.equal(a.counts.find(([k])=>k==='Module-pack collectors')[1],'20');
 assert.equal(b.counts.find(([k])=>k==='Read-only collectors')[1],'45');
 assert.match(a.envelope,/DIAG_ENVELOPE_BEGIN/);
 assert.match(b.envelope,/KI-EVIDENCE-BEGIN/);
 assert.notEqual(a.envelope,b.envelope);
 assert.notEqual(a.provenance,b.provenance);
 assert.throws(()=>model.getTrack('combined'),/Unknown catalogue identity/);
});
test('all isolated native review controls retain NOT RUN and HOLD',()=>{
 for(const key of ['module','knowledge']){
  const report=model.evaluate(key);
  assert.equal(report.rows.length,6);
  assert.equal(report.release,'HOLD');assert.equal(report.native_executed,0);
  assert.equal(report.dev_verified,0);assert.equal(report.production_verified,0);
  assert.ok(report.rows.every(r=>r.evidence_class==='SOURCE-ONLY'&&r.execution==='NOT RUN'&&r.review==='UNREVIEWED'&&r.release==='HOLD'&&r.dev_verified===false&&r.screenshot_approved===false));
 }
});
test('combined review exports twelve unique source-traced controls, never merges evidence contracts',()=>{
 const report=model.evaluate('both');
 assert.equal(report.rows.length,12);
 assert.equal(new Set(report.rows.map(x=>x.control_id)).size,12);
 assert.deepEqual(report.rows.slice(0,6).map(x=>x.control_id),['DLC-M01','DLC-M02','DLC-M03','DLC-M04','DLC-M05','DLC-M06']);
 assert.deepEqual(report.rows.slice(6).map(x=>x.control_id),['DLC-K01','DLC-K02','DLC-K03','DLC-K04','DLC-K05','DLC-K06']);
 const csv=model.exportCsv(report);
 assert.equal(csv.split('\r\n').filter(Boolean).length,13);
 assert.match(csv,/SOURCE-ONLY/);assert.match(csv,/NOT RUN/);assert.match(csv,/HOLD/);
 assert.doesNotMatch(csv,/sys_id|instance_url|customer_name|email_address|login_password/i);
});
test('unknown tracks and altered control status or source fields fail closed',()=>{
 assert.throws(()=>model.evaluate('native'),/Unknown catalogue identity/);
 const report=model.evaluate('both');
 assert.throws(()=>model.exportCsv({...report,rows:report.rows.slice(1)}),/Source row count changed/);
 assert.throws(()=>model.exportCsv({...report,rows:report.rows.map((r,i)=>i===0?{...r,release:'GO'}:r)}),/Source assertion changed/);
 assert.throws(()=>model.exportCsv({...report,rows:report.rows.map((r,i)=>i===0?{...r,required_native_evidence:'all passed'}:r)}),/Source assertion changed/);
 assert.throws(()=>model.exportCsv({selection:'production',rows:report.rows}),/Invalid lineage report/);
});
test('responsive catalogue controls are accessible and acknowledge screenshot/DEV status',()=>{
 assert.match(html,/id="lineage-review"/);assert.match(html,/id="lineage-track"/);
 assert.match(html,/id="lineage-gates"/);assert.match(html,/id="lineage-status"[^>]*role="status"[^>]*aria-live="polite"/);
 assert.match(html,/diagnostic-lineage-review\.js/);
 assert.match(html,/NOT A SERVICENOW SCREENSHOT/);
 assert.match(html,/Source lineage/);
 assert.match(html,/max-width:680px/);
 assert.doesNotMatch(html,/<iframe\b/i);
});
