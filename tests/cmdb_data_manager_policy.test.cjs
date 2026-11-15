"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const model = require("../cmdb-data-manager-policy-model.js");
test("20 unique DEV controls in four five-control policy scenarios",()=>{
  assert.equal(model.checks.length,20);
  assert.equal(new Set(model.checks.map(x=>x.id)).size,20);
  for(const s of model.scenarios) assert.equal(model.rows(s.id).length,5);
});
test("synthetic readiness cannot be mistaken for native acceptance",()=>{
  for(const s of model.scenarios){
    const a=model.assess(s.id);
    assert.equal(a.nativeStatus,"NOT RUN");
    assert.equal(a.evidenceClass,"MOCK-ONLY");
    assert.ok(["HOLD","REVIEW REQUIRED"].includes(a.readiness));
  }
  assert.equal(model.assess("retire").readiness,"HOLD");
  assert.equal(model.assess("archive").readiness,"REVIEW REQUIRED");
  assert.equal(model.assess("delete").readiness,"HOLD");
  assert.match(model.assess("delete").blockers.join(";"),/preservation hold/i);
  assert.equal(model.assess("attest").readiness,"HOLD");
});
test("every CSV row is immutable HOLD and empty of private execution fields",()=>{
  const all=model.rows("all");
  assert.equal(all.length,20);
  for(const row of all){
    assert.equal(row.length,model.headers.length);
    assert.deepEqual(row.slice(4,7),["NOT RUN","HOLD","MOCK-ONLY"]);
    assert.ok(row.slice(7).every(v=>v===""));
  }
  assert.equal(model.toCsv("all").trim().split("\r\n").length,21);
  assert.equal(model.toCsv("archive").trim().split("\r\n").length,6);
});
test("no unknown scenario can be silently substituted",()=>{
  assert.equal(model.getScenario("unknown"),null);
  assert.throws(()=>model.assess("unknown"),/Unknown scenario/);
  assert.throws(()=>model.toCsv("unknown"),/Unknown export scenario/);
});
test("static controls do not carry CI IDs, contact details or API credentials",()=>{
  const raw=JSON.stringify(model.rows("all"));
  assert.doesNotMatch(raw,/sys_id|bearer\s|password|service-now\.com|@example\.com/i);
});
