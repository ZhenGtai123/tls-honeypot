<?php require_once IUBENDA_PLUGIN_PATH . '/views/partials/header.php'; ?>
<div class="main-box">
    <?php require_once IUBENDA_PLUGIN_PATH . '/views/partials/siteInfo.php'; ?>
    <?php require_once IUBENDA_PLUGIN_PATH . 'views/partials/breadcrumb.php'; ?>
    <form class="ajax-form-to-options">
        <input hidden name="iubenda_section_name" value="iubenda_cookie_law_solution">
        <input hidden name="iubenda_section_key" value="plugin-settings">
        <input hidden name="action" value="ajax_save_options">
        <input hidden name="_redirect" value="<?php echo esc_url(add_query_arg(['view' => 'products-page'], iubenda()->base_url)) ?>">
        <div class="p-3 m-3">
            <label class="checkbox-regular">
                <input type="checkbox" class="mr-2" name="iubenda_plugin_settings[ctype]" value="1" <?php checked( true, (bool) iubenda()->options['cs']['ctype'] ) ?>>
                <span><?php _e('Restrict the plugin to run only for requests that have "Content-type: text / html" (recommended)', 'iubenda') ?></span>
            </label>
            <label class="checkbox-regular">
                <input type="checkbox" class="mr-2" name="iubenda_plugin_settings[output_feed]" value="1" <?php checked( true, (bool) iubenda()->options['cs']['output_feed'] ) ?>>
                <span><?php _e('Do not run the plugin inside the RSS feed (recommended)', 'iubenda') ?></span>
            </label>
            <label class="checkbox-regular">
                <input type="checkbox" class="mr-2" name="iubenda_plugin_settings[output_post]" value="1" <?php checked( true, (bool) iubenda()->options['cs']['output_post'] ) ?>>
                <span><?php _e('Do not run the plugin on POST requests (recommended)', 'iubenda') ?></span>
            </label>
            <label class="checkbox-regular">
                <input type="checkbox" class="mr-2" name="iubenda_plugin_settings[deactivation]" value="1" <?php checked( true, (bool) iubenda()->options['cs']['deactivation'] ) ?>>
                <span><?php _e('Delete all plugin data upon deactivation', 'iubenda') ?></span>
            </label>
            <div class="mt-5">
                <h4><?php _e('Menu position', 'iubenda') ?></h4>
                <div class="mb-2 d-flex align-items-center flex-wrap">
                    <label class="radio-regular mr-3">
                        <input type="radio" name="iubenda_plugin_settings[menu_position]" value="topmenu" class="mr-2" <?php checked( 'topmenu', iubenda()->options['cs']['menu_position'] ) ?>>
                        <span><?php _e('Top menu', 'iubenda') ?></span>
                    </label>
                    <label class="mr-4 radio-regular text-xs">
                        <input type="radio" name="iubenda_plugin_settings[menu_position]" value="submenu" class="mr-2" <?php checked( 'submenu', iubenda()->options['cs']['menu_position'] ) ?>>
                        <span><?php _e('Submenu', 'iubenda') ?></span>
                    </label>
                </div>
                <p class="description"><?php _e('Select whether to display iubenda in a top admin menu or the Settings submenu.', 'iubenda') ?></p>
            </div>
        </div>
        <hr>
        <div class="p-4 d-flex justify-content-end">
            <input class="btn btn-gray-lighter btn-sm mr-2" type="button" value="<?php _e('Cancel', 'iubenda') ?>" onclick="window.location.href = '<?php echo esc_url(add_query_arg(array('view' => 'products-page'), iubenda()->base_url)) ?>'"/>
            <button type="submit" class="btn btn-green-primary btn-sm" value="Save" name="save">
                <span class="button__text"><?php _e('Save settings', 'iubenda') ?></span>
            </button>
        </div>
    </form>
</div>
<?php require_once IUBENDA_PLUGIN_PATH . 'views/partials/footer.php'; ?>
