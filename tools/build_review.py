"""Build the offline form; AI suggestions never count as human choices."""
import csv
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
source = json.loads((root / "collection/sources.json").read_text())["posts"]
by_id = {p["id"]: p for p in source}
with (root / "labels.csv").open(newline="", encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))
posts = []
for row in rows:
    post_id = int(row["note"].split("hn_id=")[1].split(";")[0])
    post = by_id[post_id]
    assert post["text"] == row["text"]
    posts.append(post)
suggestions = json.loads((root / "collection/ai-suggestions.json").read_text())["suggestions"]
assert all(s["row"] > 20 for s in suggestions)
payload = json.dumps({"posts": posts, "suggestions": suggestions,
                      "criteria": (root / "criteria.md").read_text()}, ensure_ascii=False).replace("<", "\\u003c")
html = r'''<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>TakeMeter — review your dataset</title>
<style>
body{margin:0;background:#f3f5fa;color:#162138;font:16px/1.55 system-ui,sans-serif}main{max-width:900px;margin:auto;padding:24px}section{background:white;border:1px solid #dce1eb;border-radius:14px;padding:22px;margin:18px 0}h1,h2{margin-top:0}button,input,select,textarea{font:inherit}button{background:#164f95;color:white;border:0;border-radius:8px;padding:11px 15px;margin:5px 5px 5px 0;cursor:pointer}button.secondary{background:#e8edf5;color:#162138}button:disabled{opacity:.4;cursor:default}textarea,select{box-sizing:border-box;padding:10px;border:1px solid #b6c0d0;border-radius:7px;width:100%;margin:6px 0}textarea{min-height:90px}.post,pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f8fafc;padding:18px;border-radius:8px}pre{font:inherit}small,.muted{color:#546277}.badge{display:inline-block;background:#eef3fc;padding:4px 10px;border-radius:30px}#message{font-weight:600;color:#175c38}a{color:#164f95}details{margin:12px 0}progress{width:100%;height:16px}.suggestion{border-left:4px solid #bd7d13;padding:12px;background:#fff7e5;margin:15px 0}[hidden]{display:none!important}
</style><main>
<h1>TakeMeter dataset review</h1>
<p class="muted">Your criteria are committed. Next: 20 independent labels, then review 180 AI suggestions.</p>
<section><h2>Start here</h2>
<p>The working file uses the first 200 collected comments in their original order. Another 60 remain in the source archive. No comment is shortened. Read the reading pack and review the draft definitions before starting.</p>
<p><strong>Comments 1–20:</strong> choose labels yourself without AI advice. <strong>Comments 21–200:</strong> read the full comment, consider the AI suggestion, then choose or correct its label. Nothing is counted as reviewed until you save your own choice.</p>
<details><summary>Label definitions and decision rules</summary><ul><li><strong>analysis:</strong> Supports its main claim with a specific, checkable detail, concrete first-hand observation or relevant cited source.</li><li><strong>unsupported:</strong> Primarily a statement, judgment, joke, agreement or reaction without specific support for its main point.</li><li><strong>question:</strong> Primarily requests information or clarification without advancing its own answer or advocating a conclusion.</li></ul><p>Supporting details must relate to the main claim. “I agree 100%” is not evidence. A quotation that the writer rejects does not by itself support the rejection. Rhetorical or self-answered questions follow the analysis/unsupported rule. Classify support present in the text; this is not fact-checking.</p></details>
<label><input id="taxonomy_ok" type="checkbox"> I have reviewed these definitions and will apply them consistently.</label>
<p><label>Resume an earlier downloaded checkpoint: <input id="state_import" type="file" accept=".json"></label></p>
</section>
<section><h2>Your committed acceptance criteria</h2><p>These are the criteria you supplied and committed before training. You do not need to write them again.</p><details><summary>Read the five criteria</summary><pre id="criteria"></pre></details></section>
<section><h2>Read and label each comment</h2><p id="progress_text"></p><progress id="progress" max="200" value="0"></progress><p><span class="badge" id="stage"></span></p><a id="source" target="_blank" rel="noopener"></a><p id="story"></p><div class="post" id="post"></div>
<div id="suggestion" class="suggestion" hidden><strong>AI suggestion — not a reviewed label</strong><p id="suggested_label"></p><p id="suggested_reason"></p><p id="boundary"></p></div>
<label>Your choice<select id="label"><option value="">Choose a label after reading</option><option>analysis</option><option>unsupported</option><option>question</option></select></label>
<label><input id="hard" type="checkbox"> This was a hard case for me</label><textarea id="note" placeholder="For a hard case: name both candidate labels and explain your decision using the rule."></textarea>
<button id="save">Save my choice and continue</button><button id="back" class="secondary">Previous</button><button id="next" class="secondary">Next saved comment</button><p id="counts"></p>
<button id="csv_export">Download labels.csv</button><button id="state_export" class="secondary">Download checkpoint</button><button id="dataset_export" class="secondary">Download dataset evidence</button>
<p>Record at least three actual hard-case decisions. AI boundary flags are suggestions and do not count as your decisions. The assignment cap is 70% for any label; your own criterion 3 sets a stricter 15%–45% target.</p>
</section><p id="message" role="status"></p><p class="muted">This runs offline and does not update GitHub. Download your CSV and checkpoint before closing. Replace labels.csv in your repository with the exported file and commit it before training.</p></main>
<script>
const data=__DATA__,posts=data.posts;
const suggestions=new Map(data.suggestions.map(s=>[s.source_id,s]));
const KEY='takemeter-hn-review-v1',allowed=['analysis','unsupported','question'];
const blank=()=>({label:'',note:'',hard:false,saved_at:null,provenance:''});
let state={index:0,taxonomy_ok:false,labels:posts.map(blank)};
function normalize(raw,version){
 if(!raw||!Array.isArray(raw.labels)||raw.labels.length<posts.length)throw Error('Checkpoint has too few comments.');
 const labels=raw.labels.slice(0,posts.length).map((r,i)=>{
  if(!r||!allowed.includes(r.label)&&r.label!=='')throw Error('Unknown label in checkpoint.');
  const provenance=i<20?'cold':version===1?'manual':r.provenance;
  if(r.label&&i>=20&&!['manual','ai_prelabel'].includes(provenance))throw Error('Missing label provenance.');
  return {label:r.label,note:String(r.note||''),hard:Boolean(r.hard),saved_at:r.saved_at||null,provenance:r.label?provenance:''};
 });
 return {index:Math.max(0,Math.min(posts.length-1,Number.isInteger(raw.index)?raw.index:0)),taxonomy_ok:Boolean(raw.taxonomy_ok),labels};
}
try{const old=JSON.parse(localStorage.getItem(KEY)||'null');if(old)state=normalize(old,old.version||1);}catch(e){}
const $=id=>document.getElementById(id),message=t=>$('message').textContent=t;
function persist(){try{localStorage.setItem(KEY,JSON.stringify({...state,version:2}));}catch(e){message('Download a checkpoint to preserve this session.');}}
function coldDone(){return state.labels.slice(0,20).every(r=>r.label);}
function download(name,body,type){const a=document.createElement('a'),url=URL.createObjectURL(new Blob([body],{type}));a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
function render(){
 if(!coldDone()&&state.index>=20)state.index=state.labels.slice(0,20).findIndex(r=>!r.label);
 const i=state.index,p=posts[i],r=state.labels[i],s=i>=20&&coldDone()?suggestions.get(p.id):null;
 const done=state.labels.filter(x=>x.label).length,cold=state.labels.slice(0,20).filter(x=>x.label).length;
 $('progress_text').textContent=`${done}/${posts.length} human choices saved · ${cold}/20 cold labels · comment ${i+1}`;$('progress').max=posts.length;$('progress').value=done;
 $('stage').textContent=i<20?'Cold: your independent choice':'Review the AI suggestion and choose your label';
 $('source').textContent=`HN ${p.id} · original comment`;$('source').href=p.source_url;$('story').textContent=p.story_title;$('post').textContent=p.text;
 $('suggestion').hidden=!s;$('suggested_label').textContent=s?s.label:'';$('suggested_reason').textContent=s?s.reason:'';$('boundary').textContent=s&&s.alternative?`Boundary to review: ${s.label} versus ${s.alternative}. This is not a student hard-case decision.`:'';
 $('label').value=r.label;$('note').value=r.note;$('hard').checked=r.hard;$('taxonomy_ok').checked=state.taxonomy_ok;
 $('back').disabled=i===0;$('next').disabled=i===posts.length-1||!r.label||i===19&&!coldDone();
 const counts={analysis:0,unsupported:0,question:0};state.labels.forEach(x=>{if(x.label)counts[x.label]++});
 $('counts').textContent='Reviewed choices only: '+Object.entries(counts).map(([l,n])=>`${l}: ${n} (${done?(100*n/done).toFixed(1):0}%)`).join(' · ');persist();
}
function csvBody(){
 const quote=x=>'"'+String(x).replaceAll('"','""')+'"';
 return 'text,label,note\r\n'+posts.map((p,i)=>{
  const r=state.labels[i],s=i>=20?suggestions.get(p.id):null;
  const stage=r.label?(i<20?'cold':r.provenance==='manual'?'manual; human_reviewed':'ai_prelabel; human_reviewed'):(i<20?'cold_pending':s?'ai_prelabel; review_pending':'unlabeled');
  let note=`${stage}; hn_id=${p.id}; source=${p.source_url}`;
  if(s&&(!r.label||r.provenance==='ai_prelabel'))note+=`; ai_suggested=${s.label}; ai_reason=${s.reason}`+(s.alternative?`; boundary_candidate=${s.alternative}`:'');
  if(r.label&&r.hard)note+='; hard_case';if(r.note)note+='; human_note='+r.note;
  return [p.text,r.label||s?.label||'',note].map(quote).join(',');
 }).join('\r\n')+'\r\n';
}
$('taxonomy_ok').onchange=()=>{state.taxonomy_ok=$('taxonomy_ok').checked;persist()};
$('save').onclick=()=>{
 if(!state.taxonomy_ok)return message('Review the taxonomy first.');if(state.index>=20&&!coldDone())return message('Complete the 20 independent labels first.');
 if(!$('label').value)return message('Read the whole comment and choose a label.');if($('hard').checked&&!$('note').value.trim())return message('Name both candidate labels and explain your decision.');
 const i=state.index;state.labels[i]={label:$('label').value,note:$('note').value.trim(),hard:$('hard').checked,saved_at:new Date().toISOString(),provenance:i<20?'cold':'ai_prelabel'};
 const missing=state.labels.findIndex(r=>!r.label);if(missing>=0)state.index=missing;message('Your choice is saved locally. Download a checkpoint to keep a copy.');render();
};
$('back').onclick=()=>{state.index=Math.max(0,state.index-1);render()};$('next').onclick=()=>{state.index=Math.min(posts.length-1,state.index+1);render()};
$('csv_export').onclick=()=>{download('labels.csv',csvBody(),'text/csv;charset=utf-8');const done=state.labels.filter(r=>r.label).length;message(`CSV downloaded: ${done} reviewed choices. Unfinished rows retain pending markers. Upload this file to GitHub; this form does not push it.`)};
$('state_export').onclick=()=>download('review-checkpoint.json',JSON.stringify({version:2,post_ids:posts.map(p=>p.id),state},null,2),'application/json');
$('state_import').onchange=async e=>{try{
 const d=JSON.parse(await e.target.files[0].text());if(![1,2].includes(d.version)||!Array.isArray(d.post_ids)||JSON.stringify(d.post_ids.slice(0,posts.length))!==JSON.stringify(posts.map(p=>p.id)))throw Error('This checkpoint belongs to another collection.');
 const restored=normalize(d.state,d.version);state=restored;render();message('Checkpoint restored. Earlier manual choices keep their manual provenance.');
}catch(err){message(err.message)}};
$('dataset_export').onclick=()=>{
 const done=state.labels.filter(r=>r.label).length,counts={analysis:0,unsupported:0,question:0};state.labels.forEach(r=>{if(r.label)counts[r.label]++});
 let text='# Dataset review evidence\n\nOnly saved human choices are counted below. AI suggestions still awaiting review are excluded.\n\n'+`Working comments: ${posts.length}. Reviewed: ${done}. Pending: ${posts.length-done}.\n\n`+'| Label | Reviewed count | Share of reviewed |\n|---|---:|---:|\n'+Object.entries(counts).map(([l,n])=>`| ${l} | ${n} | ${done?(100*n/done).toFixed(1)+'%':'undefined'} |`).join('\n')+'\n\n## Student hard-case decisions\n';
 let hard=0;posts.forEach((p,i)=>{const r=state.labels[i];if(r.label&&r.hard){hard++;text+=`\n### ${hard}. HN ${p.id}\n\n${p.source_url}\n\n`+p.text.split('\n').map(line=>'> '+line).join('\n')+`\n\n**Chosen label:** ${r.label}\n\n**Student explanation:** ${r.note}\n`;}});
 text+=`\nSaved student hard cases: ${hard}. At least three are required.\n`;download('dataset-review.md',text,'text/markdown');message('Reviewed counts and your saved hard-case decisions exported.');
};
$('criteria').textContent=data.criteria;render();
</script></html>'''
(root / "annotation_review.html").write_text(html.replace("__DATA__", payload), encoding="utf-8")
print(f"Built review form: {len(posts)} posts; {len(suggestions)} unreviewed AI suggestions; 20 untouched cold rows.")
