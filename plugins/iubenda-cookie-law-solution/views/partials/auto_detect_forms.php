<?php
$cons_page_configuration = get_option('iubenda_consent_solution');

if ($cons_page_configuration && iub_array_get($cons_page_configuration, 'public_api_key')){

    $form_id = ! empty( $_GET['form_id'] ) ? absint( $_GET['form_id'] ) : 0;
    $form = ! empty( $form_id ) ? iubenda()->forms->get_form( $form_id ) : false;

    $supported_forms = iubenda()->forms->sources;

    // list screen
    if ( ! class_exists( 'WP_List_Table' ) )
        include_once( ABSPATH . 'wp-admin/includes/class-wp-list-table.php' );

    include_once( IUBENDA_PLUGIN_PATH . '/includes/forms-list-table.php' );

    $list_table = new iubenda_List_Table_Forms();

    echo '
                <div id="iubenda-consent-forms">';
    $list_table->views();
    $list_table->prepare_items();
    $list_table->display();

    echo '
                </div>';
}else{
    ?>
    <p><?php _e('This section lists the forms available for field mapping. The plugin currently supports & detects: WordPress Comment, Contact Form 7, WooCommerce Checkout and WP Forms.', 'iubenda') ?></p>

    <?php

}