"use strict";
// Static, customer-neutral reviewer exercise. No network calls, uploads, browser storage or native execution.
(() => {
  const scenarios = Object.freeze({
    ownership: Object.freeze({name:"Unowned service instance",pain:"A proposed deployed service has no reliably attested operational ownership.",ootb:"Confirm the installed Service Instance class, group/owner fields and supported CSDM relationships with CI Class Manager.",test:"Exercise a null-owner negative fixture and independently attest a valid owner with source/target read-back."}),
    identity: Object.freeze({name:"Conflicting Discovery identities",pain:"Two fictional feeds present competing identifiers for one alleged configuration item.",ootb:"Review IRE identification rules, reconciliation precedence and source authority before altering transform logic.",test:"Replay a stable-identifier fixture and a collision fixture in authorised DEV; inspect actual IRE decisions and exclusions."}),
    offering: Object.freeze({name:"Unsubstantiated service offering",pain:"A notional offering has a portfolio entry but no independently proven service dependency path.",ootb:"Confirm Business Service and Service Offering semantics in Service Portfolio Management, then validate operational relationships.",test:"Obtain service-owner attestation, check typed relationship evidence and preserve unmatched dependencies as NOT ASSESSED."})
  });
  const gates = Object.freeze(["target","ire","owner","relation","health","release"]);
  const allowed = Object.freeze(["not-assessed","requested","gap","staged"]);
  const values = new Map(Object.keys(scenarios).map(key => [key,Object.fromEntries(gates.map(g => [g,"not-assessed"]))]));
  const byId = id => document.getElementById(id);
  const scenario = byId("scenario");
  const status = byId("review-state");
  function current() { return values.get(scenario.value); }
  function render() {
    const s = scenarios[scenario.value];
    if (!s) return;
    byId("scenario-name").textContent = s.name;
    byId("scenario-pain").textContent = s.pain;
    byId("scenario-ootb").textContent = s.ootb;
    byId("scenario-test").textContent = s.test;
    const currentValues = current();
    gates.forEach(key => {byId("stage-" + key).value = currentValues[key];});
    const counts = Object.fromEntries(allowed.map(v => [v,gates.filter(g => currentValues[g] === v).length]));
    byId("count-open").textContent = counts["not-assessed"];
    byId("count-request").textContent = counts.requested;
    byId("count-gap").textContent = counts.gap;
    byId("count-staged").textContent = counts.staged;
    status.textContent = counts.staged + " of 6 preparation packets staged; " + counts.gap + " decision gaps. Native verification NOT VERIFIED; publication HOLD.";
  }
  scenario.addEventListener("change",render);
  gates.forEach(key => {
    byId("stage-" + key).addEventListener("change",ev => {
      if (!allowed.includes(ev.target.value)) { ev.target.value = "not-assessed"; return; }
      current()[key] = ev.target.value;
      render();
    });
  });
  byId("reset").addEventListener("click",() => {
    gates.forEach(key => {current()[key] = "not-assessed";});
    render();
  });
  byId("export").addEventListener("click",() => {
    const packet = {
      schema_version:"csdm5-native-acceptance-preparation-v1",
      scenario_id:scenario.value,
      scenario_label:scenarios[scenario.value].name,
      source_basis:"Public CSDM 5 reference architecture, synthetic acceptance exercise",
      evidence_classification:"MOCK-ONLY",
      native_execution_status:"NOT RUN",
      native_verification_status:"NOT VERIFIED",
      independent_review_approved:false,
      production_verified:false,
      publication_status:"HOLD",
      approval_status:"UNREVIEWED",
      gates:gates.map(key => ({id:"G" + String(gates.indexOf(key) + 1).padStart(2,"0"),key,stage:current()[key]}))
    };
    const blob = new Blob([JSON.stringify(packet,null,2) + "\n"],{type:"application/json"});
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "csdm5-acceptance-" + scenario.value + "-unreviewed.json";
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
  });
  render();
})();