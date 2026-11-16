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
  function attach(doc){
    if(!doc.getElementById("tower-workstream"))return;
    const status=doc.getElementById("tower-status"),table=doc.getElementById("tower-body");
    const workstream=doc.getElementById("tower-workstream"),search=doc.getElementById("tower-search");
    const buttons=[...doc.querySelectorAll("[data-tower-export]")];
    let rows;
    try{
      rows=createRows({
        ire:root.CMDBSourceAcceptance,tags:root.CMDBTagGovernance,
        health:root.CMDBHealthAssurance,relationships:root.CMDBRelationshipAssurance,lifecycle:root.CMDBPolicyLab
      });
    }catch(error){
      status.textContent="HOLD — "+error.message;
      buttons.forEach(b=>b.disabled=true);
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
    display();
  }
  if(typeof document!=="undefined")document.addEventListener("DOMContentLoaded",()=>attach(document));
  return Object.freeze({EXPECTED,METADATA,HEADERS,createRows,filterRows,csv,attach});
});
