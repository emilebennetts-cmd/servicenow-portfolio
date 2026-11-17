/* Public, synthetic-only pattern item consumption gate.
   No ServiceNow API, private records, screenshot or outbound network path. */
(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.PatternConsumptionContract = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";
  const TYPES = Object.freeze([
    Object.freeze({id:"workshop", label:"Workshop questions", output:"Workshop draft"}),
    Object.freeze({id:"requirement", label:"Requirements", output:"Requirement draft"}),
    Object.freeze({id:"decision", label:"Design decisions", output:"Decision register draft"}),
    Object.freeze({id:"build", label:"Build guidance", output:"Build specification draft"}),
    Object.freeze({id:"test", label:"Acceptance tests", output:"Unrun test plan"}),
    Object.freeze({id:"handover", label:"Operational handover", output:"Handover checklist"})
  ]);
  const all = TYPES.map(t => t.id);
  const EXAMPLES = Object.freeze([
    Object.freeze({id:"parent-only", title:"Historical parent-only reference", note:"Representative of a source-only pattern parent when linked items are not available in the repository. This is NOT a live assessment of the 96-pattern export.", parent:true, items:[], versionPinned:false, fitReviewed:false, entitlementReviewed:false, ownerReviewed:false}),
    Object.freeze({id:"draft-pack", title:"Unapproved draft pack", note:"Synthetic partial item set. Resembles a draft review boundary but does not reproduce the private MIM pack or its child records.", parent:true, items:["workshop","requirement","test"], versionPinned:true, fitReviewed:false, entitlementReviewed:false, ownerReviewed:false}),
    Object.freeze({id:"governed-draft", title:"Governed draft candidate", note:"Illustrative complete typed items and design review; there is still no native target acceptance or independent deployment evidence.", parent:true, items:all, versionPinned:true, fitReviewed:true, entitlementReviewed:true, ownerReviewed:true}),
    Object.freeze({id:"no-parent", title:"Unresolved parent identity", note:"A source item set without an authoritative parent identity must fail closed, even when other metadata appears complete.", parent:false, items:all, versionPinned:true, fitReviewed:true, entitlementReviewed:true, ownerReviewed:true})
  ]);
  const known = new Set(all);
  function evaluate(input) {
    if (!input || typeof input !== "object" || !Array.isArray(input.items)) throw new TypeError("Typed item list required");
    if (input.items.some(id => !known.has(id)) || new Set(input.items).size !== input.items.length)
      throw new TypeError("Unknown or duplicate source item type");
    const present = new Set(input.items);
    const gates = Object.freeze([
      {name:"Authoritative parent identity", pass:input.parent === true},
      {name:"Source version pinned", pass:input.versionPinned === true},
      {name:"OOTB fit reviewed", pass:input.fitReviewed === true},
      {name:"Target entitlement reviewed", pass:input.entitlementReviewed === true},
      {name:"Accountable pattern-owner review", pass:input.ownerReviewed === true}
    ]);
    const blockers = gates.filter(g => !g.pass).map(g => g.name);
    if (!present.size) blockers.push("Linked pattern items not present in source");
    const canDraft = blockers.length === 0;
    const rows = TYPES.map(t => {
      const exists = present.has(t.id);
      const disposition = !input.parent ? "BLOCKED - PARENT UNRESOLVED"
        : !exists ? "BLOCKED - SOURCE ITEM MISSING"
        : !canDraft ? "HOLD - REVIEW PREREQUISITES"
        : "DRAFT ELIGIBLE - SYNTHETIC ONLY";
      const nextAction = !input.parent ? "Resolve authoritative parent and source identity"
        : !exists ? "Recover reviewed typed source item; never invent child content"
        : !canDraft ? "Complete source pin, OOTB, entitlement and owner reviews"
        : "Create controlled draft; execute native acceptance and independent review";
      return Object.freeze({type:t.id, source:t.label, output:t.output, exists, disposition, nextAction, nativeStatus:"NOT RUN", reviewStatus:"UNREVIEWED", releaseStatus:"HOLD", evidenceClass:"MOCK-ONLY"});
    });
    return Object.freeze({id:String(input.id||"synthetic"), title:String(input.title||"Synthetic case"), note:String(input.note||""), canDraft, blockers:Object.freeze(blockers), gates:Object.freeze(gates), rows:Object.freeze(rows), releaseStatus:"HOLD", evidenceClass:"MOCK-ONLY", targetExecution:"NOT RUN"});
  }
  function csvCell(value) {
    let s = String(value == null ? "" : value);
    if (/^\s*[=+@-]/.test(s)) s = "'" + s;
    return '"' + s.replace(/"/g, '""') + '"';
  }
  function toCSV(result) {
    if (!result || !Array.isArray(result.rows) || result.rows.length !== TYPES.length ||
        result.releaseStatus !== "HOLD" || result.evidenceClass !== "MOCK-ONLY" ||
        result.rows.some((r,i) => r.type !== TYPES[i].id || r.releaseStatus !== "HOLD" || r.nativeStatus !== "NOT RUN" || r.evidenceClass !== "MOCK-ONLY"))
      throw new TypeError("Untrusted or altered demonstration receipt");
    const header = ["scenario","source_type","target_draft","source_available","disposition","next_action","native_execution","independent_review","release","evidence_class"];
    const lines = [header.map(csvCell).join(",")];
    for (const row of result.rows) lines.push([result.id,row.type,row.output,row.exists ? "YES" : "NO",row.disposition,row.nextAction,row.nativeStatus,row.reviewStatus,row.releaseStatus,row.evidenceClass].map(csvCell).join(","));
    return "\ufeff" + lines.join("\r\n") + "\r\n";
  }
  return Object.freeze({TYPES, EXAMPLES, evaluate, toCSV});
});
