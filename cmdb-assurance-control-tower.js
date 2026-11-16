"use strict";
/* 117 source-derived CMDB native acceptance prompts; read-only browser-local.
   Every result is NOT RUN / HOLD / MOCK-ONLY. Never queries an instance. */
(function(root,factory){
  const api=factory(root);
  if(typeof module==="object"&&module.exports)module.exports=api;
  else root.CMDBAssuranceTower=api;
})(typeof globalThis!=="undefined"?globalThis:this,function(root){
  const EXPECTED=Object.freeze({identity:18,tags:25,health:24,relationships:30,lifecycle:20});
  const METADATA=Object.freeze([
    {key:"identity",title:"Identification & IRE",page:"cmdb-source-onboarding-lab.html#native-handoff",risk:"Source collisions, matching and precedence"},
    {key:"tags",title:"Tag governance",page:"cmdb-tag-governance-lab.html",risk:"Ownership, cost centre and source value drift"},
    {key:"health",title:"CMDB Health",page:"cmdb-health-assurance-lab.html",risk:"Job freshness, cohort lineage and score comparability"},
    {key:"relationships",title:"Relationship integrity",page:"cmdb-relationship-assurance-lab.html",risk:"Duplicate, orphaned, stale or invalid CI edges"},
    {key:"lifecycle",title:"Data Manager",page:"cmdb-data-manager-governance-lab.html",risk:"Retirement, legal holds, deletion and attestation"}
  ]);
  const HEADERS=Object.freeze(["Control ID","Workstream","Synthetic scenario","Native validation action","Expected independent evidence","Native execution","Release decision","Evidence class","Instance","Installed version","Executor","Execution UTC","Private evidence receipt","Independent reviewer"]);

  /* Reviewer planning sequence only. Not ServiceNow transaction order or runtime evidence. */
  const STAGES=Object.freeze([
    Object.freeze({key:"identity",step:1,title:"CI identity and source precedence",entry:"Target release, scope, IRE rules, source authority and synthetic payload approved",dependency:"Authorised non-production instance and negative-persona test accounts",owner:"CMDB lead and source-system owner",exit:"Identity, collision and replay evidence independently accepted"}),
    Object.freeze({key:"tags",step:2,title:"Tag and key-value governance",entry:"Identity and replay evidence independently accepted",dependency:"Upstream tagging owner, naming policy and controlled source correction",owner:"Cloud source owner and CMDB data steward",exit:"Corrected values persist after source replay"}),
    Object.freeze({key:"health",step:3,title:"Health KPI provenance",entry:"Identity and metadata baselines accepted; effective jobs and rules captured",dependency:"Named KPI owner, eligible CI population and comparable measurement windows",owner:"CMDB health owner and independent reviewer",exit:"Job completion and comparable denominator independently reconciled"}),
    Object.freeze({key:"relationships",step:4,title:"Relationship and topology integrity",entry:"Stable CI identities and effective relationship rules captured",dependency:"Service ownership and approved dependency samples",owner:"Service Mapping lead and CMDB relationship steward",exit:"Graph integrity and negative access outcomes reviewed"}),
    Object.freeze({key:"lifecycle",step:5,title:"Data Manager lifecycle and attestation",entry:"Source replay and topology evidence accepted; retention and legal holds reviewed",dependency:"Asset owner approval, policy exclusions and recovery/rollback plan",owner:"Lifecycle policy owner and independent change approver",exit:"Policy effects, audit, re-ingestion and rollback proof reviewed"})
  ]);
  const PLAN_HEADERS=Object.freeze(["Review stage","Control domain","Entry evidence prerequisite","Cross-domain dependency","Accountable role","Exit evidence criterion","Control ID","Synthetic scenario","Native DEV action","Expected independent evidence","Native execution","Release decision","Evidence class","Instance","Installed version","Executor","Execution UTC","Private evidence receipt","Independent reviewer"]);
  function createRows(d){
    if(!d||!d.ire||!d.tags||!d.health||!d.relationships||!d.lifecycle)throw Error("Missing source model: export HOLD");
    const rows=[];
    function add(key,id,scenario,action,expected){
      if(!id||!action||!expected)throw Error("Incomplete control: export HOLD");
      rows.push(Object.freeze({key,id:String(id),scenario:String(scenario||""),action:String(action),expected:String(expected),native:"NOT RUN",decision:"HOLD",evidence:"MOCK-ONLY"}));
    }
    d.ire.buildRows("all").forEach(r=>add("identity",r.test_id,r.scenario,r.native_action,r.expected_evidence));
    d.tags.gates.forEach(r=>add("tags",r.id,r.scenario,r.action,r.expected));
    d.health.gates.forEach(r=>add("health",r.id,r.scenario,r.action,r.expected));
    d.relationships.gates.forEach(r=>add("relationships",r.id,r.scenario,r.action,r.expected));
    d.lifecycle.checks.forEach(r=>add("lifecycle",r.id,r.scenario,r.step,r.evidence));
    Object.entries(EXPECTED).forEach(([key,n])=>{
      if(rows.filter(r=>r.key===key).length!==n)throw Error("Source model count drift for "+key+": export HOLD");
    });
    if(new Set(rows.map(r=>r.key+":"+r.id)).size!==rows.length)throw Error("Duplicate control IDs: export HOLD");
    return Object.freeze(rows);
  }
  function filterRows(rows,key,query){
    if(key!=="all"&&!METADATA.some(m=>m.key===key))throw Error("Unknown workstream");
    const q=String(query||"").trim().toLowerCase();
    return rows.filter(r=>(key==="all"||r.key===key)&&[r.id,r.scenario,r.action,r.expected,r.key].join(" ").toLowerCase().includes(q));
  }
  function cell(x){
    let s=String(x==null?"":x);
    if(/^\s*[=+\-@]/.test(s))s="'"+s;
    return '"'+s.replace(/"/g,'""')+'"';
  }
  function csv(rows){
    return [HEADERS,...rows.map(r=>[
      r.id,METADATA.find(m=>m.key===r.key).title,r.scenario,r.action,r.expected,
      "NOT RUN","HOLD","MOCK-ONLY","","","","","",""
    ])].map(r=>r.map(cell).join(",")).join("\r\n")+"\r\n";
  }

  function planRows(rows){
    if(!Array.isArray(rows)||rows.length!==117)throw Error("Native execution plan requires all 117 source controls: HOLD");
    const seen=new Set();
    const result=[];
    STAGES.forEach(stage=>{
      const inStage=rows.filter(r=>r.key===stage.key);
      if(inStage.length!==EXPECTED[stage.key])throw Error("Native plan source drift: HOLD");
      inStage.forEach(r=>{
        const marker=r.key+":"+r.id;
        if(!r.id||!r.action||!r.expected||seen.has(marker)||r.native!=="NOT RUN"||r.decision!=="HOLD"||r.evidence!=="MOCK-ONLY")throw Error("Unreviewed or changed native evidence: HOLD");
        seen.add(marker);
        result.push(Object.freeze({...r,step:stage.step,stage:stage.title,entry:stage.entry,dependency:stage.dependency,owner:stage.owner,exit:stage.exit}));
      });
    });
    if(result.length!==117||seen.size!==117)throw Error("Incomplete source execution plan: HOLD");
    return Object.freeze(result);
  }
  function planCsv(rows){
    return [PLAN_HEADERS,...planRows(rows).map(r=>[
      String(r.step)+" / "+r.stage, METADATA.find(m=>m.key===r.key).title,r.entry,r.dependency,r.owner,r.exit,
      r.id,r.scenario,r.action,r.expected,"NOT RUN","HOLD","MOCK-ONLY","","","","","",""
    ])].map(r=>r.map(cell).join(",")).join("\r\n")+"\r\n";
  }
  function attach(doc){
    if(!doc.getElementById("tower-workstream"))return;
    const status=doc.getElementById("tower-status"),table=doc.getElementById("tower-body");
    const workstream=doc.getElementById("tower-workstream"),search=doc.getElementById("tower-search");
    const buttons=[...doc.querySelectorAll("[data-tower-export]")];
    const planButton=doc.getElementById("tower-plan-export");
    let rows;
    try{
      rows=createRows({
        ire:root.CMDBSourceAcceptance,tags:root.CMDBTagGovernance,
        health:root.CMDBHealthAssurance,relationships:root.CMDBRelationshipAssurance,lifecycle:root.CMDBPolicyLab
      });
    }catch(error){
      status.textContent="HOLD — "+error.message;
      buttons.forEach(b=>b.disabled=true);
      if(planButton)planButton.disabled=true;
      return;
    }
    function display(){
      const matches=filterRows(rows,workstream.value,search.value);
      doc.getElementById("tower-count").textContent=matches.length+" of 117 source-derived gates · all NOT RUN / HOLD";
      table.replaceChildren();
      matches.slice(0,30).forEach(r=>{
        const tr=doc.createElement("tr");
        [r.id,METADATA.find(m=>m.key===r.key).title,r.scenario,r.action,"NOT RUN / HOLD"].forEach(v=>{
          const td=doc.createElement("td");td.textContent=v;tr.append(td);
        });
        table.append(tr);
      });
      doc.getElementById("tower-note").textContent=matches.length>30?"Showing first 30 matches. Export includes every match.":"Showing all matches.";
      status.textContent="Browser-local inspection only. No native execution or approval.";
    }
    workstream.addEventListener("change",display);search.addEventListener("input",display);
    buttons.forEach(b=>b.addEventListener("click",()=>{
      const kind=b.getAttribute("data-tower-export");
      const selected=kind==="all"?rows:filterRows(rows,workstream.value,search.value);
      const object=URL.createObjectURL(new Blob([csv(selected)],{type:"text/csv;charset=utf-8"}));
      const link=doc.createElement("a");link.href=object;
      link.download="cmdb-assurance-"+kind+"-"+selected.length+"-HOLD.csv";
      doc.body.append(link);link.click();link.remove();URL.revokeObjectURL(object);
      status.textContent=selected.length+" controls exported. All results remain NOT RUN / HOLD / MOCK-ONLY.";
    }));
    if(planButton)planButton.addEventListener("click",()=>{
      try{
        const content=planCsv(rows); // always full, never filtered or user-editable
        const object=URL.createObjectURL(new Blob([content],{type:"text/csv;charset=utf-8"}));
        const link=doc.createElement("a");link.href=object;
        link.download="cmdb-assurance-native-execution-sequence-117-HOLD.csv";
        doc.body.append(link);link.click();link.remove();URL.revokeObjectURL(object);
        doc.getElementById("tower-plan-status").textContent="117 source controls exported in illustrative dependency order. All native results NOT RUN / HOLD / MOCK-ONLY.";
      }catch(error){
        planButton.disabled=true;
        doc.getElementById("tower-plan-status").textContent="HOLD — "+error.message;
      }
    });
    display();
  }
  if(typeof document!=="undefined")document.addEventListener("DOMContentLoaded",()=>attach(document));
  return Object.freeze({EXPECTED,METADATA,HEADERS,STAGES,PLAN_HEADERS,createRows,filterRows,csv,planRows,planCsv,attach});
});
