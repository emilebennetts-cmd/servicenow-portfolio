/* Public, source-document snapshot crosswalk. Does not attest native ServiceNow execution. */
(function(root,factory){const api=factory();if(typeof module==="object"&&module.exports)module.exports=api;else root.DocCurrencyGate=api;})(typeof globalThis!=="undefined"?globalThis:this,function(){
  "use strict";
  const docs=Object.freeze([
    Object.freeze({id:"ASBUILT-SEP30",name:"Delivery Solution As-Built",version:"4.6.1",cutoff:"2026-09-30",kind:"SOURCE DOCUMENT",scope:"Delivery lifecycle, controls and handover",next:"Reconcile procedures to authorised installed target, then obtain owner acceptance."}),
    Object.freeze({id:"TRAINING-SEP30",name:"Delivery User Guides & Training",version:"4.6.1",cutoff:"2026-09-30",kind:"CONTROLLED DRAFT",scope:"Persona tasks, safety rules and unfilled screen-capture placeholders",next:"Rehearse on target DEV release; re-capture approved screens and secure trainer/owner sign-off."}),
    Object.freeze({id:"ARCH-OCT19",name:"Delivery Architecture",version:"4.22.2",cutoff:"2026-10-19",kind:"SOURCE/HISTORICAL DEV DOCUMENT",scope:"Generator, role/ACL, integration and transport boundaries",next:"Reconfirm target package, scope, ACL, entitlement and current DEV read-back."}),
    Object.freeze({id:"DIAG-DEMO",name:"Diagnostic Completion Runbook",version:null,cutoff:"historical controlled showcase",kind:"FICTIONAL SHOWCASE RUNBOOK",scope:"Finding-to-delivery reconciliation, G2 licensing and simulated deployment",next:"Do not transfer demo gates to live acceptance; map findings to authorised target evidence."})
  ]);
  const versions=Object.freeze(["4.6.1","4.22.2"]);
  function rows(target){
    if(!versions.includes(target))throw Error("Unsupported evidence target: choose a controlled snapshot.");
    return docs.map(d=>{
      const alignment=d.version===null?"UNVERSIONED / SHOWCASE":d.version===target?"SNAPSHOT MATCH":"DOCUMENT DRIFT";
      return Object.freeze({...d,alignment,decision:"HOLD",nativeVerification:"NOT RUN",publication:"NOT AUTHORISED"});
    });
  }
  function csv(target){
    const fields=["Doc ID","Controlled document","Snapshot","Evidence cutoff","Target","Comparison","Native acceptance","Decision","Next evidence action"];
    const records=rows(target).map(d=>[d.id,d.name,d.version||"none",d.cutoff,target,d.alignment,d.nativeVerification,d.decision,d.next]);
    const esc=v=>'"'+String(v).replace(/"/g,'""').replace(/^([=+\-@\t\r])/,"'$1")+'"';
    return [fields,...records].map(row=>row.map(esc).join(",")).join("\r\n")+"\r\n";
  }
  return Object.freeze({docs,versions,rows,csv});
});