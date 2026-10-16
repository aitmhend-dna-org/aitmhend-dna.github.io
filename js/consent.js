// North African Origins — ask before Google Analytics sets cookies.
//
// Google's "basic" consent mode: nothing from Google Analytics loads until the
// reader says yes. This script builds the question in the page's language (en,
// fr, ar) and shows it along the bottom when there is no answer yet, or the
// answer is more than six months old (the CNIL's guidance). Yes loads gtag
// with ads storage, ad user data and ad personalisation denied, and host-only
// cookies that last 13 months. No, or withdrawing a yes from the footer's
// Cookies button, turns the tag off and deletes its cookies. The answer lives
// in localStorage; when that is blocked, nothing is stored and the reader is
// simply asked again. Without JavaScript there is no question and no counting.
//
// Each page loads this file with `defer` and the measurement id in `data-ga`:
//   <script defer src="js/consent.js" data-ga="G-…"></script>
(function () {
  var KEY = "nao-consent";
  var MAX_AGE = 182 * 24 * 60 * 60 * 1000;   // about six months
  var COOKIE_SECONDS = 13 * 30 * 24 * 60 * 60; // 13 months
  var TEXT = {
    en: {
      label: "Cookies",
      ask: "May Google Analytics set cookies to count your visit and the pages you read? Nothing from Google Analytics loads unless you accept.",
      more: "What is counted",
      refuse: "Refuse",
      accept: "Accept",
      accepted: "Your answer: accepted on ",
      refused: "Your answer: refused on ",
      locale: "en-GB",
      dir: ""
    },
    fr: {
      label: "Cookies",
      ask: "Google Analytics peut-il déposer des cookies pour compter votre visite et les pages lues ? Rien ne se charge depuis Google Analytics sans votre accord.",
      more: "Ce qui est mesuré",
      refuse: "Refuser",
      accept: "Accepter",
      accepted: "Votre réponse : acceptée le ",
      refused: "Votre réponse : refusée le ",
      locale: "fr-FR",
      dir: "fr/"
    },
    ar: {
      label: "ملفات تعريف الارتباط",
      ask: "هل تسمح لـ Google Analytics بوضع ملفات تعريف الارتباط لإحصاء زيارتك والصفحات التي تقرؤها؟ لا يُحمَّل شيء من Google Analytics إلا إذا وافقت.",
      more: "ما الذي يُحصى",
      refuse: "رفض",
      accept: "قبول",
      accepted: "جوابك: قبول بتاريخ ",
      refused: "جوابك: رفض بتاريخ ",
      locale: "ar-MA",
      dir: "ar/"
    }
  };

  var me = document.currentScript;
  var id = me && me.getAttribute("data-ga");
  if (!id || !document.body) return;
  var root = document.documentElement;
  var t = TEXT[(root.lang || "en").slice(0, 2)] || TEXT.en;
  var returnTo = null;  // focus goes back to the opener only if one opened the banner
  var loaded = false;

  function el(tag, cls, text) {
    var node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text) node.textContent = text;
    return node;
  }

  // The banner: not modal, along the bottom, Refuse and Accept the same button.
  var box = el("div", "consent");
  box.setAttribute("role", "region");
  box.setAttribute("aria-label", t.label);
  box.hidden = true;
  var stripe = el("div", "stripe");
  stripe.setAttribute("aria-hidden", "true");
  var row = el("div", "container consent__row");
  var ask = el("p", "consent__text", t.ask + " ");
  var more = el("a", "", t.more);
  more.href = new URL("../" + t.dir + "privacy.html", me.src).href;
  ask.appendChild(more);
  var choices = el("div", "consent__choices");
  [["denied", t.refuse], ["granted", t.accept]].forEach(function (c) {
    var button = el("button", "btn consent__btn", c[1]);
    button.type = "button";
    button.setAttribute("data-consent", c[0]);
    button.addEventListener("click", function () { answer(c[0]); });
    choices.appendChild(button);
  });
  var now = el("p", "consent__now");
  now.hidden = true;
  row.appendChild(ask);
  row.appendChild(choices);
  row.appendChild(now);
  box.appendChild(stripe);
  box.appendChild(row);
  document.body.appendChild(box);

  function read() {
    try {
      var saved = JSON.parse(localStorage.getItem(KEY));
      if (saved && (saved.v === "granted" || saved.v === "denied") && Date.now() - saved.t < MAX_AGE) {
        return saved;
      }
    } catch (e) {}
    return null;
  }

  function write(value) {
    try { localStorage.setItem(KEY, JSON.stringify({ v: value, t: Date.now() })); } catch (e) {}
  }

  function gtag() { window.dataLayer.push(arguments); }

  function load() {
    window["ga-disable-" + id] = false;
    if (loaded) {
      gtag("consent", "update", { analytics_storage: "granted" });
      return;
    }
    loaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = gtag;
    gtag("consent", "default", {
      analytics_storage: "granted",
      ad_storage: "denied",
      ad_user_data: "denied",
      ad_personalization: "denied"
    });
    gtag("js", new Date());
    gtag("config", id, {
      cookie_domain: "none",          // host-only: the cookie stays on this site
      cookie_expires: COOKIE_SECONDS,
      allow_google_signals: false,
      allow_ad_personalization_signals: false
    });
    var tag = document.createElement("script");
    tag.async = true;
    tag.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(id);
    document.head.appendChild(tag);
  }

  function stop() {
    window["ga-disable-" + id] = true;
    if (loaded) gtag("consent", "update", { analytics_storage: "denied" });
    // Every Google Analytics cookie, host-only and on each parent domain.
    var labels = location.hostname.split(".");
    document.cookie.split(";").forEach(function (pair) {
      var name = pair.split("=")[0].replace(/^\s+|\s+$/g, "");
      if (!/^(_ga|_ga_.+|_gid|_gat.*)$/.test(name)) return;
      document.cookie = name + "=; Max-Age=0; path=/";
      for (var i = 0; i < labels.length - 1; i++) {
        document.cookie = name + "=; Max-Age=0; path=/; domain=." + labels.slice(i).join(".");
      }
    });
  }

  function pad() {
    root.style.setProperty("--consent-h", box.offsetHeight + "px");
  }

  function show(saved) {
    now.textContent = saved
      ? (saved.v === "granted" ? t.accepted : t.refused) +
        new Date(saved.t).toLocaleDateString(t.locale, { day: "numeric", month: "long", year: "numeric" }) + "."
      : "";
    now.hidden = !saved;
    box.hidden = false;
    root.classList.add("has-consent");
    pad();
  }

  function hide() {
    box.hidden = true;
    root.classList.remove("has-consent");
  }

  function answer(value) {
    write(value);
    hide();
    if (value === "granted") load(); else stop();
    if (returnTo) returnTo.focus();
    returnTo = null;
  }

  window.addEventListener("resize", function () { if (!box.hidden) pad(); });

  // The way back to the question: the footer's Cookies button on every page,
  // and the button on the privacy page. Both stay hidden without this script.
  Array.prototype.forEach.call(document.querySelectorAll("[data-consent-wrap]"), function (wrap) {
    wrap.hidden = false;
  });
  Array.prototype.forEach.call(document.querySelectorAll("[data-consent-open]"), function (opener) {
    opener.addEventListener("click", function () {
      returnTo = opener;
      show(read());
      choices.firstChild.focus();
    });
  });

  var saved = read();
  if (saved && saved.v === "granted") load();
  else if (!saved) show(null);
})();
