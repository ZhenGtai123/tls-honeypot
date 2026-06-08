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
                    'title' => esc_html__( 'Free VS Pro', 'cf7-extensions' ),
                    'desc'  => esc_html__( 'Freely use these elements to create your site. You can enable which you are not using, and, all associated assets will be disable to improve your site loading speed.', 'cf7-extensions' )
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
                    'title' => esc_html__( 'Global Settings', 'cf7-extensions' ),
                    'desc'  => esc_html__( 'Set the fields value to use these features', 'cf7-extensions' ),
                ],
            ),
            'extensions' => array(
                'id'    => 'htcf7ext_opt_extensions',
                'title' => esc_html__( 'Extensions', 'cf7-extensions' ),
                'icon'  => 'dashicons dashicons-superhero',
                'content' => [
                    'header' => false,
                    'footer' => true,
                    'column' => 3,
                    'enableall' => false,
                    'title' => esc_html__( 'Enable/Disable Extensions', 'cf7-extensions' ),
                    'desc'  => esc_html__( 'Set the fields value to use these features', 'cf7-extensions' ),
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
                    'name'  => esc_html__( 'IP Address', 'cf7-extensions' ),
                    'type'  => 'switcher',
                    'default'=>'on',
                    'label_on' => esc_html__( 'On', 'cf7-extensions' ),
                    'label_off' => esc_html__( 'Off', 'cf7-extensions' ),
                    'desc' => esc_html__('Enable this option to make the sender\'s IP Address visible.', 'cf7-extensions')
                ),
                array(
                    'id'  => 'reffer_link_enable',
                    'name'  => esc_html__( 'Referer Link', 'cf7-extensions' ),
                    'type'  => 'switcher',
                    'default'=>'on',
                    'label_on' => esc_html__( 'On', 'cf7-extensions' ),
                    'label_off' => esc_html__( 'Off', 'cf7-extensions' ),
                    'desc' => esc_html__('Enable this option to make the referrer link visible.', 'cf7-extensions')
                ),

            ),

            'htcf7ext_opt_extensions' => array(
                array(
                    'id'  => 'redirection_extension',
                    'name'  => esc_html__( 'Redirection', 'cf7-extensions' ),
                    'type'  => 'module',
                    'section'  => 'htcf7ext_redirection_extension_module_settings',
                    'setting_fields' => array(
                        array(
                            'id'  => 'redirection_enable',
                            'name' => esc_html__( 'Enable / Disable' ),
                            'desc'  => esc_html__( 'You can enable / disable redirection from here.', 'cf7-extensions' ),
                            'type'  => 'checkbox',
                            'default' => 'on',
                            'class' => 'htcf7ext-action-field-left',
                            'label_on' => esc_html__( 'On', 'cf7-extensions' ),
                            'label_off' => esc_html__( 'Off', 'cf7-extensions' ),
                        ),
                        array(
                            'id'  => 'redirection_delay',
                            'name'  => esc_html__( 'Redirection Delay', 'cf7-extensions' ),
                            'type'  => 'number',
                            'default'=>'250',
                            'label_on' => esc_html__( 'On', 'cf7-extensions' ),
                            'label_off' => esc_html__( 'Off', 'cf7-extensions' ),
                            'desc' => esc_html__('Input a positive integer value for the dalay of redirection. The values in milliseconds. Default:200', 'cf7-extensions'),
                            'condition' => [['condition_key' => 'redirection_enable', 'condition_value' => 'on']]
                        ),
                    )
                ),


                array(
                    'id'  => 'mailchimp_extension',
                    'name'  => esc_html__( 'MailChimp', 'cf7-extensions' ),
                    'type'  => 'element',
                    'default'=>'on',
                    'label_on' => esc_html__( 'On', 'cf7-extensions' ),
                    'label_off' => esc_html__( 'Off', 'cf7-extensions' ),
                ),
                array(
                    'id'  => 'conditional_field',
                    'name'  => esc_html__( 'Conditional Field', 'cf7-extensions' ),
                    'type'  => 'module',
                    'section'  => 'htcf7ext_conditional_field_module_settings',
                    'setting_fields' => array(
                        array(
                            'id'  => 'conditional_field_enable',
                            'name' => esc_html__( 'Enable / Disable' ),
                            'desc'  => esc_html__( 'You can enable / disable Connditional Field from here.', 'cf7-extensions' ),
                            'type'  => 'checkbox',
                            'default' => 'on',
                            'class' => 'htcf7ext-action-field-left',
                            'label_on' => esc_html__( 'On', 'cf7-extensions' ),
                            'label_off' => esc_html__( 'Off', 'cf7-extensions' ),
                        ),
                        array(
                            'id'  => 'conditional_mode',
                            'name'  => esc_html__( 'Conditional UI Mode', 'cf7-extensions' ),
                            'type'  => 'select',
                            'default'=>'normal',
                            'options' => array(
                                'normal' => esc_html__('Default', 'cf7-extensions'),
                                'text'   => esc_html__('Text Mode', 'cf7-extensions'),
                            ),
                            'label_on' => esc_html__( 'On', 'cf7-extensions' ),
                            'label_off' => esc_html__( 'Off', 'cf7-extensions' ),
                            'desc' => esc_html__('Set the Conditional Ui mode.', 'cf7-extensions'),
                            'condition' => [['condition_key' => 'conditional_field_enable', 'condition_value' => 'on']]
                        ),
                        array(
                            'id'  => 'animation_enable',
                            'name'  => esc_html__( 'Animation', 'cf7-extensions' ),
                            'type'  => 'checkbox',
                            'default'=>'on',
                            'label_on' => esc_html__( 'On', 'cf7-extensions' ),
                            'label_off' => esc_html__( 'Off', 'cf7-extensions' ),
                            'desc' => esc_html__('Enable Conditional Field Animation to show and hide field.', 'cf7-extensions'),
                            'condition' => [['condition_key' => 'conditional_field_enable', 'condition_value' => 'on']]
                        ),
                        array(
                            'id'  => 'admimation_in_time',
                            'name'  => esc_html__( 'Animation In Time', 'cf7-extensions' ),
                            'type'  => 'number',
                            'default'=>'250',
                            'label_on' => esc_html__( 'On', 'cf7-extensions' ),
                            'label_off' => esc_html__( 'Off', 'cf7-extensions' ),
                            'desc' => esc_html__('Input a positive integer value for animation in time. The values in milliseconds and it will be applied for each field. Default: 250', 'cf7-extensions'),
                            'condition' => [
                                ['condition_key' => 'conditional_field_enable', 'condition_value' => 'on'],
                                ['condition_key' => 'animation_enable', 'condition_value' => 'on']
                            ]
                        ),
                        array(
                            'id'  => 'admimation_out_time',
                            'name'  => esc_html__( 'Animation Out Time', 'cf7-extensions' ),
                            'type'  => 'number',
                            'default'=>'250',
                            'label_on' => esc_html__( 'On', 'cf7-extensions' ),
                            'label_off' => esc_html__( 'Off', 'cf7-extensions' ),
                            'desc' => esc_html__('Input a positive integer value for animation in time. The values in milliseconds and it will be applied for each field. Default: 250', 'cf7-extensions'),
                            'condition' => [
                                ['condition_key' => 'conditional_field_enable', 'condition_value' => 'on'],
                                ['condition_key' => 'animation_enable', 'condition_value' => 'on']
                            ]
                        ),

                    )
                ),
                array(
                    'id'  => 'range_extension',
                    'name'  => __( 'Range Slider', 'cf7-extensions-pro' ),
                    'type'  => 'element',
                    'default'=>'off',
                    'label_on' => __( 'On', 'cf7-extensions-pro' ),
                    'label_off' => __( 'Off', 'cf7-extensions-pro' ),
                ),
                array(
                    'id'  => 'column_extension',
                    'name'  => __( 'Column Field', 'cf7-extensions' ),
                    'type'  => 'element',
                    'default'=>'off',
                    'label_on' => __( 'On', 'cf7-extensions' ),
                    'label_off' => __( 'Off', 'cf7-extensions' ),
                ),
                array(
                    'id'  => 'form_styler',
                    'name'  => __( 'Form Styler', 'cf7-extensions-pro' ),
                    'type'  => 'module',
                    'default'=>'off',
                    'label_on' => __( 'On', 'cf7-extensions-pro' ),
                    'label_off' => __( 'Off', 'cf7-extensions-pro' ),
                    'section'  => 'htcf7ext_form_styler_module_settings',
                    'is_pro' => true,
                ),
                array(
                    'id'  => 'ip_geo_extension',
                    'name'  => __( 'Autocomplete IP Geo Fields (Country, City, State, Zip)', 'cf7-extensions' ),
                    'type'  => 'element',
                    'default'=>'off',
                    'label_on' => __( 'On', 'cf7-extensions' ),
                    'label_off' => __( 'Off', 'cf7-extensions' ),
                    'is_pro' => true,
                ),
                array(
                    'id'  => 'popup_extension',
                    'name'  => esc_html__( 'Popup Form Response', 'cf7-extensions' ),
                    'type'  => 'element',
                    'default'=>'off',
                    'label_on' => esc_html__( 'On', 'cf7-extensions' ),
                    'label_off' => esc_html__( 'Off', 'cf7-extensions' ),
                    'is_pro' => true,
                ),
                array(
                    'id'  => 'repeater_field_extensions',
                    'name'  => esc_html__( 'Repeater Field', 'cf7-extensions' ),
                    'type'  => 'element',
                    'default'=>'off',
                    'label_on' => esc_html__( 'On', 'cf7-extensions' ),
                    'label_off' => esc_html__( 'Off', 'cf7-extensions' ),
                    'is_pro' => true,
                ),
                array(
                    'id'  => 'unique_field_extensions',
                    'name'  => esc_html__( 'Already Submitted', 'cf7-extensions' ),
                    'type'  => 'element',
                    'default'=>'off',
                    'label_on' => esc_html__( 'On', 'cf7-extensions' ),
                    'label_off' => esc_html__( 'Off', 'cf7-extensions' ),
                    'is_pro' => true,
                ),
                array(
                    'id'  => 'advance_telephone',
                    'name'  => esc_html__( 'Advanced Telephone', 'cf7-extensions' ),
                    'type'  => 'element',
                    'default'=>'off',
                    'label_on' => esc_html__( 'On', 'cf7-extensions' ),
                    'label_off' => esc_html__( 'Off', 'cf7-extensions' ),
                    'is_pro' => true,
                ),
                array(
                    'id'  => 'drag_and_drop_upload',
                    'name'  => esc_html__( 'Drag and Drop File Upload', 'cf7-extensions' ),
                    'type'  => 'element',
                    'default'=>'off',
                    'label_on' => esc_html__( 'On', 'cf7-extensions' ),
                    'label_off' => esc_html__( 'Off', 'cf7-extensions' ),
                    'is_pro' => true,
                ),
                array(
                    'id'  => 'acceptance_field',
                    'name'  => esc_html__( 'Acceptance Field', 'cf7-extensions' ),
                    'type'  => 'element',
                    'default'=>'off',
                    'label_on' => esc_html__( 'On', 'cf7-extensions' ),
                    'label_off' => esc_html__( 'Off', 'cf7-extensions' ),
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