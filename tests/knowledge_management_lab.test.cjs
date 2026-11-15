"use strict";
const assert=require("node:assert/strict");
const {test}=require("node:test");
const {SCENARIOS,HEADERS,getScenario,rowsFor,allRows,csvFor,allCsv}=require("../knowledge-management-implementation-lab.js");
test("exactly three Knowledge journeys, eight unique DEV gates each",()=>{
 const seen=new Set();
 for(const key of ["author","access","retire"]){
   const s=getScenario(key);
   assert.ok(s);assert.equal(s.gates.length,8);assert.equal(s.flow.length,4);
   for(const gate of s.gates){assert.equal(gate.length,4);assert.match(gate[0],/^KN-[ART]\d\d$/);assert.ok(!seen.has(gate[0]));seen.add(gate[0]);}
 }
 assert.equal(seen.size,24);
 assert.equal(getScenario("__proto__"),null);
 assert.equal(getScenario("constructor"),null);
 assert.equal(getScenario("nope"),null);
});
test("all 24 rows remain MOCK-ONLY, NOT RUN and HOLD after reading every design gate",()=>{
 const marks={};
 for(const key of Object.keys(SCENARIOS))marks[key]=new Set(getScenario(key).gates.map(g=>g[0]));
 const rows=allRows(marks);
 assert.equal(rows.length,24);
 assert.ok(rows.every(r=>r.read==="REVIEWED"&&r.native==="NOT RUN"&&r.release==="HOLD"&&r.classification==="MOCK-ONLY"));
 const csv=allCsv(marks);
 assert.equal(csv.trim().split("\r\n").length,25);
 for(const claim of ["NOT RUN","HOLD","MOCK-ONLY"])assert.equal(csv.split('"'+claim+'"').length-1,24);
 assert.doesNotMatch(csv,/"(PASSED|APPROVED|DEV-VERIFIED|PRODUCTION-VERIFIED)"/);
 for(const gate of rows)assert.equal(csv.split('"'+gate.id+'"').length-1,1);
 assert.ok(HEADERS.includes("Evidence receipt alias (private)"));
 assert.ok(HEADERS.includes("Independent reviewer (private)"));
 assert.ok(csv.trim().split("\r\n").slice(1).every(line=>line.endsWith(',"","","","","",""')));
});
test("unknown journey and malicious mark IDs cannot introduce arbitrary CSV fields",()=>{
 assert.equal(csvFor("__proto__",["KN-A01"]),"");
 assert.deepEqual(rowsFor("constructor",new Set(["KN-A01"])),[]);
 const first=rowsFor("author",new Set(["KN-A01","=HYPERLINK(foo)","\r\nINJECT"]));
 assert.equal(first.length,8);assert.equal(first.filter(r=>r.read==="REVIEWED").length,1);
 assert.equal(allRows(null).length,24);
 assert.equal(allRows({author:["KN-A02"]}).filter(r=>r.read==="REVIEWED").length,1);
});
test("selected export has eight gates with fixed native outcome and blank private receipts",()=>{
 for(const key of ["author","access","retire"]){
   const csv=csvFor(key,new Set());
   assert.equal(csv.trim().split("\r\n").length,9);
   assert.equal(csv.split('"NOT RUN"').length-1,8);
   assert.equal(csv.split('"HOLD"').length-1,8);
   assert.equal(csv.split('"MOCK-ONLY"').length-1,8);
   assert.ok(csv.startsWith('"Scenario","Test ID"'));
 }
});
