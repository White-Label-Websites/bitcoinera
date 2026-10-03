// Polishes the Affcoin signup widget once its script has injected the form:
// links the legal wording to our pages, adds autofill hints and a password
// toggle, and gives the button a clearer label.
(function(){
  var host=document.querySelector(".wl-signup");if(!host)return;
  function link(label,re,href,text){
    if(!label||label.querySelector("a"))return;
    label.innerHTML=label.innerHTML.replace(re,'<a href="'+href+'" target="_blank" rel="noopener">'+text+"</a>");
    label.querySelector("a").addEventListener("click",function(e){e.stopPropagation()});
  }
  function polish(){
    var form=host.querySelector(".signup_form");if(!form||form.dataset.polished)return false;
    form.dataset.polished="1";
    link(form.querySelector('label[for="terms"]'),/terms and conditions/i,"/terms/","terms and conditions");
    var nl=form.querySelector('label[for="newsletter"]');
    link(nl,/privacy policy/i,"/privacy-policy/","privacy policy");
    var ac={firstname:"given-name",lastname:"family-name",email:"email",password:"new-password",phone:"tel"};
    Object.keys(ac).forEach(function(n){var i=form.querySelector('[name="'+n+'"]');if(i)i.setAttribute("autocomplete",ac[n])});
    var pw=form.querySelector('input[name="password"]');
    if(pw&&pw.parentNode){
      var wrap=document.createElement("div");wrap.className="pw-wrap";
      pw.parentNode.insertBefore(wrap,pw);wrap.appendChild(pw);
      var t=document.createElement("button");t.type="button";t.className="pw-toggle";t.textContent="Show";
      t.setAttribute("aria-label","Show password");
      t.addEventListener("click",function(){var show=pw.type==="password";pw.type=show?"text":"password";t.textContent=show?"Hide":"Show";t.setAttribute("aria-label",show?"Hide password":"Show password")});
      wrap.appendChild(t);
    }
    var btn=form.querySelector('input[type="submit"]');
    if(btn){
      btn.value="Create my free account";
      var p=document.createElement("p");p.className="signup-reassure";
      p.textContent="$10,000 virtual balance · Live market prices";
      btn.parentNode.appendChild(p);
    }
    return true;
  }
  if(polish())return;
  var mo=new MutationObserver(function(){if(polish())mo.disconnect()});
  mo.observe(host,{childList:true,subtree:true});
})();
