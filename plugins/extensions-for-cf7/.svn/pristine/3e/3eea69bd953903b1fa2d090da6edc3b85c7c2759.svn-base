<?php
/**
 * @phpcs:disable WordPress.DB.PreparedSQL.InterpolatedNotPrepared, WordPress.DB.DirectDatabaseQuery.DirectQuery, WordPress.DB.DirectDatabaseQuery.NoCaching
 */
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

		global $wpdb;
		$entry_id = !empty($_REQUEST['entry_id']) ? sanitize_text_field($_REQUEST['entry_id']) : 0;
		$table_name = $wpdb->prefix.'extcf7_db';
	
		$result = $wpdb->query( $wpdb->prepare(
			"UPDATE $table_name SET status = %s WHERE id = %d",
			'read',
			$entry_id
		));
	
		if( $result ){
			$total = $wpdb->get_var($wpdb->prepare("SELECT COUNT(*) FROM $table_name WHERE status = 'unread' "));
			wp_send_json_success(['html' => $html, 'total'=> $total, 'message' => __('Unread Message', 'cf7-extensions')]);
		} else {
			wp_send_json_success(['html' => $html]);
		}
    }
}

Ajax_Actions::instance();