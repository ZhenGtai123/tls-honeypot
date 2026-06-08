<?php
namespace HTCf7Ext\Admin;

class Options_Field {

    /**
     * [$_instance]
     * @var null
     */
    private static $_instance = null;

    /**
     * [instance] Initializes a singleton instance
     * @return [Admin]
     */
    public static function instance() {
        if ( is_null( self::$_instance ) ) {
            self::$_instance = new self();
        }
        return self::$_instance;
    }

    public function get_settings_tabs(){
        $tabs = array(
            'forms' => [
                'id'    => 'forms_tab',
                'title' => esc_html__( 'Forms', 'cf7-extensions' ),
                'icon'  => 'dashicons dashicons-feedback',
                'content' => [
                    'header' => false,
                    'footer' => false,
                    'title' => __( 'Free VS Pro', 'cf7-extensions' ),
                    'desc'  => __( 'Freely use these elements to create your site. You can enable which you are not using, and, all associated assets will be disable to improve your site loading speed.', 'cf7-extensions' ),
                    'extraClass' => 'azadd',
                ],
            ],
            'entries' => array(
                'id'    => 'submissions_tab',
                'title' =>  esc_html__( 'Submissions', 'cf7-extensions' ),
                'icon'  => 'dashicons dashicons-list-view',
                'content' => [
                    'header' => false,
                    'footer' => false,
                    'savebtn' => false,
                    'enableall' => false,
                ],
            ),
            'settings' => array(
                'id'    => 'htcf7ext_opt',
                'title' => esc_html__( 'Global Settings', 'cf7-extensions' ),
                'icon'  => 'dashicons dashicons-admin-generic',
                'content' => [
                    'header' => false,
                    'enableall' => false,
                    'title' => __( 'Global Settings', 'cf7-extensions' ),
                    'desc'  => __( 'Set the fields value to use these features', 'cf7-extensions' ),
                ],
            ),
            'extensions' => array(
                'id'    => 'htcf7ext_opt_extensions',
                'title' => esc_html__( 'Extensions', 'cf7-extensions' ),
                'icon'  => 'dashicons dashicons-superhero',
                'content' => [
                    'header' => false,
                    'footer' => false,
                    'column' => 3,
                    'enableall' => false,
                    'title' => __( 'Enable/Disable Extensions', 'cf7-extensions' ),
                    'desc'  => __( 'Set the fields value to use these features', 'cf7-extensions' ),
                ],
            ),
        );

        return apply_filters( 'htcf7ext_admin_fields_sections', $tabs );

    }

    public function get_settings_subtabs(){

        $subtabs = array();

        return apply_filters( 'htcf7ext_admin_fields_sub_sections', $subtabs );
    }

