<?php
namespace HTCf7Ext\Admin;

class Menu {

    /**
     * [init]
     */
    public function init() {
        add_action( 'admin_menu', [ $this, 'admin_menu' ], 220 );
    }

    /**
     * Register Menu
     *
     * @return void
     */
    public function admin_menu(){
        global $submenu;

        $slug        = 'contat-form-list';
        $capability  = 'manage_options';

        $hook = add_menu_page(
			esc_html__('Cf7 Extensions','cf7-extensions'),
			esc_html__('Cf7 Extensions','cf7-extensions'),
            $capability,
            $slug,
            [ $this, 'plugin_page' ],
			'dashicons-media-text',
			55
        );

        if ( current_user_can( $capability ) ) {
            $submenu[ $slug ][] = array( esc_html__( 'Forms', 'cf7-extensions' ), $capability, 'admin.php?page=' . $slug . '#/forms' );
            $submenu[ $slug ][] = array( esc_html__( 'Submissions', 'cf7-extensions' ), $capability, 'admin.php?page=' . $slug . '#/entries' );
            $submenu[ $slug ][] = array( esc_html__( 'Global Settings', 'cf7-extensions' ), $capability, 'admin.php?page=' . $slug . '#/settings' );
            $submenu[ $slug ][] = array( esc_html__( 'Extensions', 'cf7-extensions' ), $capability, 'admin.php?page=' . $slug . '#/extensions' );
        }

        htcf7ext_update_menu_badge();

        add_action( 'load-' . $hook, [ $this, 'init_hooks'] );
    }

    /**
     * Initialize our hooks for the admin page
     *
     * @return void
     */
    public function init_hooks() {
        add_action( 'admin_enqueue_scripts', [ $this, 'enqueue_scripts' ] );
    }

