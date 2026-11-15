"use strict";
const {test}=require("node:test");
const assert=require("node:assert/strict");
const fs=require("node:fs");
const path=require("node:path");
const vm=require("node:vm");
const page=fs.readFileSync(path.join(__dirname,"..","workbench-source-dev-gap-board.html"),"utf8");
function harness(){
  const captured={blob:null,clicked:false,revoked:false};
  const buttons=["All","Delivery","Diagnostic","Cross-workbench"].map(filter=>({
    dataset:{filter},attributes:{},setAttribute(k,v){this.attributes[k]=v;},
    addEventListener(k,fn){assert.equal(k,"click");this.click=fn;}
  }));
  const cards=[...page.matchAll(/<article class="gate" data-group="([^"]+)"/g)].map(x=>({dataset:{group:x[1]},hidden:false}));
  const nodes={results:{textContent:""},download:{disabled:true,addEventListener(k,fn){assert.equal(k,"click");this.click=fn;}}, "export-status":{textContent:""}};
  const document={
    querySelectorAll(sel){if(sel==="[data-filter]")return buttons;if(sel===".gate")return cards;throw Error(sel);},
    getElementById(id){if(!nodes[id])throw Error(id);return nodes[id];},
    createElement(tag){assert.equal(tag,"a");return {click(){captured.clicked=true;},remove(){}};},
    body:{appendChild(){}}
  };
  class BlobStub {constructor(parts,options){captured.blob=parts.join("");captured.mime=options.type;}}
  const URLStub={createObjectURL(){return "blob:synthetic";},revokeObjectURL(url){assert.equal(url,"blob:synthetic");captured.revoked=true;}};
  const script=page.match(/<script>([\s\S]*?)<\/script>/);
  assert.ok(script,"inline offline script exists");
  vm.runInNewContext(script[1],{document,Blob:BlobStub,URL:URLStub});
  return {buttons,cards,nodes,captured};
}
test("12 unique controls, expected split, review remains NOT RUN",()=>{
  const matches=[...page.matchAll(/<article class="gate" data-group="([^"]+)" aria-labelledby="gate-([^"]+)"/g)];
  assert.equal(matches.length,12);
  assert.equal(new Set(matches.map(x=>x[2])).size,12);
  assert.deepEqual(["Delivery","Diagnostic","Cross-workbench"].map(x=>matches.filter(g=>g[1]===x).length),[5,4,3]);
  assert.equal((page.match(/NOT RUN · HOLD<\/span>/g)||[]).length,12);
});
test("filtering is accessible, complete and does not promote verification",()=>{
  const h=harness();
  assert.equal(h.nodes.download.disabled,false);
  for(const [filter,expected] of [["Delivery",5],["Diagnostic",4],["Cross-workbench",3],["All",12]]){
    const button=h.buttons.find(x=>x.dataset.filter===filter);
    button.click();
    assert.equal(h.cards.filter(x=>!x.hidden).length,expected);
    assert.equal(button.attributes["aria-pressed"],"true");
    assert.match(h.nodes.results.textContent,new RegExp("^"+expected+" of 12"));
  }
});
test("CSV exports every gate, no approvals, with blank private receipts",()=>{
  const h=harness();h.nodes.download.click();
  const lines=h.captured.blob.trim().split("\r\n");
  assert.equal(lines.length,13);
  assert.ok(lines[0].includes("independent_reviewer"));
  assert.ok(lines.slice(1).every(x=>x.includes('"NOT RUN","HOLD","SOURCE-ONLY"')));
  assert.ok(lines.slice(1).every(x=>x.endsWith(',"","","","","",""')));
  assert.doesNotMatch(h.captured.blob,/DEV-VERIFIED|PRODUCTION-VERIFIED|"PASSED"|"APPROVED"/);
  assert.ok(h.captured.clicked && h.captured.revoked);
  assert.equal(h.captured.mime,"text/csv;charset=utf-8");
});
test("page is offline, accessibly labelled and never renders a real screenshot",()=>{
  for(const fragment of ['id="main"','role="group"','aria-live="polite"','prefers-reduced-motion',"connect-src 'none'","img-src 'none'","form-action 'none'","no ServiceNow subscription","DEV-REPORTED","SOURCE-ONLY"]){
    assert.ok(page.includes(fragment),fragment);
  }
  assert.doesNotMatch(page,/<(?:img|iframe|picture)\b/i);
  assert.doesNotMatch(page,/\blocalStorage\b|\bsessionStorage\b|\bfetch\s*\(|XMLHttpRequest/);
});
