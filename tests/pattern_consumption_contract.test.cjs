"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const contract = require("../pattern-consumption-contract.js");
test("only six source-defined target types; no invented children", () => {
  assert.equal(contract.TYPES.length, 6);
  assert.equal(new Set(contract.TYPES.map(x=>x.id)).size, 6);
  const p=contract.evaluate(contract.EXAMPLES[0]);
  assert.equal(p.rows.length, 6);
  assert.equal(p.canDraft, false);
  assert.equal(p.rows.filter(x=>x.exists).length, 0);
  assert(p.rows.every(x=>x.disposition.includes("SOURCE ITEM MISSING")));
});
test("unapproved partial draft never generates a false complete delivery package", () => {
  const p=contract.evaluate(contract.EXAMPLES[1]);
  assert.equal(p.rows.filter(x=>x.exists).length, 3);
  assert(p.rows.every(x=>x.disposition.startsWith("HOLD") || x.disposition.startsWith("BLOCKED")));
  assert(p.blockers.some(x=>x.includes("entitlement")));
  assert.equal(p.releaseStatus, "HOLD");
});
test("complete synthetic review remains draft-only / not native acceptance", () => {
  const p=contract.evaluate(contract.EXAMPLES[2]);
  assert.equal(p.canDraft,true);
  assert(p.rows.every(x=>x.disposition==="DRAFT ELIGIBLE - SYNTHETIC ONLY"));
  assert(p.rows.every(x=>x.nativeStatus==="NOT RUN" && x.reviewStatus==="UNREVIEWED" && x.releaseStatus==="HOLD"));
  assert.equal(p.evidenceClass,"MOCK-ONLY");
});
test("unresolved parent always blocks even with complete child list", () => {
  const p=contract.evaluate(contract.EXAMPLES[3]);
  assert.equal(p.canDraft,false);
  assert(p.rows.every(x=>x.disposition==="BLOCKED - PARENT UNRESOLVED"));
});
test("unknown and duplicated source types fail closed", () => {
  assert.throws(()=>contract.evaluate({...contract.EXAMPLES[2],items:["test","test"]}),/Unknown or duplicate/);
  assert.throws(()=>contract.evaluate({...contract.EXAMPLES[2],items:["sys_user"]}),/Unknown or duplicate/);
  assert.throws(()=>contract.evaluate({...contract.EXAMPLES[2],items:null}),/Typed item/);
});
test("CSV keeps six rows, no GO or DEV proof, and no private evidence fields", () => {
  const csv=contract.toCSV(contract.evaluate(contract.EXAMPLES[2]));
  assert.equal(csv.split("\r\n").filter(Boolean).length,7);
  assert.equal((csv.match(/"HOLD"/g)||[]).length,6);
  assert.equal((csv.match(/"NOT RUN"/g)||[]).length,6);
  assert.equal((csv.match(/"MOCK-ONLY"/g)||[]).length,6);
  assert(!/sys_id|instance_url|customer|screenshot_url|credential/i.test(csv));
  assert.throws(()=>contract.toCSV({releaseStatus:"GO",rows:[]}),/Untrusted/);
});
test("CSV quoting neutralises unexpected formula prefixes", () => {
  const p=contract.evaluate({...contract.EXAMPLES[2],id:"=HYPERLINK('bad')"});
  const csv=contract.toCSV(p);
  assert(csv.includes("\"'=HYPERLINK('bad')\""));
});
