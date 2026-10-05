# Generates the static content pages of bitcoinera.com and its sitemap.
# Run from anywhere: python3 _build/build_pages.py (writes <slug>/index.html
# next to this folder). GitHub Pages skips folders starting with "_".
import os, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://bitcoinera.com"
GA_ID = "G-9W341WVCHC"
UPDATED = "3 October 2026"

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://bitcoinera.com/{slug}/">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://bitcoinera.com/{slug}/">
<meta property="og:type" content="{ogtype}">
{robots}<meta name="theme-color" content="#ffffff">
<link rel="preload" href="/assets/fonts/Archivo-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/fonts/fonts.css">
<link rel="stylesheet" href="/assets/site.css">
<script src="/assets/consent.js" data-ga="{ga}"></script>
{jsonld}</head>
<body>
<p class="notice" role="note">Educational simulator. Virtual money only: no deposit, no real trading.</p>

<div class="wrap top">
  <a class="mark" href="/"><img src="/assets/logo.png" alt="Bitcoin Era" width="192" height="34"></a>
  <nav aria-label="Main"><a href="/#rules">The rules</a><a href="/contact/"{cur_contact}>Contact</a></nav>
</div>

<main class="page">
  <div class="wrap">
    <p class="kicker">{kicker}</p>
    <h1>{h1}</h1>
{updated}    <div class="prose">
{body}
    </div>
  </div>
</main>

<footer>
  <div class="wrap">
    {footer_nav}
    <span>&copy; 2026 Bitcoin Era</span>
    <small>Educational simulator. All balances are virtual and no real money is traded. Nothing on this site is financial advice. Crypto-assets are high risk and results on virtual money do not predict real results. Sign-up is handled by our partner AFFCOIN, and we may receive a commission when you open an account.</small>
  </div>
</footer>
{scripts}</body>
</html>
"""

CTA = """      <div class="page-cta">
        <p>{text}</p>
        <a class="btn" href="/#start">Build my first bot <span aria-hidden="true">&rarr;</span></a>
      </div>"""

PAGES = []

# ---------------------------------------------------------------- contact
PAGES.append(dict(
  slug="contact", kicker="Contact", h1="Talk to the Bitcoin Era team",
  title="Contact | Bitcoin Era",
  desc="Questions about the crypto bot challenges, your virtual balance or the rules? Send the Bitcoin Era team a message and we will reply by email.",
  body="""      <p>Questions about a challenge, the rules or how your bot is evaluated? Send us a message and we will reply by email, usually within two working days.</p>
      <form class="cform" id="cform" novalidate>
        <div class="row">
          <label>Name<input name="name" type="text" autocomplete="name" maxlength="100" required></label>
          <label>Email<input name="email" type="email" autocomplete="email" maxlength="200" required></label>
        </div>
        <label>Message<textarea name="message" maxlength="5000" required></textarea></label>
        <div class="hp" aria-hidden="true"><label>Website<input name="website" type="text" tabindex="-1" autocomplete="off"></label></div>
        <button class="btn" type="submit">Send message <span aria-hidden="true">&rarr;</span></button>
        <p class="cform-status" role="status" aria-live="polite"></p>
      </form>
      <h2>Login, password or verification code</h2>
      <p>Accounts are handled by our partner AFFCOIN. For a lost password, a verification code that never arrived or a request about your account data, you can also write to <a href="mailto:support@affcoin.com">support@affcoin.com</a>.</p>
      <div class="callout"><p><strong>We will never ask you for money, a card number or a crypto wallet.</strong> Every balance on Bitcoin Era is virtual. If someone contacts you on our behalf and asks for a payment, it is not us.</p></div>""",
  scripts="""<script>
