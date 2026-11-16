"use strict";
const test=require("node:test");
const assert=require("node:assert/strict");
const fs=require("node:fs");
const path=require("node:path");
const lab=require("../cmdb-health-assurance-model.js");

test("four distinct synthetic numerator/denominator investigations",()=>{
  assert.deepEqual(lab.cohortScenarios.map(x=>x.id),["remediated","denominator","rule-change","incomplete"]);
  assert.equal(new Set(lab.cohortScenarios.map(x=>x.id)).size,4);
  const expected=[{delta:12,comparable:true},{delta:17.5,comparable:false},{delta:15,comparable:false},{delta:12,comparable:false}];
  lab.cohortScenarios.forEach((s,i)=>{
    const result=lab.compareCohort(s.id);
    assert.equal(result.delta,expected[i].delta);
    assert.equal(result.comparable,expected[i].comparable);
    assert.equal(result.nativeStatus,"NOT RUN");
    assert.equal(result.releaseDecision,"HOLD");
    assert.equal(result.evidence,"MOCK-ONLY");
  });
});

test("denominator shrinkage and changed rule invalidate positive percentage headlines",()=>{
  const scope=lab.compareCohort("denominator");
  assert.equal(scope.before,70);
  assert.equal(scope.after,87.5);
  assert.ok(scope.reasons.some(s=>/denominator changed/i.test(s)));
  assert.ok(scope.reasons.some(s=>/membership/i.test(s)));
  const rule=lab.compareCohort("rule-change");
  assert.ok(rule.reasons.some(s=>/rule version/i.test(s)));
  assert.equal(rule.comparable,false);
});

test("missing completed-run evidence cannot be mistaken for fresh health",()=>{
  const incomplete=lab.compareCohort("incomplete");
  assert.equal(incomplete.comparable,false);
  assert.ok(incomplete.reasons.some(s=>/completed calculation/i.test(s)));
  assert.throws(()=>lab.compareCohort("invalid"),/Unknown comparison fixture/);
});

test("offline comparison CSV exports four cases with immutable native HOLD and no execution receipts",()=>{
  const raw=lab.cohortCsv();
  assert.equal(raw.split("\r\n").filter(Boolean).length,5);
  assert.equal(lab.cohortCsvHeaders.length,13);
  assert.equal((raw.match(/"NOT RUN","HOLD","MOCK-ONLY"/g)||[]).length,4);
  assert.doesNotMatch(raw,/password|bearer |https?:\/\/dev[0-9]+|@example\.com/i);
  assert.match(raw,/Denominator shrinkage/);
});

test("existing 24 native gates stay unchanged and HTML is source-labelled and accessible",()=>{
  assert.equal(lab.gates.length,24);
  assert.ok(lab.rows("all").every(r=>r[4]==="NOT RUN"&&r[5]==="HOLD"&&r[6]==="MOCK-ONLY"));
  const html=fs.readFileSync(path.join(__dirname,"..","cmdb-health-assurance-lab.html"),"utf8");
  assert.match(html,/id="denominator-lab"/);
  assert.match(html,/id="cohort-verdict"[^>]*role="status"[^>]*aria-live="polite"/);
  assert.match(html,/id="cohort-select"[^>]*role="group"/);
  assert.match(html,/not ServiceNow CMDB Health scores/);
  assert.match(html,/Not a capture|not an actual ServiceNow screenshot/);
  assert.doesNotMatch(html,/fetch\(|XMLHttpRequest|localStorage|sessionStorage/);
});
