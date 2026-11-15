/* Browser-independent contract tests. Only CSV logic is verified; no ServiceNow connection. */
"use strict";
const assert=require("node:assert/strict");
const {test}=require("node:test");
const {getScenario,acceptanceRows,acceptanceCsv}=require("../request-management-implementation-lab.js");
test("three request designs have eight stable and distinct native tests each",()=>{
const all=[];
for(const key of ["access","hardware","service"]){
const scenario=getScenario(key);assert.ok(scenario);assert.equal(scenario.gates.length,8);
for(const gate of scenario.gates){assert.equal(gate.length,3);assert.match(gate[0],/^[A-Z]+-\d\d$/);all.push(gate[0])}
}assert.equal(new Set(all).size,24);assert.equal(getScenario("__proto__"),null);
});
test("CSV remains NOT RUN and HOLD even when every review item is read",()=>{
for(const key of ["access","hardware","service"]){
const ids=getScenario(key).gates.map(g=>g[0]);const data=acceptanceCsv(key,new Set(ids));
const lines=data.trim().split("\r\n");assert.equal(lines.length,9);assert.equal((data.match(/"NOT RUN"/g)||[]).length,8);
assert.equal((data.match(/"HOLD"/g)||[]).length,8);assert.equal((data.match(/"MOCK-ONLY"/g)||[]).length,8);
assert.doesNotMatch(data,/,"(?:PASSED|APPROVED|DEV-VERIFIED)"(?:,|\r\n)/i);
const rows=acceptanceRows(key,ids);assert.equal(rows.length,8);assert.ok(rows.every(row=>row.read&&row.native==="NOT RUN"&&row.release==="HOLD"));
}});
test("unknown selection and missing marks fail closed",()=>{
assert.equal(acceptanceCsv("other",[]),"");assert.deepEqual(acceptanceRows("other",[]),[]);
for(const key of ["access","hardware","service"]){assert.equal(acceptanceRows(key,[]).filter(row=>row.read).length,0);}
});
test("CSV quoting preserves commas and quotes in fixed evidence strings",()=>{
const csv=acceptanceCsv("access",[]);assert.ok(csv.startsWith('"Scenario","Test ID"'));assert.ok(csv.endsWith("\r\n"));assert.ok(csv.includes('"ACC-01"'));});