(function(){
  var f=document.getElementById("cform");if(!f)return;
  var st=f.querySelector(".cform-status"),btn=f.querySelector("button");
  function show(msg,cls){st.textContent=msg;st.className="cform-status "+(cls||"")}
  f.addEventListener("submit",function(e){
    e.preventDefault();
    var d={name:f.name.value.trim(),email:f.email.value.trim(),message:f.message.value.trim(),website:f.website.value};
    if(!d.name||!d.message||!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(d.email)){show("Please fill in your name, a valid email and a message.","err");return}
    btn.disabled=true;show("Sending...");
    fetch("https://bitcoinera-contact.martinratinaud.workers.dev",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(d)})
      .then(function(r){return r.json().then(function(j){return{ok:r.ok&&j.ok,j:j}})})
      .then(function(res){if(res.ok){f.reset();show("Thanks, your message has been sent. We will reply by email.","ok")}else{show(res.j.error||"Message could not be sent. Please try again later.","err")}})
      .catch(function(){show("Message could not be sent. Please try again later.","err")})
      .then(function(){btn.disabled=false});
  });
})();
</script>
"""))

# ---------------------------------------------------------------- legal notice
# TODO before going live: replace the publisher block with the legal entity
# (company name, registration number, address, director of publication).
PAGES.append(dict(
  slug="legal-notice", kicker="Legal", h1="Legal notice", title="Legal notice | Bitcoin Era",
  desc="Who publishes bitcoinera.com, who hosts it, who runs the trading accounts and how to reach us.",
  body="""      <h2>Publisher</h2>
      <dl class="facts">
        <dt>Site</dt><dd>bitcoinera.com</dd>
        <!-- TODO: legal entity, registration number and registered address of the publisher -->
        <dt>Publisher</dt><dd>Bitcoin Era, independent publisher and owner of the bitcoinera.com domain name</dd>
        <dt>Contact</dt><dd><a href="/contact/">Contact form</a></dd>
      </dl>
      <h2>Hosting</h2>
      <dl class="facts">
        <dt>Host</dt><dd>GitHub, Inc. (GitHub Pages)</dd>
        <dt>Address</dt><dd>88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, United States</dd>
        <dt>Contact form relay</dt><dd>Cloudflare, Inc., 101 Townsend Street, San Francisco, CA 94107, United States</dd>
      </dl>
      <h2>Accounts and affiliate disclosure</h2>
      <p>Account creation and login are handled by our partner AFFCOIN, an affiliate network. We may receive a commission when you open an account through this site. This never costs you anything, since the challenge is free. AFFCOIN can be reached at <a href="https://affcoin.com/" rel="nofollow noopener" target="_blank">affcoin.com</a> and <a href="mailto:contact@affcoin.com">contact@affcoin.com</a>. The data you enter in the sign-up form is sent directly to AFFCOIN and handled under <a href="https://affcoin.com/privacy" rel="nofollow noopener" target="_blank">its privacy policy</a>.</p>
      <h2>No connection with the former &ldquo;Bitcoin Era&rdquo; software</h2>
      <p>The bitcoinera.com domain name was acquired by an independent publisher. It runs a free educational trading simulator and has no connection with any automated trading software sold under the same name.</p>
      <h2>Not financial advice</h2>
      <p>Bitcoin Era is an educational simulator. Every balance is virtual, no real money is traded and nothing on this site is investment, financial or tax advice, or an invitation to buy crypto-assets. Results achieved with virtual money do not predict results with real money. Crypto-assets are high risk: you could lose all the money you invest, and you are unlikely to be protected if something goes wrong.</p>
      <h2>Intellectual property</h2>
      <p>The texts, design and code of this site belong to the publisher unless stated otherwise. Brand names quoted on this site belong to their owners and are used for identification only.</p>
      <h2>Related pages</h2>
      <ul><li><a href="/terms/">Terms of use</a></li><li><a href="/privacy-policy/">Privacy policy</a></li></ul>"""))

# ---------------------------------------------------------------- privacy
PAGES.append(dict(
  slug="privacy-policy", kicker="Legal", h1="Privacy policy", title="Privacy policy | Bitcoin Era",
  desc="What personal data bitcoinera.com collects, why, who receives it, how long it is kept and how to exercise your rights.",
  body="""      <p>This policy explains what happens to your personal data when you visit bitcoinera.com, write to us or open an account. We collect as little as we can.</p>
      <h2>1. Who is responsible</h2>
      <p>The publisher of bitcoinera.com (see the <a href="/legal-notice/">legal notice</a>) is responsible for the data collected through this site&rsquo;s contact form. Data entered in the sign-up form is collected on this page and sent directly to our partner AFFCOIN. For that collection and transfer we act together with AFFCOIN; AFFCOIN then handles your account and is responsible for it under <a href="https://affcoin.com/privacy" rel="nofollow noopener" target="_blank">its own privacy policy</a>. You can exercise your rights with either of us.</p>
      <h2>2. What we collect and why</h2>
      <table>
        <thead><tr><th>When</th><th>Data</th><th>Purpose</th><th>Legal basis</th></tr></thead>
        <tbody>
          <tr><td>You use the contact form</td><td>Name, email, message</td><td>Answer your message</td><td>Legitimate interest, or steps before a contract</td></tr>
          <tr><td>You open an account</td><td>First and last name, email, password, phone number, newsletter choice</td><td>Create and run your challenge account, verify it, and send you news if you opted in (handled by AFFCOIN)</td><td>Contract; consent for the newsletter</td></tr>
          <tr><td>You visit any page</td><td>IP address, browser, pages requested (technical logs)</td><td>Deliver the site and keep it secure</td><td>Legitimate interest</td></tr>
        </tbody>
      </table>
      <p>We do not sell your data and we do not run advertising trackers on this site. Analytics only uses cookies if you accept them (see section 5).</p>
      <h2>3. Who receives it</h2>
      <ul>
        <li><strong>AFFCOIN</strong> and the providers it works with, for everything you type in the sign-up form, sent directly from your browser to its servers.</li>
        <li><strong>Cloudflare</strong>, which relays contact-form messages to our mailbox.</li>
        <li><strong>GitHub</strong>, which hosts the site and keeps technical access logs.</li>
        <li><strong>Google</strong> (Google Analytics), only if you accept analytics cookies: pages viewed, approximate location, device and browser, used to count visits. IP addresses are not stored by Google Analytics 4. Data may be processed in the United States under the EU-US Data Privacy Framework.</li>
      </ul>
      <p>Some of these providers are based in the United States. Transfers rely on the safeguards they offer, such as the EU-US Data Privacy Framework or standard contractual clauses.</p>
      <h2>4. How long we keep it</h2>
      <p>Contact messages are kept for up to 3 years after our last exchange, then deleted. Account data is kept by AFFCOIN for as long as your account is open and then according to its policy.</p>
      <h2 id="cookies">5. Cookies</h2>
      <p>We use Google Analytics cookies (<code>_ga</code>, <code>_ga_*</code>, kept up to 13 months) to count visits and see which pages are useful. They are set only after you click &ldquo;Accept&rdquo; in the cookie banner. If you decline, Google Analytics runs without cookies and receives no identifier for you. We do not use advertising cookies. Your choice is stored in your browser and you can change it at any time with the <a href="/privacy-policy/#cookies" data-cookie-settings>cookie settings</a> link at the bottom of every page.</p>
      <p>Our fonts are served from our own host. The sign-up widget, loaded from affcoin.com, may store what it needs to run the form and your session. Those cookies are covered by AFFCOIN&rsquo;s policy.</p>
      <h2>6. Your rights</h2>
      <p>You can ask to access, correct or delete your data, object to its use, restrict it, or receive a copy. Withdraw your newsletter consent at any time with the unsubscribe link in each email. To exercise a right, use our <a href="/contact/">contact form</a>, or write to <a href="mailto:support@affcoin.com">support@affcoin.com</a> for account data. You can also complain to your data protection authority.</p>
      <h2>7. Changes</h2>
      <p>We will update this page when our practices change. The date at the top shows the latest version.</p>"""))

# ---------------------------------------------------------------- terms
PAGES.append(dict(
  slug="terms", kicker="Legal", h1="Terms of use", title="Terms of use | Bitcoin Era",
  desc="The rules for using bitcoinera.com and taking part in the virtual crypto bot trading challenges.",
  body="""      <p>By using bitcoinera.com or opening an account through it, you accept these terms. If you do not agree with them, please do not use the site.</p>
      <h2>1. What Bitcoin Era is</h2>
      <p>Bitcoin Era is an educational simulator. You build a crypto trading bot, run it on live market prices with a <strong>virtual balance of $10,000</strong>, and try to clear three levels. No real money is deposited, traded or won, and the virtual balance has no cash value.</p>
      <h2>2. Who can join</h2>
      <p>You must be at least 18 years old and allowed to use this kind of service where you live. One person, one account. The information you give when signing up must be accurate.</p>
      <h2>3. Your account</h2>
      <p>Accounts are created and run by our partner AFFCOIN, whose own terms also apply. We may receive a commission when you open an account. Keep your password private. You are responsible for what happens under your account.</p>
      <h2>4. Challenge rules</h2>
      <table>
        <thead><tr><th>Level</th><th>Target</th><th>Min. days</th><th>Max. days</th><th>Max. drawdown</th><th>Daily drawdown</th></tr></thead>
        <tbody>
          <tr><td>Level 1</td><td>+10%</td><td>5</td><td>10</td><td>-10%</td><td>-5%</td></tr>
          <tr><td>Level 2</td><td>+5%</td><td>5</td><td>No limit</td><td>-10%</td><td>-5%</td></tr>
          <tr><td>Level 3</td><td>+5%</td><td>None</td><td>No limit</td><td>-10%</td><td>-5%</td></tr>
        </tbody>
      </table>
      <p>Breaching the daily or the maximum drawdown ends the challenge immediately. We may adjust the rules for future challenges; a challenge already running keeps the rules it started with.</p>
      <h2>5. Fair use</h2>
      <p>Do not exploit bugs, price-feed errors or latency, share accounts, use several accounts to game the levels, or attack the platform. We may suspend an account that breaks these rules.</p>
      <h2>6. No financial advice, no guarantee</h2>
      <p>Nothing on Bitcoin Era is investment, financial or tax advice, or an invitation to buy crypto-assets. Performance on virtual money does not predict results on real money, and crypto-assets are high risk. The service is provided as is, and may be interrupted for maintenance.</p>
      <h2>7. Liability</h2>
      <p>Since no real money is at stake, we are not liable for any trading decision you take outside Bitcoin Era, or for any loss arising from it. Nothing in these terms limits liability that cannot legally be limited.</p>
      <h2>8. Personal data</h2>
      <p>See our <a href="/privacy-policy/">privacy policy</a>.</p>
      <h2>9. Changes and contact</h2>
      <p>We may update these terms; the date at the top shows the current version. Questions: <a href="/contact/">contact us</a>.</p>"""))

# ---------------------------------------------------------------- guide (SEO: crypto prop firm / challenge)
GUIDE_FAQ = [
  ("What is a crypto prop firm challenge?", "It is an evaluation where you trade a firm's account under strict rules, usually a profit target plus daily and maximum loss limits. Pass it and the firm lets you trade a larger funded account and share the profits."),
  ("Why do most traders fail prop firm challenges?", "Usually because of the drawdown limits, not the profit target. One bad day or one oversized position breaks the daily limit and ends the evaluation."),
  ("Can I practise a prop firm challenge for free?", "Yes. On Bitcoin Era you run a bot on live crypto prices with a virtual $10,000 under the same kind of rules: a profit target, a -10% maximum drawdown and a -5% daily drawdown."),
]
PAGES.append(dict(
  slug="crypto-prop-firm-challenge", kicker="Guide", ogtype="article",
  h1="Crypto prop firm challenges: how they work and how to practise",
  title="Crypto Prop Firm Challenge: Rules Explained + Free Practice",
  desc="How crypto prop firm challenges work: profit targets, daily and maximum drawdown, minimum trading days. Practise the same rules for free with a trading bot and virtual money.",
  body="""      <p>A prop firm challenge is a trading exam. You trade under fixed rules, and if you pass, the firm gives you access to a larger account. Crypto prop firms apply the same idea to Bitcoin and other crypto-assets. The rules are simple to read and hard to respect, which is why practising them first pays off.</p>
      <h2>The rules you will meet</h2>
      <h3>Profit target</h3>
      <p>The gain you need before the evaluation ends, often between 5% and 10% of the starting balance.</p>
      <h3>Maximum drawdown</h3>
      <p>How far the balance may fall below its starting point over the whole challenge. Touch it and the challenge is over.</p>
      <h3>Daily drawdown</h3>
      <p>The largest loss allowed within a single day. It is the rule that ends most attempts, because one emotional day is enough.</p>
      <h3>Minimum and maximum trading days</h3>
      <p>A minimum stops you from passing on one lucky trade. A maximum forces you to reach the target within a set time.</p>
      <h2>Why a bot helps</h2>
      <p>Most challenges are lost to discipline, not to analysis. A bot follows its rules every time: same position size, same stop, no revenge trade after a loss. Building one also forces you to write your strategy down, which shows its weak spots before the market does.</p>
      <h2>Practise the same rules for free</h2>
      <p>Bitcoin Era runs your bot on live crypto prices with a <strong>virtual $10,000</strong> and evaluates it with prop-style rules:</p>
      <table>
        <thead><tr><th>Level</th><th>Target</th><th>Min. days</th><th>Max. days</th><th>Max. drawdown</th><th>Daily drawdown</th></tr></thead>
        <tbody>
          <tr><td>Level 1</td><td>+10%</td><td>5</td><td>10</td><td>-10%</td><td>-5%</td></tr>
          <tr><td>Level 2</td><td>+5%</td><td>5</td><td>No limit</td><td>-10%</td><td>-5%</td></tr>
          <tr><td>Level 3</td><td>+5%</td><td>None</td><td>No limit</td><td>-10%</td><td>-5%</td></tr>
        </tbody>
      </table>
      <p>No evaluation fee and no real money: if your bot breaks a limit, you review what happened and start again.</p>
      <h2>Frequently asked questions</h2>