    public function get_registered_settings(){
        $settings = array(

            // Forms tab
            'forms_tab' => array(
                array(
                    'id'   => 'htcf7ext_forms',
                    'type' => 'html',
                    'html' => $this->render_forms(),
                    'class' => 'htcf7ext_forms'
                ),
                
            ),

            // Submissions tab
            'submissions_tab' => array(
                
                array(
                    'id'   => 'htcf7ext_submissions',
                    'type' => 'html',
                    'html' => $this->render_submissions(),
                    'class' => 'htcf7ext_form_entries'
                ),
                
            ),

            // Global Settings tab
            'htcf7ext_opt' => array(
                array(
                    'id'  => 'ip_address_enable',
                    'name'  => __( 'IP Address', 'cf7-extensions' ),
                    'type'  => 'switcher',
                    'default'=>'on',
                    'label_on' => __( 'On', 'cf7-extensions' ),
                    'label_off' => __( 'Off', 'cf7-extensions' ),
                    'desc' => __('Enable this option to make the sender\'s IP Address visible.', 'cf7-extensions')
                ),
                array(
                    'id'  => 'reffer_link_enable',
                    'name'  => __( 'Referer Link', 'cf7-extensions' ),
                    'type'  => 'switcher',
                    'default'=>'on',
                    'label_on' => __( 'On', 'cf7-extensions' ),
                    'label_off' => __( 'Off', 'cf7-extensions' ),
                    'desc' => __('Enable this option to make the referrer link visible.', 'cf7-extensions')
                ),
                array(
                    'id'  => 'conditional_mode',
                    'name'  => __( 'Conditional UI Mode', 'cf7-extensions' ),
                    'type'  => 'select',
                    'default'=>'normal',
                    'options' => array(
                        'normal' => __('Default', 'cf7-extensions'),
                        'text'   => __('Text Mode', 'cf7-extensions'),
                    ),
                    'label_on' => __( 'On', 'cf7-extensions' ),
                    'label_off' => __( 'Off', 'cf7-extensions' ),
                    'desc' => __('Set the Conditional Ui mode.', 'cf7-extensions')
                ),
                array(
                    'id'  => 'redirection_delay',
                    'name'  => __( 'Redirection Delay', 'cf7-extensions' ),
                    'type'  => 'number',
                    'default'=>'250',
                    'label_on' => __( 'On', 'cf7-extensions' ),
                    'label_off' => __( 'Off', 'cf7-extensions' ),
                    'desc' => __('Input a positive integer value for the dalay of redirection. The values in milliseconds. Default:200', 'cf7-extensions')
                ),
                array(
                    'id'  => 'animation_enable',
                    'name'  => __( 'Animation', 'cf7-extensions' ),
                    'type'  => 'switcher',
                    'default'=>'on',
                    'label_on' => __( 'On', 'cf7-extensions' ),
                    'label_off' => __( 'Off', 'cf7-extensions' ),
                    'desc' => __('Enable Conditional Field Animation to show and hide field.', 'cf7-extensions')
                ),
                array(
                    'id'  => 'admimation_in_time',
                    'name'  => __( 'Animation In Time', 'cf7-extensions' ),
                    'type'  => 'number',
                    'default'=>'250',
                    'label_on' => __( 'On', 'cf7-extensions' ),
                    'label_off' => __( 'Off', 'cf7-extensions' ),
                    'desc' => __('Input a positive integer value for animation in time. The values in milliseconds and it will be applied for each field. Default: 250', 'cf7-extensions')
                ),
                array(
                    'id'  => 'admimation_out_time',
                    'name'  => __( 'Animation Out Time', 'cf7-extensions' ),
                    'type'  => 'number',
                    'default'=>'250',
                    'label_on' => __( 'On', 'cf7-extensions' ),
                    'label_off' => __( 'Off', 'cf7-extensions' ),
                    'desc' => __('Input a positive integer value for animation in time. The values in milliseconds and it will be applied for each field. Default: 250', 'cf7-extensions')
                ),
            ),

            'htcf7ext_opt_extensions' => array(
                array(
                    'id'  => 'popup_extension',
                    'name'  => __( 'Popup Form Response', 'cf7-extensions' ),
                    'type'  => 'element',
                    'default'=>'off',
                    'label_on' => __( 'On', 'cf7-extensions' ),
                    'label_off' => __( 'Off', 'cf7-extensions' ),
                    'is_pro' => true,
                ),
                array(
                    'id'  => 'repeater_field_extensions',
                    'name'  => __( 'Repeater Field', 'cf7-extensions' ),
                    'type'  => 'element',
                    'default'=>'off',
                    'label_on' => __( 'On', 'cf7-extensions' ),
                    'label_off' => __( 'Off', 'cf7-extensions' ),
                    'is_pro' => true,
                ),
                array(
                    'id'  => 'unique_field_extensions',
                    'name'  => __( 'Already Submitted', 'cf7-extensions' ),
                    'type'  => 'element',
                    'default'=>'off',
                    'label_on' => __( 'On', 'cf7-extensions' ),
                    'label_off' => __( 'Off', 'cf7-extensions' ),
                    'is_pro' => true,
                ),
                array(
                    'id'  => 'advance_telephone',
                    'name'  => __( 'Advanced Telephone', 'cf7-extensions' ),
                    'type'  => 'element',
                    'default'=>'off',
                    'label_on' => __( 'On', 'cf7-extensions' ),
                    'label_off' => __( 'Off', 'cf7-extensions' ),
                    'is_pro' => true,
                ),
                array(
                    'id'  => 'drag_and_drop_upload',
                    'name'  => __( 'Drag and Drop File Upload', 'cf7-extensions' ),
                    'type'  => 'element',
                    'default'=>'off',
                    'label_on' => __( 'On', 'cf7-extensions' ),
                    'label_off' => __( 'Off', 'cf7-extensions' ),
                    'is_pro' => true,
                ),
                array(
                    'id'  => 'acceptance_field',
                    'name'  => __( 'Acceptance Field', 'cf7-extensions' ),
                    'type'  => 'element',
                    'default'=>'off',
                    'label_on' => __( 'On', 'cf7-extensions' ),
                    'label_off' => __( 'Off', 'cf7-extensions' ),
                    'is_pro' => true,
                ),
            ),

        );

        return apply_filters( 'htcf7ext_admin_fields', $settings );

    }

    public function render_forms(){
        ob_start();
        include_once HTCF7EXTOPT_INCLUDES .'/templates/dashboard-forms.php';
        return ob_get_clean();
    }

    public function render_submissions(){
        ob_start();
        include_once HTCF7EXTOPT_INCLUDES .'/templates/dashboard-submissions.php';
        return ob_get_clean();
    }

}