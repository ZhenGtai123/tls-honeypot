<?php
/**
 * @phpcs:disable WordPress.Security.NonceVerification.Recommended, WordPress.Security.NonceVerification.Missing
 */
if( ! defined( 'ABSPATH' ) ) exit(); // Exit if accessed directly

/**
 * HT Cf7 Admin
*/
class Extensions_Cf7_Admin_Setting
{
    private $extcf7_layout_instance;

	function __construct($extcf7_layout_instance)
	{	
        $this->extcf7_layout_instance = $extcf7_layout_instance;
        add_action( 'admin_enqueue_scripts', array($this, 'extcf7_admin_assets'), 11 );
	}

    function extcf7_admin_assets($hook){
        if("toplevel_page_contat-form-list" === $hook || 'toplevel_page_wpcf7' === $hook || "ht-cf7-extension_page_cf7-conditional-settings" === $hook || 'ht-cf7-extension_page_general-settings' === $hook || 'ht-cf7-extension_page_cf7-pro-features' === $hook){
            wp_enqueue_style( 'ht-cf7-admin-style', CF7_EXTENTIONS_PL_URL.'admin/assets/css/admin-style.css','',CF7_EXTENTIONS_PL_VERSION);

            wp_enqueue_script( 'wp-jquery-ui-dialog');
            wp_enqueue_script( 'ht-cf7-admin-script', CF7_EXTENTIONS_PL_URL.'admin/assets/js/admin.js', array('jquery'), CF7_EXTENTIONS_PL_VERSION, true);

            $localize_animation_data = [
                'animitation_status' => htcf7ext_get_module_option( 'htcf7ext_conditional_field_module_settings','conditional_field','animation_enable','on' )
            ];
            wp_localize_script( 'ht-cf7-admin-script', 'extcf7_animation_info', $localize_animation_data);

            $localize_vars = array();
            $localize_vars['ajax_url']  = admin_url( 'admin-ajax.php' );
            $localize_vars['nonce']	    = wp_create_nonce('htcf7ext_nonce');
            wp_localize_script( 'ht-cf7-admin-script', 'htcf7ext_params', $localize_vars );
        }

        if('toplevel_page_wpcf7' === $hook ){

            wp_enqueue_script( 'ht-cf7-metabox-script', CF7_EXTENTIONS_PL_URL.'admin/assets/js/metabox.js', array('jquery'), CF7_EXTENTIONS_PL_VERSION, true);

            if ( 'on' == htcf7ext_get_module_option( 'htcf7ext_conditional_field_module_settings','conditional_field','conditional_field_enable','on' ) ) {
                wp_enqueue_script( 'ht-cf7-conditional-script', CF7_EXTENTIONS_PL_URL.'admin/assets/js/conditional.js', array('jquery'), CF7_EXTENTIONS_PL_VERSION, true);

                $localize_condition_mode_data = [
                    'conditional_mode' => htcf7ext_get_module_option( 'htcf7ext_conditional_field_module_settings','conditional_field','conditional_mode','normal'),
                ];
                wp_localize_script( 'ht-cf7-conditional-script', 'extcf7_conditional_mode', $localize_condition_mode_data);
                $ajaxurl = "var ajaxurl='".admin_url( 'admin-ajax.php')."'";
                wp_add_inline_script('ht-cf7-conditional-script',$ajaxurl);
            }



            if( 'on' == htcf7ext_get_module_option( 'htcf7ext_redirection_extension_module_settings','redirection_extension','redirection_enable','on' ) ) {
                wp_enqueue_script( 'ht-cf7-redirection-script', CF7_EXTENTIONS_PL_URL.'admin/assets/js/redirection.js', array('jquery'), CF7_EXTENTIONS_PL_VERSION, true);
            }
           
            if ( 'on' == htcf7ext_get_option('htcf7ext_opt_extensions', 'mailchimp_extension', 'on') ) {
                wp_enqueue_script( 'ht-cf7-mailchimp-map-script', CF7_EXTENTIONS_PL_URL.'admin/assets/js/mailchimp-map.js', array('jquery'), CF7_EXTENTIONS_PL_VERSION, true);

                $extcf7_mailchimp_map_data = [
                    'nonce' => wp_create_nonce('extcf7_mailchimp_map_active_nonce')
                ];
                wp_localize_script( 'ht-cf7-mailchimp-map-script', 'extcf7_mailchimp_map_data', $extcf7_mailchimp_map_data);
            }
            if ( 'on' == htcf7ext_get_option('htcf7ext_opt_extensions', 'column_extension', 'off') ) {
                wp_enqueue_script( 'ht-cf7-column-script', CF7_EXTENTIONS_PL_URL.'admin/assets/js/column.js', array('jquery'), CF7_EXTENTIONS_PL_VERSION, true);
            }

        }

        if("toplevel_page_contat-form-list" === $hook){
            wp_enqueue_style('jquery-datepicker-style', CF7_EXTENTIONS_PL_URL.'admin/assets/css/jquery-ui.css', [], CF7_EXTENTIONS_PL_VERSION);
            wp_enqueue_script('jquery-ui-datepicker');
            wp_enqueue_script('jquery-ui-dialog');

            wp_dequeue_script('monsterinsights-admin-common-script');
            wp_dequeue_script('wur_settings_cute_alert_script');
        }

    }

