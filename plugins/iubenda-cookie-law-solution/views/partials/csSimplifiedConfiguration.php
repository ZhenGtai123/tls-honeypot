<div class="d-lg-flex">

    <?php require_once IUBENDA_PLUGIN_PATH . '/views/partials/bannerPosition.php'; ?>
    <?php require_once IUBENDA_PLUGIN_PATH . '/views/partials/bannerStyle.php'; ?>

</div>

<div class="mb-5">
  <h4><?php _e('Legislation', 'iubenda') ?></h4>
  <div class="scrollable gap-fixer">
    <fieldset class="d-flex radio-large">
      <div class="radio-controller">
        <input type="radio" id="radioGdpr" name="iubenda_cookie_law_solution[simplified][legislation]" value="gdpr" <?php checked( 'gdpr', iub_array_get(iubenda()->options['cs'], 'simplified.legislation'), true ) ?> required>
        <label for="radioGdpr"><?php _e('GDPR Only', 'iubenda') ?></label>
      </div>
      <div class="radio-controller">
        <input type="radio" id="radioCcpa" name="iubenda_cookie_law_solution[simplified][legislation]" value="ccpa" <?php checked( 'ccpa', iub_array_get(iubenda()->options['cs'], 'simplified.legislation'), true ) ?> required>
        <label for="radioCcpa"><?php _e('CCPA Only', 'iubenda') ?></label>
      </div>
      <div class="radio-controller">
        <input type="radio" id="radioLGPD" name="iubenda_cookie_law_solution[simplified][legislation]" value="lgpd" <?php checked( 'lgpd', iub_array_get(iubenda()->options['cs'], 'simplified.legislation'), true ) ?> required>
        <label for="radioLGPD"><?php _e('LGPD Only', 'iubenda') ?></label>
      </div>
      <div class="radio-controller">
        <input type="radio" id="radioAll" name="iubenda_cookie_law_solution[simplified][legislation]" value="all" <?php checked( 'all', iub_array_get(iubenda()->options['cs'], 'simplified.legislation'), true ) ?> required>
        <label for="radioAll"><?php _e('All', 'iubenda') ?></label>
      </div>
    </fieldset>
  </div>
</div>

<div class="mb-5">
  <h4><?php _e('Require consent from', 'iubenda') ?></h4>
  <div class="scrollable gap-fixer">
    <fieldset class="d-flex radio-large">
        <div class="radio-controller">
            <input type="radio" id="radioWorldwide" name="iubenda_cookie_law_solution[simplified][require_consent]" value="worldwide" <?php checked( 'worldwide', iub_array_get(iubenda()->options['cs'], 'simplified.require_consent') ) ?> required>
            <label for="radioWorldwide">
                <div class="d-flex align-items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="30" viewBox="0 0 32 30">
                        <g fill="none" fill-rule="evenodd" transform="translate(1 1.632)">
                            <circle cx="18" cy="14.368" r="13" fill="currentColor" fill-opacity=".1" />
                            <circle cx="13" cy="13.368" r="13" stroke="currentColor" />
                            <path stroke="currentColor" d="M17.545 4.368h-3.409l-2.045 1.715v1.143h-2.046L8 8.368v1.143h3.409l.682.572h1.364l1.363 1.143h2.727l1.364 1.142 1.364-1.142H23M15.5 15.243h-1.25l-1.875-1.875h-2.5L8 15.243l1.25 3.125h1.875l1.25 1.25v3.125l.625.625h1.25l1.875-1.875v-1.875L18 17.743z" />
                        </g>
                    </svg>
                    <span class="ml-2"><?php _e('Worldwide', 'iubenda') ?></span>
                </div>
            </label>
    </div>
        <div class="radio-controller">
        <input type="radio" id="radioEU" name="iubenda_cookie_law_solution[simplified][require_consent]" value="eu_only" <?php checked( 'eu_only', iub_array_get(iubenda()->options['cs'], 'simplified.require_consent'), true ) ?> required>
        <label for="radioEU">
          <div class=" d-flex align-items-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="30" height="28" viewBox="0 0 30 28">
              <g fill="none" fill-rule="evenodd">
                <path fill="currentColor" fill-opacity=".1" d="M4.5 5.5H30v18H4.5z" />
                <path fill="currentColor" d="M13.5 7a.75.75 0 100-1.5.75.75 0 000 1.5zM13.5 17.5a.75.75 0 100-1.5.75.75 0 000 1.5zM18 11.5a.75.75 0 101.5 0 .75.75 0 00-1.5 0zM7.5 11.5a.75.75 0 101.5 0 .75.75 0 00-1.5 0zM16.682 14.682a.75.75 0 101.06 1.06.75.75 0 00-1.06-1.06zM9.257 7.257a.75.75 0 101.061 1.061.75.75 0 00-1.06-1.06zM10.318 14.682a.75.75 0 10-1.06 1.06.75.75 0 001.06-1.06zM17.743 7.257a.75.75 0 10-1.061 1.061.75.75 0 001.06-1.06z" />
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="M.75 2.5h25.391v18H.75z" />
                <path class="svg-stroke" fill="#D8D8D8" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="M.75 1v26.027" />
              </g>
            </svg>
            <span class="ml-2"><?php _e('EU Only', 'iubenda') ?></span>
          </div>
        </label>
      </div>
    </fieldset>
  </div>
</div>

<div class="my-5">
  <h4><?php _e('Banner buttons', 'iubenda') ?></h4>
  <fieldset>
    <label class="checkbox-regular">
      <input type="checkbox" class="mr-2 tcf-dependency" name="iubenda_cookie_law_solution[simplified][explicit_accept]" <?php checked( true, (bool) iub_array_get(iubenda()->options['cs'], 'simplified.explicit_accept')); ?> <?php echo true == (bool) iub_array_get(iubenda()->options['cs'], 'simplified.tcf') ? 'disabled':null ?>>
      <span><?php _e('Explicit Accept and Customize buttons', 'iubenda') ?></span>
    </label>

    <label class="checkbox-regular">
      <input type="checkbox" class="mr-2 tcf-dependency" name="iubenda_cookie_law_solution[simplified][explicit_reject]" <?php checked( true, (bool) iub_array_get(iubenda()->options['cs'], 'simplified.explicit_reject')); ?> <?php echo true == (bool) iub_array_get(iubenda()->options['cs'], 'simplified.tcf') ? 'disabled':null ?>>
      <span><?php _e('Explicit Reject button', 'iubenda') ?></span>
    </label>
  </fieldset>
</div>

<div class="my-5">
  <h4><?php _e('Other options', 'iubenda') ?></h4>
  <label class="checkbox-regular">
    <input type="checkbox" class="mr-2 iub-toggle-elements-status" data-group=".tcf-dependency" name="iubenda_cookie_law_solution[simplified][tcf]" <?php checked( true, (bool) iub_array_get(iubenda()->options['cs'], 'simplified.tcf')); ?>>
    <span>
      <div>
        <?php _e('Enable IAB Transparency and Consent Framework', 'iubenda') ?> - <a target="_blank" href="<?php echo iubenda()->settings->links['enable_iab']; ?>" class="link-underline"><?php _e('Learn More', 'iubenda') ?></a></div>
        <div class="notice notice--warning mt-2 p-3 d-flex align-items-center text-warning text-xs">
          <img class="mr-2" src="<?php echo IUBENDA_PLUGIN_URL ?>/assets/images/warning-icon.svg">

          <p><?php _e('You should activate this feature if you show ads on your website', 'iubenda') ?></p>
        </div>
      </span>
    </label>
    
  </div>
