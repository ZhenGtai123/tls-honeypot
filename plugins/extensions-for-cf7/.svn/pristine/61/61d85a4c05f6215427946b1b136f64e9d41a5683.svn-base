<?php
/**
 * Contact Form Database Inialiaze
 * @phpcs:disable WordPress.DB.PreparedSQL.InterpolatedNotPrepared, WordPress.DB.DirectDatabaseQuery.DirectQuery, WordPress.DB.DirectDatabaseQuery.NoCaching,
 */
class Extensions_Cf7 {

  /**
   * [$_instance]
   * @var null
  */
  private static $_instance = null;

  /**
   * [$instance_installer_class]
  */
  private $Cf7_installer;

  /**
   * [instance] Initializes a singleton instance
   * @return [Docus]
  */
  public static function instance($Cf7_installer) {
    if ( is_null( self::$_instance ) ) {
      self::$_instance = new self();
      self::$_instance->Cf7_installer = $Cf7_installer;
    }
    return self::$_instance;
  }

	function __construct(){
    if ( ! function_exists('is_plugin_active') ){ include_once( ABSPATH . 'wp-admin/includes/plugin.php' ); }
    add_action( 'init', [ $this, 'i18n'] );
    add_action( 'plugins_loaded', [ $this, 'init' ] );
    register_activation_hook(CF7_EXTENTIONS_PL_ROOT, [$this, 'activate']);
    add_action('in_admin_header', [$this, 'remove_admin_notice'], 1000);
    if(function_exists('is_plugin_active') && !is_plugin_active('contact-form-7/wp-contact-form-7.php')) {
      return;
    }
    add_action( 'wp_enqueue_scripts', [ $this, 'extcf7_enqueue_script' ] );
    add_action( 'activated_plugin', [ $this, 'plugin_redirection_page' ] ); 

    // Vue Settings panel
    require_once ( CF7_EXTENTIONS_PL_PATH . 'includes/class-ajax-actions.php' );
    require_once ( CF7_EXTENTIONS_PL_PATH . 'admin/settings-panel/settings-panel.php' );

    add_action('admin_init', [$this, 'show_diagnostic_notice']);
    add_action('admin_init', [$this, 'show_rating_notice']);
    add_action('admin_init', [$this, 'show_promo_notice']);
	}

  /**
   * Remove all Notices on admin pages.
   * @return void
   */
  function remove_admin_notice(){
      $current_screen = get_current_screen();
      $hide_screen = ['toplevel_page_contat-form-list', 'cf7-extensions_page_cf7-extensions-recommendations', 'update'];
      if(  in_array( $current_screen->id, $hide_screen) ){
          remove_all_actions('admin_notices');
          remove_all_actions('all_admin_notices');
      }
  }

  /**
   * [i18n] Load Text Domain
   * @return [void]
  */
  public function i18n() {
    load_plugin_textdomain( 'cf7-extensions',false, dirname( plugin_basename( CF7_EXTENTIONS_PL_ROOT ) ) . '/languages/' );
  }

  public function init() {
      // Contact Form 7
      if ( ! is_plugin_active( 'contact-form-7/wp-contact-form-7.php' ) ) {
        add_action('admin_notices', [ $this, 'admin_notic_missing_contact_form_7' ] );
        return ;
      }else{
        $extcf7_path = plugin_dir_path( dirname( CF7_EXTENTIONS_PL_ROOT ) ) . 'contact-form-7/wp-contact-form-7.php';
        $extcf7_data = get_plugin_data( $extcf7_path, false, false );

        if( 5.3 > $extcf7_data['Version'] ){
          add_action('admin_notices', [ $this, 'admin_notic_old_contact_form_7' ] );
          return;
        }
      }

    /**
     * Add plugin setting link to the plugin.
     */
    add_filter('plugin_action_links_' . CF7_EXTENTIONS_PL_BASE, [$this, 'plugins_setting_links']);

  	// Plugins Required File
  	$this->includes();

    $this->update_database();
  }