""" + "\n".join(f"      <h3>{q}</h3>\n      <p>{a}</p>" for q, a in GUIDE_FAQ) + "\n" + CTA.format(text="Put your strategy through a prop-style test."),
  jsonld=[
    {"@context":"https://schema.org","@type":"Article","headline":"Crypto prop firm challenges: how they work and how to practise","datePublished":"2026-10-03","dateModified":"2026-10-03","author":{"@type":"Organization","name":"Bitcoin Era"},"publisher":{"@type":"Organization","name":"Bitcoin Era"},"mainEntityOfPage":"https://bitcoinera.com/crypto-prop-firm-challenge/"},
    {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q, a in GUIDE_FAQ]},
  ]))


# ---------------------------------------------------------------- SEO guides
# One dict per guide; guide() adds the FAQ block, the CTA, the related-guides
# list and the Article + FAQPage JSON-LD.
LEVELS_TABLE = """      <table>
        <thead><tr><th>Level</th><th>Target</th><th>Min. days</th><th>Max. days</th><th>Max. drawdown</th><th>Daily drawdown</th></tr></thead>
        <tbody>
          <tr><td>Level 1</td><td>+10%</td><td>5</td><td>10</td><td>-10%</td><td>-5%</td></tr>
          <tr><td>Level 2</td><td>+5%</td><td>5</td><td>No limit</td><td>-10%</td><td>-5%</td></tr>
          <tr><td>Level 3</td><td>+5%</td><td>None</td><td>No limit</td><td>-10%</td><td>-5%</td></tr>
        </tbody>
      </table>"""

def guide(slug, h1, title, desc, body, faq, cta, short):
    PAGES.append(dict(
      slug=slug, kicker="Guide", ogtype="article", h1=h1, title=title, desc=desc, short=short,
      body=body + "\n      <h2>Frequently asked questions</h2>\n"
        + "\n".join(f"      <h3>{q}</h3>\n      <p>{a}</p>" for q, a in faq)
        + "\n" + CTA.format(text=cta) + "\n{related}",
      jsonld=[
        {"@context":"https://schema.org","@type":"Article","headline":h1,"datePublished":"2026-10-03","dateModified":"2026-10-03","author":{"@type":"Organization","name":"Bitcoin Era"},"publisher":{"@type":"Organization","name":"Bitcoin Era"},"mainEntityOfPage":f"{SITE}/{slug}/"},
        {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q, a in faq]},
      ]))

# Existing guides get a short label for the related-guides list.
for p in PAGES:
    if p["slug"] == "crypto-prop-firm-challenge": p["short"] = "Crypto prop firm challenges explained"
    if p["kicker"] in ("Review", "Guide"): p["body"] += "\n{related}"

# ---- free crypto prop firm challenge (US 210, KD 5)
guide("free-crypto-prop-firm-challenge",
  "Free crypto prop firm challenge: practise the rules without paying a fee",
  "Free Crypto Prop Firm Challenge: Practise With Virtual Money",
  "Most crypto prop firm challenges cost $50 to $600 per attempt. Here is how to practise the same targets and drawdown limits for free, with a trading bot and a virtual $10,000.",
  """      <p>Crypto prop firms sell evaluations. You pay an entry fee, trade a demo account under strict rules, and if you pass, the firm lets you trade a larger account and keeps part of the profits. The fee is lost every time you break a rule, and most attempts end that way. A free practice challenge lets you find out where your strategy breaks before you pay anyone.</p>
      <div class="callout"><p><strong>What this page offers.</strong> Bitcoin Era is a free, educational challenge on live crypto prices with a virtual balance. It does not fund accounts or pay out profits. It shows you whether your approach survives prop-style rules, at no cost.</p></div>
      <h2>Why prop firm challenges cost money</h2>
      <p>The entry fee is the business model. A firm charges each candidate for the evaluation, and only a small share of candidates ever reach a funded account. The fee usually scales with the account size: a small account costs a few dozen dollars, a large one several hundred. Some firms refund the fee with the first profit split, others do not. Read the terms before paying, and check what happens if the firm changes its rules or closes.</p>
      <h2>What a free challenge should test</h2>
      <p>A useful practice run copies the constraints that end real evaluations. The profit target matters less than people think. Traders rarely fail because they cannot make 10%; they fail because one bad session breaks the loss limit. A good free challenge should therefore apply:</p>
      <ul>
        <li><strong>A daily loss limit</strong>, the rule that ends most attempts.</li>
        <li><strong>A maximum drawdown</strong> over the whole evaluation.</li>
        <li><strong>A minimum number of trading days</strong>, so one lucky trade cannot pass the test.</li>
        <li><strong>Live market prices</strong>, because replaying a calm historical week teaches little about a volatile one.</li>
      </ul>
      <h2>The Bitcoin Era rules</h2>
      <p>Every bot starts with a virtual $10,000 and trades on live prices. It has to clear three levels in a row:</p>
