/* Synthetic Diagnostic -> Delivery handoff review. Never accesses a ServiceNow instance. */
"use strict";
(function (root) {
  const states = Object.freeze({
    ready: {label:"Reviewed draft candidate", version:"1.0-draft", reviewed:true, authorised:true, evidence:true, supported:true, conflict:false, replay:false},
    review: {label:"Approval missing", version:"1.0-draft", reviewed:false, authorised:true, evidence:true, supported:true, conflict:false, replay:false},
    version: {label:"Unknown contract version", version:"2.0-unknown", reviewed:true, authorised:true, evidence:true, supported:true, conflict:false, replay:false},
    evidence: {label:"Evidence reference absent", version:"1.0-draft", reviewed:true, authorised:true, evidence:false, supported:true, conflict:false, replay:false},
    role: {label:"Unauthorised initiator", version:"1.0-draft", reviewed:true, authorised:false, evidence:true, supported:true, conflict:false, replay:false},
    scope: {label:"Unsupported process scope", version:"1.0-draft", reviewed:true, authorised:true, evidence:true, supported:false, conflict:false, replay:false},
    conflict: {label:"Edited requirement exists", version:"1.0-draft", reviewed:true, authorised:true, evidence:true, supported:true, conflict:true, replay:false},
    replay: {label:"Correlation replay", version:"1.0-draft", reviewed:true, authorised:true, evidence:true, supported:true, conflict:false, replay:true}
  });
  const tests = [
    ["version","Recognised version","1.0-draft"],
    ["authorised","Scoped role checked","true"],
    ["reviewed","Human review decision recorded","true"],
    ["evidence","Evidence reference available","true"],
    ["supported","Scope supported for preview","true"],
    ["conflict","No edited requirement conflict","false"]
  ];
  function evaluate(values) {
    const checks = tests.map(([field,name,wanted])=>({
      field, name, pass:String(values[field])===wanted
    }));
    let outcome="DRAFT ELIGIBLE (SIMULATED)", reason="A server-side implementation would still require ACLs, an authenticated reviewer, and a write transaction.";
    if (values.version!=="1.0-draft") {
      outcome="REJECT — UNSUPPORTED VERSION"; reason="No draft should be created for a contract version the adapter does not recognise.";
    } else if (!values.authorised) {
      outcome="REJECT — AUTHORISATION"; reason="Client-side role claims are not trusted. Real authorisation must be resolved on the ServiceNow server.";
    } else if (!values.reviewed || !values.evidence) {
      outcome="HOLD — INCOMPLETE REVIEW"; reason="An attested review and an authorised evidence reference are both required before any draft handoff.";
    } else if (!values.supported) {
      outcome="MANUAL SCOPE REVIEW"; reason="An unsupported scope must not be silently mapped to a native template.";
    } else if (values.conflict) {
      outcome="HOLD — HUMAN EDIT CONFLICT"; reason="A draft must never overwrite existing accepted requirements or edits.";
    } else if (values.replay) {
      outcome="REUSE DRAFT (SIMULATED)"; reason="An idempotency lookup would return the existing authorised draft, never a second record.";
    }
    return {
      schema:"portfolio-handoff-local/1",
      classification:"MOCK-ONLY",
      contract_status:"PROPOSED — NOT DEPLOYED",
      native_execution:"NOT RUN",
      production_verification:"NOT VERIFIED",
      publication_decision:"HOLD",
      source_system:"synthetic-diagnostic-workbench",
      target_system:"synthetic-delivery-workbench",
      correlation_id:"DEMO-FINDING-001",
      outcome, reason, checks,
      wrote_records:false,
      checked_native_permissions:false
    };
  }
  if (typeof module!=="undefined" && module.exports) module.exports={states,evaluate};
  if (typeof document==="undefined") return;
  const form=document.getElementById("hc-form");
  if (!form) return;
  const scenario=document.getElementById("hc-scenario");
  const version=document.getElementById("hc-version");
  const fields=["reviewed","authorised","evidence","supported","conflict","replay"];
  const output=document.getElementById("hc-output");
  const status=document.getElementById("hc-status");
  const reason=document.getElementById("hc-reason");
  const list=document.getElementById("hc-checks");
  let receipt=null;
  Object.entries(states).forEach(([key,item])=>{
    const option=document.createElement("option");
    option.value=key; option.textContent=item.label; scenario.appendChild(option);
  });
  function snapshot() {
    const state={version:version.value};
    fields.forEach(field=>{state[field]=document.getElementById("hc-"+field).checked;});
    return state;
  }
  function render() {
    receipt=evaluate(snapshot());
    status.textContent=receipt.outcome;
    reason.textContent=receipt.reason;
    list.replaceChildren();
    receipt.checks.forEach(check=>{
      const item=document.createElement("li");
      item.textContent=(check.pass?"PASS (SIMULATED): ":"BLOCKED (SIMULATED): ")+check.name;
      item.className=check.pass?"hc-pass":"hc-block";
      list.appendChild(item);
    });
    output.textContent=JSON.stringify(receipt,null,2);
  }
  function choose() {
    const values=states[scenario.value];
    version.value=values.version;
    fields.forEach(field=>{document.getElementById("hc-"+field).checked=values[field];});
    render();
  }
  scenario.addEventListener("change",choose);
  form.addEventListener("change",event=>{if(event.target!==scenario)render();});
  form.addEventListener("submit",event=>event.preventDefault());
  document.getElementById("hc-download").addEventListener("click",()=>{
    render();
    const blob=new Blob([JSON.stringify(receipt,null,2)+"\n"],{type:"application/json"});
    const url=URL.createObjectURL(blob);
    const anchor=document.createElement("a");
    anchor.href=url; anchor.download="synthetic-handoff-review.json";
    document.body.appendChild(anchor); anchor.click(); anchor.remove();
    setTimeout(()=>URL.revokeObjectURL(url),1000);
  });
  choose();
})(typeof window!=="undefined"?window:null);
