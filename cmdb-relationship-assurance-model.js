"use strict";
/* Synthetic, self-contained CMDB relationship graph. Never connects to ServiceNow. */
(function(root,factory){const api=factory();if(typeof module==="object"&&module.exports)module.exports=api;else root.CMDBRelationshipAssurance=api;})(typeof globalThis!=="undefined"?globalThis:this,function(){
const TYPE="Depends on::Used by";
const nodes={
 "SYN-APP-01":{label:"Order application",kind:"application",stale:false},
 "SYN-SRV-01":{label:"Application server",kind:"server",stale:false},
 "SYN-SRV-02":{label:"Retired server",kind:"server",stale:true}
};
const scenarios=[
{id:"duplicate",name:"Duplicate relationship",kind:"Duplicate",summary:"Two provider feeds assert an identical relationship and port.",edges:[{parent:"SYN-APP-01",child:"SYN-SRV-01",type:TYPE,port:"",source:"Inventory"},{parent:"SYN-APP-01",child:"SYN-SRV-01",type:TYPE,port:"",source:"Connector"}],action:"Confirm source precedence and duplicate handling; do not delete one row without approved provenance and a replay test."},
{id:"orphan",name:"Orphaned endpoint",kind:"Orphan",summary:"The relationship refers to a CI that does not exist in this fictional sample.",edges:[{parent:"SYN-APP-01",child:"SYN-UNKNOWN",type:TYPE,port:"",source:"Inventory"}],action:"Check referential integrity, lifecycle status and ingestion failure; no automatic orphan deletion."},
{id:"stale",name:"Stale related CI",kind:"Stale",summary:"One endpoint is flagged stale by the synthetic fixture, making its relationship suspect.",edges:[{parent:"SYN-APP-01",child:"SYN-SRV-02",type:TYPE,port:"",source:"Discovery"}],action:"Inspect the effective native staleness rules, discovery freshness, source exceptions and CI owner before deciding."},
{id:"direction",name:"Invalid class direction",kind:"Governance",summary:"A server depends on an application, contrary to the explicitly fictional suggested relationship rule.",edges:[{parent:"SYN-SRV-01",child:"SYN-APP-01",type:TYPE,port:"",source:"Manual edit"}],action:"Use CI Class Manager suggested/dependent rules and effective inheritance to evaluate the native direction, not this sample policy."},
{id:"baseline",name:"Apparently clean topology",kind:"Review",summary:"No synthetic rule finding; this is not evidence of a passing native health processor.",edges:[{parent:"SYN-APP-01",child:"SYN-SRV-01",type:TYPE,port:"",source:"Discovery"}],action:"Capture a dated native Relationship Health processor run, effective rules, stable population and independent reviewer approval."}
];
const allowed=[{parentKind:"application",childKind:"server",type:TYPE}]; // synthetic policy, NOT platform defaults
function assess(id){
 const s=scenarios.find(x=>x.id===id);if(!s)throw Error("Unknown synthetic relationship scenario");
 const findings=[],seen=new Set();
 for(let i=0;i<s.edges.length;i++){
  const e=s.edges[i],p=nodes[e.parent],c=nodes[e.child],key=[e.parent,e.child,e.type,e.port||""].join("|");
  if(seen.has(key))findings.push({kind:"duplicate",edge:i+1,text:"Repeated parent, child, type and port in sample"}); else seen.add(key);
  if(!p||!c||!e.type)findings.push({kind:"orphan",edge:i+1,text:"Missing endpoint or relationship type in sample"});
  if((p&&p.stale)||(c&&c.stale))findings.push({kind:"stale",edge:i+1,text:"One related CI is synthetically flagged stale"});
  if(p&&c&&!allowed.some(rule=>rule.parentKind===p.kind&&rule.childKind===c.kind&&rule.type===e.type))findings.push({kind:"governance",edge:i+1,text:"Violates this lab's fictional class/direction rule"});
 }
 return {scenario:s,findings,ciCount:new Set(s.edges.flatMap(e=>[e.parent,e.child])).size,edgeCount:s.edges.length,decision:findings.length?"HOLD — INVESTIGATE":"REVIEW — NOT APPROVED",evidence:"MOCK-ONLY",native:"NOT RUN",release:"HOLD"};
}
const gateTypes=[
["SCOPE","Read installed application/release, role and class scope; identify processor job enablement"],
["RELATION","Read cmdb_rel_ci and relationship-type records for an authorised synthetic sample; preserve sys_ids and provenance privately"],
["RULE","Read CI Class Manager suggested/dependent rules, inheritance, effective direction and exceptions"],
["HEALTH","Run or inspect the native Relationship Compliance Processor and reconcile affected counts, denominator and timestamp"],
["PERSONA","Execute allowed and denied persona ACL checks; record real role and outcome privately"],
["REVIEW","Re-run ingestion and impact review; obtain independent owner and release sign-off"]
];
const gates=scenarios.flatMap((s,i)=>gateTypes.map(([k,action],j)=>({id:"REL-"+String(i+1).padStart(2,"0")+"-"+String(j+1).padStart(2,"0"),scenario:s.id,action,expected:"Dated private native read-back and independent reviewer receipt required",status:"NOT RUN",decision:"HOLD",evidence:"MOCK-ONLY"})));
const headers=["Control ID","Synthetic scenario","Native validation action","Expected independent evidence","Native execution","Release decision","Evidence label","Instance alias","Release / version","Executor","Timestamp UTC","Private receipt","Independent reviewer"];
function q(x){return '"'+String(x??"").replace(/"/g,'""')+'"';}
function csv(id="all"){
 if(id!=="all"&&!scenarios.some(x=>x.id===id))throw Error("Unknown export scenario");
 const selected=gates.filter(x=>id==="all"||x.scenario===id);
 return [headers,...selected.map(x=>[x.id,x.scenario,x.action,x.expected,x.status,x.decision,x.evidence,"","","","","",""])].map(row=>row.map(q).join(",")).join("\r\n")+"\r\n";
}
function attach(doc){
 if(!doc||!doc.getElementById)return;
 const buttons=Array.from(doc.querySelectorAll("[data-case]")),panel=doc.getElementById("inspection");
 const el=(tag,klass,value)=>{const n=doc.createElement(tag);if(klass)n.className=klass;if(value!==undefined)n.textContent=String(value);return n;};
 function show(id){
  const r=assess(id),s=r.scenario;
  buttons.forEach(b=>b.setAttribute("aria-pressed",String(b.getAttribute("data-case")===id)));
  panel.replaceChildren();
  panel.append(el("p","kicker",s.kind+" / SYNTHETIC"),el("h3","",s.name),el("p","",s.summary));
  const metrics=el("div","metrics");for(const [v,label] of [[r.ciCount,"Fixture identifiers"],[r.edgeCount,"Fixture relationships"],[r.findings.length,"Review findings"]]){const c=el("div","metric");c.append(el("strong","",v),el("span","",label));metrics.append(c);}panel.append(metrics);
  const frame=el("section","mock");frame.setAttribute("aria-label","Illustrative relationship records, not a ServiceNow screenshot");
  frame.append(el("div","mockhead","ILLUSTRATIVE CMDB RELATIONSHIP REVIEW · NOT AN INSTANCE CAPTURE"));
  for(const edge of s.edges){const line=el("div","edge");line.append(el("strong","",edge.parent),el("span","arrow","→ "+edge.child),el("small","",edge.type+" · "+edge.source));frame.append(line);}panel.append(frame);
  const verdict=el("div","verdict");verdict.append(el("strong","",r.decision),el("p","",s.action));panel.append(verdict);
  const ul=el("ul","findings");
  if(!r.findings.length)ul.append(el("li","","No sample anomalies; native health remains NOT RUN."));
  for(const finding of r.findings)ul.append(el("li","",finding.kind.toUpperCase()+": "+finding.text));
  panel.append(el("h4","","Review findings"),ul);
  const selected=doc.getElementById("export-selected");selected.setAttribute("data-export",id);
  const count=doc.getElementById("test-count");count.textContent="6 native DEV gates remain NOT RUN / HOLD for "+s.name+".";
 }
 buttons.forEach(b=>b.addEventListener("click",()=>show(b.getAttribute("data-case"))));
 doc.querySelectorAll("[data-export]").forEach(b=>b.addEventListener("click",()=>{
  const id=b.getAttribute("data-export"),blob=new Blob([csv(id)],{type:"text/csv;charset=utf-8"}),url=URL.createObjectURL(blob),a=doc.createElement("a");
  a.href=url;a.download="cmdb-relationship-"+(id==="all"?"30-gates":id+"-6-gates")+".csv";doc.body.append(a);a.click();a.remove();URL.revokeObjectURL(url);
 }));
 show("duplicate");
}
if(typeof document!=="undefined")document.addEventListener("DOMContentLoaded",()=>attach(document));
return {scenarios,nodes,allowed,gateTypes,gates,headers,assess,csv,attach};
});