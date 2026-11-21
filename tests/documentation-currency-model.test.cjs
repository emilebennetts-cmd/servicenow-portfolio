"use strict";
const test=require("node:test");
const assert=require("node:assert/strict");
const m=require("../documentation-currency-model.js");
test("four immutable public document identities",()=>{
  assert.equal(m.docs.length,4);
  assert.equal(new Set(m.docs.map(d=>d.id)).size,4);
  assert.ok(m.docs.every(d=>Object.isFrozen(d)));
});
test("September document is not current October architecture",()=>{
  const rows=m.rows("4.22.2");
  assert.equal(rows.find(x=>x.id==="ASBUILT-SEP30").alignment,"DOCUMENT DRIFT");
  assert.equal(rows.find(x=>x.id==="TRAINING-SEP30").alignment,"DOCUMENT DRIFT");
  assert.equal(rows.find(x=>x.id==="ARCH-OCT19").alignment,"SNAPSHOT MATCH");
});
test("older snapshot is retained without certifying newer architecture",()=>{
  assert.equal(m.rows("4.6.1").find(x=>x.id==="ARCH-OCT19").alignment,"DOCUMENT DRIFT");
  assert.equal(m.rows("4.6.1").filter(x=>x.alignment==="SNAPSHOT MATCH").length,2);
});
test("fictional diagnostic runbook remains unversioned regardless of selection",()=>{
  for(const target of m.versions)assert.equal(m.rows(target).find(x=>x.id==="DIAG-DEMO").alignment,"UNVERSIONED / SHOWCASE");
});
test("matching document is never native acceptance or publication approval",()=>{
  for(const target of m.versions)for(const row of m.rows(target)){
    assert.equal(row.decision,"HOLD");
    assert.equal(row.nativeVerification,"NOT RUN");
    assert.equal(row.publication,"NOT AUTHORISED");
  }
});
test("unknown target fails closed",()=>{
  for(const value of ["prod","latest","4.22.3","","4.6.1;DROP",null])assert.throws(()=>m.rows(value),/Unsupported evidence target/);
  assert.throws(()=>m.csv("production"));
});
test("CSV is minimal, four rows, HOLD-only and contains no instance/customer identifiers",()=>{
  const csv=m.csv("4.22.2");
  assert.equal(csv.trim().split("\r\n").length,5);
  assert.equal((csv.match(/"HOLD"/g)||[]).length,4);
  assert.equal((csv.match(/"NOT RUN"/g)||[]).length,4);
  assert.doesNotMatch(csv,/https?:|@[^\s]+\.|sys_id|dev438211|DemoClient23|customer|approved\s+production/i);
});
test("public document snapshot has no private URLs or source code",()=>{
  const serialized=JSON.stringify(m.docs);
  assert.doesNotMatch(serialized,/github\.com|drive\.google\.com|docs\.google\.com|client|password|sys_id|x_1577958/i);
});