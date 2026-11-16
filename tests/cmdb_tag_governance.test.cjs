"use strict";
const test=require("node:test"),assert=require("node:assert/strict"),fs=require("node:fs"),path=require("node:path");
const lab=require("../cmdb-tag-governance-model.js");
test("five distinct offline tag policy scenarios preserve HOLD and synthetic evidence",()=>{
 assert.equal(lab.scenarios.length,5);assert.equal(new Set(lab.scenarios.map(s=>s.id)).size,5);
 for(const scenario of lab.scenarios){const r=lab.evaluate(scenario.id);assert.equal(r.releaseDecision,"HOLD");assert.equal(r.nativeStatus,"NOT RUN");assert.equal(r.evidence,"MOCK-ONLY");assert.ok(r.tagCount>0);}
});
test("canonical aliases, owner gaps and source overwrite are differentiated",()=>{
 assert.equal(lab.canon(" Env "),"environment");assert.equal(lab.value(" PROD "),"production");
 assert.ok(lab.evaluate("key-drift").findings.some(f=>f.kind==="variant"));
 assert.ok(lab.evaluate("missing-cost").findings.some(f=>f.kind==="missing"));
 assert.ok(lab.evaluate("collision").findings.some(f=>f.kind==="conflict"));
 assert.ok(lab.evaluate("reingestion").findings.some(f=>f.kind==="authority"));
 assert.equal(lab.evaluate("baseline").findings.length,0);
 assert.throws(()=>lab.evaluate("unknown"),/Unknown synthetic scenario/);
});
test("all 25 DEV gates have unique identity, immutable hold, blank execution fields",()=>{
 assert.equal(lab.gates.length,25);assert.equal(new Set(lab.gates.map(g=>g.id)).size,25);
 for(const g of lab.gates){assert.equal(g.nativeStatus,"NOT RUN");assert.equal(g.releaseDecision,"HOLD");assert.equal(g.classification,"MOCK-ONLY");}
 const all=lab.csv();assert.equal(all.split("\r\n").filter(Boolean).length,26);
 assert.equal((all.match(/"NOT RUN","HOLD","MOCK-ONLY"/g)||[]).length,25);
 assert.equal(lab.csv("baseline").split("\r\n").filter(Boolean).length,6);
 assert.throws(()=>lab.csv("bad"),/Unknown export scenario/);
 assert.doesNotMatch(all,/https?:|@|token|password|bearer |dev[0-9]+/i);
});
test("public page has strict offline CSP, accessible controls and truthful source boundaries",()=>{
 const html=fs.readFileSync(path.join(__dirname,"..","cmdb-tag-governance-lab.html"),"utf8");
 for(const phrase of ['id="tag-lab"','aria-live="polite"','data-export="all"','MOCK-ONLY','NOT RUN','PRODUCTION-VERIFIED','cmdb_key_value','Service Mapping','Tag Governance'])assert.ok(html.includes(phrase),phrase);
 assert.match(html,/connect-src 'none'/);assert.match(html,/script-src 'self'/);
 assert.doesNotMatch(html,/fetch\(|XMLHttpRequest|localStorage|sessionStorage|<img\b/i);
});
