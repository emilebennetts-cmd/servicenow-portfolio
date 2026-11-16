"use strict";
const test=require("node:test");
const assert=require("node:assert/strict");
const lab=require("../cmdb-health-assurance-model.js");

test("four distinct synthetic CMDB Health cases and 24 unique native gates",()=>{
  assert.equal(lab.scenarios.length,4);
  assert.equal(lab.gates.length,24);
  assert.equal(new Set(lab.gates.map(g=>g.id)).size,24);
  assert.deepEqual(lab.scenarios.map(s=>lab.rows(s.id).length),[6,6,6,6]);
  assert.deepEqual(lab.scenarios.map(s=>s.theme),["Completeness","Correctness","Compliance","Relationship health"]);
});
test("every scenario remains MOCK ONLY and release HOLD",()=>{
  for(const s of lab.scenarios){
    const verdict=lab.assess(s.id);
    assert.equal(verdict.status,"NOT RUN");
    assert.equal(verdict.decision,"HOLD");
    assert.equal(verdict.evidence,"MOCK-ONLY");
    assert.ok(verdict.risk.length>=3);
  }
  assert.equal(lab.scenario("unknown"),null);
  assert.throws(()=>lab.assess("unknown"),/Unknown health scenario/);
});
test("24-gate DEV worksheet cannot invent execution receipts",()=>{
  const data=lab.rows("all");
  assert.equal(data.length,24);
  for(const row of data){
    assert.equal(row.length,lab.headers.length);
    assert.deepEqual(row.slice(4,7),["NOT RUN","HOLD","MOCK-ONLY"]);
    assert.ok(row.slice(7).every(v=>v===""));
  }
  assert.equal(lab.csv("all").trim().split("\r\n").length,25);
  assert.equal(lab.csv("jobs").trim().split("\r\n").length,7);
  assert.throws(()=>lab.csv("invalid"),/Unknown export selector/);
});
test("spreadsheet injection neutralisation and no private instance/PII in gates",()=>{
  const result=lab.csv("all");
  assert.doesNotMatch(result,/(dev\d+|[a-f0-9]{32}|password|bearer\s|@example\.com)/i);
  assert.ok(result.includes('"CH-JOB-01"'));
  assert.ok(result.includes('"CH-REL-06"'));
});