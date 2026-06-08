<div class="cs_banner_theme">
  <h4><?php _e('Theme', 'iubenda') ?></h4>
  <div class="scrollable gap-fixer">
    <fieldset class="theme-select d-flex">
      <div class="mr-2">
        <label class="radio-theme radio-theme-dark">
          <input type="radio" name="iubenda_cookie_law_solution[simplified][banner_style]" value="dark" <?php echo checked( 'dark', iub_array_get(iubenda()->options['cs'], 'simplified.banner_style'), false) ?>>
        </label>
        <p class="text-xs text-center"><?php _e('Dark', 'iubenda') ?></p>
      </div>
      <div class="mr-2">
        <label class="radio-theme radio-theme-light">
          <input type="radio" name="iubenda_cookie_law_solution[simplified][banner_style]" value="light" <?php echo checked( 'light', iub_array_get(iubenda()->options['cs'], 'simplified.banner_style'), false) ?>>
        </label>
        <p class="text-xs text-center"><?php _e('Light', 'iubenda') ?></p>
      </div>
    </fieldset>
  </div>
</div>