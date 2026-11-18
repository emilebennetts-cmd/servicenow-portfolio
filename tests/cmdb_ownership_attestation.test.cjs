"use strict";
const test=require("node:test");
const assert=require("node:assert/strict");
const fs=require("node:fs");
const path=require("node:path");
const gate=require("../cmdb-ownership-attestation-model.js");
const page=fs.readFileSync(path.join(__dirname,"..","cmdb-ownership-attestation-lab.html"),"utf8");

test("six unique advisory gates and six fixed synthetic cases",()=>{
 assert.equal(gate.GATES.length,6);assert.equal(new Set(gate.GATES.map(x=>x.id)).size,6);
 assert.equal(gate.CASES.length,6);assert.equal(new Set(gate.CASES.map(x=>x.id)).size,6);
});
test("all scenarios retain HOLD / NOT RUN / MOCK-ONLY",()=>{
 for(const item of gate.CASES){
   const v=gate.evaluate(item.id);
   assert.equal(v.controls.length,6);assert.equal(v.releaseStatus,"HOLD");
   assert.equal(v.nativeStatus,"NOT RUN");assert.equal(v.evidenceClass,"MOCK-ONLY");
   assert(v.controls.every(x=>["SIMULATED READY","REQUIRES REVIEW"].includes(x.disposition)));
 }
});
test("missing owner and support prevent native candidacy",()=>{
 const v=gate.evaluate("missing-owner");
 assert.equal(v.ready,false);assert.equal(v.controls.find(x=>x.id==="business_owner").passed,false);
 assert.equal(v.controls.find(x=>x.id==="support_owner").passed,false);
});
test("source conflict and criticality gap fail separately",()=>{
 for(const [id,key] of [["source-conflict","source_authority"],["criticality-gap","criticality"]]){
  const v=gate.evaluate(id);assert.equal(v.ready,false);assert.equal(v.controls.find(x=>x.id===key).passed,false);
 }
});
test("90-day illustrative recency rule rejects the expired scenario",()=>{
 assert.equal(gate.REVIEW_DAYS,90);
 const v=gate.evaluate("stale-attestation");assert.equal(v.controls.find(x=>x.id==="recency").passed,false);
});
test("independent reviewer mismatch holds release",()=>{
 const v=gate.evaluate("self-approval");assert.equal(v.ready,false);
 assert.equal(v.controls.find(x=>x.id==="independent_review").passed,false);
});
test("fully green scenario remains a non-certifying candidate",()=>{
 const v=gate.evaluate("ready-candidate");assert.equal(v.ready,true);
 assert.equal(v.result,"CANDIDATE FOR NATIVE REVIEW");
 assert.equal(v.releaseStatus,"HOLD");assert.equal(v.nativeStatus,"NOT RUN");
});
test("unknown scenario is rejected, not treated as passed",()=>{
 assert.throws(()=>gate.evaluate("a-client-ci"),/Unknown synthetic scenario/);
 assert.throws(()=>gate.toCSV("a-client-ci"),/Unknown synthetic scenario/);
});
test("CSV has six rows and cannot leak identity, customer or DEV approvals",()=>{
 for(const c of gate.CASES){
 const csv=gate.toCSV(c.id);
 assert.equal(csv.trim().split("\r\n").length,7);
 assert.equal((csv.match(/"HOLD"/g)||[]).length,6);
 assert.equal((csv.match(/"NOT RUN"/g)||[]).length,6);
 assert.equal((csv.match(/"MOCK-ONLY"/g)||[]).length,6);
 assert(!/sys_id|instance_url|credentials|customer_id|screenshot_url|production_verified/i.test(csv));
 }
});
test("public HTML explicitly labels simulation, contains local-only CSP and mobile layout",()=>{
 assert.match(page,/MOCK-ONLY interactive examples/);
 assert.match(page,/connect-src 'none'/);
 assert.match(page,/@media\(max-width:480px\)/);
 assert.match(page,/CMDBOwnerGate/);
 assert.match(page,/src="\.\/cmdb-ownership-attestation-model\.js"/);
 assert.doesNotMatch(page,/https?:\/\/(?!www\.w3\.org)/i);
});
