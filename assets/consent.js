// Google Analytics 4 behind a consent banner (Consent Mode v2).
// Nothing is measured with cookies until the visitor clicks "Accept"; the
// choice is remembered in localStorage and can be changed from any element
// with [data-cookie-settings]. The measurement ID comes from data-ga on the
// <script> tag, so the same file serves every white-label site.
(function(){
  var me=document.currentScript,id=me&&me.getAttribute("data-ga");if(!id)return;
  var KEY="consent.v1",choice=null;
  try{choice=localStorage.getItem(KEY)}catch(e){}
  window.dataLayer=window.dataLayer||[];
  function gtag(){dataLayer.push(arguments)}window.gtag=gtag;
  var granted=choice==="granted"?"granted":"denied";
  gtag("consent","default",{ad_storage:"denied",ad_user_data:"denied",ad_personalization:"denied",analytics_storage:granted,wait_for_update:500});
  gtag("js",new Date());gtag("config",id);
  var s=document.createElement("script");s.async=true;s.src="https://www.googletagmanager.com/gtag/js?id="+id;document.head.appendChild(s);

  function save(v){
    try{localStorage.setItem(KEY,v)}catch(e){}
    gtag("consent","update",{analytics_storage:v});
  }
  function banner(){
    if(document.querySelector(".consent"))return;
    var b=document.createElement("div");b.className="consent";b.setAttribute("role","dialog");b.setAttribute("aria-label","Cookie choice");
    b.innerHTML='<p>We use Google Analytics cookies to count visits and see which pages help. Nothing else. <a href="/privacy-policy/#cookies">Details</a></p>'+
      '<div class="consent-actions"><button type="button" data-v="denied">Decline</button><button type="button" class="yes" data-v="granted">Accept</button></div>';
    b.addEventListener("click",function(e){var v=e.target.getAttribute&&e.target.getAttribute("data-v");if(!v)return;save(v);b.remove()});
    document.body.appendChild(b);
  }
  function ready(fn){document.readyState==="loading"?document.addEventListener("DOMContentLoaded",fn):fn()}
  ready(function(){
    if(!choice)banner();
    document.addEventListener("click",function(e){
      var t=e.target.closest&&e.target.closest("[data-cookie-settings]");if(!t)return;
      e.preventDefault();banner();
    });
  });
})();
