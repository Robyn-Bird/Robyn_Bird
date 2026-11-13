#!/usr/bin/env python3
"""Stamps robynbird.com pages from one shared header/footer. Run: python3 build.py <site dir>"""
import sys, pathlib, re

REPO = pathlib.Path(sys.argv[1])
SITE = "https://www.robynbird.com"
SRC = (REPO / "index.html").read_text()
ICONS = re.search(r'(<div class="icons".*?</div>)', SRC, re.S).group(1)
ROBIN = re.search(r'(<svg class="birdy perch-bird".*?</svg>)', SRC, re.S).group(1)
WAFFLE = re.search(r'(<svg viewBox="0 0 24 24" aria-hidden="true"><circle.*?</svg>)', SRC, re.S).group(1)

# The photo used across the site. Swap these when the new candid photo lands.
PHOTO_WEBP = "assets/robyn-640.webp 640w, assets/robyn-960.webp 960w"
PHOTO_JPG = "assets/robyn.jpg"

MENU = [("", "Home"), ("about/", "About Robyn"), ("#community", "In the community"),
        ("campaign/", "The 2026 campaign"), ("#stay", "Get in touch")]


def page(path, title, desc, body, current, extra_head=""):
    depth = path.count("/")
    up = "../" * depth
    nav = []
    for href, label in MENU:
        h = (up + href) if (depth or not href.startswith("#")) else href
        cur = ' aria-current="page"' if href == current else ""
        nav.append(f'        <a href="{h or "./"}"{cur}>{label}</a>')
    url = f"{SITE}/{path}"
    body = body.replace('src="assets/', f'src="{up}assets/').replace('srcset="assets/', f'srcset="{up}assets/') \
               .replace(', assets/', f', {up}assets/').replace('href="about/', f'href="{up}about/') \
               .replace('href="campaign/', f'href="{up}campaign/')
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<!--
  robynbird.com · Robyn Bird, Port Richmond, Philadelphia
  © 2026 Friends of Robyn Bird. All rights reserved. Designed and built by Shirah M. Brown.
-->
<script src="/assets/site-guard.js"></script>
<meta name="author" content="Friends of Robyn Bird">
<meta name="designer" content="Shirah M. Brown">
<script src="/assets/ga-gate.js"></script>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="profile">
<meta property="og:site_name" content="Robyn Bird">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/share-robyn.jpg?v=12">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#041581">
<link rel="icon" type="image/png" sizes="32x32" href="{up}assets/favicon-32.png?v=2">
<link rel="apple-touch-icon" href="{up}assets/apple-touch-icon.png?v=2">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&family=Roboto+Slab:wght@500;700&family=Public+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap">
<link rel="stylesheet" href="{up}assets/site.css?v=rb3">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Person","name":"Robyn Bird","url":"{SITE}/","image":"{SITE}/{PHOTO_JPG}","jobTitle":"Public Relations and Government Affairs","worksFor":{{"@type":"Organization","name":"IAFF Local 22, Philadelphia Firefighters and Paramedics Union"}},"homeLocation":{{"@type":"Place","name":"Port Richmond, Philadelphia, PA"}},"sameAs":["https://www.facebook.com/voterobynbird/","https://www.instagram.com/VoteRobynBird","https://www.tiktok.com/@voterobynbird","https://x.com/voterobynbird","https://ballotpedia.org/Robyn_Bird","https://www.voterobynbird.com/"]}}
</script>
{extra_head}</head>
<body class="pe rb rb2">
<a class="skip" href="#main">Skip to content</a>

<header class="top rb-top">
  <div class="wrap">
    <a class="rb-brand" href="{up or './'}" aria-label="Robyn Bird, home"><img src="{up}assets/logo-robyn-navy.png" alt="Robyn" width="144" height="62"></a>
    <div class="top-actions">
      <a class="btn btn-white" href="{up}#stay">Get in touch</a>
      <button class="waffle" id="menuBtn" type="button" aria-label="Menu" aria-expanded="false" aria-controls="siteMenu">
        {WAFFLE}
      </button>
    </div>
    <nav class="menu" id="siteMenu" aria-label="Site" hidden>
{chr(10).join(nav)}
    </nav>
  </div>
</header>

<main id="main">
{body}
{STAY.replace("{ROBIN}", ROBIN)}
</main>

