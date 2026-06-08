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
			__('HT Cf7 Extension','cf7-extensions'),
			__('HT Cf7 Extension','cf7-extensions'),
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
                'pro' => __( 'Pro', 'cf7-extensions' ),
                'modal' => [
                    'title' => __( 'BUY PRO', 'cf7-extensions' ),
                    'buynow' => __( 'Buy Now', 'cf7-extensions' ),
                    'desc' => __( 'Our free version is great, but it doesn\'t have all our advanced features. The best way to unlock all of the features in our plugin is by purchasing the pro version.', 'cf7-extensions' )
                ],
                'saveButton' => [
                    'text'   => __( 'Save Settings', 'cf7-extensions' ),
                    'saving' => __( 'Saving...', 'cf7-extensions' ),
                    'saved'  => __( 'Data Saved', 'cf7-extensions' ),
                ],
                'enableAllButton' => [
                    'enable'   => __( 'Enable All', 'cf7-extensions' ),
                    'disable'  => __( 'Disable All', 'cf7-extensions' ),
                ],
                'resetButton' => [
                    'text'   => __( 'Reset All Settings', 'cf7-extensions' ),
                    'reseting'  => __( 'Resetting...', 'cf7-extensions' ),
                    'reseted'  => __( 'All Data Restored', 'cf7-extensions' ),
                    'alert' => [
                        'one'=>[
                            'title' => __( 'Are you sure?', 'cf7-extensions' ),
                            'text' => __( 'It will reset all the settings to default, and all the changes you made will be deleted.', 'cf7-extensions' ),
                            'confirm' => __( 'Yes', 'cf7-extensions' ),
                            'cancel' => __( 'No', 'cf7-extensions' ),
                        ],
                        'two'=>[
                            'title' => __( 'Reset!', 'cf7-extensions' ),
                            'text' => __( 'All settings has been reset successfully.', 'cf7-extensions' ),
                            'confirm' => __( 'OK', 'cf7-extensions' ),
                        ]
                    ],
                ]
            ]
        ];
        wp_localize_script( 'htcf7extopt-admin', 'htcf7extOptions', $option_localize_script );
    }

    /**
     * Render our admin page
     *
     * @return void
     */
    public function plugin_page() {
        ob_start();
		include_once HTCF7EXTOPT_INCLUDES .'/templates/settings-page.php';
		echo ob_get_clean();
    }

}
