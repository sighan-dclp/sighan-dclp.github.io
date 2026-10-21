/* ==========================================================================
   SIGHAN — English / 简体中文 / 繁體中文 switch
   Every page carries all three languages. Text marked lang="en", lang="zh-Hans"
   or lang="zh-Hant" is shown only when <html lang> matches (see "Language
   switch" in style.css). This file loads in <head>, before the page paints, so
   the right language shows from the first frame. Without JavaScript the site
   stays in English.

   Which language a visitor sees, in order of precedence:
     1. ?lang= in the URL — en, zh-Hans or zh-Hant (zh alone means Simplified);
        use it for links shared with Chinese readers;
     2. the language they last picked with the EN / 简 / 繁 switch;
     3. their browser's first preferred language: Traditional for zh-TW, zh-HK,
        zh-MO and zh-Hant, Simplified for any other Chinese, else English.
   ========================================================================== */

(function () {
  var root = document.documentElement;
  var KEY = 'sighan-lang';
  var titles = {
    'en': document.title,
    'zh-Hans': root.getAttribute('data-title-zh-hans'),
    'zh-Hant': root.getAttribute('data-title-zh-hant')
  };

  // Map any spelling of a language we serve onto en / zh-Hans / zh-Hant.
  function normalize(tag) {
    if (!tag) return null;
    tag = String(tag).toLowerCase();
    if (tag === 'en' || tag.indexOf('en-') === 0) return 'en';
    if (!/^zh(-|$)/.test(tag)) return null;
    return /^zh-(hant|tw|hk|mo)\b/.test(tag) ? 'zh-Hant' : 'zh-Hans';
  }

  function saved() {
    try { return normalize(localStorage.getItem(KEY)); } catch (e) { return null; }
  }
  function save(lang) {
    try { localStorage.setItem(KEY, lang); } catch (e) { /* storage blocked: choice lasts this page only */ }
  }
  function fromUrl() {
    var m = /[?&]lang=([A-Za-z-]+)/.exec(location.search);
    return m ? normalize(m[1]) : null;
  }
  function fromBrowser() {
    var first = (navigator.languages && navigator.languages[0]) || navigator.language || '';
    return normalize(first) || 'en';
  }

  function apply(lang) {
    root.lang = lang;
    document.title = titles[lang] || titles.en;
    var buttons = document.querySelectorAll('[data-set-lang]');
    for (var i = 0; i < buttons.length; i++) {
      buttons[i].setAttribute('aria-pressed', String(buttons[i].getAttribute('data-set-lang') === lang));
    }
  }

  // Keep the address bar shareable: it carries ?lang= while the page is in Chinese.
  function syncUrl(lang) {
    try {
      var url = new URL(location.href);
      if (lang === 'en') url.searchParams.delete('lang');
      else url.searchParams.set('lang', lang);
      history.replaceState(history.state, '', url);
    } catch (e) { /* file:// and some embedded browsers refuse; the switch still works */ }
  }

  var current = fromUrl();
  if (current) save(current);
  else current = saved() || fromBrowser();

  root.classList.add('js');
  apply(current);

  document.addEventListener('DOMContentLoaded', function () {
    apply(current);   // the switch buttons exist now
    document.addEventListener('click', function (event) {
      var button = event.target.closest && event.target.closest('[data-set-lang]');
      if (!button) return;
      current = button.getAttribute('data-set-lang');
      save(current);
      apply(current);
      syncUrl(current);
    });
  });
})();