  /**
	 *include file
	*/
  public function includes() {
    require_once ( CF7_EXTENTIONS_PL_PATH . 'includes/helper-functions.php' );
    require_once ( CF7_EXTENTIONS_PL_PATH . 'includes/class.form-data-store.php' );


    if ( 'on' == htcf7ext_get_module_option( 'htcf7ext_conditional_field_module_settings','conditional_field','conditional_field_enable','on' ) ) {
      require_once ( CF7_EXTENTIONS_PL_PATH . 'admin/include/class.cf7-conditional.php' );
      require_once ( CF7_EXTENTIONS_PL_PATH . 'admin/include/class.cf7-condition-setup.php' );
    }

    if ( 'on' == htcf7ext_get_module_option( 'htcf7ext_redirection_extension_module_settings','redirection_extension','redirection_enable','on' ) ) {
      require_once ( CF7_EXTENTIONS_PL_PATH . 'admin/include/class.cf7-redirection.php' );
    }

    if ( 'on' == htcf7ext_get_option('htcf7ext_opt_extensions', 'mailchimp_extension', 'on') ) {
      require_once ( CF7_EXTENTIONS_PL_PATH . 'includes/class.mailchimp-subscribe.php' );
    }
    if( 'on' == htcf7ext_get_option('htcf7ext_opt_extensions', 'range_extension', 'off') ) {
      require_once ( CF7_EXTENTIONS_PL_PATH . 'admin/include/class.cf7-range-slider.php' );
    }
    if( 'on' == htcf7ext_get_option('htcf7ext_opt_extensions', 'column_extension', 'on') ) {
      require_once ( CF7_EXTENTIONS_PL_PATH . 'admin/include/class.cf7-column.php' );
    }
  
    if(is_admin()){
      require_once ( CF7_EXTENTIONS_PL_PATH . 'admin/include/class.cf7-metabox.php' );
      require_once ( CF7_EXTENTIONS_PL_PATH . 'admin/include/class.download-csv.php' );
      require_once ( CF7_EXTENTIONS_PL_PATH . 'admin/include/class.cf7-post-list.php' );
      if(isset($_SERVER['REQUEST_URI']) && strpos($_SERVER['REQUEST_URI'], 'contat-form-list')) {
        require_once ( CF7_EXTENTIONS_PL_PATH . 'admin/include/class.cf7-form-data-list.php' );
      }
      require_once ( CF7_EXTENTIONS_PL_PATH . 'admin/include/class.cf7-form-data-detail.php' );

      if ( 'on' == htcf7ext_get_option('htcf7ext_opt_extensions', 'mailchimp_extension', 'on') ) {
        require_once ( CF7_EXTENTIONS_PL_PATH . 'admin/include/class.cf7-mailchimp-map.php' );
      }
      require_once ( CF7_EXTENTIONS_PL_PATH . 'admin/include/Recommended_Plugins.php' );
      require_once ( CF7_EXTENTIONS_PL_PATH . 'admin/include/class.cf7-extensions-recomendation.php' );
      require_once ( CF7_EXTENTIONS_PL_PATH . 'admin/include/class-diagnostic-data.php' );
      require_once ( CF7_EXTENTIONS_PL_PATH . 'admin/include/class-notice-manager.php' );
      require_once ( CF7_EXTENTIONS_PL_PATH . 'admin/include/class.notices.php' );
      require_once ( CF7_EXTENTIONS_PL_PATH . 'admin/admin-init.php' );
    }
  }

  function update_database() {
    if(!get_option('extcf7_db_table_alter_status', false)) {
      global $wpdb;
      $table_name = $wpdb->prefix .'extcf7_db';
      $column_exists = $wpdb->get_results($wpdb->prepare(
          "SHOW COLUMNS FROM $table_name LIKE %s",
          'status'
      ));
      if(empty($column_exists)) {
          $wpdb->query("ALTER TABLE $table_name ADD COLUMN status ENUM('read', 'unread') DEFAULT 'unread' NOT NULL" ); //phpcs:ignore WordPress.DB.DirectDatabaseQuery.SchemaChange
          $wpdb->query("UPDATE $table_name SET status = 'read'" );
      }
      update_option('extcf7_db_table_alter_status', true);
    }
  }

  /**
  * Plugins setting links

  * @param  array plugin default action links
  * @return array plugin action link
  */
  function plugins_setting_links($links) {
      $link = sprintf(
          '<a href="%1$s">%2$s</a>',
          admin_url('admin.php?page=contat-form-list#/forms'),
          esc_html__( 'Settings', 'cf7-extensions' )
      );
      array_unshift($links, $link);
      return $links; 
  }

