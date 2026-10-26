<?php
/**
 * Plugin Name: Mode Rokt Demo Post
 * Description: Rokt per post, with a choice of Rokt placement (Mike 10/26): "Article"
 *   (prod.rokt.freefindsarticle, option `mode_rokt_popup_post_ids`) or "Overlay"
 *   (prod.rokt.freefindsoverlay, option `mode_rokt_overlay_post_ids`). Set from the Posts list hover
 *   links (Rokt: Article / Rokt: Overlay / Disable Rokt) or the editor sidebar box "Rokt". Those posts
 *   get the Rokt ad on landing, and the Mode Popup Waterfall plus the site's other ad networks
 *   (AdSense, Taboola, SmartRecognition) are switched off there so only Rokt shows. Each placement
 *   is its own Rokt page, so each reports separately.
 *   Separately, internal demo posts listed in option `mode_rokt_hidden_post_ids` are reachable by
 *   direct link only (kept out of listings, feeds, search, sitemaps, related posts, REST lists).
 *   Assets are served from /rokt-demo/.
 */

if (!defined('ABSPATH')) exit;

// Rokt placements a post can run: key => [label, option holding its post ids, Rokt page identifier].
function mode_rokt_units() {
    return [
        'article' => ['Article', 'mode_rokt_popup_post_ids', 'rokt.freefindsarticle'],
        'overlay' => ['Overlay', 'mode_rokt_overlay_post_ids', 'rokt.freefindsoverlay'],
    ];
}

function mode_rokt_unit_ids($unit) {
    $u = mode_rokt_units()[$unit] ?? null;
    return $u ? array_map('intval', (array) get_option($u[1], [])) : [];
}

// The placement this post runs ('article' / 'overlay'), or '' when Rokt is off.
function mode_rokt_unit($post_id = null) {
    $post_id = (int) ($post_id ?: get_queried_object_id());
    if (!$post_id) return '';
    foreach (array_keys(mode_rokt_units()) as $unit) {
        if (in_array($post_id, mode_rokt_unit_ids($unit), true)) return $unit;
    }
    return '';
}

function mode_rokt_has_popup($post_id = null) {
    return mode_rokt_unit($post_id) !== '';
}

function mode_rokt_demo_ids() {
    return array_map('intval', (array) get_option('mode_rokt_hidden_post_ids', []));
}

function mode_rokt_is_demo($post_id = null) {
    $post_id = $post_id ?: get_queried_object_id();
    return $post_id && in_array((int) $post_id, mode_rokt_demo_ids(), true);
}

// One placement per post: take it out of every list, then add it to $unit's ('' = off).
function mode_rokt_set_unit($post_id, $unit) {
    foreach (mode_rokt_units() as $key => $u) {
        $ids = array_diff(mode_rokt_unit_ids($key), [(int) $post_id]);
        if ($key === $unit) $ids[] = (int) $post_id;
        update_option($u[1], array_values($ids), false);
    }
}

/* ---------- Posts list: Rokt: Article / Rokt: Overlay / Disable Rokt ---------- */

add_filter('post_row_actions', function ($actions, $post) {
    if ($post->post_type !== 'post' || !current_user_can('edit_post', $post->ID)) return $actions;
    $now = mode_rokt_unit($post->ID);
    $link = function ($unit, $text) use ($post) {
        $url = wp_nonce_url(admin_url('admin-post.php?action=mode_rokt_toggle&post=' . $post->ID . '&unit=' . $unit), 'mode_rokt_toggle_' . $post->ID);
        return '<a href="' . esc_url($url) . '">' . esc_html($text) . '</a>';
    };
    foreach (mode_rokt_units() as $key => $u) {
        if ($key !== $now) $actions['mode_rokt_' . $key] = $link($key, 'Rokt: ' . $u[0]);
    }
    if ($now) $actions['mode_rokt_off'] = $link('off', 'Disable Rokt');
    return $actions;
}, 10, 2);