""" + LEVELS_TABLE + """
      <p>Breaking the daily drawdown (-5% within 24 hours) or the maximum drawdown (-10%) ends the run on the spot, exactly as it would in a paid evaluation. You can then read what happened, adjust the strategy and start a new bot.</p>
      <h2>How to use a free challenge before a paid one</h2>
      <ol>
        <li><strong>Write your rules down.</strong> Entry signal, exit signal, position size, maximum loss per trade. If you cannot write it, a bot cannot run it.</li>
        <li><strong>Size positions from the loss limit backwards.</strong> With a -5% daily limit, risking 2% per trade leaves room for two losing trades in a day. Risking 5% leaves room for one.</li>
        <li><strong>Run Level 1 at least twice.</strong> One pass can be luck. Two passes in different market conditions say more.</li>
        <li><strong>Look at the worst day, not the final balance.</strong> The worst day tells you how close you came to failing.</li>
        <li><strong>Only then compare paid firms.</strong> Check the fee, the rules, the payout terms, the firm&rsquo;s track record and where it is registered.</li>
      </ol>
      <h2>Free challenge vs paid evaluation</h2>
      <table>
        <thead><tr><th></th><th>Bitcoin Era (free)</th><th>Typical paid crypto evaluation</th></tr></thead>
        <tbody>
          <tr><td>Entry fee</td><td>None</td><td>Usually tens to hundreds of dollars</td></tr>
          <tr><td>Money at stake</td><td>None, virtual $10,000</td><td>The fee</td></tr>
          <tr><td>Prices</td><td>Live market</td><td>Live market</td></tr>
          <tr><td>Loss limits</td><td>-5% daily, -10% max</td><td>Similar ranges</td></tr>
          <tr><td>Reward</td><td>A clear verdict on your strategy</td><td>Access to a funded account, if you pass</td></tr>
        </tbody>
      </table>
      <p>For a full breakdown of each rule, read our guide to <a href="/crypto-prop-firm-challenge/">how crypto prop firm challenges work</a>.</p>""",
  [
    ("Is there a free crypto prop firm challenge?", "Some firms run occasional free trials or competitions, but standard evaluations charge a fee. Bitcoin Era is a free practice challenge with prop-style rules and a virtual $10,000. It does not fund accounts."),
    ("Does Bitcoin Era give me a funded account?", "No. Bitcoin Era is an educational simulator. All balances are virtual and no profits are paid out. It is built to test a strategy before you consider a paid evaluation."),
    ("What rule fails most prop firm challenges?", "The daily loss limit. One oversized position or one bad session breaks it, even when the strategy is profitable over a full week."),
    ("Do I need a card to start?", "No. Signing up asks for no card, no deposit and no payment of any kind."),
  ],
  "Find out where your strategy breaks, for free.",
  "Free crypto prop firm challenge")

# ---- crypto trading simulator (US 260, KD 13; paper trading crypto US 390, KD 8)
guide("crypto-trading-simulator",
  "Crypto trading simulator: paper trade on live prices with a virtual $10,000",
  "Crypto Trading Simulator: Free Paper Trading on Live Prices",
  "A free crypto trading simulator for paper trading: live market prices, a virtual $10,000, and prop-style drawdown rules that tell you whether your strategy holds up.",
  """      <p>A crypto trading simulator lets you buy and sell on real market prices with money that does not exist. You see what your strategy would have done, without paying for the lesson. Traders call it paper trading, from the days when people wrote imaginary orders on paper.</p>
      <h2>What a good simulator gives you</h2>
      <ul>
        <li><strong>Live prices.</strong> Your orders fill against the market as it moves today, including the volatile hours.</li>
        <li><strong>A realistic balance.</strong> Practising with $1,000,000 teaches bad sizing habits. A $10,000 balance is closer to what most people would actually risk.</li>
        <li><strong>Rules that stop you.</strong> Without a loss limit, a simulator lets you average down forever. Real accounts do not.</li>
        <li><strong>A record you can read.</strong> Every trade, the worst day, the deepest drawdown.</li>
      </ul>
      <h2>Paper trading vs backtesting</h2>
      <p>A backtest replays a strategy on past data in seconds. It is fast and useful for a first filter, but it is easy to fit a strategy to the past by accident. Paper trading runs the strategy forward, on prices nobody has seen yet. It is slower, and much harder to fool. Use both: backtest to discard bad ideas, paper trade to check the survivors.</p>
      <table>
        <thead><tr><th></th><th>Backtest</th><th>Paper trading (simulator)</th></tr></thead>
        <tbody>
          <tr><td>Data</td><td>Past prices</td><td>Live prices</td></tr>
          <tr><td>Speed</td><td>Seconds</td><td>Days or weeks</td></tr>
          <tr><td>Risk of fitting the past</td><td>High</td><td>Low</td></tr>
          <tr><td>Best for</td><td>Discarding ideas</td><td>Confirming a strategy</td></tr>
        </tbody>
      </table>
      <h2>How the Bitcoin Era simulator works</h2>
      <p>You build a bot from your trading rules and it starts with a virtual $10,000. It trades on live crypto prices and has to clear three levels, each with a profit target and the same two loss limits: -10% maximum drawdown and -5% daily drawdown.</p>
