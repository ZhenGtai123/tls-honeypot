  <div class="tabs">
    <h3 class="text-bold text-gray text-md mb-0"><?php _e('Configuration', 'iubenda') ?></h3>
    <div class="scrollable gap-fixer">
      <fieldset class="radio-large">
        <div class="d-flex tabs__nav">
            <?php
            if (iub_array_get(iubenda()->options['global_options'], 'site_id')) {
                ?>
                <div class="m-1 mr-2 tabs__nav__item <?php echo iub_array_get(iubenda()->options['cs'], 'configuration_type') == 'simplified' ?: 'active' ?>" data-target="configuration-type-simplified-tab" data-group="configuration-type">
                    <input class="section-radio-control cs-configuration-type" type="radio" id="radioSimplified" name="iubenda_cookie_law_solution[configuration_type]" value="simplified" <?php checked('simplified', iub_array_get(iubenda()->options['cs'], 'configuration_type')) ?>>
                    <label for="radioSimplified">
                        <div class=" d-flex align-items-center">
                            <svg xmlns="http://www.w3.org/2000/svg" width="29" height="27" viewBox="0 0 29 27">
                                <title><?php _e('Simplified', 'iubenda') ?></title>
                                <g fill="none" fill-rule="evenodd" transform="translate(1 1)">
                                    <rect width="25" height="11" stroke="currentColor" rx="5.5"/>
                                    <rect width="25" height="11" y="14" fill="currentColor" stroke="currentColor" rx="5.5"/>
                                    <rect width="7" height="7" x="2" y="2" fill="currentColor" rx="3.5"/>
                                    <rect width="7" height="7" x="16" y="16" fill="#FFF" rx="3.5"/>
                                    <rect width="25" height="11" x="3" y="2" fill="currentColor" fill-opacity=".119" rx="5.5"/>
                                </g>
                            </svg>
                            <span href="#tab-3" class="ml-2"><?php _e('Simplified', 'iubenda') ?></span>
                        </div>
                    </label>
                </div>
                <?php
            }
            ?>
          <div class="m-1 mr-2 tabs__nav__item <?php echo iub_array_get(iubenda()->options['cs'], 'configuration_type') == 'manual' ?: 'active' ?>" data-target="configuration-type-manual-tab" data-group="configuration-type">
            <input type="radio" id="radioManual" class="section-radio-control cs-configuration-type" name="iubenda_cookie_law_solution[configuration_type]" value="manual" <?php checked( 'manual', iub_array_get(iubenda()->options['cs'], 'configuration_type') ) ?>>
            <label for="radioManual">
              <div class="d-flex align-items-center">
                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" viewBox="0 0 25 25">
                  <title><?php _e('Manual embed', 'iubenda') ?></title>
                  <g fill="none" fill-rule="evenodd" transform="translate(1 1)">
                    <rect width="21" height="21" x="3" y="3" fill="currentColor" fill-opacity=".119" rx="2" />
                    <rect width="21" height="21" stroke="currentColor" rx="2" />
                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="M5.818 6.406l5.657 4-5.657 4M11.5 14.5h4" />
                  </g>
                </svg>
                <span href="#tab-4" class="ml-2"><?php _e('Manual embed', 'iubenda') ?></span>
              </div>
            </label>
          </div>
          
        </div>
      </fieldset>
    </div>
    <div class="my-4 subOptions">
        <?php
        if (iub_array_get(iubenda()->options['global_options'], 'site_id')) {
            ?>
            <section class="tabs__target <?php echo iub_array_get(iubenda()->options['cs'], 'configuration_type') != 'simplified' ?: 'active' ?>" data-target="configuration-type-simplified-tab" data-group="configuration-type">
                <?php require_once IUBENDA_PLUGIN_PATH . 'views/partials/csSimplifiedConfiguration.php'; ?>
            </section>
            <?php
        }
        ?>
      <section class="tabs__target <?php echo iub_array_get(iubenda()->options['cs'], 'configuration_type') != 'manual' ?: 'active' ?>" data-target="configuration-type-manual-tab" data-group="configuration-type">
        <?php require_once IUBENDA_PLUGIN_PATH . 'views/partials/csManualConfiguration.php'; ?>
      </section>
    </div>
  </div>

  <div class="d-flex align-items-center pt-3">
    <label class="checkbox-regular">
      <input type="checkbox" class="mr-2 section-checkbox-control" name="iubenda_cookie_law_solution[amp_support]" value="1" <?php checked( true, (bool) iubenda()->options['cs']['amp_support'] ) ?> data-section-name="#amp_support"/>
      <span><?php _e('Enable Google AMP support', 'iubenda') ?> <a target="_blank" href="<?php echo iubenda()->settings->links["enable_amp_support"]; ?>" class="ml-1 tooltip-icon">?</a></span>
    </label>
  </div>
  <section id="amp_support" class="subOptions my-2 <?php echo (bool) iubenda()->options['cs']['amp_support'] ?: 'hidden' ?>">
    <h4><?php _e('Select the iubenda AMP configuration file location.', 'iubenda') ?></h4>
    <div class="mb-2 d-flex flex-wrap align-items-center">
      <label class="radio-regular mb-3 mr-4">
        <input type="radio" name="iubenda_cookie_law_solution[amp_source]" value="local" class="mr-2 section-radio-control" data-section-name="#auto_generated_conf_file" data-section-group=".amp_configuration_file" <?php checked( 'local', iub_array_get(iubenda()->options['cs'], 'amp_source')) ?>>
        <span><?php _e('Auto-generated configuration file', 'iubenda') ?></span>
      </label>
      <label class="mr-4 mb-3 radio-regular text-xs">
        <input type="radio" name="iubenda_cookie_law_solution[amp_source]" value="remote" class="mr-2 section-radio-control" data-section-name="#custom_conf_file" data-section-group=".amp_configuration_file" <?php checked( 'remote', iub_array_get(iubenda()->options['cs'], 'amp_source')) ?>>
        <span><?php _e('Custom configuration file', 'iubenda') ?></span>
      </label>
    </div>

    <section id="auto_generated_conf_file" class="text-xs text-gray amp_configuration_file <?php echo iub_array_get(iubenda()->options['cs'], 'amp_source') == 'local' ?: 'hidden' ?>">
      <div class="border-1 border-gray rounded mt-2 py-2 px-3 d-flex flex-wrap align-items-center">
          <?php

          if (empty(iubenda()->options['cs']['amp_template_done'])) {
              echo '
					<p class="description">' . _e('No file available. Save changes to generate iubenda AMP configuration file.', 'iubenda') . '</p>';
          } else {
          ?>
          <table class="table">
              <tbody>
              <?php
              // multilang support
              if (iubenda()->multilang && !empty(iubenda()->languages)) {
                  foreach (iubenda()->languages as $lang_id => $lang_name) {
                    if(!iub_array_get(iubenda()->options['cs']['amp_template_done'], $lang_id, false) ?: false){
                        continue;
                    }
                      ?>
                      <tr>
                          <td><p class="text-bold"><?php echo $lang_name ?></p></td>
                          <td>
                              <a href="<?php echo iubenda()->AMP->get_amp_template_url($lang_id) ?>" target="_blank"><?php echo iubenda()->AMP->get_amp_template_url($lang_id) ?></a>
                          </td>
                      </tr>
                      <?php
                  }
              } else {
                  ?>
                  <tr>
                      <td><p class="text-bold"><?php _e('Default language', 'iubenda') ?></p></td>
                      <td>
                          <a href="<?php echo iubenda()->AMP->get_amp_template_url() ?>" target="_blank"><?php echo iubenda()->AMP->get_amp_template_url() ?></a>
                      </td>
                  </tr>
                  <?php
              }
              }
              ?>
              </tbody>
          </table>
      </div>

      <div class="notice notice--general mt-2 p-3 d-flex align-items-center text-xs">
        <p><?php _e('Seeing the AMP cookie notice when testing from Google but not when visiting your AMP pages directly?', 'iubenda') ?> <a target="_blank" href="<?php echo iubenda()->settings->links["amp_support"]; ?>" class="link-underline"><?php _e('Learn how to fix it', 'iubenda') ?></a></p>
      </div>

    </section>
    <section id="custom_conf_file" class="text-xs text-gray amp_configuration_file <?php echo iub_array_get(iubenda()->options['cs'], 'amp_source') == 'remote' ?: 'hidden' ?>">
        <table class="table">
            <tbody>
            <?php
            $languages = (new ProductHelper())->get_languages();
            foreach ($languages as $lang_id => $lang_name){
                ?>
                <tr>
                    <td><label class="text-bold" for="iub_amp_template-<?php echo $lang_id; ?>"><?php echo $lang_name; ?></label></td>
                    <td><input id="iub_amp_template-<?php echo $lang_id; ?>" type="text" class="regular-text" name="iubenda_cookie_law_solution[amp_template][<?php echo $lang_id; ?>]" value="<?php echo iub_array_get(iubenda()->options['cs'], "amp_template.{$lang_id}") ?>"/></td>
                </tr>
            <?php } ?>
            </tbody>
        </table>
    </section>
  </section>

  <div class="d-flex align-items-center pt-3">
      <label class="checkbox-regular">
          <input type="checkbox" name="iubenda_cookie_law_solution[parse]" value="1" class="mr-2 section-checkbox-control" data-section-name="#iub_parser_engine_container" <?php checked( true, (bool) iubenda()->options['cs']['parse'] ) ?>>
          <span><?php _e('Automatically block scripts detected by the plugin', 'iubenda') ?> <a target="_blank" href="<?php echo iubenda()->settings->links['automatic_block_scripts']; ?>" class="ml-1 tooltip-icon">?</a></span>
      </label>
  </div>
  <section id="iub_parser_engine_container" class="subOptions <?php echo (bool) iubenda()->options['cs']['parse']?: 'hidden' ?>">
      <h4><?php _e('Select Parsing Engine', 'iubenda') ?></h4>
      <div class="mb-3 d-flex flex-wrap align-items-center">
          <label class="radio-regular mr-4 mb-3">
              <input type="radio" name="iubenda_cookie_law_solution[parser_engine]" value="new" class="mr-2 section-radio-control" <?php checked( 'new', iubenda()->options['cs']['parser_engine'] ) ?>>
              <span><?php _e('Primary', 'iubenda') ?></span>
          </label>
          <label class="mr-4 mb-3 radio-regular text-xs">
              <input type="radio" name="iubenda_cookie_law_solution[parser_engine]" value="default" class="mr-2 section-radio-control" <?php checked( 'default', iubenda()->options['cs']['parser_engine'] ) ?>>
              <span><?php _e('Secondary', 'iubenda') ?></span>
          </label>
      </div>
      <div class="mb-2 d-flex flex-wrap align-items-center">
          <label class="checkbox-regular">
              <input type="checkbox" name="iubenda_cookie_law_solution[skip_parsing]" value="1" class="mr-2 section-checkbox-control" data-section-name="#section-block-script" <?php checked( true, (bool) iubenda()->options['cs']['skip_parsing'] ) ?>>
              <div class="px-0 py-1">
                <span class="p-0"><?php _e('Leave scripts untouched on the page if the user has already given consent', 'iubenda') ?></span>
                <div class="notice notice--info mt-2 mb-3 p-3 d-flex align-items-center text-xs">
                   <p><?php _e("Enable this option to improve performance <strong>only</strong> if your site does <strong>not</strong> use a cache system or a cache plugin and if you're <strong>not</strong> collecting per-category consent. If you're in doubt, keep this setting disabled", 'iubenda') ?></p>
                </div>
              </div>
          </label>
         
      </div>

      <h4><?php _e('Blocked domains', 'iubenda') ?></h4>
      <fieldset class="custom-scripts mb-3 p-0 tabs tabs--style2">
          <ul class="tabs__nav text-xs">
              <li data-target="tab-custom-scripts" data-group="custom-scripts" class="tabs__nav__item active"><?php _e('Custom scripts', 'iubenda') ?></li>
              <li data-target="tab-custom-iframes" data-group="custom-scripts" class="tabs__nav__item"><?php _e('Custom iframes', 'iubenda') ?></li>
          </ul>
          <div data-target="tab-custom-scripts" data-group="custom-scripts" class="tabs__target p-3 active">
              <section id="custom-script-field" class="custom-script-field hidden">
                  <input type="text" class="regular-text" name="iubenda_cookie_law_solution[custom_scripts][script][]" placeholder="<?php _e('Enter custom script', 'iubenda') ?>" disabled>
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
                          <input type="text" class="regular-text" name="iubenda_cookie_law_solution[custom_scripts][script][]" placeholder="<?php _e('Enter custom script', 'iubenda') ?>" value="<?php echo esc_attr( stripslashes($script) ); ?>">
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
                  <input type="text" class="regular-text" name="iubenda_cookie_law_solution[custom_iframes][iframe][]" placeholder="<?php _e('Enter custom iframe', 'iubenda') ?>" disabled>
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
  </section>

  <div class="pt-3">

  </div>
