/* Session deck engine: scroll-snap slides, keys, index, full screen, reveal steps, ?shot=N. */
(function(){
  var blocks=[].slice.call(document.querySelectorAll('section.block'));
  var cur=0, root=document.documentElement, timers=[];
  var bar=document.getElementById('bar'), where=document.getElementById('where');
  var list=document.getElementById('index-list');
  var mq=window.matchMedia('(prefers-reduced-motion: reduce)');
  var reduce=mq.matches;

  blocks.forEach(function(b,i){
    var li=document.createElement('li'), btn=document.createElement('button');
    btn.type='button'; btn.textContent=(i+1)+'. '+(b.dataset.title||'Slide');
    btn.addEventListener('click',function(){hideIndex();go(i)});
    li.appendChild(btn); list.appendChild(li);
  });
  var idxBtns=[].slice.call(list.querySelectorAll('button'));

  function mark(i){
    cur=i;
    root.classList.toggle('at-cover',i===0||i===blocks.length-1);
    where.textContent=(i+1)+' / '+blocks.length;
    var pct=blocks.length>1?Math.round(i/(blocks.length-1)*100):0;
    bar.style.width=pct+'%'; bar.setAttribute('aria-valuenow',pct);
    idxBtns.forEach(function(x,k){x.setAttribute('aria-current',k===i?'true':'false')});
  }
  function go(i){
    i=Math.max(0,Math.min(blocks.length-1,i));
    blocks[i].scrollIntoView({behavior:reduce?'auto':'smooth',block:'start'});
    mark(i);
  }
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){if(e.isIntersecting)mark(blocks.indexOf(e.target))});
  },{rootMargin:'-50% 0px -50% 0px',threshold:0});
  blocks.forEach(function(b){io.observe(b)});

  /* reveal sections and step through [data-step] items, once each */
  function showAll(){
    root.classList.remove('motion'); timers.forEach(clearTimeout); timers=[];
    blocks.forEach(function(b){b.classList.add('in')});
    [].forEach.call(document.querySelectorAll('[data-step]'),function(el){el.classList.add('on')});
  }
  function reveal(b){
    if(b.classList.contains('in'))return;
    b.classList.add('in');
    var steps=[].slice.call(b.querySelectorAll('[data-step]'));
    var nums=steps.map(function(e){return +e.getAttribute('data-step')})
      .filter(function(v,i,a){return a.indexOf(v)===i}).sort(function(a,b){return a-b});
    nums.forEach(function(n,i){
      timers.push(setTimeout(function(){
        steps.forEach(function(e){if(+e.getAttribute('data-step')===n)e.classList.add('on')});
      },500+i*420));
    });
  }
  if(!mq.matches){
    root.classList.add('motion');
    var ro=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting)reveal(e.target)})},{threshold:0.35});
    blocks.forEach(function(b){ro.observe(b)});
    setTimeout(function(){blocks.forEach(function(b){var r=b.getBoundingClientRect();if(r.top<innerHeight*.65&&r.bottom>innerHeight*.35)reveal(b)})},120);
    setTimeout(function(){if(!blocks.some(function(b){return b.classList.contains('in')}))showAll()},2500);   /* nothing may stay hidden */
  }else{showAll()}
  if(mq.addEventListener)mq.addEventListener('change',function(e){if(e.matches)showAll()});

  /* full screen (F) */
  var fsRoot=root, fsBtn=document.getElementById('fs');
  var fsReq=fsRoot.requestFullscreen||fsRoot.webkitRequestFullscreen;
  function inFs(){return !!(document.fullscreenElement||document.webkitFullscreenElement)}
  function toggleFs(){
    if(!fsReq)return;
    if(inFs()){(document.exitFullscreen||document.webkitExitFullscreen).call(document)}
    else{var r=fsReq.call(fsRoot,{navigationUI:'hide'});if(r&&r.catch)r.catch(function(){})}
  }
  if(fsBtn){if(!fsReq)fsBtn.style.display='none';else fsBtn.addEventListener('click',function(e){e.stopPropagation();toggleFs()})}
  function fsResnap(){setTimeout(function(){if(blocks[cur])blocks[cur].scrollIntoView({behavior:'auto',block:'start'})},150)}
  document.addEventListener('fullscreenchange',fsResnap);
  document.addEventListener('webkitfullscreenchange',fsResnap);

  function hideIndex(){document.body.classList.remove('show-index')}
  function toggleIndex(){var on=document.body.classList.toggle('show-index');if(on)idxBtns[cur].focus()}
  document.addEventListener('keydown',function(e){
    if(e.metaKey||e.ctrlKey||e.altKey)return;
    var k=e.key;
    if(document.body.classList.contains('show-index')){if(k==='Escape'||k==='g'||k==='G'){e.preventDefault();hideIndex()}return}
    if(k==='ArrowDown'||k==='ArrowRight'||k==='PageDown'||k===' '){e.preventDefault();go(cur+1)}
    else if(k==='ArrowUp'||k==='ArrowLeft'||k==='PageUp'){e.preventDefault();go(cur-1)}
    else if(k==='Home'){e.preventDefault();go(0)}
    else if(k==='End'){e.preventDefault();go(blocks.length-1)}
    else if(k==='g'||k==='G'){e.preventDefault();toggleIndex()}
    else if(k==='f'||k==='F'){e.preventDefault();toggleFs()}
  });


  /* ?shot=N: show slide N alone, fully revealed, (screenshots, PDF export) */
  var shotM=location.search.match(/[?&]shot=(\d+)/);
  if(shotM){
    var sn=+shotM[1]-1;
    root.classList.add('shot');
    blocks.forEach(function(b,k){b.classList.toggle('shotsel',k===sn);b.classList.add('in')});
    [].forEach.call(document.querySelectorAll('[data-step]'),function(e){e.classList.add('on')});
  }
  mark(0);
})();