<footer class="pe-foot rb-foot">
  <div class="wrap">
    {ICONS}
    <div class="foot-legal">
      <p class="paidfor">Paid for by Friends of Robyn Bird</p>
      <p class="rb-copy">© 2026 Friends of Robyn Bird. All rights reserved.</p>
    </div>
  </div>
</footer>

<script>
(function () {{
  const btn = document.getElementById("menuBtn"), menu = document.getElementById("siteMenu");
  const set = (open) => {{ menu.hidden = !open; btn.setAttribute("aria-expanded", String(open)); }};
  btn.addEventListener("click", (e) => {{ e.stopPropagation(); set(menu.hidden); }});
  menu.addEventListener("click", (e) => {{ if (e.target.closest("a")) set(false); }});
  document.addEventListener("click", (e) => {{ if (!menu.hidden && !menu.contains(e.target)) set(false); }});
  document.addEventListener("keydown", (e) => {{ if (e.key === "Escape" && !menu.hidden) {{ set(false); btn.focus(); }} }});
}})();
</script>
{FORM_JS}
</body>
</html>
'''
    out = REPO / path / "index.html" if path else REPO / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)


STAY = '''  <section class="vol pe-stay rb-stay" id="stay">
    <div class="wrap">
      <div class="sec-head">
        <p class="eyebrow">Get in touch</p>
        <h2>Let's keep talk<span class="perch">i{ROBIN}</span>ng</h2>
        <p>Questions, invitations or a problem on your block. Robyn reads every one.</p>
      </div>
      <div class="pe-form">
        <form id="joinForm" novalidate>
          <div class="field full"><label for="name">Name</label><input id="name" name="name" type="text" autocomplete="name" required></div>
          <div class="field"><label for="phone">Phone number</label><input id="phone" name="phone" type="tel" autocomplete="tel" required></div>
          <div class="field"><label for="email">Email <span class="opt-note">(optional)</span></label><input id="email" name="email" type="email" autocomplete="email"></div>
          <div class="field full rb-note"><label for="note">What's on your mind? <span class="opt-note">(optional)</span></label><textarea id="note" name="note" rows="4"></textarea></div>
          <label class="rb-check"><input id="invite" name="invite" type="checkbox"> <span>I'd like to invite Robyn to speak or attend an event.</span></label>
          <label class="rb-check"><input id="women" name="women" type="checkbox"> <span>I want to help get more women involved in our neighborhoods and local government.</span></label>
          <div class="hp" aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden"><label for="website">Website</label><input id="website" name="website" type="text" tabindex="-1" autocomplete="off"></div>
          <div class="form-foot">
            <button class="btn btn-navy" type="submit" id="joinBtn">Send to Robyn</button>
            <small>Robyn uses this only to get back to you. We never share your information.</small>
          </div>
          <p class="err" id="formErr" hidden></p>
          <div class="thanks" id="thanks" hidden>
            <h2>Thank you!</h2>
            <p>Robyn will be in touch. Talk soon, neighbor.</p>
          </div>
        </form>
      </div>
    </div>
  </section>'''

FORM_JS = '''<script>
/* Sends messages into Robyn's "Get in Touch" Google Form (same responses sheet as the campaign site). */
const GOOGLE_FORM = {
  action: "https://docs.google.com/forms/d/e/1FAIpQLScv42GFhPPAWPjRcF5a376TyfZ7b13SApjjgMnx9__YIwsHYw/formResponse",
  name: "entry.574465594", phone: "entry.1545288065", notes: "entry.121815469", email: "entry.1614426159"
};
(function () {
  const $ = (id) => document.getElementById(id);
  const form = $("joinForm"); if (!form) return;
  const pageStart = Date.now();
  document.querySelectorAll("a[data-women]").forEach((a) => a.addEventListener("click", () => { $("women").checked = true; }));
  document.querySelectorAll("a[data-invite]").forEach((a) => a.addEventListener("click", () => { $("invite").checked = true; }));
  const showThanks = () => {
    [...form.querySelectorAll(".field, .form-foot, .rb-check")].forEach((el) => (el.hidden = true));
    $("thanks").hidden = false;
  };
  form.addEventListener("submit", async (ev) => {
    ev.preventDefault();
    if ($("website").value || Date.now() - pageStart < 3000) { showThanks(); return; }
    const err = $("formErr"); err.hidden = true;
    const name = $("name").value.trim(), phone = $("phone").value.trim(), email = $("email").value.trim(), note = $("note").value.trim();
    const women = $("women").checked, invite = $("invite").checked;
    if (!name || !phone) { err.textContent = "Add your name and phone number so Robyn can reach you."; err.hidden = false; return; }
    if (email && !/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(email)) { err.textContent = "That email doesn't look right. Fix it or leave it blank."; err.hidden = false; return; }
    const btn = $("joinBtn"); btn.disabled = true; btn.textContent = "Sending…";
    try {
      const tags = ["[robynbird.com" + location.pathname + "]"];
      if (invite) tags.push("Invite to speak/event: yes");
      if (women) tags.push("Women in local government: yes");
      const body = new URLSearchParams();
      body.append(GOOGLE_FORM.name, name);
      body.append(GOOGLE_FORM.phone, phone);
      body.append(GOOGLE_FORM.notes, tags.join(" ") + (note ? " | " + note : ""));
      if (email) body.append(GOOGLE_FORM.email, email);
      await fetch(GOOGLE_FORM.action, { method: "POST", mode: "no-cors", body });
      if (window.gtag) gtag("event", "get_in_touch", { invite: invite ? "yes" : "no", women_interest: women ? "yes" : "no" });
      showThanks();
      form.scrollIntoView({ behavior: "smooth", block: "start" });
    } catch (e) {
      err.textContent = "That didn't go through. Check your connection and try again.";
      err.hidden = false; btn.disabled = false; btn.textContent = "Send to Robyn";
    }
  });
})();
</script>'''

HOODS = ["Port Richmond", "Bridesburg", "Fishtown", "Harrowgate", "Frankford", "Tacony", "Wissinoming", "Northwood"]
PHOTO = f'<picture><source type="image/webp" srcset="{PHOTO_WEBP}" sizes="(max-width: 760px) 44vw, 440px"><img src="{PHOTO_JPG}" alt="Robyn Bird in Port Richmond, Philadelphia" width="960" height="960" fetchpriority="high"></picture>'

# ---------------- Home ----------------
home = f'''  <section class="hero rb-hero">
    <div class="wrap">
      <div class="hero-copy">
        <h1><span class="h1-name">Port Richmond, Philadelphia</span>Robyn <em>Bird</em></h1>
        <p class="lede">Committeeperson, neighbor and voice for Philadelphia's firefighters and paramedics. Four generations deep in the River Wards.</p>
        <div class="rb-hero-btns">
          <a class="btn btn-white" href="#stay">Get in touch</a>
          <a class="btn btn-ghost" href="about/">My story</a>
        </div>
      </div>
      <figure class="photo">{PHOTO}</figure>
    </div>
  </section>

  <section class="block rb-who">
    <div class="wrap">
      <div class="sec-head">
        <p class="eyebrow">Who I am</p>
        <h2>River Wards to my core</h2>
      </div>
      <div class="rb-who-grid">
        <p class="rb-who-lead">Four generations of my family have lived in the same Port Richmond rowhouse. They came from Poland through Ellis Island and never stopped serving, from World War I and Omaha Beach to Iraq and today's firehouses.</p>
        <div class="rb-who-body">
          <p>I learned early what it means to fight for the people around you. That's what I do at work, and it's what I do on my block.</p>
          <p>I'm not going anywhere. These are the neighborhoods that raised me, and I'm still showing up for them.</p>
          <p><a class="rb-link" href="about/">Read my story</a></p>
        </div>
      </div>
    </div>
  </section>

  <section class="block rb-do" id="community">
    <div class="wrap">
      <div class="sec-head">
        <p class="eyebrow">What I do</p>
        <h2>Work, block and community</h2>
      </div>
      <div class="rb-pillars">
        <article class="rb-pillar">
          <p class="rb-tag">Robyn &middot; In the community</p>
          <h3>Committeeperson</h3>
          <p>I'm the neighbor you call when you need something from the city, a question answered about voting, or someone to show up at the civic meeting. Committeepeople are the first link between our blocks and local government, and I take that seriously.</p>
          <ul>
            <li>Helping neighbors register, find their polling place and vote</li>
            <li>Connecting people with city services and the right office</li>
            <li>Civic associations, block cleanups and community events</li>
          </ul>
        </article>
        <article class="rb-pillar">
          <p class="rb-tag">Robyn &middot; Local 22</p>
          <h3>Public relations &amp; government affairs</h3>
          <p>I work alongside Philadelphia's firefighters and paramedics at IAFF Local&nbsp;22, telling their story and standing up for the people who run toward danger for all of us.</p>
          <ul>
            <li>Public relations and media for the union</li>
            <li>Government affairs on the issues that affect first responders</li>
            <li>Advocating for staffing, resources and respect</li>
          </ul>
        </article>
        <article class="rb-pillar">
          <p class="rb-tag">Robyn &middot; Women at the table</p>
          <h3>More women involved</h3>
          <p>The decisions that shape our blocks get made close to home. I'm working to get more young women off the sidelines and into their neighborhoods and local government.</p>
          <p>If you've been thinking about getting involved, let's do it together.</p>
          <a class="rb-link" href="#stay" data-women="1">Count me in</a>
        </article>
      </div>
    </div>
  </section>

  <section class="block rb-stand">
    <div class="wrap">
      <div class="sec-head">
        <p class="eyebrow">What I stand for</p>
        <h2>Commonsense, close to home</h2>
      </div>
      <div class="rb-cards rb-cards-4">
        <div class="rb-card"><h3>Safe streets</h3><p>Back the firefighters, paramedics and police who protect us. Stand with victims, not criminals. Clean, safe blocks where kids can play outside.</p></div>
        <div class="rb-card"><h3>Good schools</h3><p>Strong neighborhood public schools, and real choice for the parents who know their kids best.</p></div>
        <div class="rb-card"><h3>Staying put</h3><p>Families who built these neighborhoods should be able to afford to stay, with fair property taxes, lower utility bills and good union jobs.</p></div>
        <div class="rb-card"><h3>Neighbors first</h3><p>Local government touches every block, every day. I'll help anyone who asks, no matter their party.</p></div>
      </div>
    </div>
  </section>

  <section class="rb-duo">
    <div class="wrap">
      <div class="rb-panel">
        <p class="eyebrow">Speaking &amp; events</p>
        <h2>Invite me</h2>
        <p>Civic associations, community meetings, panels and podcasts. I'm glad to talk public safety, the River Wards, and why local government matters.</p>
        <a class="btn btn-white" href="#stay" data-invite="1">Invite Robyn</a>
      </div>
      <div class="rb-panel">
        <p class="eyebrow">In 2026</p>
        <h2>I ran for the River Wards</h2>
        <p>I ran for State Representative because I love where I'm from. What I heard at thousands of doors still guides everything I do.</p>
        <a class="btn btn-white" href="campaign/">About the campaign</a>
      </div>
    </div>
  </section>'''
page("", "Robyn Bird | Port Richmond, Philadelphia",
     "Robyn Bird of Port Richmond, Philadelphia: committeeperson, public relations and government affairs for IAFF Local 22, and a River Wards neighbor four generations deep.",
     home, "")

# ---------------- About ----------------
about = '''  <section class="pagehead rb-pagehead">
    <div class="wrap">
      <p class="eyebrow">Meet Robyn Bird</p>
      <h1>About Robyn</h1>
    </div>
  </section>

  <section class="block issue pe-about">
    <div class="wrap prose">
      <figure class="story-photo"><picture><source type="image/webp" srcset="''' + PHOTO_WEBP + '''" sizes="(max-width: 760px) 92vw, 320px"><img src="''' + PHOTO_JPG + '''" alt="Robyn Bird" width="960" height="960" loading="lazy"></picture></figure>

      <h2>River Wards to her core</h2>
      <p>Robyn Bird personifies the rowhouse neighborhoods of the River Wards. Four generations of her family have lived in the same rowhouse. They came from Poland through Ellis Island and never stopped serving, from World War I and Omaha Beach to Iraq and today's firehouses. Service runs deep in Robyn's blood.</p>

      <h2>A fighter for her neighbors</h2>
      <p>Robyn learned early what it means to fight. At just 15, she lost her father to the heroin crisis, and she has been fighting for the people around her ever since. She wants every family in the River Wards to know their voice matters, and that someone will make sure it's heard.</p>

      <h2>At work</h2>
      <p>Robyn works in public relations and government affairs for IAFF Local&nbsp;22, side by side with Philadelphia's firefighters and paramedics, the men and women who run toward danger.</p>

      <h2>On the block</h2>
      <p>As a committeeperson, Robyn is the neighbor people call for help with voting, city services and getting answers. She's working to bring more young women into their neighborhoods and local government.</p>

      <h2>In 2026</h2>
      <p>Robyn ran for State Representative in the River Wards. <a href="campaign/">Read about the campaign</a>.</p>

      <p><a class="btn btn-navy" href="#stay">Get in touch with Robyn</a></p>
    </div>
  </section>'''
page("about/", "About Robyn Bird | Port Richmond, Philadelphia",
     "Robyn Bird is River Wards to her core: four generations in the same Port Richmond rowhouse, committeeperson, and a voice for Philadelphia's firefighters and paramedics.",
     about, "about/")

# ---------------- 2026 campaign ----------------
camp = '''  <section class="pagehead rb-pagehead">
    <div class="wrap">
      <p class="eyebrow">2026 &middot; PA House, 177th District</p>
      <h1>The 2026 campaign</h1>
      <p>In 2026 Robyn ran for State Representative for the River Wards, her first run for office.</p>
    </div>
  </section>

  <section class="block issue rb-pri">
    <div class="wrap prose">
      <figure class="rb-camp-photo"><picture><source type="image/webp" srcset="assets/robyn-bird-640.webp 640w, assets/robyn-bird-960.webp 960w" sizes="(max-width: 760px) 92vw, 320px"><img src="assets/robyn-bird.jpg" alt="Robyn Bird, 2026 candidate for State Representative" width="960" height="960" loading="lazy"></picture></figure>
      <h2>Why I ran</h2>
      <p>I ran because I love where I'm from. At door after door I met neighbors who didn't know who represents them, and families worried about whether they can afford to stay. I wanted them to have someone who actually shows up.</p>

      <h2>What I ran on</h2>
      <ul class="rb-list">
        <li><strong>Safe streets.</strong> Back the firefighters, paramedics and police who protect us, and stand with victims, not criminals.</li>
        <li><strong>Schools that work.</strong> Strong neighborhood public schools, and real school choice for parents.</li>
        <li><strong>Neighborhoods families can afford.</strong> Protect homeowners and seniors from rising property taxes and utility costs, and grow good union jobs.</li>
        <li><strong>Someone who shows up.</strong> Help anyone who asks, no matter their party.</li>
      </ul>

      <h2>Endorsed by</h2>
      <div class="rb-endorse">
        <figure><img src="assets/iaff-local-22.jpg" alt="IAFF Local 22" width="120" height="120" loading="lazy"><figcaption>IAFF Local&nbsp;22, Philadelphia Firefighters &amp; Paramedics</figcaption></figure>
        <figure><img src="assets/ppffa-logo.png" alt="PA Professional Fire Fighters Association" width="120" height="120" loading="lazy"><figcaption>PA Professional Fire Fighters Association</figcaption></figure>
        <figure class="rb-endorse-text"><figcaption>PA Young Republicans</figcaption></figure>
      </div>
      <p class="pull">“I have seen Robyn's dedication firsthand. She cares about the people of this union, takes their concerns to heart and is willing to have the difficult conversations necessary to fight for us.”<cite>Mike Bresnan, President, IAFF Local 22</cite></p>

      <h2>In the press</h2>
      <ul class="rb-list">
        <li>The Kathy Barnette Show</li>
        <li>Northeast Times</li>
        <li>The Philadelphia Citizen</li>
        <li>Billy Penn</li>
      </ul>

      <h2>Thank you</h2>
      <div class="rb-letter">
        <p>I ran because I love where I'm from, and I still do. To every voter, neighbor, friend and donor who opened your door, took a sign, gave what you could or stopped me on the street to talk: thank you. To the firefighters and paramedics of Local&nbsp;22, who had my back from day one: I'll never forget it.</p>
        <p>I heard you at every door. You want safe streets, good schools and someone who actually shows up. That doesn't stop because an election did.</p>
        <p><strong>I'm not going anywhere.</strong></p>
        <p class="sig"><img src="assets/email/signature-robyn.png" alt="&ndash; Robyn" width="189" height="63"></p>
      </div>
      <p><a class="rb-link rb-link-navy" href="https://www.voterobynbird.com/" target="_blank" rel="noopener">The campaign website</a></p>
    </div>
  </section>'''
page("campaign/", "The 2026 campaign | Robyn Bird",
     "Robyn Bird's 2026 run for State Representative in the River Wards: why she ran, what she ran on, endorsements and press.",
     camp, "campaign/")
print("built")