	function extcf7_form_data_page() {
       $layout_instance = $this->extcf7_layout_instance->get_layout_instance();
       if($layout_instance instanceof Extensions_Cf7_Form_Datalist_Render){
            echo wp_kses_post($layout_instance->cf7_layout_render());
       }
    }

    function extcf7_condition_page(){
        echo '<h2>'.esc_html__( 'Conditional Field Options','cf7-extensions' ).'</h2>';
        echo '<form action="options.php" method="post">';
        settings_fields( 'conditional-settings-group' );
        do_settings_sections( 'cf7-conditional-settings' );
        require_once( CF7_EXTENTIONS_PL_PATH.'admin/template/conditional-setting.php');
        submit_button();
        echo '</form>';
    }	

    function extcf7_redirection_page(){
        echo '<h2>'.esc_html__( 'Redirection Setting','cf7-extensions' ).'</h2>';
        echo '<form action="options.php" method="post">';
        settings_fields( 'redirection-setting' );
        do_settings_sections( 'cf7-redirection-settings' );
        $redirection_delay = htcf7ext_get_option('htcf7ext_opt', 'redirection_delay', '200');
        $link = admin_url().'admin.php?page=wpcf7';
        ?>
            <table class="form-table" role="presentation">
                <tbody>
                    <tr>
                        <th scope="row"><?php echo esc_html__('Redirection Delay','cf7-extensions');?></th>
                        <td>
                            <input type="text" class="regular-text" name="redirection_delay" value="<?php echo esc_attr($redirection_delay); ?>">
                            <p><?php echo esc_html__('Input a positive integer value for the dalay of redirection. The values in milliseconds(Default:200)','cf7-extensions'); ?></p>
                        </td>
                    </tr>
                </tbody>
            </table>
            <div class="cf7-editor-link">
                <a href="<?php echo esc_url($link); ?>"><?php echo esc_html__('Go To Contact Form 7 Editor','cf7-extensions'); ?></a>
            </div>
        <?php
        submit_button();
        echo '</form>';
    }   

    function extcf7_general_settings(){
        echo '<h2>'.esc_html__( 'Settings','cf7-extensions' ).'</h2>';
        echo '<form action="options.php" class="extcf7_pro-from-wraper" method="post">';
        settings_fields( 'general-settings-group' );
        do_settings_sections( 'cf7-general-settings' );
        require_once( CF7_EXTENTIONS_PL_PATH.'admin/template/general-options-layout.php');
        submit_button();
        echo '</form>';
    }

    function extcf7_extensions_page(){
        echo '<h2>'.esc_html__( 'Extensions','cf7-extensions' ).'</h2>';
        require_once( CF7_EXTENTIONS_PL_PATH.'admin/template/pro-feature-list.php');
    }
}

$extcf7_layout_instance = new Extensions_Cf7_Layout_Instance();
new Extensions_Cf7_Admin_Setting($extcf7_layout_instance);

/**
 * HT Cf7 Form DB layout instance
*/
class Extensions_Cf7_Layout_Instance
{
    
    function get_layout_instance(){
        $cf7_id  = empty($_GET['cf7_id']) ? 0 : absint($_GET['cf7_id']);
        $cf7em_id = empty($_GET['cf7em_id']) ? 0 : absint($_GET['cf7em_id']);

        if ( !empty($cf7_id) && empty($cf7em_id) ) {
            return new Extensions_Cf7_Page();
        }else if(!empty($cf7_id) && !empty($cf7em_id)){
            return new Extensions_Cf7_Detail_Page();
        }else{
            return new Extensions_Cf7_Post_List();
        }
    }
}

