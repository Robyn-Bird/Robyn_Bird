/* robynbird.com · © 2026 Friends of Robyn Bird. All rights reserved. Designed and built by Shirah M. Brown. RB-177-SMB-2026 */
/*
  Analytics gate for robynbird.com and voterobynbird.com
  - Skips obvious automation (headless browsers, crawlers, webdriver).
  - Counts only visitors whose device is set to a continental US time zone.
  - Loads Google Analytics only after a real interaction (scroll, tap, mouse move, key press)
    AND at least 3 seconds on the page. Visits shorter than that aren't counted.
  - Counts clicks on any Donate link (Anedot) as the donate_click key event (after 3 seconds).
  - Visit any page with ?notrack=1 once on a device to stop counting it; ?notrack=0 undoes it.
*/
(function () {
  var GA_ID = 'G-9QTPPFE9CN';

  try {
    var q = new URLSearchParams(location.search).get('notrack');
    if (q === '1') localStorage.setItem('rb_notrack', '1');
    if (q === '0') localStorage.removeItem('rb_notrack');
    if (localStorage.getItem('rb_notrack') === '1') return;
  } catch (e) {}

  var ua = navigator.userAgent || '';
  if (navigator.webdriver) return;
  if (/bot|crawl|spider|slurp|headless|phantom|lighthouse|pingdom|uptime|monitor|python|curl|wget|httpclient|scrapy|preview/i.test(ua)) return;
  if (!navigator.languages || navigator.languages.length === 0) return;

  // Continental US only, judged by the device's time zone (excludes Alaska, Hawaii, territories, abroad)
  try {
    var tz = Intl.DateTimeFormat().resolvedOptions().timeZone || '';
    var conus = /^America\/(New_York|Detroit|Chicago|Denver|Boise|Phoenix|Los_Angeles|Menominee|Indiana\/.+|Kentucky\/.+|North_Dakota\/.+)$|^US\/(Eastern|Central|Mountain|Pacific|Arizona|East-Indiana|Michigan|Indiana-Starke)$/;
    if (!conus.test(tz)) return;
  } catch (e) {}

  var MIN_MS = 3000;
  var start = Date.now();
  var interacted = false;

  var loaded = false;
  var events = ['scroll', 'pointermove', 'pointerdown', 'touchstart', 'keydown'];

  function onInteract() {
    interacted = true;
    var wait = MIN_MS - (Date.now() - start);
    if (wait <= 0) loadAnalytics(); else setTimeout(loadAnalytics, wait);
  }

  function loadAnalytics() {
    if (loaded) return;
    loaded = true;
    events.forEach(function (ev) { window.removeEventListener(ev, onInteract, true); });

    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { dataLayer.push(arguments); };
    gtag('js', new Date());
    gtag('config', GA_ID);

    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
  }

  events.forEach(function (ev) {
    window.addEventListener(ev, onInteract, { capture: true, passive: true });
  });

  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href*="anedot.com"]');
    if (!a) return;
    interacted = true;
    if (Date.now() - start < MIN_MS) return;
    loadAnalytics();
    gtag('event', 'donate_click', { link_url: a.href, page_path: location.pathname, transport_type: 'beacon' });
  }, true);
})();
