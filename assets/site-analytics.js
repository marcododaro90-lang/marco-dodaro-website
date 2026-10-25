(function () {
  'use strict';
  if (window.marcoCookieConsent) return;
  var ID = 'G-MDB7M27NGN';
  var KEY = 'md_cookie_consent_v1';
  var TTL = 180 * 24 * 60 * 60 * 1000;
  var started = false;
  var banner;
  var previousFocus;
  var stored = null;
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
  window['ga-disable-' + ID] = true;
  window.gtag('consent', 'default', {
    analytics_storage: 'denied', ad_storage: 'denied',
    ad_user_data: 'denied', ad_personalization: 'denied'
  });

  function readChoice() {
    try {
      var value = JSON.parse(localStorage.getItem(KEY));
      var age = value && Date.now() - value.at;
      var expires = new Date(value && value.at);
      expires.setMonth(expires.getMonth() + 6);
      if (value && value.version === 1 && typeof value.analytics === 'boolean' &&
          Number.isFinite(value.at) && age >= 0 && Date.now() < expires.getTime()) return value;
    } catch (e) { /* A blocked store never implies consent. */ }
    return null;
  }

  function clearAnalyticsCookies() {
    var names = document.cookie.split(';').map(function (entry) { return entry.trim().split('=')[0]; });
    var host = location.hostname;
    var domains = ['', host, '.' + host];
    var parts = host.split('.');
    while (parts.length > 2) { parts.shift(); domains.push(parts.join('.'), '.' + parts.join('.')); }
    names.forEach(function (name) {
      if (!/^_ga(?:_|$)/.test(name)) return;
      domains.forEach(function (domain) {
        document.cookie = name + '=; Max-Age=0; path=/; SameSite=Lax' + (domain ? '; domain=' + domain : '');
      });
    });
  }

  function enableAnalytics() {
    window['ga-disable-' + ID] = false;
    window.gtag('consent', 'update', {
      analytics_storage: 'granted', ad_storage: 'denied',
      ad_user_data: 'denied', ad_personalization: 'denied'
    });
    if (started) return;
    started = true;
    window.gtag('js', new Date());
    var referrer = '';
    try { var ref = new URL(document.referrer); referrer = ref.origin + ref.pathname; } catch (e) { /* No referrer. */ }
    window.gtag('config', ID, {
      allow_google_signals: false,
      allow_ad_personalization_signals: false,
      cookie_expires: TTL / 1000,
      cookie_update: false,
      page_location: location.origin + location.pathname,
      page_referrer: referrer
    });
    var script = document.createElement('script');
    script.id = 'md-google-analytics';
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + ID;
    document.head.appendChild(script);
  }

  function hideBanner() {
    banner.hidden = true;
    if (previousFocus && previousFocus.focus) previousFocus.focus();
  }

  function saveChoice(allow) {
    stored = { version: 1, analytics: allow, at: Date.now() };
    try { localStorage.setItem(KEY, JSON.stringify(stored)); } catch (e) { /* Choice applies to this page. */ }
    hideBanner();
    if (allow) enableAnalytics();
    else {
      window['ga-disable-' + ID] = true;
      clearAnalyticsCookies();
      if (started) {
        window.gtag('consent', 'update', {
          analytics_storage: 'denied', ad_storage: 'denied',
          ad_user_data: 'denied', ad_personalization: 'denied'
        });
        location.reload();
      }
    }
  }

  function openPreferences() {
    previousFocus = document.activeElement;
    document.getElementById('md-cookie-status').textContent = stored ?
      'Scelta attuale: statistiche ' + (stored.analytics ? 'consentite.' : 'rifiutate.') : '';
    banner.hidden = false;
    document.getElementById('md-cookie-reject').focus();
  }

  function init() {
    var style = document.createElement('style');
    style.textContent = '#md-cookie-banner[hidden]{display:none!important}#md-cookie-banner{position:fixed;left:0;right:0;bottom:0;z-index:9999;background:#141414;color:#f4f4f0;border-top:1px solid #555;padding:20px 24px;font-family:Inter,sans-serif;display:flex;align-items:center;justify-content:space-between;gap:20px;flex-wrap:wrap;max-height:80vh;overflow:auto;box-sizing:border-box}#md-cookie-banner p{margin:0;max-width:720px;font-size:.92rem;line-height:1.5;color:#f4f4f0}#md-cookie-banner a{color:#f0a471;text-decoration:underline}#md-cookie-actions{display:flex;gap:12px;flex-wrap:wrap}#md-cookie-actions button{background:#f4f4f0;color:#141414;border:1px solid #f4f4f0;padding:12px 18px;border-radius:999px;font:600 .9rem Inter,sans-serif;cursor:pointer;min-height:44px}#md-cookie-actions button:focus-visible,#md-cookie-preferences:focus-visible{outline:3px solid #f0a471;outline-offset:4px}#md-cookie-status{font-size:.8rem!important;margin-top:6px!important}#md-cookie-preferences{background:none;border:0;padding:4px 0;color:inherit;text-decoration:underline;font:inherit;cursor:pointer} @media(max-width:600px){#md-cookie-banner{padding:18px}#md-cookie-actions{width:100%}#md-cookie-actions button{flex:1}}';
    document.head.appendChild(style);
    banner = document.createElement('div');
    banner.id = 'md-cookie-banner';
    banner.hidden = true;
    banner.setAttribute('role', 'region');
    banner.setAttribute('aria-label', 'Preferenze cookie');
    banner.innerHTML = '<div><p>Questo sito usa strumenti tecnici necessari e, solo con il tuo consenso, Google Analytics per misurare visite e utilizzo dei contenuti. Puoi accettare o rifiutare i cookie statistici e cambiare scelta da “Preferenze cookie” nel footer. <a href="privacy-cookie-policy.html">Privacy e Cookie Policy</a>.</p><p id="md-cookie-status" aria-live="polite"></p></div><div id="md-cookie-actions"><button type="button" id="md-cookie-reject">Rifiuta statistiche</button><button type="button" id="md-cookie-accept">Accetta statistiche</button></div>';
    document.body.appendChild(banner);
    document.getElementById('md-cookie-reject').addEventListener('click', function () { saveChoice(false); });
    document.getElementById('md-cookie-accept').addEventListener('click', function () { saveChoice(true); });
    banner.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') { if (stored) hideBanner(); else saveChoice(false); }
    });
    var preferences = document.createElement('button');
    preferences.id = 'md-cookie-preferences';
    preferences.type = 'button';
    preferences.textContent = 'Preferenze cookie';
    preferences.addEventListener('click', openPreferences);
    var target = document.querySelector('.footer-bottom') || document.querySelector('footer') || document.body;
    target.appendChild(preferences);
    stored = readChoice();
    if (stored && stored.analytics) enableAnalytics();
    else {
      clearAnalyticsCookies();
      if (!stored) banner.hidden = false;
    }
  }

  window.marcoCookieConsent = { open: openPreferences };
  window.addEventListener('storage', function (event) {
    if (event.key !== KEY && event.key !== null) return;
    var value = readChoice();
    if (started && (!value || !value.analytics)) {
      window['ga-disable-' + ID] = true;
      clearAnalyticsCookies();
      location.reload();
    } else if (value && value.analytics) { stored = value; hideBanner(); enableAnalytics(); }
    else { stored = value; if (!value) openPreferences(); }
  });
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
}());
