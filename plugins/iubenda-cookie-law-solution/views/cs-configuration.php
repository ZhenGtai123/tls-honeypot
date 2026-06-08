<?php require_once IUBENDA_PLUGIN_PATH . 'views/partials/header.php'; ?>
<div class="main-box">
    <?php require_once IUBENDA_PLUGIN_PATH . 'views/partials/siteInfo.php'; ?>
    <?php require_once IUBENDA_PLUGIN_PATH . 'views/partials/breadcrumb.php'; ?>
    <form class="ajax-form-to-options">
        <input hidden name="iubenda_section_name" value="iubenda_cookie_law_solution">
        <input hidden name="iubenda_section_key" value="cs">
        <input hidden name="action" value="ajax_save_options">
        <input hidden name="_redirect" value="<?php echo esc_url(add_query_arg(['view' => 'products-page'], iubenda()->base_url)) ?>">
        <div class="p-4 p-lg-5">
            <?php require_once IUBENDA_PLUGIN_PATH . 'views/partials/csGeneralSettings.php'; ?>
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
<?php require_once IUBENDA_PLUGIN_PATH . '/views/partials/modals/modal_ops_embed_invalid.php'; ?>
<?php require_once IUBENDA_PLUGIN_PATH . 'views/partials/footer.php'; ?>