  /**
   *enqueue script
  */
  public function extcf7_enqueue_script(){

    wp_enqueue_style( 'cf7-extension-front-style', CF7_EXTENTIONS_PL_URL.'assets/css/cf7-extension-front-style.css', [], CF7_EXTENTIONS_PL_VERSION);

    if('on' == htcf7ext_get_option('htcf7ext_opt_extensions', 'range_extension', 'off')){
      wp_enqueue_style('jquery-ui-style', '//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css');
      wp_enqueue_script('jquery-ui-slider');
      wp_enqueue_script('touch-punch', '//cdnjs.cloudflare.com/ajax/libs/jqueryui-touch-punch/0.2.3/jquery.ui.touch-punch.min.js', ['jquery-ui-slider'], CF7_EXTENTIONS_PL_VERSION, true);
      wp_enqueue_script( 'extcf7-range-slider', CF7_EXTENTIONS_PL_URL.'assets/js/range-slider.js', array('jquery-ui-slider'), CF7_EXTENTIONS_PL_VERSION, true);
    }

    if( 'on' == htcf7ext_get_module_option( 'htcf7ext_conditional_field_module_settings','conditional_field','conditional_field_enable','on') ) {
      wp_enqueue_script( 'extcf7-conditional-field-script', CF7_EXTENTIONS_PL_URL.'assets/js/conditional-field.js', array('jquery'), CF7_EXTENTIONS_PL_VERSION, true);

      $localize_conditional_data = [
        'animitation_status' => htcf7ext_get_module_option( 'htcf7ext_conditional_field_module_settings','conditional_field','animation_enable','on'),
        'animitation_in_time' => htcf7ext_get_module_option( 'htcf7ext_conditional_field_module_settings','conditional_field','admimation_in_time',250),
        'animitation_out_time' => htcf7ext_get_module_option( 'htcf7ext_conditional_field_module_settings','conditional_field','admimation_out_time',250),
      ];
      if ( class_exists( '\Elementor\Plugin' ) && ( \Elementor\Plugin::$instance->editor->is_edit_mode() || \Elementor\Plugin::$instance->preview->is_preview_mode() ) ) {
        $localize_conditional_data['elementor_editor_mode'] = 'true';
      } else {
        $localize_conditional_data['elementor_editor_mode'] =  'false';
      }

      wp_localize_script( 'extcf7-conditional-field-script', 'extcf7_conditional_settings', $localize_conditional_data);

    }

    if( 'on' == htcf7ext_get_module_option( 'htcf7ext_redirection_extension_module_settings','redirection_extension','redirection_enable','on' ) ) {

      wp_enqueue_script( 'extcf7-redirect-script', CF7_EXTENTIONS_PL_URL.'assets/js/redirect.js', array('jquery'), CF7_EXTENTIONS_PL_VERSION, true);
      $localize_redirection_data = ['redirection_delay' => htcf7ext_get_module_option( 'htcf7ext_redirection_extension_module_settings','redirection_extension','redirection_delay', 200 )];

      wp_localize_script( 'extcf7-redirect-script', 'extcf7_redirection_settings', $localize_redirection_data );
    }

    wp_enqueue_script( 'extcf7-frontend-js', CF7_EXTENTIONS_PL_URL.'assets/js/frontend.js', [], CF7_EXTENTIONS_PL_VERSION, true);
  }

  /**
  * [admin_notic_missing_Contact Form 7] Admin Notice For missing Contact Form 7
  * @return [void]
  */
  public function admin_notic_missing_contact_form_7(){
    $contact_form_7 = 'contact-form-7/wp-contact-form-7.php';
    if( $this->is_plugins_active( $contact_form_7 ) ) {
      if( ! current_user_can( 'activate_plugins' ) ) {
        return;
      }
      $activation_url = wp_nonce_url( 'plugins.php?action=activate&amp;plugin=' . $contact_form_7 . '&amp;plugin_status=all&amp;paged=1&amp;s', 'activate-plugin_' . $contact_form_7 );
      /*
      * translators: %1$s: strong start tag
      * translators: %2$s: strong end tag
      */
      $message = sprintf( esc_html__( '%1$sExtensions For CF7 %2$s requires %1$s"Contact Form 7"%2$s plugin to be active. Please activate Contact Form 7 to continue.', 'cf7-extensions' ), '<strong>', '</strong>');
      $button_text = esc_html__( 'Activate Contact Form 7', 'cf7-extensions' );
    }else{
      if( ! current_user_can( 'activate_plugins' ) ) {
        return;
      }
      $activation_url = wp_nonce_url( self_admin_url( 'update.php?action=install-plugin&plugin=contact-form-7' ), 'install-plugin_contact-form-7' );
      /*
      * translators: %1$s: strong start tag
      * translators: %2$s: strong end tag
      */
      $message = sprintf( esc_html__( '%1$sExtensions For CF7.%2$s requires %1$s"Contact Form 7"%2$s plugin to be installed and activated. Please install Contact Form 7 to continue.', 'cf7-extensions' ), '<strong>', '</strong>' );
      $button_text = esc_html__( 'Install Contact Form 7', 'cf7-extensions' );
    }
    $button = '<p><a href="' . $activation_url . '" class="button-primary">' . $button_text . '</a></p>';
    printf( '<div class="error"><p>%1$s</p>%2$s</div>', wp_kses_post( $message ), wp_kses_post($button) );
  }

  /**
  * [admin_notic_old_Contact Form 7] Admin Notice For old Contact Form 7
  * @return [void]
  */
  public function admin_notic_old_contact_form_7(){
    echo '<div class="error"><p><strong>';
      echo esc_html__('Error: Contact Form 7 version is too old. Extensions For CF7 is compatible from version 5.3 and above. Please update Contact Form 7.','cf7-extensions');
    echo '</strong></p></div>';
  }

