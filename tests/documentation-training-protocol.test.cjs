"use strict";
const test=require("node:test");
const assert=require("node:assert/strict");
const fs=require("node:fs");
const path=require("node:path");
const model=require("../documentation-currency-model.js");

test("fifteen source-backed controls have unique stable IDs, five personas and three per role",()=>{
 assert.equal(model.protocols.length,15);
 assert.equal(new Set(model.protocols.map(p=>p.id)).size,15);
 assert.ok(model.protocols.every(Object.isFrozen));
 for(const role of model.personas)assert.equal(model.protocols.filter(p=>p.persona===role.id).length,3);
});
test("two source snapshots retain identical test designs without implying current DEV alignment",()=>{
 for(const release of model.versions){
  const all=model.protocolRows(release);
  assert.equal(all.length,15);
  assert.ok(all.every(p=>Object.isFrozen(p)));
  assert.ok(all.every(p=>p.referenceRelease===release && p.classification==="SOURCE-ONLY" &&
   p.execution==="NOT RUN" && p.approval==="HOLD" && p.production==="NOT VERIFIED" &&
   p.screenshot==="NOT AUTHORISED"));
  assert.ok(all.every(p=>p.expected.length>45 && p.negative.length>35 &&
   p.source.includes("§") && p.entitlement.length>15));
  for(const persona of model.personas)assert.equal(model.protocolRows(release,persona.id).length,3);
 }
});
test("unsupported release and persona fail closed for rows and CSV",()=>{
 for(const bad of ["production","latest","",null,{},["4.22.2"]]){
  assert.throws(()=>model.protocolRows(bad));
  assert.throws(()=>model.protocolCsv(bad));
 }
 for(const bad of ["admin","__proto__","all-roles","",null]){
  assert.throws(()=>model.protocolRows("4.22.2",bad));
  assert.throws(()=>model.protocolCsv("4.22.2",bad));
 }
});
test("exports are formula-safe, include negative testing and never claim acceptance",()=>{
 for(const release of model.versions){
  for(const persona of ["all",...model.personas.map(p=>p.id)]){
   const csv=model.protocolCsv(release,persona);
   const expected=persona==="all"?15:3;
   assert.equal(csv.trim().split("\r\n").length,expected+1);
   assert.equal((csv.match(/"NOT RUN"/g)||[]).length,expected);
   assert.equal((csv.match(/"HOLD"/g)||[]).length,expected);
   assert.equal((csv.match(/"SOURCE-ONLY"/g)||[]).length,expected);
   assert.match(csv,/"Required negative control"/);
   assert.doesNotMatch(csv,/"PASS"|"APPROVED"|"DEV-verified"|"production-verified"/i);
  }
 }
});
test("no private URL, customer reference, sensitive tokens or instance credentials in public model",()=>{
 const raw=JSON.stringify(model.protocols);
 assert.doesNotMatch(raw,/https?:|(?:drive|docs)\.google\.com|github\.com|dev438211|DemoClient23|sys_id|x_1577958|@[\w.-]+|client_secret|-----BEGIN/i);
});
test("public page exposes keyboard-accessible native navigator but no sign-off action",()=>{
 const html=fs.readFileSync(path.resolve(__dirname,"../documentation-currency-gate.html"),"utf8");
 for(const marker of ['id="native-training-controls"','id="protocol-filter"','id="protocol-export"',
  'id="protocol-count"','id="protocol-list"',"function drawProtocols()","model.protocolRows","model.protocolCsv"])
  assert.ok(html.includes(marker),marker+" missing");
 assert.match(html,/native execution NOT RUN/i);
 assert.match(html,/no instance or account is connected/i);
 assert.ok(!/<input[^>]+type=["']?checkbox/i.test(html),"Native gate must not expose fake checkbox approval");
});