add_action('admin_post_mode_rokt_toggle', function () {
    $post_id = (int) ($_GET['post'] ?? 0);
    check_admin_referer('mode_rokt_toggle_' . $post_id);
    if (get_post_type($post_id) !== 'post' || !current_user_can('edit_post', $post_id)) wp_die('Cannot change this post.');
    $unit = sanitize_key($_GET['unit'] ?? '');
    mode_rokt_set_unit($post_id, isset(mode_rokt_units()[$unit]) ? $unit : '');
    wp_safe_redirect(wp_get_referer() ?: admin_url('edit.php'));
    exit;
});

// "Rokt" column so it's easy to see which posts have it on.
add_filter('manage_post_posts_columns', function ($cols) {
    $cols['mode_rokt'] = 'Rokt';
    return $cols;
});
add_action('manage_post_posts_custom_column', function ($col, $post_id) {
    if ($col !== 'mode_rokt') return;
    $unit = mode_rokt_unit($post_id);
    echo $unit ? '<strong style="color:#F7007C">' . esc_html(mode_rokt_units()[$unit][0]) . '</strong>' : '—';
}, 10, 2);

/* ---------- Editor sidebar: same switch ---------- */

add_action('add_meta_boxes_post', function () {
    add_meta_box('mode-rokt-toggles', 'Rokt', function ($post) {
        wp_nonce_field('mode_rokt_toggles', 'mode_rokt_nonce');
        $now = mode_rokt_unit($post->ID);
        $choices = ['' => 'Off'];
        foreach (mode_rokt_units() as $key => $u) $choices[$key] = $u[0];
        foreach ($choices as $key => $text) { ?>
        <p style="margin:4px 0"><label><input type="radio" name="mode_rokt_unit" value="<?php echo esc_attr($key); ?>" <?php checked($now, $key); ?> />
          <?php echo esc_html($text); ?></label></p>
        <?php } ?>
        <p class="description">Article or Overlay shows that Rokt placement on landing and switches off the other popups and ads on this post.</p>
        <?php
    }, 'post', 'side', 'high');
});

add_action('save_post_post', function ($post_id) {
    if (!isset($_POST['mode_rokt_nonce']) || !wp_verify_nonce($_POST['mode_rokt_nonce'], 'mode_rokt_toggles')) return;
    if (wp_is_post_revision($post_id) || !current_user_can('edit_post', $post_id)) return;
    $unit = sanitize_key($_POST['mode_rokt_unit'] ?? '');
    mode_rokt_set_unit($post_id, isset(mode_rokt_units()[$unit]) ? $unit : '');
});

/* ---------- Keep hidden posts unfindable ---------- */

add_action('pre_get_posts', function ($q) {
    if (is_admin() || $q->is_singular()) return;
    $ids = mode_rokt_demo_ids();
    if (!$ids) return;
    $q->set('post__not_in', array_merge((array) $q->get('post__not_in'), $ids));
});

// Jetpack Search answers the site's search box from its own index and skips post__not_in
// above, so drop hidden posts from the results it hands back too (10/26: search still
// listed the JCPenney test post).
add_filter('the_posts', function ($posts, $q) {
    if (is_admin() || $q->is_singular()) return $posts;
    $ids = mode_rokt_demo_ids();
    if (!$ids || !$posts) return $posts;
    return array_values(array_filter($posts, function ($p) use ($ids) {
        return !in_array((int) (is_object($p) ? $p->ID : $p), $ids, true);
    }));
}, 10, 2);

add_filter('wp_robots', function ($robots) {
    if (is_singular() && mode_rokt_is_demo()) {
        $robots['noindex'] = true;
        $robots['nofollow'] = true;
    }
    return $robots;
});

add_filter('wp_sitemaps_posts_query_args', function ($args) {
    $args['post__not_in'] = array_merge($args['post__not_in'] ?? [], mode_rokt_demo_ids());
    return $args;
});

add_filter('jetpack_sitemap_skip_post', function ($skip, $post) {
    return $skip || mode_rokt_is_demo($post->ID ?? 0);
}, 10, 2);

add_filter('jetpack_relatedposts_filter_exclude_post_ids', function ($ids) {
    return array_merge((array) $ids, mode_rokt_demo_ids());
});

