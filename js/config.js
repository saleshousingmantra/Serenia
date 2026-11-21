/**
 * ==========================================================
 * CONFIG.JS
 * Serenia by House of Jets, Kiwale, Pune
 *
 * Central place for project settings and service credentials.
 * form.js and app.js read everything from window.SITE_CONFIG,
 * so nothing is hardcoded inside the logic files.
 *
 * Load this file BEFORE form.js and app.js.
 *
 * Supabase is the shared project used by all landing pages;
 * each enquiry row is tagged with this site's PROJECT_NAME.
 * ==========================================================
 */

window.SITE_CONFIG = {

  /* Shared Supabase project: all websites' leads go here. The "project" field on each row tells them apart. */
  SUPABASE_URL: "https://rgzpytocxhjzxsopkrmu.supabase.co",
  SUPABASE_ANON_KEY: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJnenB5dG9jeGhqenhzb3Brcm11Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODU5Mjg0MDcsImV4cCI6MjEwMTUwNDQwN30.pMm_t48EOxFd2pnbu2gy4y7EK8fzmem3H4zbbpiqNJ4",

  /* Supabase table that stores enquiries */
  SUPABASE_TABLE: "enquiries",

  /* Default project label saved with every enquiry row */
  PROJECT_NAME: "Serenia by House of Jets",

  DEFAULT_DEVELOPER_NAME: "House of Jets",

  /* Relationship manager assigned to every enquiry */
  DEFAULT_MANAGER_NAME: "Rishabh",
  DEFAULT_MANAGER_EMAIL: "",

  /* Contact numbers (digits only, with country code) */
  PHONE_WHATSAPP: "917415322403",
  PHONE_DISPLAY: "+91 74153 22403",

  /* Site */
  SITE_URL: "https://sereniakiwale.com",

  /* Placeholders for later: analytics */
  GA4_ID: "TODO_GA4_ID",
  GTM_ID: "TODO_GTM_ID",
  META_PIXEL_ID: "TODO_META_PIXEL_ID"

};

/**
 * ==========================================================
 * LEAD-SOURCE CAPTURE  (reusable — copy as-is into the next project)
 *
 * Nothing below this line is specific to this project. It only
 * depends on: this file loading before form.js/index.js (already
 * true — see the script order comment in index.html), and any form
 * on the page having two hidden fields named "source" and
 * "source_link". Drop this whole block into a new project's
 * config.js unchanged; only the credentials above need editing.
 *
 * What it does:
 *   1. On first page load in a browser tab, works out how the
 *      visitor arrived (ad click id, ?utm_source=, a known
 *      referring site, or "Direct / None") and remembers it in
 *      sessionStorage — so it survives internal navigation (e.g.
 *      reading a blog post before landing on the enquiry form)
 *      without being overwritten by the internal referrer.
 *   2. On every page's DOMContentLoaded, fills any [name="source"]
 *      field with that remembered value, and any [name="source_link"]
 *      field with the current page's URL (so that one always shows
 *      exactly which page the enquiry was submitted from).
 *
 * form.js then just reads those two fields like any other field
 * and sends them to Supabase — no changes needed there per project,
 * as long as the "enquiries" table (or equivalent) has "source" and
 * "source_link" columns.
 * ==========================================================
 */
(function () {

  var STORAGE_KEY = "lead_source";

  /* Map a referring domain to a friendly label. Extend this list per
     project as needed (e.g. add local classifieds/portal sites). */
  var KNOWN_REFERRERS = {
    "google.com": "Google (organic)",
    "google.co.in": "Google (organic)",
    "bing.com": "Bing (organic)",
    "facebook.com": "Facebook",
    "l.facebook.com": "Facebook",
    "instagram.com": "Instagram",
    "l.instagram.com": "Instagram",
    "youtube.com": "YouTube",
    "wa.me": "WhatsApp",
    "web.whatsapp.com": "WhatsApp",
    "t.co": "Twitter / X",
    "x.com": "Twitter / X",
    "linkedin.com": "LinkedIn"
  };

  function detectSource() {
    var params = new URLSearchParams(window.location.search);

    if (params.get("utm_source")) {
      var s = params.get("utm_source");
      if (params.get("utm_medium")) s += " / " + params.get("utm_medium");
      return s;
    }
    if (params.get("gclid")) return "Google Ads";
    if (params.get("fbclid")) return "Facebook Ads";

    if (document.referrer) {
      try {
        var host = new URL(document.referrer).hostname.replace(/^www\./, "");
        return KNOWN_REFERRERS[host] || host;
      } catch (e) {
        return "Direct / None";
      }
    }
    return "Direct / None";
  }

  /* Capture once per browser tab session (first touch only). */
  try {
    if (window.sessionStorage && !sessionStorage.getItem(STORAGE_KEY)) {
      sessionStorage.setItem(STORAGE_KEY, detectSource());
    }
  } catch (e) {
    /* Private/incognito mode or storage blocked — fields below simply
       fall back to "Direct / None" and the current URL. Never blocks
       the page or the form. */
  }

  /* Fill every matching field on every page, once the DOM is ready. */
  document.addEventListener("DOMContentLoaded", function () {
    try {
      var source = (window.sessionStorage && sessionStorage.getItem(STORAGE_KEY)) || "Direct / None";
      document.querySelectorAll('[name="source"]').forEach(function (el) {
        el.value = source;
      });
      document.querySelectorAll('[name="source_link"]').forEach(function (el) {
        el.value = window.location.href;
      });
    } catch (e) {
      /* no-op — forms still submit fine without these two fields */
    }
  });

})();
