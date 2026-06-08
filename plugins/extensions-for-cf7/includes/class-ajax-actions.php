<?php
namespace HTCf7Ext;

/**
 * Contact Form Database Inialiaze
*/
class Ajax_Actions {
	/**
	 * [$_instance]
	 *
	 * @var null
	 */
	private static $_instance = null;

	/**
	 * [instance] Initializes a singleton instance
	 *
	 * @return [Easy_Google_Analytics]
	 */
	public static function instance() {
		if ( is_null( self::$_instance ) ) {
			self::$_instance = new self();
		}
		return self::$_instance;
	}

	function __construct(){
        add_action( 'wp_ajax_htcf7ext_view_formdata', array($this, 'htcf7ext_view_formdata_cb') );
    }

    public function htcf7ext_view_formdata_cb(){
        // Verify nonce
        check_ajax_referer( 'htcf7ext_nonce', 'nonce' );
        $html = '';

        ob_start();
        include CF7_EXTENTIONS_PL_PATH . 'admin/include/tmpl-form-data.php';
        $html = ob_get_clean();

        wp_send_json_success($html);
    }
}

Ajax_Actions::instance();