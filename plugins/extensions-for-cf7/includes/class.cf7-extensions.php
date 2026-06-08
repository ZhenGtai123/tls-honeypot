<?php
/**
 * Contact Form Database Inialiaze
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
    add_action( 'wp_enqueue_scripts', [ $this, 'extcf7_enqueue_script' ] );
    register_activation_hook(CF7_EXTENTIONS_PL_ROOT, [$this, 'activate']);
    add_action( 'activated_plugin', [ $this, 'plugin_redirection_page' ] ); 

    // Vue Settings panel
    require_once ( CF7_EXTENTIONS_PL_PATH . 'includes/class-ajax-actions.php' );
    require_once ( CF7_EXTENTIONS_PL_PATH . 'admin/settings-panel/settings-panel.php' );
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
  }

  /**
	 *include file
	*/
  public function includes() {
    require_once ( CF7_EXTENTIONS_PL_PATH . 'includes/helper-functions.php' );
    require_once ( CF7_EXTENTIONS_PL_PATH . 'includes/class.form-data-store.php' );
    require_once ( CF7_EXTENTIONS_PL_PATH . 'admin/include/class.cf7-conditional.php' );
    require_once ( CF7_EXTENTIONS_PL_PATH . 'admin/include/class.cf7-condition-setup.php' );
    require_once ( CF7_EXTENTIONS_PL_PATH . 'admin/include/class.cf7-redirection.php' );
    require_once ( CF7_EXTENTIONS_PL_PATH . 'includes/class.mailchimp-subscribe.php' );
    if(is_admin()){
      require_once ( CF7_EXTENTIONS_PL_PATH . 'admin/include/class.download-csv.php' );
      require_once ( CF7_EXTENTIONS_PL_PATH . 'admin/include/class.cf7-post-list.php' );
      require_once ( CF7_EXTENTIONS_PL_PATH . 'admin/include/class.cf7-form-data-list.php' );
      require_once ( CF7_EXTENTIONS_PL_PATH . 'admin/include/class.cf7-form-data-detail.php' );
      require_once ( CF7_EXTENTIONS_PL_PATH . 'admin/include/class.cf7-mailchimp-map.php' );
      require_once ( CF7_EXTENTIONS_PL_PATH . 'admin/include/Recommended_Plugins.php' );
      require_once ( CF7_EXTENTIONS_PL_PATH . 'admin/include/class.cf7-extensions-recomendation.php' );
      require_once ( CF7_EXTENTIONS_PL_PATH . 'admin/include/class-diagnostic-data.php' );
      require_once ( CF7_EXTENTIONS_PL_PATH . 'admin/admin-init.php' );
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
          __( 'Settings', 'cf7-extensions' )
      );
      array_unshift($links, $link);
      return $links; 
  }

  /**
   *enqueue script
  */
  public function extcf7_enqueue_script(){
    wp_enqueue_script( 'extcf7-conditional-field-script', CF7_EXTENTIONS_PL_URL.'assets/js/conditional-field.js', array('jquery'), CF7_EXTENTIONS_PL_VERSION, true);
    wp_enqueue_script( 'extcf7-redirect-script', CF7_EXTENTIONS_PL_URL.'assets/js/redirect.js', array('jquery'),CF7_EXTENTIONS_PL_VERSION, true);
    $localize_conditional_data = [
      'animitation_status' => htcf7ext_get_option('htcf7ext_opt', 'animation_enable', 'on'),
      'animitation_in_time' => htcf7ext_get_option('htcf7ext_opt', 'admimation_in_time', '250'),
      'animitation_out_time' => htcf7ext_get_option('htcf7ext_opt', 'admimation_out_time', '250'),
    ];

    if ( class_exists( '\Elementor\Plugin' ) && ( \Elementor\Plugin::$instance->editor->is_edit_mode() || \Elementor\Plugin::$instance->preview->is_preview_mode() ) ) {
      $localize_conditional_data['elementor_editor_mode'] = 'true';
    } else {
      $localize_conditional_data['elementor_editor_mode'] =  'false';
    }

    $localize_redirection_data = ['redirection_delay' => htcf7ext_get_option('htcf7ext_opt', 'redirection_delay', '200')];
    wp_localize_script( 'extcf7-conditional-field-script', 'extcf7_conditional_settings', $localize_conditional_data);
    wp_localize_script( 'extcf7-redirect-script', 'extcf7_redirection_settings', $localize_redirection_data);
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
      $message = sprintf( __( '%1$sExtensions For CF7 %2$s requires %1$s"Contact Form 7"%2$s plugin to be active. Please activate Contact Form 7 to continue.', 'cf7-extensions' ), '<strong>', '</strong>');
      $button_text = __( 'Activate Contact Form 7', 'cf7-extensions' );
    }else{
      if( ! current_user_can( 'activate_plugins' ) ) {
        return;
      }
      $activation_url = wp_nonce_url( self_admin_url( 'update.php?action=install-plugin&plugin=contact-form-7' ), 'install-plugin_contact-form-7' );
      $message = sprintf( __( '%1$sExtensions For CF7.%2$s requires %1$s"Contact Form 7"%2$s plugin to be installed and activated. Please install Contact Form 7 to continue.', 'cf7-extensions' ), '<strong>', '</strong>' );
      $button_text = __( 'Install Contact Form 7', 'cf7-extensions' );
    }
    $button = '<p><a href="' . $activation_url . '" class="button-primary">' . $button_text . '</a></p>';
    printf( '<div class="error"><p>%1$s</p>%2$s</div>', __( $message ), $button );
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
      
}

$gpr_installer = new Extensions_Cf7_Installer();
Extensions_Cf7::instance($gpr_installer);