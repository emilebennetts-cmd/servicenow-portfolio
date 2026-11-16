'use strict';
const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const model=require('../diagnostic-envelope-assurance-model.js');
const html=fs.readFileSync(path.join(__dirname,'..','diagnostic-envelope-assurance-lab.html'),'utf8');
test('15 distinct synthetic failure-mode cases, eight immutable native HOLD gates',()=>{
 assert.equal(model.cases.length,15);assert.equal(new Set(model.cases.map(x=>x.id)).size,15);
 assert.equal(model.nativeGates.length,8);assert.equal(new Set(model.nativeGates.map(x=>x.id)).size,8);
 assert.ok(model.nativeGates.every(x=>/^DEA-N0[1-8]$/.test(x.id)));
 for(const x of model.cases){
  const r=model.assess(x.id);assert.equal(r.decision,x.expected);assert.equal(r.release_decision,'HOLD');
  assert.equal(r.evidence_class,'MOCK-ONLY');assert.equal(r.native_execution,'NOT RUN');
  assert.equal(r.dev_verified,false);assert.equal(r.production_verified,false);assert.equal(r.screenshot_approved,false);
 }
});
test('absent DIAG wrapper or reversed, duplicated markers fail closed',()=>{
 const good=model.fixture('valid');
 assert.throws(()=>model.parse(good.replace('DIAG_ENVELOPE_END','INVALID_END')));
 assert.throws(()=>model.parse(good+'DIAG_ENVELOPE_BEGIN'));
 assert.throws(()=>model.parse('DIAG_ENVELOPE_END\n'+good));
 assert.throws(()=>model.parse('a'.repeat(24577)));
});
test('read-only/PII/schema violations reject; not-applicable is not a healthy zero',()=>{
 assert.equal(model.assess('schema').decision,'REJECT');
 assert.equal(model.assess('write').decision,'REJECT');
 assert.equal(model.assess('pii').decision,'REJECT');
 assert.equal(model.assess('sensitive').decision,'REJECT');
 assert.equal(model.assess('not-applicable').decision,'NOT_APPLICABLE');
 assert.equal(model.assess('zero').decision,'REVIEW');
 assert.equal(model.assess('capped').decision,'INCOMPLETE');
 assert.equal(model.assess('valid').decision,'CAN_REVIEW');
});
test('source contract separates output groups from the incident population',()=>{
 const env=model.parse(model.fixture('valid'));
 assert.equal(env.record_count,env.results.length);
 assert.equal(env.record_count,1);assert.equal(env.metrics.total,120);
 assert.equal(model.assess('no-groups').decision,'CAN_REVIEW');
 assert.equal(model.assess('zero').decision,'REVIEW');
 assert.equal(model.assess('count-drift').decision,'INCOMPLETE');
});
test('adversarial payloads fail closed without publishing or certifying records',()=>{
 for(const key of ['payload-injection','unsafe-result','malformed-note'])assert.equal(model.assess(key).decision,'REJECT');
 assert.equal(model.assess('open-over-total').decision,'INCOMPLETE');
 const env=model.parse(model.fixture('valid'));
 env.results.push({kind:'state_breakdown',field:'state',value:'person@example.invalid',count:1});
 const wrap=x=>'DIAG_ENVELOPE_BEGIN\\n'+JSON.stringify(x)+'\\nDIAG_ENVELOPE_END';
 assert.equal(model.evaluate(wrap(env)).decision,'REJECT');
});
test('denominator drift and non-finite or malformed metrics cannot be accepted',()=>{
 const e=model.parse(model.fixture('valid'));
 e.record_count=12;
 const wrap=x=>'DIAG_ENVELOPE_BEGIN\n'+JSON.stringify(x)+'\nDIAG_ENVELOPE_END';
 assert.equal(model.evaluate(wrap(e)).decision,'INCOMPLETE');
 e.metrics.total='120';
 assert.equal(model.evaluate(wrap(e)).decision,'REJECT');
});
test('exports contain only synthetic metadata, 15+8 HOLD rows and no private fields',()=>{
 const a=model.exportCases(),b=model.exportNativeGates();
 assert.equal(a.split('\r\n').filter(Boolean).length,16);
 assert.equal(b.split('\r\n').filter(Boolean).length,9);
 assert.equal((a.match(/"HOLD"/g)||[]).length,15);
 assert.equal((b.match(/"HOLD"/g)||[]).length,8);
 for(const token of ['sys_id','instance_url','user_email','captured_at','consumer_record','bearer','api_key']){assert.doesNotMatch(a,new RegExp(token,'i'));assert.doesNotMatch(b,new RegExp(token,'i'));}
 assert.equal((b.match(/"NOT RUN"/g)||[]).length,8);
});
test('public lab has accessible controls, no data entry or network calls',()=>{
 for(const token of ['id="scenario"','id="decision" role="status" aria-live="polite"','id="download-examples"','id="download-gates"','NOT A SERVICENOW SCREENSHOT','SOURCE-ONLY','MOCK-ONLY','DEV-VERIFIED','PRODUCTION-VERIFIED',"connect-src 'none'"]){assert.ok(html.includes(token),token);}
 for(const text of [html,fs.readFileSync(path.join(__dirname,'..','diagnostic-envelope-assurance-model.js'),'utf8')]){
  assert.doesNotMatch(text,/fetch\s*\(|XMLHttpRequest|localStorage|indexedDB|document\.cookie|<iframe|<img\b/);
 }
 assert.throws(()=>model.assess('production'),/Unknown synthetic/);
});