""" + LEVELS_TABLE + """
      <p>If the bot breaks a limit, the run stops and you can see where the strategy cracked. That is the point of the exercise: finding the weak spot while it costs nothing.</p>
      <h2>Mistakes to avoid when paper trading</h2>
      <ol>
        <li><strong>Trading bigger than you ever would with real money.</strong> The result is meaningless if the size is.</li>
        <li><strong>Resetting after every loss.</strong> A strategy has to survive its bad weeks, not only its good ones.</li>
        <li><strong>Judging on one week.</strong> Crypto can trend for days. Run at least two levels before drawing conclusions.</li>
        <li><strong>Ignoring fees and slippage.</strong> On real exchanges each trade costs a little. Strategies that trade very often feel it most.</li>
      </ol>
      <h2>Is it a game?</h2>
      <p>The levels make it feel like one, and that helps you come back. The rules, though, are the ones serious traders work under. Clearing Level 3 means your bot made money on live prices without a single day worse than -5%.</p>""",
  [
    ("Is there a free crypto trading simulator?", "Yes. Bitcoin Era is free and needs no card or deposit. Your bot trades on live crypto prices with a virtual $10,000."),
    ("What is paper trading in crypto?", "Paper trading means placing simulated trades on real market prices with virtual money, to test a strategy without risking your own funds."),
    ("Are simulator results the same as real trading?", "No. Real trading adds fees, slippage and emotion. A simulator shows whether a strategy has a chance; it cannot promise the same result with real money."),
    ("Can I use a simulator to practise for a prop firm?", "Yes. The Bitcoin Era levels use a profit target, a -10% maximum drawdown and a -5% daily drawdown, the same kind of rules prop firm evaluations apply."),
  ],
  "Try your strategy on live prices, with virtual money.",
  "Crypto trading simulator")

# ---- claude trading bot (US 390, UK 110, KD 0). SERP = build tutorials.
guide("claude-trading-bot",
  "Claude trading bot: how to build one and test it safely",
  "Claude Trading Bot: Build One and Test It on Virtual Money",
  "How people use Claude to write a crypto trading bot, what an AI model can and cannot do for your strategy, and how to test the result on live prices with virtual money.",
  """      <p>Claude is a general AI assistant made by Anthropic. It does not trade by itself, and Anthropic does not sell a trading bot. What people call a &ldquo;Claude trading bot&rdquo; is a bot whose code or rules were written with Claude&rsquo;s help, or a script that asks Claude for an opinion before placing an order. This guide covers both, and how to test the result before any money is involved.</p>
      <div class="callout"><p><strong>Independent guide.</strong> Bitcoin Era is not affiliated with Anthropic. Claude is a trademark of Anthropic.</p></div>
      <h2>Three ways people use Claude for trading</h2>
      <h3>1. Writing the strategy code</h3>
      <p>You describe your rules in plain English (&ldquo;buy when the 20-period average crosses above the 50, sell on the opposite cross, never risk more than 1% per trade&rdquo;) and ask Claude to turn them into Python or Pine Script. This is where AI saves the most time. It still makes mistakes, so read the code and test it.</p>
      <h3>2. Reviewing an existing strategy</h3>
      <p>Paste your rules and ask what could break them: a gap overnight, a sudden spike, a quiet sideways week. A model is good at listing scenarios you did not think about. It cannot tell you which one will happen.</p>
      <h3>3. Asking the model at trade time</h3>
      <p>Some builders call the Claude API from their bot and let it read news or chart data before each trade. This is the riskiest use. Answers vary from one call to the next, they cost money per request, and a confident answer is not a correct one.</p>
      <h2>What an AI model cannot do</h2>
      <ul>
        <li><strong>Predict prices.</strong> No model knows tomorrow&rsquo;s price. Anyone selling an AI that does is selling something else.</li>
        <li><strong>Prove a strategy works.</strong> Only results on prices the strategy has never seen can do that.</li>
        <li><strong>Manage your risk for you.</strong> Position size and loss limits are your decision. Write them into the bot.</li>
      </ul>
      <h2>A simple workflow</h2>
      <ol>
        <li>Write your strategy in plain sentences, with entry, exit, size and maximum loss.</li>
        <li>Ask Claude to turn it into code, then ask it to list edge cases the code does not handle.</li>
        <li>Backtest quickly on past data to discard obvious failures.</li>
        <li>Run the surviving version forward on live prices with virtual money, under hard loss limits.</li>
        <li>Only consider real money after the bot has survived several weeks without breaking a limit.</li>
      </ol>
      <h2>Test it on Bitcoin Era</h2>
      <p>Step 4 is what Bitcoin Era is for. Your bot starts with a virtual $10,000 on live crypto prices and has to clear three levels with a -10% maximum drawdown and a -5% daily drawdown. Whether the rules came from you, from Claude or from ChatGPT, the market judges them the same way.</p>
      <h2>Prompts that help</h2>
      <ul>
        <li>&ldquo;Turn these rules into Python. Add a hard stop that closes every position if the account is down 5% today.&rdquo;</li>
        <li>&ldquo;List ten market situations where this strategy loses money.&rdquo;</li>
        <li>&ldquo;Explain this code line by line so I can check it does what I described.&rdquo;</li>
      </ul>""",
  [
    ("Is there an official Claude trading bot?", "No. Anthropic makes Claude, a general AI assistant, and does not sell a trading bot. Products using the name are built by third parties."),
    ("Can Claude predict crypto prices?", "No. Claude can write code, explain indicators and list risks, but no AI model knows future prices."),
    ("Is a bot written with Claude better than one written with ChatGPT?", "The model matters less than the rules and the testing. Both can write working code and both make mistakes. Test the bot on live prices with virtual money before trusting it."),
    ("Where can I test an AI trading bot for free?", "On Bitcoin Era your bot trades live crypto prices with a virtual $10,000 under prop-style drawdown rules, with no card or deposit."),
  ],
  "Wrote a bot with AI? See if it survives live prices.",
  "Claude trading bot guide")

# ---- crypto trading bot competition (US 320, KD 31)
guide("crypto-trading-bot-competition",
  "Crypto trading bot competitions: how they work and how to prepare",
  "Crypto Trading Bot Competition: How They Work and How to Prepare",
  "What crypto trading bot competitions measure, the rules that decide them, and how to prepare your bot with a free three-level challenge on live prices.",
  """      <p>A crypto trading bot competition puts automated strategies side by side on the same market, over the same period, and ranks them. Exchanges, data platforms and communities run them, sometimes with prizes. Whatever the organiser, the useful question is the same: does your bot make money without blowing up along the way?</p>
      <h2>What competitions usually measure</h2>
      <ul>
        <li><strong>Return.</strong> How much the balance grew over the period.</li>
        <li><strong>Drawdown.</strong> How far the balance fell at its worst. Many competitions disqualify a bot past a set limit.</li>
        <li><strong>Risk-adjusted return.</strong> Return divided by volatility or drawdown, so a reckless bot cannot win on luck alone.</li>
        <li><strong>Consistency.</strong> A minimum number of trading days or trades, so one big bet cannot decide the ranking.</li>
      </ul>
      <h2>Why most bots lose a competition early</h2>
      <p>Competitions reward the bots that are still running at the end. A strategy that doubles in three days and then breaks the loss limit on day four ranks below a dull one that made 8% with no bad day. The common causes of early exits are oversized positions, no stop on a single trade, and strategies tuned to one kind of market that meet another.</p>
      <h2>How to prepare a bot</h2>
      <ol>
        <li><strong>Read the scoring rules first.</strong> A return-only ranking and a risk-adjusted one call for different bots.</li>
        <li><strong>Hard-code the loss limits.</strong> If the competition stops you at -10%, make your bot stop itself at -8%.</li>
        <li><strong>Run it forward on live prices.</strong> A backtest is not enough; you want to see the bot handle markets it was not tuned on.</li>
        <li><strong>Keep the logs.</strong> When a run fails, the log of the worst day tells you what to change.</li>
      </ol>
      <h2>A free three-level challenge to train on</h2>
      <p>Bitcoin Era is a challenge against fixed rules, open all year. Your bot starts with a virtual $10,000 on live crypto prices and has to clear three levels in a row:</p>