add_filter('rest_post_query', function ($args) {
    $args['post__not_in'] = array_merge($args['post__not_in'] ?? [], mode_rokt_demo_ids());
    return $args;
});

// Never email subscribers or auto-share a demo post.
add_filter('jetpack_is_post_mailable', function ($mailable, $post_id = 0) {
    return mode_rokt_is_demo($post_id) ? false : $mailable;
}, 10, 2);
add_filter('publicize_should_publicize_published_post', function ($should, $post) {
    return ($post && mode_rokt_is_demo($post->ID)) ? false : $should;
}, 10, 2);

/* ---------- Popup on posts with it switched on ---------- */

// Only the Rokt popup on this page: switch off the normal waterfall.
add_action('wp', function () {
    if (!is_singular() || !mode_rokt_has_popup() || !class_exists('Mode_Popup_Waterfall')) return;
    $mpw = Mode_Popup_Waterfall::get_instance();
    remove_action('wp_head', [$mpw, 'inject_legacy_blocker'], 1);
    remove_action('wp_footer', [$mpw, 'inject_waterfall_script'], 99);
});

// Only Rokt monetizes this page: strip the site's other ad networks (AdSense via Site Kit,
// Taboola, SmartRecognition). Analytics/conversion pixels are left alone.
add_filter('googlesitekit_adsense_tag_blocked', function ($blocked) {
    return (is_singular() && mode_rokt_has_popup()) ? true : $blocked;
});

add_action('template_redirect', function () {
    if (!is_singular() || !mode_rokt_has_popup()) return;
    ob_start(function ($html) {
        return preg_replace([
            '#<script[^>]*adsbygoogle\.js[^>]*>\s*</script>#i',
            '#<!-- BEGIN SMART RECOGNITION CODE -->.*?<!-- END SMART RECOGNITION CODE -->#is',
            '#<script[^>]*>(?:(?!</script>).)*_taboola(?:(?!</script>).)*</script>#is',
            '#<div id="taboola-[^"]*"></div>#i',
        ], '', $html);
    });
});

// Pick up the reader's email from the link (email=, or aff_sub5= when it holds a real address) and
// take it out of the address bar before analytics and ad pixels read the page URL.
add_action('wp_head', function () {
    if (!is_singular() || !mode_rokt_has_popup()) return;
    ?>
    <script>
    (function () {
      try {
        var u = new URL(window.location.href), p = u.searchParams, ok = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        ['email', 'aff_sub5'].forEach(function (k) {
          var v = p.get(k);
          if (v && ok.test(v)) { window.MODE_ROKT_EMAIL = window.MODE_ROKT_EMAIL || v; p.delete(k); }
        });
        if (window.MODE_ROKT_EMAIL) {
          var q = p.toString();
          history.replaceState(history.state, '', u.pathname + (q ? '?' + q : '') + u.hash);
        }
      } catch (_) {}
    })();
    </script>
    <?php
}, 0);

