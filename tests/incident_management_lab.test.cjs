"use strict";
const assert=require("node:assert/strict");
const {test}=require("node:test");
const {SCENARIOS,KEYS,HEADERS,getScenario,rowsFor,allRows,scenarioCsv,allCsv}=require("../incident-management-implementation-lab.js");
test("three synthetic journeys have 24 distinct accountable controls",()=>{
 assert.deepEqual(KEYS,["intake","restore","close"]);const ids=new Set();
 for(const key of KEYS){const s=getScenario(key);assert.equal(s.gates.length,8);assert.equal(s.flow.length,4);assert.equal(s.fields.length,4);for(const [id,control,expected,persona] of s.gates){assert.match(id,/^IN-[IRC]\d\d$/);assert.ok(!ids.has(id));ids.add(id);assert.ok(control&&expected&&persona)}}
 assert.equal(ids.size,24);for(const key of ["__proto__","constructor","toString","unknown"])assert.equal(getScenario(key),null);
});
test("design marks cannot promote native execution",()=>{
 const marks=Object.fromEntries(KEYS.map(key=>[key,new Set(getScenario(key).gates.map(g=>g[0]))]));
 const rows=allRows(marks),csv=allCsv(marks);assert.equal(rows.length,24);assert.equal(csv.trim().split("\r\n").length,25);
 assert.ok(rows.every(r=>r.read==="REVIEWED"&&r.native==="NOT RUN"&&r.release==="HOLD"&&r.classification==="MOCK-ONLY"));
 for(const value of ["NOT RUN","HOLD","MOCK-ONLY"])assert.equal(csv.split('"'+value+'"').length-1,24);
 assert.doesNotMatch(csv,/"(PASSED|APPROVED|DEV-VERIFIED|PRODUCTION-VERIFIED)"/);
 assert.ok(csv.trim().split("\r\n").slice(1).every(line=>line.endsWith(',"","","","","",""')));
 assert.ok(HEADERS.includes("Independent reviewer (private)"));
});
test("unknown scenario and hostile reading marks remain inert",()=>{
 assert.equal(scenarioCsv("__proto__",["IN-I01"]),"");assert.deepEqual(rowsFor("constructor",new Set(["IN-I01"])),[]);
 const rows=rowsFor("intake",new Set(["IN-I01","=HYPERLINK(x)","\r\nfake"]));assert.equal(rows.filter(r=>r.read==="REVIEWED").length,1);
 assert.equal(allRows(null).length,24);
 for(const key of KEYS){const csv=scenarioCsv(key,new Set());assert.equal(csv.trim().split("\r\n").length,9);for(const value of ["NOT RUN","HOLD","MOCK-ONLY"])assert.equal(csv.split('"'+value+'"').length-1,8)}
});