""" + LEVELS_TABLE + """
      <p>The same two limits apply at every level: -10% maximum drawdown and -5% daily drawdown. Breaking either ends the run, the way a strict competition would. It costs nothing, and you can start a new bot as soon as you have fixed what broke.</p>
      <h2>Competition vs challenge</h2>
      <table>
        <thead><tr><th></th><th>Bot competition</th><th>Bitcoin Era challenge</th></tr></thead>
        <tbody>
          <tr><td>When</td><td>Fixed dates</td><td>Any time</td></tr>
          <tr><td>You compete against</td><td>Other bots</td><td>Fixed, public rules</td></tr>
          <tr><td>Money at stake</td><td>Varies by organiser</td><td>None, virtual $10,000</td></tr>
          <tr><td>Best for</td><td>Ranking your bot</td><td>Getting it ready</td></tr>
        </tbody>
      </table>""",
  [
    ("What is a crypto trading bot competition?", "An event where automated trading strategies run on the same market over the same period and are ranked, usually by return, drawdown or a risk-adjusted score."),
    ("How do I win a trading bot competition?", "Read the scoring rules, keep drawdowns well inside the limits and test the bot forward on live prices beforehand. Bots that stay in the game usually beat bots that swing big."),
    ("Is Bitcoin Era a competition?", "It is a challenge against fixed rules, open all year: three levels with profit targets and drawdown limits, on live prices with virtual money."),
    ("Do I need real money to enter?", "Not on Bitcoin Era. Every balance is virtual and sign-up asks for no card or deposit."),
  ],
  "Get your bot competition-ready on live prices.",
  "Crypto trading bot competitions")

# ---- free crypto trading bot (free ai trading bot US 320, KD 8)
guide("free-crypto-trading-bot",
  "Free crypto trading bot: build your own and test it without risk",
  "Free Crypto Trading Bot: Build Your Own and Test It Risk-Free",
  "Where to find a free crypto trading bot, which free offers to avoid, and how to build your own bot and test it on live prices with a virtual $10,000.",
  """      <p>&ldquo;Free trading bot&rdquo; covers very different things: open-source software you run yourself, free tiers of paid platforms, and ads promising daily profits for free. The first two can be useful.</p>
      <h2>Free bots that are worth a look</h2>
      <ul>
        <li><strong>Open-source bots.</strong> Free code you install and configure. Powerful, but you handle the setup, the exchange keys and the security.</li>
        <li><strong>Free tiers of bot platforms.</strong> Usually limited in the number of bots or exchanges, enough to learn how grid or DCA bots behave.</li>
        <li><strong>Exchange-built bots.</strong> Some exchanges offer simple grid and DCA bots inside their app at no extra charge beyond trading fees.</li>
        <li><strong>Simulators.</strong> Free places to run a bot on live prices with virtual money, like Bitcoin Era.</li>
      </ul>
      <h2>Free offers to avoid</h2>
      <h2>Build your own instead</h2>
      <p>A bot is a set of rules a computer follows without hesitation. You decide the rules; the bot applies them. Writing them yourself means you know exactly why each trade happens.</p>
      <ol>
        <li><strong>Pick one market.</strong> BTC/USD is a sensible start: liquid and closely watched.</li>
        <li><strong>Choose an entry and an exit.</strong> For example, a moving-average cross, or buying a dip of a set size.</li>
        <li><strong>Set the size.</strong> A fixed share of the balance per trade, small enough to survive a losing streak.</li>
        <li><strong>Set the brakes.</strong> A stop per trade and a daily loss limit that stops the bot.</li>
      </ol>
      <h2>Then test it for free</h2>
      <p>On Bitcoin Era your bot starts with a virtual $10,000 and trades live crypto prices. It has to clear three levels with profit targets, a -10% maximum drawdown and a -5% daily drawdown. No card and no deposit at any point.</p>