add_action('wp_head', function () {
    if (!is_singular() || !mode_rokt_has_popup()) return;
    ?>
    <script src="/rokt-demo/rokt-init.js?v=prod-20261023"></script>
    <style>
      #mode-overlay{position:fixed!important;inset:0;width:100%;height:100%;background:rgba(0,0,0,.5);
        z-index:2147483647!important;display:flex!important;visibility:visible!important;align-items:center;
        justify-content:center;padding:16px;box-sizing:border-box;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif}
      #mode-overlay.mode-hidden{display:none!important}
      #mode-overlay.mode-waiting{visibility:hidden!important;pointer-events:none}
      #mode-overlay *{box-sizing:border-box}
      #mode-popup{max-width:600px;width:100%;max-height:calc(100vh - 32px);overflow:auto;background:#fff;
        border-radius:24px;box-shadow:0 20px 60px rgba(0,0,0,.2);position:relative}
      @media (max-width:599px){#mode-popup{max-width:340px}}
      #mode-popup .mode-close{position:absolute;top:16px;right:16px;width:36px;height:36px;padding:0;
        background:rgba(128,128,128,.15);border:none;border-radius:50%;display:flex;align-items:center;
        justify-content:center;cursor:pointer;z-index:10;box-shadow:0 2px 8px rgba(0,0,0,.15)}
      #mode-popup .mode-logo{position:absolute;top:24px;left:24px;width:56px;height:56px;border-radius:50%;
        overflow:hidden;z-index:10;box-shadow:0 4px 12px rgba(0,0,0,.15);background:#fff}
      #mode-popup .mode-logo img{width:100%;height:100%;object-fit:cover;margin:0}
      #mode-popup .mode-content{padding:92px 32px 24px;text-align:center}
      #mode-popup .mode-pill{background:linear-gradient(135deg,#F7007C 0%,#C4005F 100%);color:#fff;
        padding:8px 16px;border-radius:20px;font-size:14px;margin-bottom:12px;display:inline-block;
        font-weight:600;box-shadow:0 4px 12px rgba(247,0,124,.12);line-height:1.3}
      #mode-popup .mode-title{margin:8px 0;font-size:24px;font-weight:800;line-height:1.2;color:#111827}
      #mode-popup .rokt-slot{margin:16px 0 8px;min-height:180px;display:flex;flex-direction:column;
        align-items:stretch;justify-content:center}
      #rokt-placeholder{width:100%}
      #mode-popup .mode-footer{padding:12px 0 20px;display:flex;justify-content:center}
      #mode-popup .mode-footer img{height:34px;width:auto;margin:0}
    </style>
    <?php
}, 2);

