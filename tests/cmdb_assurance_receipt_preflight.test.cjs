"use strict";
const test=require("node:test"),assert=require("node:assert/strict"),fs=require("node:fs"),path=require("node:path");
const tower=require("../cmdb-assurance-control-tower.js");
const preflight=require("../cmdb-assurance-receipt-preflight.js");
const deps={ire:require("../cmdb-source-acceptance.js"),tags:require("../cmdb-tag-governance-model.js"),health:require("../cmdb-health-assurance-model.js"),relationships:require("../cmdb-relationship-assurance-model.js"),lifecycle:require("../cmdb-data-manager-policy-model.js")};
const rows=tower.createRows(deps);
const exported=()=>tower.planCsv(rows);
const encode=table=>table.map(row=>row.map(c=>'"'+String(c).replace(/"/g,'""')+'"').join(",")).join("\r\n")+"\r\n";
const edited=fn=>{const table=preflight.parseCsv(exported());fn(table);return encode(table);};
const candidate=(table)=>{
  const row=table[1],date=new Date(Date.now()-86400000).toISOString().slice(0,19)+"Z";
  row.splice(10,9,"PASS","HOLD","DEV-REPORTED","syntheticdev","Zurich","builder01",date,"EV-TEST-0001","reviewer01");
};
test("exact 117-row default HOLD export passes metadata structure but never certifies DEV",()=>{
  const parsed=preflight.parseCsv("\ufeff"+exported());
  assert.equal(parsed.length,118);
  assert.deepEqual(parsed[0],preflight.HEADERS);
  const result=preflight.audit(exported(),tower,rows);
  assert.equal(result.valid,true);
  assert.equal(result.hold,true);assert.equal(result.certified,false);
  assert.equal(result.pending,117);
  assert.equal(result.reviewMetadataComplete,0);
  assert.equal(result.passReported,0);
  assert.match(result.message,/HOLD/);
});
test("one reported candidate must still remain HOLD and DEV-REPORTED, never DEV-VERIFIED",()=>{
  const result=preflight.audit(edited(candidate),tower,rows);
  assert.equal(result.valid,true);
  assert.equal(result.pending,116);
  assert.equal(result.passReported,1);
  assert.equal(result.reviewMetadataComplete,1);
  assert.equal(result.certified,false);
  assert.match(result.message,/no DEV or Production execution has been independently verified/);
});
test("candidate without distinct reviewer, timestamp, receipt or target metadata fails closed",()=>{
  for(const col of [13,14,15,16,17,18]){
    const result=preflight.audit(edited(t=>{candidate(t);t[1][col]="";}),tower,rows);
    assert.equal(result.valid,false,"column "+col);
    assert.equal(result.hold,true);
    assert.ok(result.issues.some(i=>i.id===rows[0].id),"column "+col);
  }
  const same=preflight.audit(edited(t=>{candidate(t);t[1][18]="builder01";}),tower,rows);
  assert.equal(same.valid,false);
});
test("changed native source action, duplicate ID, missing row and extra row are rejected",()=>{
  assert.equal(preflight.audit(edited(t=>{t[1][8]="UNREVIEWED ACTION";}),tower,rows).valid,false);
  assert.equal(preflight.audit(edited(t=>{t[2][6]=t[1][6];t[2][1]=t[1][1];}),tower,rows).valid,false);
  assert.equal(preflight.audit(edited(t=>{t.pop();}),tower,rows).valid,false);
  assert.equal(preflight.audit(edited(t=>{t.push([...t[1]]);}),tower,rows).valid,false);
});
test("release GO, unsupported class and future timestamp cannot be laundering into verified",()=>{
  assert.equal(preflight.audit(edited(t=>{t[1][11]="GO";}),tower,rows).valid,false);
  assert.equal(preflight.audit(edited(t=>{candidate(t);t[1][12]="DEV-VERIFIED";}),tower,rows).valid,false);
  assert.equal(preflight.audit(edited(t=>{candidate(t);t[1][16]=new Date(Date.now()+86400000).toISOString().slice(0,19)+"Z";}),tower,rows).valid,false);
  assert.equal(preflight.audit(edited(t=>{t[0][1]="Different domain";}),tower,rows).valid,false);
});
test("malformed and oversized CSV fail safely without exposing input",()=>{
  for(const malformed of ['"unterminated','a,b\n','"x"oops\n', "x".repeat(preflight.MAX_BYTES+1)]){
    assert.equal(preflight.audit(malformed,tower,rows).valid,false);
  }
  assert.throws(()=>preflight.parseCsv('"a"oops,b'),/Unexpected/);
});
test("offline UI discloses native HOLD, no network or persistent storage",()=>{
  const html=fs.readFileSync(path.join(__dirname,"..","cmdb-assurance-control-tower.html"),"utf8");
  const js=fs.readFileSync(path.join(__dirname,"..","cmdb-assurance-receipt-preflight.js"),"utf8");
  for(const token of ['id="native-receipt-preflight"','id="tower-receipt-file"','id="tower-receipt-status"','id="tower-receipt-issues"','id="tower-receipt-stage-body"','id="tower-receipt-stage-export"','cmdb-assurance-receipt-preflight.js','connect-src \'none\'',"no upload","DEV-VERIFIED 0","PRODUCTION-VERIFIED 0"])assert.ok(html.includes(token),token);
  assert.doesNotMatch(js,/localStorage|sessionStorage|indexedDB|XMLHttpRequest|fetch\s*\(|sendBeacon|WebSocket|<script/i);
  assert.doesNotMatch(html,/<img\b|<iframe\b|<form\b/i);
});


test("five-stage aggregate triage reconciles all 117 public source controls without certification",()=>{
  const r=preflight.stageTriage(exported(),tower,rows);
  assert.equal(r.parsed,true);assert.equal(r.inspected.valid,true);
  assert.equal(r.hold,true);assert.equal(r.certified,false);
  assert.deepEqual(r.stages.map(s=>s.expected),[18,25,24,30,20]);
  assert.deepEqual(r.stages.map(s=>s.matched),[18,25,24,30,20]);
  assert.deepEqual(r.stages.map(s=>s.pending),[18,25,24,30,20]);
  assert.ok(r.stages.every(s=>s.release==="HOLD"&&s.missing===0&&s.drift===0));
  const csv=preflight.stageCsv(r);
  assert.equal(csv.trim().split(/\r?\n/).length,6);
  assert.match(csv,/NOT INDEPENDENTLY VERIFIED/);
  assert.doesNotMatch(csv,/instance|syntheticdev|EV-TEST/i);
});
test("reported PASS, FAIL and BLOCKED never promote native acceptance",()=>{
  const input=edited(t=>{
    candidate(t);
    t[2].splice(10,9,"FAIL","HOLD","DEV-REPORTED","syntheticdev","Zurich","builder01",t[1][16],"EV-TEST-0002","reviewer01");
    t[3].splice(10,9,"BLOCKED","HOLD","DEV-REPORTED","syntheticdev","Zurich","builder01",t[1][16],"EV-TEST-0003","reviewer01");
  });
  const r=preflight.stageTriage(input,tower,rows);
  assert.equal(r.parsed,true);
  assert.equal(r.stages[0].passReported,1);
  assert.equal(r.stages[0].failReported,1);
  assert.equal(r.stages[0].blockedReported,1);
  assert.equal(r.stages[0].pending,15);
  assert.equal(r.inspected.certified,false);assert.ok(r.stages.every(s=>s.release==="HOLD"));
  assert.match(preflight.stageCsv(r),/REVIEW ISSUES|FORMAT CHECK ONLY/);
});
test("source changes and unknown IDs are counted without reflecting imported identifiers",()=>{
  const altered=edited(t=>{t[1][8]="UNREVIEWED SOURCE ACTION";t[2][6]="SECRET-CANARY-123";});
  const r=preflight.stageTriage(altered,tower,rows);
  assert.equal(r.parsed,true);
  assert.equal(r.inspected.valid,false);
  assert.equal(r.stages[0].matched,16);
  assert.equal(r.stages[0].drift,1);
  assert.equal(r.stages[0].missing,2);
  assert.equal(r.unmapped,1);
  assert.ok(r.inspected.issues.some(x=>x.id==="ROW-2"));
  assert.doesNotMatch(JSON.stringify(r.inspected.issues),/SECRET-CANARY/);
  const out=preflight.stageCsv(r);
  assert.doesNotMatch(out,/SECRET-CANARY|UNREVIEWED SOURCE ACTION/);
  assert.match(out,/REVIEW ISSUES/);
});
test("private candidate values cannot reach aggregate output and malformed imports cannot export",()=>{
  const input=edited(t=>{candidate(t);t[1][13]="private.example.com/secret/CANARY-999";});
  const r=preflight.stageTriage(input,tower,rows);
  assert.equal(r.inspected.valid,false);
  assert.equal(r.parsed,true);
  assert.doesNotMatch(JSON.stringify(r.stages)+preflight.stageCsv(r),/CANARY-999|private.example.com|reviewer01|builder01|EV-TEST-0001/);
  for(const malformed of ['"unterminated',exported().slice(0,100), "x".repeat(preflight.MAX_BYTES+1)]){
    const bad=preflight.stageTriage(malformed,tower,rows);
    assert.equal(bad.parsed,false);
    assert.throws(()=>preflight.stageCsv(bad),/HOLD/);
  }
});