""" + LEVELS_TABLE + """
      <p>A free bot is only useful if you know how it behaves on a bad day. Finding that out with virtual money is the cheapest lesson in trading.</p>
      <h2>Free bot options compared</h2>
      <table>
        <thead><tr><th></th><th>Cost</th><th>Real money involved</th><th>Effort</th></tr></thead>
        <tbody>
          <tr><td>Open-source bot</td><td>Free, plus hosting</td><td>Yes, on your exchange</td><td>High</td></tr>
          <tr><td>Platform free tier</td><td>Free, limited</td><td>Yes, on your exchange</td><td>Medium</td></tr>
          <tr><td>Bitcoin Era challenge</td><td>Free</td><td>No, virtual $10,000</td><td>Low</td></tr>
        </tbody>
      </table>""",
  [
    ("Is there a free crypto trading bot that works?", "Free open-source bots and free tiers exist and do what their rules say. Whether they make money depends on the strategy, which is why testing on virtual money first matters."),
    ("Can I test a trading bot without money?", "Yes. On Bitcoin Era your bot runs on live crypto prices with a virtual $10,000, with no card or deposit."),
    ("Do I need to code to build a bot?", "Writing your rules clearly matters more than code. AI assistants can turn plain-English rules into code, and some platforms let you set rules without coding."),
  ],
  "Build a bot and test it for free.",
  "Free crypto trading bot")

GUIDES = [p for p in PAGES if p["kicker"] in ("Review", "Guide")]
FOOTER_NAV = ('<nav aria-label="Footer">' + "".join(f'<a href="/{g["slug"]}/">{g["short"]}</a>' for g in GUIDES)
  + '<a href="/contact/">Contact</a><a href="/terms/">Terms</a><a href="/privacy-policy/">Privacy</a><a href="/legal-notice/">Legal notice</a>'
  + '<a href="/privacy-policy/#cookies" data-cookie-settings>Cookie settings</a></nav>')

def related(slug):
    items = "".join(f'<li><a href="/{g["slug"]}/">{g["short"]}</a></li>' for g in GUIDES if g["slug"] != slug)
    return f"      <h2>Related guides</h2>\n      <ul>{items}</ul>"

for p in PAGES:
    jsonld = "".join('<script type="application/ld+json">\n' + json.dumps(j, ensure_ascii=False) + "\n</script>\n" for j in p.get("jsonld", []))
    html = HEAD.format(
        title=p["title"], desc=p["desc"], slug=p["slug"], ogtype=p.get("ogtype", "website"),
        robots="", jsonld=jsonld, kicker=p["kicker"], h1=p["h1"], updated="" if p["slug"]=="contact" else f'    <p class="updated">Last updated: {UPDATED}</p>\n', body=p["body"].replace("{related}", related(p["slug"])), ga=GA_ID, footer_nav=FOOTER_NAV,
        cur_contact=' aria-current="page"' if p["slug"] == "contact" else "",
        scripts=p.get("scripts", ""))
    os.makedirs(os.path.join(ROOT, p["slug"]), exist_ok=True)
    open(os.path.join(ROOT, p["slug"], "index.html"), "w").write(html)

urls = [("", "1.0")] + [(p["slug"] + "/", "0.8" if p in GUIDES else "0.3") for p in PAGES]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sm += "".join(f"  <url><loc>{SITE}/{u}</loc><lastmod>2026-10-03</lastmod><priority>{pr}</priority></url>\n" for u, pr in urls)
sm += "</urlset>\n"
open(os.path.join(ROOT, "sitemap.xml"), "w").write(sm)
open(os.path.join(ROOT, "robots.txt"), "w").write("User-agent: *\nAllow: /\nDisallow: /app/\n\nSitemap: https://bitcoinera.com/sitemap.xml\n")
# Old URLs from the former site that still receive links (see 0_inbox/search backlinks report):
# GitHub Pages cannot send 301s, an instant meta refresh is read by Google as a permanent redirect.
STUB = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>Moved</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="https://bitcoinera.com{to}">
<meta http-equiv="refresh" content="0; url={to}">
</head><body><p>This page has moved: <a href="{to}">{to}</a></p></body></html>
"""
for old, to in [("es/index.html", "/"), ("it/index.html", "/"), ("de/index.html", "/"), ("policy.html", "/privacy-policy/")]:
    os.makedirs(os.path.dirname(os.path.join(ROOT, old)) or ROOT, exist_ok=True)
    open(os.path.join(ROOT, old), "w").write(STUB.format(to=to))
print("built", [p["slug"] for p in PAGES])