    /**
     * Load scripts and styles for the app
     *
     * @return void
     */
    public function enqueue_scripts() {
        wp_enqueue_style('htcf7extopt-sweetalert2');
        wp_enqueue_style( 'htcf7extopt-admin' );
        wp_enqueue_style( 'htcf7extopt-style' );
        wp_enqueue_script( 'htcf7extopt-admin' );

        $settings_opt = [
            "htcf7ext_opt" => [
                "conditional_mode" => htcf7ext_get_option('htcf7ext_opt', 'conditional_mode', 'normal'),
                "animation_enable" => htcf7ext_get_option('htcf7ext_opt', 'animation_enable', 'on'),
                "admimation_in_time" => htcf7ext_get_option('htcf7ext_opt', 'admimation_in_time', '250'),
                "admimation_out_time" => htcf7ext_get_option('htcf7ext_opt', 'admimation_out_time', '250'),

                "redirection_delay" => htcf7ext_get_option('htcf7ext_opt', 'redirection_delay', '200'),

                "ip_address_enable" => htcf7ext_get_option('htcf7ext_opt', 'ip_address_enable', 'on'),
                "reffer_link_enable" => htcf7ext_get_option('htcf7ext_opt', 'reffer_link_enable', 'on'),
            ],
            "htcf7ext_opt_extensions" => [
                "redirection_extension" => htcf7ext_get_module_option( 'htcf7ext_redirection_extension_module_settings', 'redirection_extension', 'redirection_enable', 'on' ),
                "conditional_field" => htcf7ext_get_module_option( 'htcf7ext_conditional_field_module_settings', 'conditional_field', 'conditional_field_enable', 'on' ),
                "column_extension" => htcf7ext_get_option('htcf7ext_opt_extensions', 'column_extension', 'off'),
                "mailchimp_extension" => htcf7ext_get_option('htcf7ext_opt_extensions', 'mailchimp_extension', 'on'),
                "range_extension" => htcf7ext_get_option('htcf7ext_opt_extensions', 'range_extension', 'off'),
                "popup_extension" => 'off',
                "repeater_field_extensions" => 'off',
                "unique_field_extensions" => 'off',
                "advance_telephone" => 'off',
                "drag_and_drop_upload" => 'off',
                "acceptance_field" => 'off',
            ]
        ];

        $option_localize_script = [
            'adminUrl'      => admin_url( '/' ),
            'ajaxUrl'       => admin_url( 'admin-ajax.php' ),
            'rootApiUrl'    => esc_url_raw( rest_url() ),
            'restNonce'     => wp_create_nonce( 'wp_rest' ),
            'verifynonce'   => wp_create_nonce( 'htcf7extopt_verifynonce' ),
            'tabs'          => Options_Field::instance()->get_settings_tabs(),
            'sections'      => Options_Field::instance()->get_settings_subtabs(),
            'settings'      => Options_Field::instance()->get_registered_settings(),
            'options'       => $settings_opt,
            'labels'        => [
                'pro' => esc_html__( 'Pro', 'cf7-extensions' ),
                'modal' => [
                    'title' => esc_html__( 'BUY PRO', 'cf7-extensions' ),
                    'buynow' => esc_html__( 'Buy Now', 'cf7-extensions' ),
                    'desc' => esc_html__( 'Our free version is great, but it doesn\'t have all our advanced features. The best way to unlock all of the features in our plugin is by purchasing the pro version.', 'cf7-extensions' )
                ],
                'saveButton' => [
                    'text'   => esc_html__( 'Save Settings', 'cf7-extensions' ),
                    'saving' => esc_html__( 'Saving...', 'cf7-extensions' ),
                    'saved'  => esc_html__( 'Data Saved', 'cf7-extensions' ),
                ],
                'enableAllButton' => [
                    'enable'   => esc_html__( 'Enable All', 'cf7-extensions' ),
                    'disable'  => esc_html__( 'Disable All', 'cf7-extensions' ),
                ],
                'resetButton' => [
                    'text'   => esc_html__( 'Reset All Settings', 'cf7-extensions' ),
                    'reseting'  => esc_html__( 'Resetting...', 'cf7-extensions' ),
                    'reseted'  => esc_html__( 'All Data Restored', 'cf7-extensions' ),
                    'alert' => [
                        'one'=>[
                            'title' => esc_html__( 'Are you sure?', 'cf7-extensions' ),
                            'text' => esc_html__( 'It will reset all the settings to default, and all the changes you made will be deleted.', 'cf7-extensions' ),
                            'confirm' => esc_html__( 'Yes', 'cf7-extensions' ),
                            'cancel' => esc_html__( 'No', 'cf7-extensions' ),
                        ],
                        'two'=>[
                            'title' => esc_html__( 'Reset!', 'cf7-extensions' ),
                            'text' => esc_html__( 'All settings has been reset successfully.', 'cf7-extensions' ),
                            'confirm' => esc_html__( 'OK', 'cf7-extensions' ),
                        ]
                    ],
                ]
            ]
        ];
        // update existing data to new conditional module settings default option
        $updated_conditional_options = [
            "conditional_field" =>  wp_json_encode([
                "conditional_field_enable" => "on",
                "conditional_mode"         => htcf7ext_get_option('htcf7ext_opt', 'conditional_mode','normal'),
                "animation_enable"         => htcf7ext_get_option('htcf7ext_opt', 'animation_enable','on'),
                "admimation_in_time"       => htcf7ext_get_option('htcf7ext_opt', 'admimation_in_time',250),
                "admimation_out_time"      => htcf7ext_get_option('htcf7ext_opt', 'admimation_out_time',250),
            ]),
        ];
        
        if ( empty( htcf7ext_get_module_option( 'htcf7ext_conditional_field_module_settings' ) ) ) {
            update_option( 'htcf7ext_conditional_field_module_settings' , $updated_conditional_options );
        }

        // update existing data to new redirection module settings default option
        $updated_redirection_options = [
            "redirection_extension" =>  wp_json_encode([
                "redirection_enable" => "on",
                "redirection_delay"  => htcf7ext_get_option('htcf7ext_opt', 'redirection_delay',200),
            ]),
        ];
        
        if ( empty( htcf7ext_get_module_option( 'htcf7ext_redirection_extension_module_settings' ) ) ) {
            update_option( 'htcf7ext_redirection_extension_module_settings' , $updated_redirection_options );
        }

        wp_localize_script( 'htcf7extopt-admin', 'htcf7extOptions', $option_localize_script );
    }

    /**
     * Render our admin page
     *
     * @return void
     */
    public function plugin_page() {
        $allowed_tags = wp_kses_allowed_html('post');
        $allowed_tags['style'] = [
            'type' => true,
        ];
        ob_start();
		include_once HTCF7EXTOPT_INCLUDES .'/templates/settings-page.php';
		echo wp_kses(ob_get_clean(), $allowed_tags);
    }

}
