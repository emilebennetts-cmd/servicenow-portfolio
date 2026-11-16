'use strict';
const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const model=require('../diagnostic-coverage-gate.js');
const html=fs.readFileSync(path.join(__dirname,'..','diagnostic-coverage-explorer.html'),'utf8');

test('public source inventory maps to ten stable, distinct pack categories',()=>{
 assert.equal(model.packs.length,10);
 assert.equal(new Set(model.packs.map(p=>p.id)).size,10);
 assert.equal(new Set(model.packs.map(p=>p.label)).size,10);
 const catalog=[...html.matchAll(/class="record" data-domain="([^"]+)"/g)].map(m=>m[1].replace(/&amp;/g,'&'));
 assert.deepEqual(new Set(model.packs.map(p=>p.label)),new Set(catalog));
});
test('all four synthetic scenarios evaluate with immutable NOT RUN / HOLD / MOCK-ONLY boundaries',()=>{
 assert.deepEqual(model.profiles,['unassessed','mixed','denominator','complete']);
 for(const key of model.profiles){
  const r=model.evaluate(key);
  assert.equal(r.summary.total,10);
  assert.equal(r.summary.native_verified,0);
  assert.equal(r.summary.release,'HOLD');
  assert.ok(Object.isFrozen(r.rows));
  for(const row of r.rows){
   assert.equal(row.native_execution,'NOT RUN');assert.equal(row.release_decision,'HOLD');
   assert.equal(row.evidence_class,'MOCK-ONLY');assert.equal(row.dev_verified,false);
   assert.equal(row.production_verified,false);assert.equal(row.screenshot_approved,false);
  }
 }
});
test('no-evidence scenario keeps all ten packs NOT ASSESSED',()=>{
 const r=model.evaluate('unassessed');
 assert.equal(r.summary.reviewed_example,0);
 assert.equal(r.summary.blocked,10);
 assert.ok(r.rows.every(p=>p.code==='UNASSESSED'));
});
test('partial evidence retains entitlement, privacy, population and review blockers',()=>{
 const r=model.evaluate('mixed');
 for(const code of ['ENTITLEMENT_UNKNOWN','INVALID','CAPPED','REVIEW_PENDING','EXCLUDED'])assert.ok(r.rows.some(p=>p.code===code));
 assert.equal(r.summary.reviewed_example,2);
 assert.equal(r.summary.exclusions,1);
 assert.equal(r.summary.blocked,7);
});
test('one capped denominator blocks clean aggregate even with nine simulated reviews',()=>{
 const r=model.evaluate('denominator');
 assert.equal(r.summary.reviewed_example,9);assert.equal(r.summary.blocked,1);
 assert.equal(r.rows.filter(x=>x.code==='CAPPED').length,1);assert.equal(r.summary.release,'HOLD');
});
test('all simulated reviews still cannot certify native acceptance or change HOLD',()=>{
 const r=model.evaluate('complete');
 assert.equal(r.summary.reviewed_example,10);assert.equal(r.summary.blocked,0);
 assert.equal(r.summary.native_verified,0);
 assert.equal(r.summary.release,'HOLD');
 assert.ok(r.rows.every(x=>x.release_decision==='HOLD'));
});
test('export has exact ten canonical rows and no candidate/private evidence fields',()=>{
 const csv=model.exportCsv(model.evaluate('mixed'));
 assert.equal(csv.split('\r\n').filter(Boolean).length,11);
 assert.match(csv,/MOCK-ONLY/);assert.match(csv,/NOT RUN/);assert.match(csv,/HOLD/);
 for(const pack of model.packs)assert.ok(csv.includes(pack.id));
 assert.doesNotMatch(csv,/instance_url|sys_id|user_email|reviewer_name|approval_date|source_output/);
});
test('forged source controls or unknown scenarios fail closed',()=>{
 assert.throws(()=>model.evaluate('production'),/Unknown synthetic/);
 const real=model.evaluate('complete');
 const changed={...real,rows:real.rows.map((r,i)=>i===0?{...r,release_decision:'GO'}:r)};
 assert.throws(()=>model.exportCsv(changed),/integrity mismatch/);
 assert.throws(()=>model.exportCsv({scenario:'complete',rows:real.rows.slice(1)}),/Invalid report/);
});
test('HTML exposes accessible, source-declared mock demo and no remote collection',()=>{
 assert.match(html,/id="coverage-gate"/);assert.match(html,/diagnostic-coverage-gate\.js/);
 assert.match(html,/id="coverage-summary" role="status" aria-live="polite"/);
 assert.match(html,/ILLUSTRATIVE CONSOLE · NOT A SERVICENOW SCREENSHOT/);
 assert.match(html,/no ServiceNow subscription/);
 assert.doesNotMatch(html,/<iframe[^>]*>/i);
});