add_action('wp_footer', function () {
    if (!is_singular() || !mode_rokt_has_popup()) return;
    ?>
    <?php // Rokt QA (Mike 10/26): the hidden JCPenney test post (28805, Overlay ID) opens the popup right away,
          // even before Rokt sends an ad, so Rokt can review the placement while the Overlay ID isn't active.
          // Every other post still waits for an ad. Remove once Rokt has signed off. ?>
    <div id="mode-overlay" class="<?php echo get_queried_object_id() === 28805 ? '' : 'mode-waiting'; ?>" role="dialog" aria-modal="true" aria-label="Offer">
      <div id="mode-popup">
        <button type="button" class="mode-close" aria-label="Close">
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path d="M13 1L1 13M1 1L13 13" stroke="#555" stroke-width="2.5" stroke-linecap="round"/>
          </svg>
        </button>
        <div class="mode-logo"><img src="/rokt-demo/ff-search-icon.png?v=20260923" alt="ModeFreeFinds" /></div>
        <div class="mode-content">
          <div class="mode-pill">Thanks for reading — you've unlocked premium content!</div>
          <h2 class="mode-title">Learn More Below</h2>
          <div class="rokt-slot">
            <div id="rokt-placeholder" data-ad-slot="post_checkout_rokt"></div>
          </div>
          <div class="mode-footer"><img src="/rokt-demo/ff-full-logo.png?v=20260923" alt="ModeFreeFinds" /></div>
        </div>
      </div>
    </div>
    <script>
    (function () {
      // Dismiss: X button, clicking the dimmed area outside the popup, or Esc.
      var overlay = document.getElementById('mode-overlay');
      function close() { overlay.classList.add('mode-hidden'); }
      overlay.querySelector('.mode-close').addEventListener('click', close);
      overlay.addEventListener('click', function (e) { if (e.target === overlay) close(); });
      document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });

      if (!window.mParticle || !window.ROKT_CONFIG) { console.warn('[Rokt] SDK not initialized.'); return; }

      // Reader's email comes from the link (picked up in <head>) or the funnel session; the rest from
      // the link or funnel session. Nothing is made up: anything missing just isn't sent.
      var urlParams = new URLSearchParams(window.location.search);
      var session = {}, stored = {};
      try { session = JSON.parse(sessionStorage.getItem('funnel_params') || '{}'); } catch (_) {}
      try { stored = JSON.parse(localStorage.getItem('funnel_params') || '{}'); } catch (_) {}
      function pick(key) { return urlParams.get(key) || session[key] || stored[key] || ''; }
      function isEmail(v) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v || ''); }

      var email = [window.MODE_ROKT_EMAIL, session.email, stored.email].filter(isEmail)[0] || '';
      var firstName = pick('first_name'), lastName = pick('last_name'), zip = pick('zip');
      // Confirmation ref: the link's own ID if it has one (confirmationref=, or the TUNE
      // transaction_id / click_id the email/SMS links already carry), otherwise a new one for this visit.
      var signupId = pick('confirmationref') || pick('confirmation_ref') || pick('transaction_id') ||
        pick('click_id') || pick('signup_id') ||
        'mff-' + Date.now().toString(36) + Math.floor(Math.random() * 1e9).toString(36);
      var affId = pick('aff_id'), affSub = pick('aff_sub');
      var utmSource = affId || pick('utm_source');
      var utmContent = affSub || pick('utm_content');
      var utmMedium = pick('utm_medium'), utmCampaign = pick('utm_campaign');
      var IDENTIFIER = (window.ROKT_CONFIG.isDev ? 'stg.' : 'prod.') + <?php echo wp_json_encode(mode_rokt_units()[mode_rokt_unit()][2]); ?>;

      if (email) window.mParticle.Identity.identify({ userIdentities: { email: email } }, function (result) {
        if (!(result && result.getUser && result.getUser())) return;
        var u = result.getUser();
        if (firstName) u.setUserAttribute('firstname', firstName);
        if (lastName) u.setUserAttribute('lastname', lastName);
        if (zip) u.setUserAttribute('shippingzipcode', zip);
        u.setUserAttribute('confirmationref', signupId);
        u.setUserAttribute('country', 'US');
        if (utmSource) u.setUserAttribute('utmsource', utmSource);
        if (utmMedium) u.setUserAttribute('utmmedium', utmMedium);
        if (utmCampaign) u.setUserAttribute('utmcampaign', utmCampaign);
        if (utmContent) u.setUserAttribute('utmcontent', utmContent);
      });

      // Call selectPlacements exactly once per page view.
      window.mParticle.ready(async function () {
        try {
          // Rokt docs step 3: tell Rokt which page the reader is on.
          window.mParticle.logPageView('page_view', { screenname: location.pathname.split('/').filter(Boolean).pop() || 'home',
            url: location.href, title: document.title, referringpage: document.referrer });
          var raw = { email: email, firstname: firstName, lastname: lastName, shippingzipcode: zip,
            country: 'US', language: 'en', confirmationref: signupId, utmsource: utmSource,
            utmmedium: utmMedium, utmcampaign: utmCampaign, utmcontent: utmContent,
            customertype: 'guest', newcustomer: 'true' };
          var attributes = {};
          Object.keys(raw).forEach(function (k) { if (raw[k]) attributes[k] = String(raw[k]); });
          // Forget anything the browser remembers from an earlier visit (old demo/test links) that this
          // visit doesn't supply, so Rokt doesn't get a stale or fake email/name.
          var me = window.mParticle.Identity.getCurrentUser();
          if (me) Object.keys(raw).forEach(function (k) { if (!raw[k]) me.removeUserAttribute(k); });
          var selection = await window.mParticle.Rokt.selectPlacements({ identifier: IDENTIFIER, attributes: attributes });
          // Only show the popup once Rokt has an offer to display; no offer (e.g. session cap) = no popup.
          function show() { overlay.classList.remove('mode-waiting'); }
          if (selection && selection.on) selection.on('PLACEMENT_INTERACTIVE').subscribe(show);
          // Reader got to the end of the Rokt offers: close the popup instead of leaving it empty.
          if (selection && selection.on) {
            ['PLACEMENT_COMPLETED', 'PLACEMENT_CLOSED'].forEach(function (ev) {
              selection.on(ev).subscribe(function () { window.MODE_ROKT_DONE = ev; close(); });
            });
          }
        } catch (err) { console.error('[Rokt] selectPlacements failed', err); }
      });
    })();
    </script>
    <?php
}, 100);
