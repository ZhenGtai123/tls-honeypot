<div class="py-5">
  <label class="checkbox-regular">
    <input type="checkbox" name="iubenda_cookie_law_solution[parse]" value="1" class="mr-2 section-checkbox-control" data-section-name="#iub_parser_engine_container" <?php checked( true, (bool) iubenda()->options['cs']['parse'] ) ?>>
      <span><?php _e('Automatically block scripts detected by the plugin', 'iubenda') ?> <a target="_blank" href="<?php echo iubenda()->settings->links['automatic_block_scripts']; ?>" class="ml-1 tooltip-icon">?</a></span>
  </label>
    <section id="iub_parser_engine_container" class="subOptions <?php echo (bool) iubenda()->options['cs']['parse']?: 'hidden' ?>">
        <div class="mb-3 d-flex flex-wrap align-items-center">
            <label class="radio-regular mr-4">
                <input type="radio" name="iubenda_cookie_law_solution[parser_engine]" value="new" class="mr-2 section-radio-control" <?php checked( 'new', iubenda()->options['cs']['parser_engine'] ) ?>>
                <span><?php _e('Primary', 'iubenda') ?></span>
            </label>
            <label class="mr-4 radio-regular text-xs">
                <input type="radio" name="iubenda_cookie_law_solution[parser_engine]" value="default" class="mr-2 section-radio-control" <?php checked( 'default', iubenda()->options['cs']['parser_engine'] ) ?>>
                <span><?php _e('Secondary', 'iubenda') ?></span>
            </label>
        </div>
        <p class="px-3 mx-4"><?php _e("Select Parsing Engine", 'iubenda') ?></p>
        <br>
        <div class="mb-2 d-flex flex-wrap align-items-center">
            <label class="checkbox-regular">
                <input type="checkbox" name="iubenda_cookie_law_solution[skip_parsing]" value="1" class="mr-2 section-checkbox-control" data-section-name="#section-block-script" <?php checked( true, (bool) iubenda()->options['cs']['skip_parsing'] ) ?>>
                <span><?php _e('Leave scripts untouched on the page if the user has already given consent', 'iubenda') ?></span>
            </label>
            <p class="px-3 mx-4"><?php _e("Enable this option to improve performance <strong>only</strong> if your site does <strong>not</strong> use a cache system or a cache plugin and if you're <strong>not</strong> collecting per-category consent. If you're in doubt, keep this setting disabled", 'iubenda') ?></p>
        </div>
    </section>
  <label class="checkbox-regular">
    <input type="checkbox" class="mr-2" name="iubenda_cookie_law_solution[ctype]" value="1" <?php checked( true, (bool) iubenda()->options['cs']['ctype'] ) ?>>
    <span><?php _e('Restrict the plugin to run only for requests that have "Content-type: text / html" (recommended)', 'iubenda') ?></span>
  </label>
  <label class="checkbox-regular">
    <input type="checkbox" class="mr-2" name="iubenda_cookie_law_solution[output_feed]" value="1" <?php checked( true, (bool) iubenda()->options['cs']['output_feed'] ) ?>>
    <span><?php _e('Do not run the plugin inside the RSS feed (recommended)', 'iubenda') ?></span>
  </label>
  <label class="checkbox-regular">
    <input type="checkbox" class="mr-2" name="iubenda_cookie_law_solution[output_post]" value="1" <?php checked( true, (bool) iubenda()->options['cs']['output_post'] ) ?>>
    <span><?php _e('Do not run the plugin on POST requests (recommended)', 'iubenda') ?></span>
  </label>
  <label class="checkbox-regular">
    <input type="checkbox" class="mr-2" name="iubenda_cookie_law_solution[deactivation]" value="1" <?php checked( true, (bool) iubenda()->options['cs']['deactivation'] ) ?>>
    <span><?php _e('Delete all plugin data upon deactivation', 'iubenda') ?></span>
  </label>
