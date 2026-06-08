<?php require_once IUBENDA_PLUGIN_PATH . 'views/partials/header.php'; ?>
<div class="main-box">

    <?php require_once IUBENDA_PLUGIN_PATH . 'views/partials/siteInfo.php'; ?>

    <?php require_once IUBENDA_PLUGIN_PATH . 'views/partials/breadcrumb.php'; ?>
    <form class="ajax-form-to-options">
        <input hidden name="iubenda_section_name" value="iubenda_consent_solution">
        <input hidden name="iubenda_section_key" value="cons">
        <input hidden name="action" value="ajax_save_options">
        <input hidden name="_redirect" value="<?php echo esc_url(add_query_arg(['view' => 'products-page'], iubenda()->base_url)) ?>">
        <div class="p-4 p-lg-5 text-gray">

        <p><?php _e('Activate <strong>Consent Solution</strong> on our website in your iubenda dashboard and paste the <strong>API key</strong> here to integrate it in your website.', 'iubenda') ?></p>
        <div class="d-flex align-items-center">
            <div class="steps flex-shrink mr-3">1</div>
            <p class="text-bold"> <?php _e('Activate & Configure Consent Solution by', 'iubenda') ?>
                <a target="_blank" href="<?php echo iubenda()->settings->links['flow_page']; ?>" class="link-underline text-gray-lighter"> <?php _e('clicking here', 'iubenda') ?></a>
            </p>
        </div>
        <div class="d-flex align-items-center">
            <div class="steps flex-shrink mr-3">2</div>
            <p class="text-bold"> <?php _e('Paste your public API key here', 'iubenda') ?>
            </p>
        </div>

        <div class="subOptions">
            <div class="paste-api-form" tabindex="0">
                <input class="paste-api-input" id="public_api_key" name="iubenda_consent_solution[public_api_key]" type="text" placeholder="<?php _e('Your iubenda Javascript library public API key', 'iubenda'); ?>" value="<?php echo iub_array_get(iubenda()->options['cons'], 'public_api_key') ? iub_array_get(iubenda()->options['cons'], 'public_api_key') : false ?>" required>
                <button type="submit" id="public_api_button" class="btn btn-xs btn-green-secondary">
                    <span class="button__text"><?php _e('Confirm API', 'iubenda') ?></span>
                </button>
            </div>
        </div>

        <div class="text-right mt-2">
            <a target="_blank" href="<?php echo iubenda()->settings->links['how_generate_cons']; ?>" class="link link-helper"><span class="tooltip-icon mr-2">?</span><?php _e('Where can I find this code?', 'iubenda') ?></a>
        </div>

        <div id="public-api-key-div" class="<?php echo iub_array_get(iubenda()->options['cons'], 'public_api_key') ?: 'hidden'; ?>">
            <div class="d-flex align-items-center">
                <div class="steps flex-shrink mr-3">3</div>
                <p class="text-bold">
                    <?php _e('Add forms', 'iubenda') ?>
                </p>
            </div>
            <div class="ml-3 pl-4 mb-5">
                <div id="auto-detect-parent-div">
                    <section id="auto-detect-forms">
                        <?php require_once IUBENDA_PLUGIN_PATH . 'views/partials/auto_detect_forms.php'; ?>
                    </section>
                </div>
                <a tabindex="-1" href="<?php echo esc_url( add_query_arg( array( 'view' => 'cons-configuration', 'action' => 'autodetect' ), iubenda()->base_url ) ) ?>" class="btn btn-xs btn-gray-outline mt-2 auto-detect-forms"><?php _e('Auto-detect forms', 'iubenda') ?></a>
            </div>
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
