"use strict";
/* Offline-only preflight of a 117-row CMDB acceptance workpack.
   It never certifies an execution, posts data or stores an uploaded receipt. */
(function(root,factory){
  const api=factory(root);
  if(typeof module==="object"&&module.exports)module.exports=api;
  else root.CMDBReceiptPreflight=api;
})(typeof globalThis!=="undefined"?globalThis:this,function(root){
  const MAX_BYTES=1024*1024;
  const HEADERS=Object.freeze(["Review stage","Control domain","Entry evidence prerequisite","Cross-domain dependency","Accountable role","Exit evidence criterion","Control ID","Synthetic scenario","Native DEV action","Expected independent evidence","Native execution","Release decision","Evidence class","Instance","Installed version","Executor","Execution UTC","Private evidence receipt","Independent reviewer"]);
  const STATUS=Object.freeze(["NOT RUN","PASS","FAIL","BLOCKED"]);
  const SAFE_ID=/^[A-Za-z][A-Za-z0-9._-]{2,63}$/;
  const RECEIPT_ID=/^[A-Za-z0-9][A-Za-z0-9._:-]{5,127}$/;
  const INSTANCE_ID=/^[A-Za-z0-9][A-Za-z0-9._-]{2,79}$/;
  const UTC=/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/;

  /* Bounded RFC4180-style CSV parser: double-quotes, commas and embedded line breaks.
     Rejects malformed quoting and extra blank records rather than guessing. */
  function parseCsv(input){
    if(typeof input!=="string"||input.length>MAX_BYTES)throw Error("CSV missing or larger than 1 MiB");
    const source=input.charCodeAt(0)===0xfeff?input.slice(1):input;
    if(!source)throw Error("Empty CSV");
    const out=[];let row=[],value="",quoted=false,closed=false,started=false;
    function endCell(){row.push(value);value="";closed=false;started=false;}
    function endRow(){endCell();out.push(row);row=[];if(out.length>118)throw Error("Unexpected number of CSV records");}
    for(let i=0;i<source.length;i++){
      const c=source[i];
      if(quoted){
        if(c==='"'){
          if(source[i+1]==='"'){value+='"';i++;}
          else{quoted=false;closed=true;}
        }else value+=c;
        continue;
      }
      if(c==='"'&&!started){quoted=true;started=true;continue;}
      if(c==='"')throw Error("Malformed CSV quote");
      if(c===','){endCell();continue;}
      if(c==='\r'||c==='\n'){
        if(c==='\r'&&source[i+1]==='\n')i++;
        endRow();continue;
      }
      if(closed)throw Error("Unexpected characters after quoted field");
      value+=c;started=true;
    }
    if(quoted)throw Error("Unclosed CSV field");
    if(started||closed||value!==""||row.length)endRow();
    if(out.some(r=>r.length!==HEADERS.length))throw Error("CSV must contain exactly 19 columns on every row");
    return out;
  }
  function expectedFields(row,tower){
    const meta=tower.METADATA.find(m=>m.key===row.key);
    return [row.step+" / "+row.stage,meta.title,row.entry,row.dependency,row.owner,row.exit,row.id,row.scenario,row.action,row.expected];
  }
  function issue(issues,id,reason){
    if(issues.length<25)issues.push({id,reason});
  }
  function audit(input,tower,sourceRows,now=new Date()){
    const result={hold:true,certified:false,valid:false,pending:0,passReported:0,failReported:0,blockedReported:0,reviewMetadataComplete:0,issues:[],message:"HOLD — independent native verification is still required"};
    let parsed,reference;
    try{
      if(!tower||!sourceRows)throw Error("Source definitions unavailable");
      reference=tower.planRows(sourceRows);
      parsed=parseCsv(input);
      if(parsed.length!==118)throw Error("Exactly 117 source-control rows are required");
      if(parsed[0].some((h,i)=>h!==HEADERS[i]))throw Error("Unexpected or reordered CSV header");
    }catch(e){issue(result.issues,"WORKPACK",e.message);return result;}
    const expected=new Map(reference.map(r=>[r.key+":"+r.id,expectedFields(r,tower)]));
    const seen=new Set();
    const names=new Map(tower.METADATA.map(m=>[m.title,m.key]));
    for(let i=1;i<parsed.length;i++){
      const cells=parsed[i];
      const id=String(cells[6]||"").replace(/[^A-Za-z0-9._-]/g,"").slice(0,64)||"ROW-"+i;
      const key=names.get(cells[1]);
      const marker=key+":"+cells[6];
      if(!key||!expected.has(marker)){issue(result.issues,id,"Unexpected control domain or ID");continue;}
      if(seen.has(marker)){issue(result.issues,id,"Duplicate control");continue;}
      seen.add(marker);
      if(expected.get(marker).some((v,j)=>v!==cells[j])){
        issue(result.issues,id,"A source-controlled stage, action, dependency or expected result was changed");
        continue;
      }
      const [native,decision,evidence,instance,version,executor,time,receipt,reviewer]=cells.slice(10);
      if(!STATUS.includes(native)){issue(result.issues,id,"Native status must be NOT RUN, PASS, FAIL or BLOCKED");continue;}
      if(decision!=="HOLD"){issue(result.issues,id,"Public workpack cannot record an approval or release GO");continue;}
      if(native==="NOT RUN"){
        result.pending++;
        if(evidence!=="MOCK-ONLY"||[instance,version,executor,time,receipt,reviewer].some(Boolean))issue(result.issues,id,"Unrun row must retain MOCK-ONLY classification and blank private fields");
        continue;
      }
      if(native==="PASS")result.passReported++;
      if(native==="FAIL")result.failReported++;
      if(native==="BLOCKED")result.blockedReported++;
      if(evidence!=="DEV-REPORTED")issue(result.issues,id,"Candidate execution must be classified DEV-REPORTED, never auto-verified");
      if(!INSTANCE_ID.test(instance))issue(result.issues,id,"Use a non-sensitive target alias, not a URL");
      if(!version||version.length>60||/[\r\n@/]/.test(version))issue(result.issues,id,"Installed version metadata missing or malformed");
      if(!SAFE_ID.test(executor))issue(result.issues,id,"Use a non-sensitive executor identifier");
      if(!UTC.test(time)||!Number.isFinite(Date.parse(time))||new Date(time).toISOString().replace(".000","")!==time||Date.parse(time)>now.getTime()+300000)issue(result.issues,id,"Execution UTC must be a valid, non-future ISO timestamp");
      if(!RECEIPT_ID.test(receipt))issue(result.issues,id,"Private evidence receipt must be an opaque reference, not a URL");
      if(!SAFE_ID.test(reviewer)||reviewer.toLowerCase()===executor.toLowerCase())issue(result.issues,id,"Independent reviewer identifier is missing, malformed or equals executor");
      else result.reviewMetadataComplete++;
    }
    if(seen.size!==117)issue(result.issues,"WORKPACK","Missing or duplicate source controls");
    result.valid=result.issues.length===0;
    result.message=result.valid?
      "HOLD — format and candidate metadata checks passed; no DEV or Production execution has been independently verified":
      "HOLD — workpack integrity or candidate evidence metadata is incomplete";
    return result;
  }


  /* Local-only aggregate triage. Derive display values solely from the five public
     control models and numeric counts. Never return or export imported metadata. */
  function stageTriage(input,tower,sourceRows,now=new Date()){
    const inspected=audit(input,tower,sourceRows,now);
    const output={hold:true,certified:false,parsed:false,inspected,unmapped:0,stages:[]};
    if(!tower||!sourceRows)return output;
    try{
      const reference=tower.planRows(sourceRows);
      const table=parseCsv(input);
      if(table.length!==118||table[0].some((v,i)=>v!==HEADERS[i]))return output;
      const meta=new Map(tower.METADATA.map(m=>[m.title,m.key]));
      const stageMap=new Map(tower.STAGES.map(s=>[s.key,{
        key:s.key,title:s.title,step:s.step,expected:reference.filter(r=>r.key===s.key).length,
        matched:0,pending:0,passReported:0,failReported:0,blockedReported:0,drift:0,missing:0,
        release:"HOLD"
      }]));
      const refs=new Map(reference.map(r=>[r.key+":"+r.id,expectedFields(r,tower)]));
      const seen=new Set();
      for(const cells of table.slice(1)){
        const key=meta.get(cells[1]),marker=key+":"+cells[6];
        if(!stageMap.has(key)||!refs.has(marker)){output.unmapped++;continue;}
        const stage=stageMap.get(key);
        if(seen.has(marker)||refs.get(marker).some((v,i)=>v!==cells[i])){stage.drift++;continue;}
        seen.add(marker);stage.matched++;
        if(cells[10]==="NOT RUN")stage.pending++;
        if(cells[10]==="PASS")stage.passReported++;
        if(cells[10]==="FAIL")stage.failReported++;
        if(cells[10]==="BLOCKED")stage.blockedReported++;
      }
      stageMap.forEach(s=>{s.missing=s.expected-s.matched;output.stages.push(Object.freeze(s));});
      output.parsed=true;
    }catch(_){/* Fail closed: never derive an export from malformed or oversized input. */}
    return output;
  }
  function stageCsv(report){
    if(!report||!report.parsed||report.stages.length!==5)throw Error("HOLD — valid 117-row schema required");
    const head=["Stage","Public control domain","Expected","Source-matched","NOT RUN reported","PASS reported","FAIL reported","BLOCKED reported","Missing source matches","Duplicate or changed source rows","Public preflight","Release decision","Evidence status"];
    const esc=s=>'"'+String(s).replace(/"/g,'""')+'"';
    const rows=report.stages.map(s=>[
      s.step,s.title,s.expected,s.matched,s.pending,s.passReported,s.failReported,s.blockedReported,s.missing,s.drift,
      report.inspected.valid?"FORMAT CHECK ONLY":"REVIEW ISSUES","HOLD","NOT INDEPENDENTLY VERIFIED"
    ]);
    return [head,...rows].map(r=>r.map(esc).join(",")).join("\r\n")+"\r\n";
  }

  function attach(doc){
    const input=doc.getElementById("tower-receipt-file");
    if(!input)return;
    const status=doc.getElementById("tower-receipt-status");
    const counts=doc.getElementById("tower-receipt-counts");
    const issues=doc.getElementById("tower-receipt-issues");
    const stageBody=doc.getElementById("tower-receipt-stage-body");
    const stageExport=doc.getElementById("tower-receipt-stage-export");
    const stageNote=doc.getElementById("tower-receipt-stage-status");
    let lastStageReport=null;
    if(stageExport)stageExport.addEventListener("click",()=>{
      if(!lastStageReport||!lastStageReport.parsed)return;
      const url=URL.createObjectURL(new Blob([stageCsv(lastStageReport)],{type:"text/csv;charset=utf-8"}));
      const link=doc.createElement("a");link.href=url;link.download="cmdb-stage-triage-aggregate-HOLD.csv";
      doc.body.append(link);link.click();link.remove();URL.revokeObjectURL(url);
      stageNote.textContent="Five aggregate stage counts exported · HOLD. No private source fields or execution evidence included.";
    });
    input.addEventListener("change",async ()=>{
      const f=input.files&&input.files[0];
      input.value="";issues.replaceChildren();counts.textContent="";
      lastStageReport=null;
      if(stageBody)stageBody.replaceChildren();
      if(stageExport)stageExport.disabled=true;
      if(stageNote)stageNote.textContent="HOLD — no stage summary available.";
      if(!f){status.textContent="No file selected. Release decision HOLD.";return;}
      if(f.size>MAX_BYTES){status.textContent="HOLD — CSV is larger than 1 MiB. No data retained.";return;}
      try{
        const rows=root.CMDBAssuranceTower.createRows({
          ire:root.CMDBSourceAcceptance,tags:root.CMDBTagGovernance,health:root.CMDBHealthAssurance,
          relationships:root.CMDBRelationshipAssurance,lifecycle:root.CMDBPolicyLab
        });
        const report=stageTriage(await f.text(),root.CMDBAssuranceTower,rows);
        const result=report.inspected;
        lastStageReport=report;
        if(report.parsed&&stageBody){
          report.stages.forEach(s=>{
            const tr=doc.createElement("tr");
            [s.step+" · "+s.title,String(s.matched)+"/"+s.expected,String(s.pending),String(s.passReported),String(s.failReported),String(s.blockedReported),String(s.missing+s.drift),"HOLD"].forEach(value=>{
              const td=doc.createElement("td");td.textContent=value;tr.append(td);
            });
            stageBody.append(tr);
          });
          if(stageExport)stageExport.disabled=false;
          if(stageNote)stageNote.textContent=(result.valid?"Schema-consistent":"Issues detected")+" · "+report.unmapped+" unmatched input row(s). These are operator-reported counts, never independently verified. All stages HOLD.";
        }
        status.textContent=result.message;
        counts.textContent="117 required · "+result.pending+" NOT RUN · "+result.passReported+" PASS reported · "+result.failReported+" FAIL reported · "+result.blockedReported+" BLOCKED reported · "+result.reviewMetadataComplete+" candidate reviewer fields complete. Native DEV-VERIFIED 0 · PRODUCTION-VERIFIED 0.";
        result.issues.slice(0,8).forEach(item=>{
          const li=doc.createElement("li");li.textContent=item.id+": "+item.reason;issues.append(li);
        });
        if(result.issues.length>8){const li=doc.createElement("li");li.textContent="Additional issues withheld; correct the offline source workpack.";issues.append(li);}
      }catch(_){status.textContent="HOLD — could not inspect this file safely. No data retained.";}
    });
  }
  if(typeof document!=="undefined")document.addEventListener("DOMContentLoaded",()=>attach(document));
  return Object.freeze({MAX_BYTES,HEADERS,parseCsv,audit,stageTriage,stageCsv,attach});
});
