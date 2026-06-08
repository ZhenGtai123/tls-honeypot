<?php require_once IUBENDA_PLUGIN_PATH . '/views/partials/header.php'; ?>
<form class="ajax-form">
    <input hidden name="action" value="integrate_setup">
    <input hidden name="_redirect" value="<?php echo esc_url(add_query_arg(['view' => 'products-page'], iubenda()->base_url)) ?>">
    <input hidden name="iubenda_cookie_law_solution[configuration_type]" value="simplified">
<div class="main-box">
    <?php require_once IUBENDA_PLUGIN_PATH . '/views/partials/siteInfo.php'; ?>

    <div class="p-3 m-3">
        <?php if(iubenda()->settings->print_notices()): ?>
            <div class="p-3 m-3">
                <?php iubenda()->settings->print_notices() ?>
            </div>
        <?php endif; ?>

        <div class="radio-toggle">
            <div class="switch">
                <input type="checkbox" name="cookie_law" id="toggleAddCookieBanner" class="section-checkbox-control" data-section-name="#section-add-cookie-banner" checked/>
                <label for="toggleAddCookieBanner"></label>
            </div>
            <span><?php _e('Add a cookie banner', 'iubenda') ?></span>
        </div>
        <section id="section-add-cookie-banner">
            <?php require_once IUBENDA_PLUGIN_PATH . '/views/partials/csSimplifiedConfiguration.php'; ?>

        <div class="my-5">
            <label class="checkbox-regular">
                <input type="checkbox" class="mr-2 section-checkbox-control" name="iubenda_cookie_law_solution[amp_support]" value="1" checked data-section-name="#amp_support"/>
                <span><?php _e('Enable Google AMP support', 'iubenda') ?> <a target="_blank" href="<?php echo iubenda()->settings->links["enable_amp_support"]; ?>" class="ml-1 tooltip-icon">?</a></span>
            </label>
            <section id="amp_support" class="subOptions my-2">
                <h4><?php _e('Select the iubenda AMP configuration file location.', 'iubenda') ?></h4>
                <div class="mb-2 d-flex flex-wrap align-items-center">
                    <label class="radio-regular mr-4 mb-3">
                        <input type="radio" name="iubenda_cookie_law_solution[amp_source]" value="local" class="mr-2 section-radio-control" data-section-name="#auto_generated_conf_file" data-section-group=".amp_configuration_file" checked>
                        <span><?php _e('Auto-generated configuration file', 'iubenda') ?></span>
                    </label>
                    <label class="mr-4 mb-3 radio-regular text-xs">
                        <input type="radio" name="iubenda_cookie_law_solution[amp_source]" value="remote" class="mr-2 section-radio-control" data-section-name="#custom_conf_file" data-section-group=".amp_configuration_file">
                        <span><?php _e('Custom configuration file', 'iubenda') ?></span>
                    </label>
                </div>

                <section id="auto_generated_conf_file" class="text-xs text-gray amp_configuration_file">
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
                        $languages = (iubenda()->multilang && !empty(iubenda()->languages)) ? iubenda()->languages : ['default' => __('Default language', 'iubenda')];
                        foreach ($languages as $lang_id => $lang_name) {
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
        </div>

        <div class="my-5">
            <label class="checkbox-regular">
                <input type="checkbox" name="iubenda_cookie_law_solution[parse]" value="1" class="mr-2 section-checkbox-control" data-section-name="#iub_parser_engine_container" checked>
                <span><?php _e('Automatically block scripts detected by the plugin', 'iubenda') ?> <a target="_blank" href="<?php echo iubenda()->settings->links['automatic_block_scripts']; ?>" class="ml-1 tooltip-icon">?</a></span>
            </label>
            <section id="iub_parser_engine_container" class="subOptions">
                <h4><?php _e("Select Parsing Engine", 'iubenda') ?></h4>
                <div class="mb-3 d-flex flex-wrap align-items-center">
                    <label class="radio-regular mr-4 mb-3">
                        <input type="radio" name="iubenda_cookie_law_solution[parser_engine]" value="new" class="mr-2 section-radio-control" checked>
                        <span><?php _e('Primary', 'iubenda') ?></span>
                    </label>
                    <label class="mr-4 mb-3 radio-regular text-xs">
                        <input type="radio" name="iubenda_cookie_law_solution[parser_engine]" value="default" class="mr-2 section-radio-control">
                        <span><?php _e('Secondary', 'iubenda') ?></span>
                    </label>
                </div>
                <div class="mb-2 d-flex flex-wrap align-items-center">
                    <label class="checkbox-regular">
                        <input type="checkbox" name="iubenda_cookie_law_solution[skip_parsing]" value="1" class="mr-2 section-checkbox-control" data-section-name="#section-block-script">
                        <div class="px-0 py-1">
                            <span class="p-0"><?php _e('Leave scripts untouched on the page if the user has already given consent', 'iubenda') ?></span>
                            <div class="notice notice--info mt-2 mb-3 p-3 d-flex align-items-center text-xs">
                               <p><?php _e("Enable this option to improve performance <strong>only</strong> if your site does <strong>not</strong> use a cache system or a cache plugin and if you're <strong>not</strong> collecting per-category consent. If you're in doubt, keep this setting disabled", 'iubenda') ?></p>
                            </div>
                        </div>
                    </label>
                </div>
            </section>
        </div>
        </section>

        <div class="radio-toggle">
            <div class="switch">
                <input type="checkbox" name="privacy_policy" id="toggleAddPrivacyButton" class="section-checkbox-control" data-section-name="#section-privacy-policy-button" checked/>

                <label for="toggleAddPrivacyButton"></label>
            </div>
            <span><?php _e('Add the privacy policy button', 'iubenda') ?></span>
        </div>
        <section id="section-privacy-policy-button">
            <?php require_once IUBENDA_PLUGIN_PATH . '/views/partials/buttonStyle.php'; ?>
            <?php require_once IUBENDA_PLUGIN_PATH . '/views/partials/buttonPosition.php'; ?>
        </section>

    </div>

    <?php require_once IUBENDA_PLUGIN_PATH . '/views/partials/integrateFooter.php'; ?>

</div>
</form>
<?php require_once IUBENDA_PLUGIN_PATH . '/views/partials/footer.php'; ?>