</div>
<div class="mb-5">
    <h4><?php _e('Menu position', 'iubenda') ?></h4>
    <div class="mb-2 d-flex align-items-center flex-wrap">
        <label class="radio-regular mr-3">
            <input type="radio" name="iubenda_cookie_law_solution[menu_position]" value="topmenu" class="mr-2" <?php checked( 'topmenu', iubenda()->options['cs']['menu_position'] ) ?>>
            <span><?php _e('Top menu', 'iubenda') ?></span>
        </label>
        <label class="mr-4 radio-regular text-xs">
            <input type="radio" name="iubenda_cookie_law_solution[menu_position]" value="submenu" class="mr-2" <?php checked( 'submenu', iubenda()->options['cs']['menu_position'] ) ?>>
            <span><?php _e('Submenu', 'iubenda') ?></span>
        </label>
    </div>
    <p class="description"><?php _e('Select whether to display iubenda in a top admin menu or the Settings submenu.', 'iubenda') ?></p>
</div>

<h4><?php _e('Custom settings', 'iubenda') ?></h4>
<fieldset class="custom-scripts mb-3 p-0 tabs tabs--style2">
  <ul class="tabs__nav text-xs">
    <li data-target="tab-custom-scripts" data-group="custom-scripts" class="tabs__nav__item active"><?php _e('Custom scripts', 'iubenda') ?></li>
    <li data-target="tab-custom-iframes" data-group="custom-scripts" class="tabs__nav__item"><?php _e('Custom iframes', 'iubenda') ?></li>
  </ul>
  <div data-target="tab-custom-scripts" data-group="custom-scripts" class="tabs__target p-3 active">
      <section id="custom-script-field" class="custom-script-field hidden">
          <input type="text" class="regular-text" name="iubenda_cookie_law_solution[custom_scripts][script][]" placeholder="<?php _e('Enter custom script', 'iubenda') ?>"" disabled>
          <select name="iubenda_cookie_law_solution[custom_scripts][type][]" disabled>
              <option value="0" selected="selected"><?php _e('Not set', 'iubenda') ?></option>
              <option value="1"><?php _e('Strictly necessary', 'iubenda') ?></option>
              <option value="2"><?php _e('Basic interactions &amp; functionalities', 'iubenda') ?></option>
              <option value="3"><?php _e('Experience enhancement', 'iubenda') ?></option>
              <option value="4"><?php _e('Analytics', 'iubenda') ?></option>
              <option value="5"><?php _e('Targeting &amp; Advertising', 'iubenda') ?></option>
          </select>
          <a target="_blank" href="javascript:void(0)" class="remove-custom-script-field button-secondary remove-custom-section" data-remove-section=".custom-script-field" title="Remove">-</a>
      </section>
      <div id="custom-script-fields">
          <?php
          foreach (iubenda()->options['cs']['custom_scripts'] as $script => $type){
              ?>
              <section class="custom-script-field">
                  <input type="text" class="regular-text" name="iubenda_cookie_law_solution[custom_scripts][script][]" placeholder="<?php _e('Enter custom script', 'iubenda') ?>"" value="<?php echo esc_attr( stripslashes($script) ); ?>">
                  <select name="iubenda_cookie_law_solution[custom_scripts][type][]">
                      <option value="0" <?php selected( $type, 0 ); ?>><?php _e('Not set', 'iubenda') ?></option>
                      <option value="1" <?php selected( $type, 1 ); ?>><?php _e('Strictly necessary', 'iubenda') ?></option>
                      <option value="2" <?php selected( $type, 2 ); ?>><?php _e('Basic interactions &amp; functionalities', 'iubenda') ?></option>
                      <option value="3" <?php selected( $type, 3 ); ?>><?php _e('Experience enhancement', 'iubenda') ?></option>
                      <option value="4" <?php selected( $type, 4 ); ?>><?php _e('Analytics', 'iubenda') ?></option>
                      <option value="5" <?php selected( $type, 5 ); ?>><?php _e('Targeting &amp; Advertising', 'iubenda') ?></option>
                  </select>
                  <a target="_blank" href="javascript:void(0)" class="remove-custom-script-field button-secondary remove-custom-section" data-remove-section=".custom-script-field" title="Remove">-</a>
              </section>
          <?php }?>
      </div>

    <p class=" text-gray-lighter m-0 mb-3"><?php _e("Provide a list of domains for any custom scripts you'd like to block, and assign their purposes. To make sure they are blocked correctly, please add domains in the same format as 'example.com', without any protocols e.g. 'http://' or 'https://'. You may also use wildcards (*) to include parent domains or subdomains.", 'iubenda') ?></p>
    <button class="btn btn-gray-outline btn-xs add-custom-section" data-append-section="#custom-script-fields" data-clone-section="#custom-script-field"><?php _e('Add New Script', 'iubenda') ?></button>
  </div>
  <div data-target="tab-custom-iframes" data-group="custom-scripts" class="tabs__target p-3">
      <section id="custom-iframe-field" class="custom-iframe-field hidden">
          <input type="text" class="regular-text" name="iubenda_cookie_law_solution[custom_iframes][iframe][]" placeholder="<?php _e('Enter custom iframe', 'iubenda') ?>"" disabled>
          <select name="iubenda_cookie_law_solution[custom_iframes][type][]" disabled>
              <option value="0" selected="selected"><?php _e('Not set', 'iubenda') ?></option>
              <option value="1"><?php _e('Strictly necessary', 'iubenda') ?></option>
              <option value="2"><?php _e('Basic interactions &amp; functionalities', 'iubenda') ?></option>
              <option value="3"><?php _e('Experience enhancement', 'iubenda') ?></option>
              <option value="4"><?php _e('Analytics', 'iubenda') ?></option>
              <option value="5"><?php _e('Targeting &amp; Advertising', 'iubenda') ?></option>
          </select>
          <a target="_blank" href="javascript:void(0)" class="remove-custom-iframe-field button-secondary remove-custom-section" data-remove-section=".custom-iframe-field" title="Remove">-</a>
      </section>
      <div id="custom-iframe-fields">
          <?php
            foreach (iub_array_get(iubenda()->options['cs'],'custom_iframes') as $iframe => $type){
            ?>
              <section id="custom-iframe-field" class="custom-iframe-field">
                  <input type="text" class="regular-text" name="iubenda_cookie_law_solution[custom_iframes][iframe][]" placeholder="<?php _e('Enter custom iframe', 'iubenda') ?>"  value='<?php echo esc_attr( stripslashes($iframe) ); ?>'>
                  <select name="iubenda_cookie_law_solution[custom_iframes][type][]">
                      <option value="0" <?php selected( $type, 0 ); ?>><?php _e('Not set', 'iubenda') ?></option>
                      <option value="1" <?php selected( $type, 1 ); ?>><?php _e('Strictly necessary', 'iubenda') ?></option>
                      <option value="2" <?php selected( $type, 2 ); ?>><?php _e('Basic interactions &amp; functionalities', 'iubenda') ?></option>
                      <option value="3" <?php selected( $type, 3 ); ?>><?php _e('Experience enhancement', 'iubenda') ?></option>
                      <option value="4" <?php selected( $type, 4 ); ?>><?php _e('Analytics', 'iubenda') ?></option>
                      <option value="5" <?php selected( $type, 5 ); ?>><?php _e('Targeting &amp; Advertising', 'iubenda') ?></option>
                  </select>
                  <a target="_blank" href="javascript:void(0)" class="remove-custom-iframe-field button-secondary remove-custom-section" data-remove-section=".custom-iframe-field" title="Remove">-</a>
              </section>
            <?php }?>

      </div>
    <p class="text-gray-lighter m-0 mb-3"><?php _e("Provide a list of domains for any custom iframes you'd like to block, and assign their purposes. To make sure they are blocked correctly, please add domains in the same format as 'example.com', without any protocols e.g. 'http://' or 'https://'. You may also use wildcards (*) to include parent domains or subdomains.", 'iubenda') ?></p>
    <button class="btn btn-gray-outline btn-xs add-custom-section" data-append-section="#custom-iframe-fields" data-clone-section="#custom-iframe-field"><?php _e('Add New iframe', 'iubenda') ?></button>
  </div>
</fieldset>