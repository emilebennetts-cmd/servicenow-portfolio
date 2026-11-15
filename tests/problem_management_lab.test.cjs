"use strict";
const assert=require("node:assert/strict");
const {test}=require("node:test");
const {SCENARIOS,KEYS,HEADERS,getScenario,rowsFor,allRows,scenarioCsv,allCsv}=require("../problem-management-implementation-lab.js");
test("three journeys, 24 unique acceptance controls, four stages each",()=>{
 assert.deepEqual(KEYS,["detect","known","fix"]);const ids=new Set();
 for(const key of KEYS){const s=getScenario(key);assert.equal(s.gates.length,8);assert.equal(s.flow.length,4);
 for(const [id,control,expected,persona] of s.gates){assert.match(id,/^PR-[DKF]\d\d$/);assert.ok(!ids.has(id));ids.add(id);assert.ok(control&&expected&&persona)}}
 assert.equal(ids.size,24);for(const key of ["__proto__","constructor","nope"])assert.equal(getScenario(key),null);
});
test("marking every design control never promotes the native outcome",()=>{
 const marks=Object.fromEntries(KEYS.map(key=>[key,new Set(getScenario(key).gates.map(g=>g[0]))]));
 const rows=allRows(marks),csv=allCsv(marks);assert.equal(rows.length,24);assert.equal(csv.trim().split("\r\n").length,25);
 for(const row of rows)assert.equal(row.read,"REVIEWED");
 for(const value of ["NOT RUN","HOLD","MOCK-ONLY"])assert.equal(csv.split('"'+value+'"').length-1,24);
 assert.doesNotMatch(csv,/"(PASSED|APPROVED|DEV-VERIFIED|PRODUCTION-VERIFIED)"/);
 for(const row of rows)assert.equal(csv.split('"'+row.id+'"').length-1,1);
 assert.ok(csv.trim().split("\r\n").slice(1).every(line=>line.endsWith(',"","","","","",""')));
 assert.ok(HEADERS.includes("Independent reviewer (private)"));
});
test("unknown scenario, hostile marks and missing marks fail closed",()=>{
 assert.equal(scenarioCsv("__proto__",["PR-D01"]),"");
 assert.deepEqual(rowsFor("constructor",new Set(["PR-D01"])),[]);
 const rows=rowsFor("detect",new Set(["PR-D01","=HYPERLINK(fake)","\r\nforged"]));
 assert.equal(rows.filter(x=>x.read==="REVIEWED").length,1);
 assert.equal(allRows(null).length,24);
 for(const key of KEYS){const csv=scenarioCsv(key,new Set());assert.equal(csv.trim().split("\r\n").length,9);for(const value of ["NOT RUN","HOLD","MOCK-ONLY"])assert.equal(csv.split('"'+value+'"').length-1,8)}
});
