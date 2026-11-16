/* Public source-lineage review for two SEPARATE Diagnostic Workbench inventories.
 * This is a local, deterministic architectural walkthrough, not a live connector.
 * Historical source claims do not certify today's DEV state or customer outcomes.
 */
(function(root){
'use strict';
const tracks=Object.freeze([
 Object.freeze({
  id:'module',label:'Diagnostic module-pack catalogue',
  provenance:'Diagnostic-Workbench2 README_BUILD.md · 1 September 2026 source and historical DEV statement',
  scope:'x_1577958_dw2 base Workbench 2 (source-reported)',
  counts:Object.freeze([['Module-pack collectors','20'],['Rules','42'],['Correlations','4'],['Runbooks','67'],['Pack categories','10']]),
  envelope:'DIAG_ENVELOPE_BEGIN / DIAG_ENVELOPE_END',
  licensing:'ServiceNow platform roles and each selected product entitlement; script execution needs explicit instance approval.',
  boundaries:'The local-first Workbench does not run scripts. DIAG imports are validated; correlations suggest, not establish, causation.',
  gates:Object.freeze([
   ['Baseline identity','Read back actual installed app, version, scope and release date; compare with dated source.'],
   ['Applicability and entitlement','Review all ten pack domains against actual installed products, subscription and ACLs.'],
   ['Authorised collection','Obtain written clearance for bounded, aggregate-only read operations; Workbench never executes scripts.'],
   ['Evidence envelope','Validate DIAG markers, source population, query truncation and sensitive-data rejection.'],
   ['Rule interpretation','Reproduce relevant rule and correlation candidates; separate observations from conclusions.'],
   ['Independent sign-off','Human-review findings and draft solutions before any delivery handoff or publication.']
  ])
 }),
 Object.freeze({
  id:'knowledge',label:'Knowledge Intelligence companion',
  provenance:'Diagnostic-Workbench2 knowledge-intelligence/README.md · 30 September 2026 historical DEV statement',
  scope:'x_1577958_dw2 companion package 0.1.0 (source-reported)',
  counts:Object.freeze([['Knowledge packs','16'],['Read-only collectors','45'],['Evidence metrics','81'],['Rules and finding templates','65'],['Solution patterns','38']]),
  envelope:'==KI-EVIDENCE-BEGIN== / ==KI-EVIDENCE-END==',
  licensing:'Scoped KI roles plus actual product entitlements; external knowledge sources require content-reuse licences.',
  boundaries:'Companion package has its own KI evidence contract; historical lint or seed import is not today’s native execution.',
  gates:Object.freeze([
   ['Companion installation','Read back installed application and KI 0.1.0 update set, tables, roles and current deployment state.'],
   ['Scope and content licence','Confirm all applicable knowledge packs, licensed article sources and permissible reuse.'],
   ['Role and ACL separation','Test ki_admin/ki_user plus negative personas and evidence access restrictions.'],
   ['Collector safety','Re-run native read-only lint and approve bounded scripts before instance execution.'],
   ['Evidence interpretation','Validate KI markers, 81 metric definitions and full-population completeness; never parse as DIAG.'],
   ['Human publication review','Independently review 65 draft finding templates and 38 patterns before client reuse.']
  ])
 })
]);
function getTrack(id){
 const found=tracks.find(t=>t.id===id);
 if(!found)throw new Error('Unknown catalogue identity; review blocked');
 return found;
}
function evaluate(id){
 const selected=id==='both'?tracks:[getTrack(id)];
 const rows=[];
 for(const t of selected){
  if(t.gates.length!==6)throw new Error('Gate-count drift');
  t.gates.forEach((g,i)=>rows.push(Object.freeze({
   control_id:(t.id==='module'?'DLC-M':'DLC-K')+String(i+1).padStart(2,'0'),
   catalogue:t.label,control:g[0],required_native_evidence:g[1],
   evidence_class:'SOURCE-ONLY',execution:'NOT RUN',review:'UNREVIEWED',
   release:'HOLD',dev_verified:false,production_verified:false,
   screenshot_approved:false
  })));
 }
 if(rows.length!==selected.length*6||new Set(rows.map(r=>r.control_id)).size!==rows.length)throw new Error('Source identity drift');
 return Object.freeze({
  selection:id,rows:Object.freeze(rows),source_only:true,mock_only:true,
  native_executed:0,dev_verified:0,production_verified:0,release:'HOLD'
 });
}
const header=Object.freeze(['control_id','catalogue','control','required_native_evidence','evidence_class','execution','review','release','dev_verified','production_verified','screenshot_approved']);
function safeCsv(v){
 let s=String(v);
 if(/^[=+\-@\t\r]/.test(s))s="'"+s;
 return '"'+s.replace(/"/g,'""')+'"';
}
function exportCsv(report){
 if(!report||!['both','module','knowledge'].includes(report.selection)||!Array.isArray(report.rows))throw new Error('Invalid lineage report');
 const canonical=evaluate(report.selection);
 if(report.rows.length!==canonical.rows.length)throw new Error('Source row count changed');
 for(let i=0;i<canonical.rows.length;i++){
  const expected=canonical.rows[i],actual=report.rows[i];
  if(!actual||Object.keys(expected).some(k=>actual[k]!==expected[k]))throw new Error('Source assertion changed; export held');
 }
 return '\ufeff'+[header.map(safeCsv).join(','),...canonical.rows.map(r=>header.map(k=>safeCsv(r[k])).join(','))].join('\r\n')+'\r\n';
}
const api=Object.freeze({tracks,getTrack,evaluate,exportCsv});
if(typeof module!=='undefined'&&module.exports)module.exports=api;
root.DiagnosticLineageReview=api;
if(typeof document==='undefined')return;
const select=document.getElementById('lineage-track');
const facts=document.getElementById('lineage-facts');
const gates=document.getElementById('lineage-gates');
const status=document.getElementById('lineage-status');
const download=document.getElementById('lineage-download');
if(!select||!facts||!gates||!status||!download)return;
function make(tag,contents){const e=document.createElement(tag);e.textContent=contents;return e;}
function draw(){
 const report=evaluate(select.value);
 facts.replaceChildren();gates.replaceChildren();
 (select.value==='both'?tracks:[getTrack(select.value)]).forEach(t=>{
  const box=document.createElement('article');box.className='lineage-card';
  box.append(make('h3',t.label),make('p',t.provenance),make('p','Scope: '+t.scope));
  const dl=document.createElement('dl');
  t.counts.forEach(([key,value])=>{dl.append(make('dt',key),make('dd',value));});
  box.append(dl,make('p','Envelope: '+t.envelope),make('p','Entitlements: '+t.licensing),make('p','Boundary: '+t.boundaries));
  facts.append(box);
 });
 report.rows.forEach(row=>{
  const tr=document.createElement('tr');
  const th=make('th',row.control_id+' · '+row.control);th.scope='row';
  tr.append(th,make('td',row.catalogue),make('td',row.required_native_evidence),make('td','NOT RUN · HOLD'));
  gates.append(tr);
 });
 status.textContent=report.rows.length+' source-informed native checks · 0 executed · 0 DEV verified · 0 production verified · 0 screenshots approved · RELEASE HOLD';
}
select.addEventListener('change',draw);
download.addEventListener('click',()=>{
 try{
  const csv=exportCsv(evaluate(select.value));
  const url=URL.createObjectURL(new Blob([csv],{type:'text/csv;charset=utf-8'}));
  const a=document.createElement('a');a.href=url;a.download='diagnostic-catalogue-lineage-'+select.value+'-NOT-RUN-HOLD.csv';
  document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
 }catch(_error){status.textContent='Export rejected: canonical source identity could not be validated. HOLD.';}
});
draw();
})(typeof globalThis!=='undefined'?globalThis:this);