  /**
   * [is_plugins_active] Check Plugin is Installed or not
   * @param  [string]  $pl_file_path plugin file path
   * @return boolean  true|false
  */
  public function is_plugins_active( $pl_file_path = NULL ){
      $installed_plugins_list = get_plugins();
      return isset( $installed_plugins_list[$pl_file_path] );
  }

  /**
   *activation action
  */
  public function activate(){
    $this->Cf7_installer->run();
    $cf7_upload_dir    = wp_upload_dir();
    $cf7_dirname       = $cf7_upload_dir['basedir'].'/extcf7_uploads';
    if ( ! file_exists( $cf7_dirname ) ) {
      wp_mkdir_p( $cf7_dirname );
    }

    if( is_plugin_active('extension-for-cf7-pro/cf7-extensions-pro.php') ){
      deactivate_plugins('extension-for-cf7-pro/cf7-extensions-pro.php');
    }

  }

  /**
   *activation action
  */

  public function plugin_redirection_page($plugin){
    if( is_plugin_active('contact-form-7/wp-contact-form-7.php') ){
      if(plugin_basename(CF7_EXTENTIONS_PL_ROOT) == $plugin){
        wp_redirect( admin_url("admin.php?page=contat-form-list#/forms") );
        die();
      }
    }
  }
      
  

  
  function show_diagnostic_notice() {
      $notice_instance = \Extensions_Cf7_Diagnostic_Data::get_instance();
      ob_start();
      $notice_instance->show_notices();
      $message = ob_get_clean();
      if (! empty( $message ) ) {
          Extensions_Cf7_Notice::set_notice(
              [
                  'id'          => 'diagnostic-data',
                  'type'        => 'success',
                  'dismissible' => false,
                  'message_type' => 'html',
                  'message'     => $message,
                  'display_after'  => ( 7 * DAY_IN_SECONDS ),
                  'expire_time' => 0,
                  'close_by'    => 'transient'
              ]
          );
      }
  }
    
  function show_rating_notice() {
      $message = '<div class="extcf7-review-notice-wrap">
          <div class="extcf7-rating-notice-logo">
              <img src="' . esc_url(CF7_EXTENTIONS_PL_URL . 'assets/images/logo.jpg') . '" alt="Extensions For CF7 (Contact form 7 Database, Conditional Fields and Redirection)" style="max-width:110px"/>
          </div>
          <div class="extcf7-review-notice-content">
              <h3>'.esc_html__('Thank you for choosing Extensions For CF7 to extends Contact Form 7 functionalities.','cf7-extensions').'</h3>
              <p>'.esc_html__('Would you mind doing us a huge favor by providing your feedback on WordPress? Your support helps us spread the word and greatly boosts our motivation.','cf7-extensions').'</p>
              <div class="extcf7-review-notice-action">
                  <a href="https://wordpress.org/support/plugin/extensions-for-cf7/reviews/?filter=5#new-post" class="extcf7-review-notice button-primary" target="_blank">'.esc_html__('Ok, you deserve it!','cf7-extensions').'</a>
                  <a href="#" class="extcf7-notice-close extcf7-review-notice"><span class="dashicons dashicons-calendar"></span>'.esc_html__('Maybe Later','cf7-extensions').'</a>
                  <a href="#" data-already-did="yes" class="extcf7-notice-close extcf7-review-notice"><span class="dashicons dashicons-smiley"></span>'.esc_html__('I already did','cf7-extensions').'</a>
              </div>
          </div>
      </div>';
      if (! empty( $message ) ) {
          Extensions_Cf7_Notice::set_notice(
              [
                  'id'          => 'ratting',
                  'type'        => 'info',
                  'dismissible' => true,
                  'message_type' => 'html',
                  'message'     => $message,
                  'display_after'  => ( 14 * DAY_IN_SECONDS ),
                  'close_by'    => 'transient'
              ]
          );
      }
  }

  function show_promo_notice() {
      $noticeManager = Extensions_Cf7_Notice_Manager::instance();
      $notices = $noticeManager->get_notices_info();
      if(!empty($notices)) {
          $notices = array_map(function($notice) {
              $notice["display_after"] = false;
              $notice["expire_time"] = WEEK_IN_SECONDS;
              return $notice;
          }, $notices);
          foreach ($notices as $notice) {
              if(empty($notice['disable'])) {
                Extensions_Cf7_Notice::set_notice($notice);
              }
          }
      }
  }
}

$gpr_installer = new Extensions_Cf7_Installer();
Extensions_Cf7::instance($gpr_installer);