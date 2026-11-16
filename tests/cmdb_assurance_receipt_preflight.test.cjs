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
  const row=table[1],date=new Date(Date.now()-86400000).toISOString().replace(".000","");
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
  assert.equal(preflight.audit(edited(t=>{candidate(t);t[1][16]=new Date(Date.now()+86400000).toISOString().replace(".000","");}),tower,rows).valid,false);
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
  for(const token of ['id="native-receipt-preflight"','id="tower-receipt-file"','id="tower-receipt-status"','id="tower-receipt-issues"','cmdb-assurance-receipt-preflight.js','connect-src \'none\'',"no upload","DEV-VERIFIED 0","PRODUCTION-VERIFIED 0"])assert.ok(html.includes(token),token);
  assert.doesNotMatch(js,/localStorage|sessionStorage|indexedDB|XMLHttpRequest|fetch\s*\(|sendBeacon|WebSocket|<script/i);
  assert.doesNotMatch(html,/<img\b|<iframe\b|<form\b/i);
});
