/*
  Site guard for robynbird.com (and voterobynbird.com)
  © 2026 Friends of Robyn Bird. All rights reserved. Site by Shirah M. Brown.
  If this page is served from any address other than the official site,
  it reports the copy's address to the campaign's Google Analytics
  (event "copy_detected") and sends the visitor to the same page on
  https://www.voterobynbird.com.
*/
(function () {
  var OFFICIAL = 'https://www.robynbird.com';
  var ALLOWED = /^(www\.)?(vote)?robynbird\.com$|^robyn-bird\.github\.io$|^localhost$|^127\.0\.0\.1$/i;
  var host = location.hostname || '';
  if (ALLOWED.test(host) || location.protocol === 'file:') return;

  var target = OFFICIAL + location.pathname.replace(/^\/voterobynbird\.com/, '') + location.search + location.hash;
  var done = false;
  function go() { if (!done) { done = true; location.replace(target); } }

  try {
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function () { dataLayer.push(arguments); };
    gtag('js', new Date());
    gtag('config', 'G-9QTPPFE9CN', { send_page_view: false });
    gtag('event', 'copy_detected', {
      copy_host: host,
      copy_url: location.href.slice(0, 100),
      transport_type: 'beacon',
      event_callback: go,
      event_timeout: 1200
    });
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=G-9QTPPFE9CN';
    (document.head || document.documentElement).appendChild(s);
  } catch (e) {}
  setTimeout(go, 1500);
})();
