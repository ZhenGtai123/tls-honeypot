<?php
// exit if accessed directly
if ( ! defined( 'ABSPATH' ) )
	exit;

/**
 * iubenda_Settings class.
 *
 * @class Post_Views_Counter_Settings
 */
class iubenda_Settings {
    const IUB_QG_Response = 'iubenda_quick_generator_response';
    const IUB_NOTIFICATIONS = 'iubenda_notifications';
	public $tabs = [];
	public $action = '';
	public $links = [];
	public $notice_types = ['error', 'success', 'notice'];
	public $subject_fields = [];
    public $quick_generator = [];
    public $services = [];


	public function __construct() {
	    if(iub_array_get($_GET, 'page') == 'iubenda'){
            add_action('admin_head', array( $this, 'iubdena_hide_notices_wp' ));
        }

		// actions
		add_action( 'after_setup_theme', array( $this, 'load_defaults' ) );
		add_action( 'admin_init', array( $this, 'update_plugin' ), 9 );
		add_action( 'admin_menu', array( $this, 'admin_menu_options' ) );
        add_action( 'admin_enqueue_scripts', array( $this, 'admin_enqueue_scripts' ) );
        add_action( 'admin_print_styles', array( $this, 'admin_print_styles' ) );
        add_action( 'admin_init', array( $this, 'process_actions' ), 20 );
        add_action( 'admin_init', array( $this, 'maybe_show_notice' ) );
        add_action( 'wp_ajax_iubenda_dismiss_notice', array( $this, 'dismiss_notice' ) );
        add_action( 'wp_ajax_iubenda_dismiss_notification_alert', array( $this,
            'dismiss_notification_alert'
        ) );

        add_action( 'wp_ajax_update_options', array($this, 'update_options'));

        add_action( 'wp_ajax_quick_generator_api', array(new QuickGeneratorService(), 'quick_generator_api'));
        add_action( 'wp_ajax_integrate_setup', array(new QuickGeneratorService(), 'integrate_setup'));
        add_action( 'wp_ajax_cs_configuration', array(new QuickGeneratorService(), 'cs_configuration')); //todo - not in the right place
        add_action( 'wp_ajax_pp_configuration', array(new QuickGeneratorService(), 'pp_configuration')); //todo - not in the right place
        add_action( 'wp_ajax_tc_configuration', array(new QuickGeneratorService(), 'tc_configuration')); //todo - not in the right place
        add_action( 'wp_ajax_cons_configuration', array(new QuickGeneratorService(), 'cons_configuration')); //todo - not in the right place
        add_action( 'wp_ajax_toggle_services', array($this, 'toggle_services'));
        add_action( 'wp_ajax_save_public_api_key', array(new QuickGeneratorService(), 'save_public_api_key')); //todo - not in the right place
        add_action( 'wp_ajax_auto_detect_forms', array(new QuickGeneratorService(), 'auto_detect_forms')); //todo - not in the right place

        add_action( 'wp_ajax_ajax_save_options', array(new QuickGeneratorService(), 'ajax_save_options'));

        add_action('wp_ajax_radar_percentage_reload', array(new RadarService(), 'ask_radar_to_send_request')); //todo - not in the right place

        // Getting main div in frontpage with updated data
        add_action( 'wp_ajax_frontpage_main_box', [$this, 'get_frontpage_main_box']);

        register_setting( 'iubenda_consent_solution_forms', 'status' );

        register_setting( 'iubenda_consent_solution', 'iubenda_consent_forms' );
        add_shortcode( 'iub-tc-button', array( new QuickGeneratorService(), 'tc_button_shortcode' ) );
        add_shortcode( 'iub-pp-button', array( new QuickGeneratorService(), 'pp_button_shortcode' ) );

	}

	/**
	 * Load default settings.
	 */
	public function load_defaults() {
        $this->services = $this->services_option();

        $this->subject_fields = array(
			'id' => __( 'string', 'iubenda' ),
			'email' => __( 'string', 'iubenda' ),
			'first_name' => __( 'string', 'iubenda' ),
			'last_name' => __( 'string', 'iubenda' ),
			'full_name' => __( 'string', 'iubenda' ),
			// 'verified' => __( 'boolean', 'iubenda' ),
		);

		$this->legal_notices = array(
			'privacy_policy',
			'cookie_policy',
			'term'
		);

		$this->tabs = array(
			'cs'	 => array(
				'name'	 => __( 'Cookie Solution', 'iubenda' ),
				'key'	 => 'iubenda_cookie_law_solution',
				'submit' => 'save_iubenda_options',
				'reset'	 => 'reset_iubenda_options'
			),
			'cons'	 => array(
				'name'	 => __( 'Consent Solution', 'iubenda' ),
				'key'	 => 'iubenda_consent_solution',
				'submit' => 'save_consent_options',
				'reset'	 => 'reset_consent_options'
			)
		);

		$this->tag_types = array(
			0 => __( 'Not set', 'iubenda' ),
			1 => __( 'Strictly necessary', 'iubenda' ),
			2 => __( 'Basic interactions & functionalities', 'iubenda' ),
			3 => __( 'Experience enhancement', 'iubenda' ),
			4 => __( 'Analytics', 'iubenda' ),
			5 => __( 'Targeting & Advertising', 'iubenda' )
		);
        $siteId = iub_array_get(iubenda()->options['global_options'], 'site_id');

        $QG_Response = (new QuickGeneratorService())->QG_Response;

		$links = array(
			'en' => array(
				'iab' => 'https://www.iubenda.com/en/help/7440-enable-preference-management-iab-framework',
                'enable_iab' => 'https://www.iubenda.com/en/help/7440-iab-framework-cmp#why-publishers-should-enable-the-transparency-and-consent-framework',
                'guide'	=> 'https://www.iubenda.com/en/cookie-solution',
				'plugin_page' => 'https://www.iubenda.com/en/help/posts/1215',
				'support_forum' => 'https://support.iubenda.com/support/home',
				'documentation' => 'https://www.iubenda.com/en/help/posts/1215',
				'how_generate_tc' => 'https://www.iubenda.com/en/help/19461',
				'how_generate_cs' => 'https://www.iubenda.com/en/help/1177',
				'how_generate_pp' => 'https://www.iubenda.com/en/help/463-generate-privacy-policy',
				'how_generate_cons' => 'https://www.iubenda.com/en/help/6473-consent-solution-js-documentation#generate-embed',
				'about_pp' => 'https://www.iubenda.com/en/privacy-and-cookie-policy-generator',
				'about_cs' => 'https://www.iubenda.com/en/cookie-solution',
				'about_tc' => 'https://www.iubenda.com/en/terms-and-conditions-generator',
				'flow_page' => "https://www.iubenda.com/en/flow/{$siteId}",
				'about_cons' => 'https://www.iubenda.com/en/consent-solution',
				'amp_support' => 'https://www.iubenda.com/en/help/22135-cookie-solution-amp-wordpress#amp-domain',
				'enable_amp_support' => 'https://www.iubenda.com/en/help/22135-cookie-solution-amp-wordpress#step-2-enable-the-google-amp-support',
				'wordpress_support' => 'https://www.iubenda.com/en/help/370-how-to-use-iubenda-privacy-and-cookie-policy-on-a-wordpress-website',
				'privacy_policy_generator_edit' => iub_array_get($QG_Response, 'privacy_policies.en.edit_url', '') ?? '',
				'privacy_policy_generator_setup' => iub_array_get($QG_Response, 'privacy_policies.en.setup_url', '') ?? '',
				'automatic_block_scripts' => 'https://www.iubenda.com/en/help/1215-cookie-solution-wordpress-plugin-installation-guide#functionality',
				'how_cs_rate' => 'https://www.iubenda.com/en/help/21985-cookie-banner-do-you-really-need-one-and-how-can-you-get-a-cookie-notice-for-your-website',
				'how_cons_rate' => 'https://www.iubenda.com/en/help/3081-prior-blocking-of-cookie-scripts#wordpress',
				'how_pp_rate' => 'https://www.iubenda.com/en/help/6187-what-should-be-in-a-privacy-policy',
				'how_tc_rate' => 'https://www.iubenda.com/en/help/19482-what-should-basic-terms-and-conditions-include',
				'user_account' => 'https://www.iubenda.com/en/account',
                'amp_permission_support' => 'https://www.iubenda.com/en/help/1215#amp-permissions'
			),
            'it' => array(
                'iab' => 'https://www.iubenda.com/it/help/7440-enable-preference-management-iab-framework',
                'enable_iab' => 'https://www.iubenda.com/it/help/7440-iab-framework-cmp#why-publishers-should-enable-the-transparency-and-consent-framework',
                'guide'	=> 'https://www.iubenda.com/it/cookie-solution',
                'plugin_page' => 'https://www.iubenda.com/it/help/posts/810',
                'support_forum' => 'https://support.iubenda.com/support/home',
                'documentation' => 'https://www.iubenda.com/it/help/posts/810',
                'how_generate_tc' => 'https://www.iubenda.com/it/help/19394',
                'how_generate_cs' => 'https://www.iubenda.com/it/help/680',
                'how_generate_pp' => 'https://www.iubenda.com/it/help/463-generate-privacy-policy',
                'how_generate_cons' => 'https://www.iubenda.com/it/help/6473-consent-solution-js-documentation#generate-embed',
                'about_pp' => 'https://www.iubenda.com/it/privacy-and-cookie-policy-generator',
                'about_cs' => 'https://www.iubenda.com/it/cookie-solution',
                'about_tc' => 'https://www.iubenda.com/it/terms-and-conditions-generator',
                'flow_page' => "https://www.iubenda.com/it/flow/{$siteId}",
                'about_cons' => 'https://www.iubenda.com/it/consent-solution',
                'amp_support' => 'https://www.iubenda.com/it/help/22135-cookie-solution-amp-wordpress#amp-domain',
                'enable_amp_support' => 'https://www.iubenda.com/it/help/22135-cookie-solution-amp-wordpress#step-2-enable-the-google-amp-support',
                'wordpress_support' => 'https://www.iubenda.com/it/help/370-how-to-use-iubenda-privacy-and-cookie-policy-on-a-wordpress-website',
                'privacy_policy_generator_edit' => iub_array_get($QG_Response, 'privacy_policies.it.edit_url', '') ?? '',
                'privacy_policy_generator_setup' => iub_array_get($QG_Response, 'privacy_policies.it.setup_url', '') ?? '',
                'automatic_block_scripts' => 'https://www.iubenda.com/it/help/1215-cookie-solution-wordpress-plugin-installation-guide#functionality',
                'how_cs_rate' => 'https://www.iubenda.com/it/help/21985-cookie-banner-do-you-really-need-one-and-how-can-you-get-a-cookie-notice-for-your-website',
				'how_cons_rate' => 'https://www.iubenda.com/it/help/3081-prior-blocking-of-cookie-scripts#wordpress',
				'how_pp_rate' => 'https://www.iubenda.com/it/help/6187-what-should-be-in-a-privacy-policy',
				'how_tc_rate' => 'https://www.iubenda.com/it/help/19482-what-should-basic-terms-and-conditions-include',
                'user_account' => 'https://www.iubenda.com/it/account',
                'amp_permission_support' => 'https://www.iubenda.com/it/help/1215#amp-permissions'
            ),
            'de' => array(
                'iab' => 'https://www.iubenda.com/de/help/7440-enable-preference-management-iab-framework',
                'enable_iab' => 'https://www.iubenda.com/de/help/7440-iab-framework-cmp#why-publishers-should-enable-the-transparency-and-consent-framework',
                'guide'	=> 'https://www.iubenda.com/de/cookie-solution',
                'plugin_page' => 'https://www.iubenda.com/de/help/posts/810',
                'support_forum' => 'https://support.iubenda.com/support/home',
                'documentation' => 'https://www.iubenda.com/de/help/posts/810',
                'how_generate_tc' => 'https://www.iubenda.com/de/help/19394',
                'how_generate_cs' => 'https://www.iubenda.com/de/help/680',
                'how_generate_pp' => 'https://www.iubenda.com/de/help/463-generate-privacy-policy',
                'how_generate_cons' => 'https://www.iubenda.com/de/help/6473-consent-solution-js-documentation#generate-embed',
                'about_pp' => 'https://www.iubenda.com/de/privacy-and-cookie-policy-generator',
                'about_cs' => 'https://www.iubenda.com/de/cookie-solution',
                'about_tc' => 'https://www.iubenda.com/de/terms-and-conditions-generator',
                'flow_page' => "https://www.iubenda.com/de/flow/{$siteId}",
                'about_cons' => 'https://www.iubenda.com/de/consent-solution',
                'amp_support' => 'https://www.iubenda.com/de/help/22135-cookie-solution-amp-wordpress#amp-domain',
                'enable_amp_support' => 'https://www.iubenda.com/de/help/22135-cookie-solution-amp-wordpress#step-2-enable-the-google-amp-support',
                'wordpress_support' => 'https://www.iubenda.com/de/help/370-how-to-use-iubenda-privacy-and-cookie-policy-on-a-wordpress-website',
                'privacy_policy_generator_edit' => iub_array_get($QG_Response, 'privacy_policies.de.edit_url', '') ?? '',
                'privacy_policy_generator_setup' => iub_array_get($QG_Response, 'privacy_policies.de.setup_url', '') ?? '',
                'automatic_block_scripts' => 'https://www.iubenda.com/de/help/1215-cookie-solution-wordpress-plugin-installation-guide#functionality',
                'how_cs_rate' => 'https://www.iubenda.com/de/help/21985-cookie-banner-do-you-really-need-one-and-how-can-you-get-a-cookie-notice-for-your-website',
				'how_cons_rate' => 'https://www.iubenda.com/de/help/3081-prior-blocking-of-cookie-scripts#wordpress',
				'how_pp_rate' => 'https://www.iubenda.com/de/help/6187-what-should-be-in-a-privacy-policy',
				'how_tc_rate' => 'https://www.iubenda.com/de/help/19482-what-should-basic-terms-and-conditions-include',
                'user_account' => 'https://www.iubenda.com/de/account',
                'amp_permission_support' => 'https://www.iubenda.com/de/help/1215#amp-permissions'
            ),
            'es' => array(
                'iab' => 'https://www.iubenda.com/es/help/7440-enable-preference-management-iab-framework',
                'enable_iab' => 'https://www.iubenda.com/es/help/7440-iab-framework-cmp#why-publishers-should-enable-the-transparency-and-consent-framework',
                'guide'	=> 'https://www.iubenda.com/es/cookie-solution',
                'plugin_page' => 'https://www.iubenda.com/es/help/posts/810',
                'support_forum' => 'https://support.iubenda.com/support/home',
                'documentation' => 'https://www.iubenda.com/es/help/posts/810',
                'how_generate_tc' => 'https://www.iubenda.com/es/help/19394',
                'how_generate_cs' => 'https://www.iubenda.com/es/help/680',
                'how_generate_pp' => 'https://www.iubenda.com/es/help/463-generate-privacy-policy',
                'how_generate_cons' => 'https://www.iubenda.com/es/help/6473-consent-solution-js-documentation#generate-embed',
                'about_pp' => 'https://www.iubenda.com/es/privacy-and-cookie-policy-generator',
                'about_cs' => 'https://www.iubenda.com/es/cookie-solution',
                'about_tc' => 'https://www.iubenda.com/es/terms-and-conditions-generator',
                'flow_page' => "https://www.iubenda.com/es/flow/{$siteId}",
                'about_cons' => 'https://www.iubenda.com/es/consent-solution',
                'amp_support' => 'https://www.iubenda.com/es/help/22135-cookie-solution-amp-wordpress#amp-domain',
                'enable_amp_support' => 'https://www.iubenda.com/es/help/22135-cookie-solution-amp-wordpress#step-2-enable-the-google-amp-support',
                'wordpress_support' => 'https://www.iubenda.com/es/help/370-how-to-use-iubenda-privacy-and-cookie-policy-on-a-wordpress-website',
                'privacy_policy_generator_edit' => iub_array_get($QG_Response, 'privacy_policies.es.edit_url', '') ?? '',
                'privacy_policy_generator_setup' => iub_array_get($QG_Response, 'privacy_policies.es.setup_url', '') ?? '',
                'automatic_block_scripts' => 'https://www.iubenda.com/es/help/1215-cookie-solution-wordpress-plugin-installation-guide#functionality',
                'how_cs_rate' => 'https://www.iubenda.com/es/help/21985-cookie-banner-do-you-really-need-one-and-how-can-you-get-a-cookie-notice-for-your-website',
				'how_cons_rate' => 'https://www.iubenda.com/es/help/3081-prior-blocking-of-cookie-scripts#wordpress',
				'how_pp_rate' => 'https://www.iubenda.com/es/help/6187-what-should-be-in-a-privacy-policy',
				'how_tc_rate' => 'https://www.iubenda.com/es/help/19482-what-should-basic-terms-and-conditions-include',
                'user_account' => 'https://www.iubenda.com/es/account',
                'amp_permission_support' => 'https://www.iubenda.com/es/help/1215#amp-permissions'
            ),
            'fr' => array(
                'iab' => 'https://www.iubenda.com/fr/help/7440-enable-preference-management-iab-framework',
                'enable_iab' => 'https://www.iubenda.com/fr/help/7440-iab-framework-cmp#why-publishers-should-enable-the-transparency-and-consent-framework',
                'guide'	=> 'https://www.iubenda.com/fr/cookie-solution',
                'plugin_page' => 'https://www.iubenda.com/fr/help/posts/810',
                'support_forum' => 'https://support.iubenda.com/support/home',
                'documentation' => 'https://www.iubenda.com/fr/help/posts/810',
                'how_generate_tc' => 'https://www.iubenda.com/fr/help/19394',
                'how_generate_cs' => 'https://www.iubenda.com/fr/help/680',
                'how_generate_pp' => 'https://www.iubenda.com/fr/help/463-generate-privacy-policy',
                'how_generate_cons' => 'https://www.iubenda.com/fr/help/6473-consent-solution-js-documentation#generate-embed',
                'about_pp' => 'https://www.iubenda.com/fr/privacy-and-cookie-policy-generator',
                'about_cs' => 'https://www.iubenda.com/fr/cookie-solution',
                'about_tc' => 'https://www.iubenda.com/fr/terms-and-conditions-generator',
                'flow_page' => "https://www.iubenda.com/fr/flow/{$siteId}",
                'about_cons' => 'https://www.iubenda.com/fr/consent-solution',
                'amp_support' => 'https://www.iubenda.com/fr/help/22135-cookie-solution-amp-wordpress#amp-domain',
                'enable_amp_support' => 'https://www.iubenda.com/fr/help/22135-cookie-solution-amp-wordpress#step-2-enable-the-google-amp-support',
                'wordpress_support' => 'https://www.iubenda.com/fr/help/370-how-to-use-iubenda-privacy-and-cookie-policy-on-a-wordpress-website',
                'privacy_policy_generator_edit' => iub_array_get($QG_Response, 'privacy_policies.fr.edit_url', '') ?? '',
                'privacy_policy_generator_setup' => iub_array_get($QG_Response, 'privacy_policies.fr.setup_url', '') ?? '',
                'automatic_block_scripts' => 'https://www.iubenda.com/fr/help/1215-cookie-solution-wordpress-plugin-installation-guide#functionality',
                'how_cs_rate' => 'https://www.iubenda.com/fr/help/21985-cookie-banner-do-you-really-need-one-and-how-can-you-get-a-cookie-notice-for-your-website',
				'how_cons_rate' => 'https://www.iubenda.com/fr/help/3081-prior-blocking-of-cookie-scripts#wordpress',
				'how_pp_rate' => 'https://www.iubenda.com/fr/help/6187-what-should-be-in-a-privacy-policy',
				'how_tc_rate' => 'https://www.iubenda.com/fr/help/19482-what-should-basic-terms-and-conditions-include',
                'user_account' => 'https://www.iubenda.com/fr/account',
                'amp_permission_support' => 'https://www.iubenda.com/fr/help/1215#amp-permissions'
            ),
            'pt-br' => array(
                'iab' => 'https://www.iubenda.com/pt-br/help/7440-enable-preference-management-iab-framework',
                'enable_iab' => 'https://www.iubenda.com/pt-br/help/7440-iab-framework-cmp#why-publishers-should-enable-the-transparency-and-consent-framework',
                'guide'	=> 'https://www.iubenda.com/pt-br/cookie-solution',
                'plugin_page' => 'https://www.iubenda.com/pt-br/help/45342-cookie-solution-manual-de-instalacao-do-plugin-do-wordpress',
                'support_forum' => 'https://support.iubenda.com/support/home',
                'documentation' => 'https://www.iubenda.com/pt-br/help/45342-cookie-solution-manual-de-instalacao-do-plugin-do-wordpress',
                'how_generate_tc' => 'https://www.iubenda.com/pt-br/help/19394',
                'how_generate_cs' => 'https://www.iubenda.com/pt-br/help/680',
                'how_generate_pp' => 'https://www.iubenda.com/pt-br/help/463-generate-privacy-policy',
                'how_generate_cons' => 'https://www.iubenda.com/pt-br/help/6473-consent-solution-js-documentation#generate-embed',
                'about_pp' => 'https://www.iubenda.com/pt-br/privacy-and-cookie-policy-generator',
                'about_cs' => 'https://www.iubenda.com/pt-br/cookie-solution',
                'about_tc' => 'https://www.iubenda.com/pt-br/terms-and-conditions-generator',
                'flow_page' => "https://www.iubenda.com/pt-br/flow/{$siteId}",
                'about_cons' => 'https://www.iubenda.com/pt-br/consent-solution',
                'amp_support' => 'https://www.iubenda.com/pt-br/help/22135-cookie-solution-amp-wordpress#amp-domain',
                'enable_amp_support' => 'https://www.iubenda.com/pt-br/help/22135-cookie-solution-amp-wordpress#step-2-enable-the-google-amp-support',
                'wordpress_support' => 'https://www.iubenda.com/pt-br/help/370-how-to-use-iubenda-privacy-and-cookie-policy-on-a-wordpress-website',
                'privacy_policy_generator_edit' => iub_array_get($QG_Response, 'privacy_policies.pt-br.edit_url', '') ?? '',
                'privacy_policy_generator_setup' => iub_array_get($QG_Response, 'privacy_policies.pt-br.setup_url', '') ?? '',
                'automatic_block_scripts' => 'https://www.iubenda.com/pt-br/help/1215-cookie-solution-wordpress-plugin-installation-guide#functionality',
                'how_cs_rate' => 'https://www.iubenda.com/pt-br/help/21985-cookie-banner-do-you-really-need-one-and-how-can-you-get-a-cookie-notice-for-your-website',
                'how_cons_rate' => 'https://www.iubenda.com/pt-br/help/3081-prior-blocking-of-cookie-scripts#wordpress',
                'how_pp_rate' => 'https://www.iubenda.com/pt-br/help/6187-what-should-be-in-a-privacy-policy',
                'how_tc_rate' => 'https://www.iubenda.com/pt-br/help/19482-what-should-basic-terms-and-conditions-include',
                'user_account' => 'https://www.iubenda.com/pt-br/account',
                'amp_permission_support' => 'https://www.iubenda.com/pt-br/help/1215#amp-permissions'
            ),
            'nl' => array(
                'iab' => 'https://www.iubenda.com/nl/help/7440-enable-preference-management-iab-framework',
                'enable_iab' => 'https://www.iubenda.com/nl/help/7440-iab-framework-cmp#why-publishers-should-enable-the-transparency-and-consent-framework',
                'guide'	=> 'https://www.iubenda.com/nl/cookie-solution',
                'plugin_page' => 'https://www.iubenda.com/nl/help/posts/810',
                'support_forum' => 'https://support.iubenda.com/support/home',
                'documentation' => 'https://www.iubenda.com/nl/help/posts/810',
                'how_generate_tc' => 'https://www.iubenda.com/nl/help/19394',
                'how_generate_cs' => 'https://www.iubenda.com/nl/help/680',
                'how_generate_pp' => 'https://www.iubenda.com/nl/help/463-generate-privacy-policy',
                'how_generate_cons' => 'https://www.iubenda.com/nl/help/6473-consent-solution-js-documentation#generate-embed',
                'about_pp' => 'https://www.iubenda.com/nl/privacy-and-cookie-policy-generator',
                'about_cs' => 'https://www.iubenda.com/nl/cookie-solution',
                'about_tc' => 'https://www.iubenda.com/nl/terms-and-conditions-generator',
                'flow_page' => "https://www.iubenda.com/nl/flow/{$siteId}",
                'about_cons' => 'https://www.iubenda.com/nl/consent-solution',
                'amp_support' => 'https://www.iubenda.com/nl/help/22135-cookie-solution-amp-wordpress#amp-domain',
                'enable_amp_support' => 'https://www.iubenda.com/nl/help/22135-cookie-solution-amp-wordpress#step-2-enable-the-google-amp-support',
                'wordpress_support' => 'https://www.iubenda.com/nl/help/370-how-to-use-iubenda-privacy-and-cookie-policy-on-a-wordpress-website',
                'privacy_policy_generator_edit' => iub_array_get($QG_Response, 'privacy_policies.nl.edit_url', '') ?? '',
                'privacy_policy_generator_setup' => iub_array_get($QG_Response, 'privacy_policies.nl.setup_url', '') ?? '',
                'automatic_block_scripts' => 'https://www.iubenda.com/nl/help/1215-cookie-solution-wordpress-plugin-installation-guide#functionality',
                'how_cs_rate' => 'https://www.iubenda.com/nl/help/21985-cookie-banner-do-you-really-need-one-and-how-can-you-get-a-cookie-notice-for-your-website',
                'how_cons_rate' => 'https://www.iubenda.com/nl/help/3081-prior-blocking-of-cookie-scripts#wordpress',
                'how_pp_rate' => 'https://www.iubenda.com/nl/help/6187-what-should-be-in-a-privacy-policy',
                'how_tc_rate' => 'https://www.iubenda.com/nl/help/19482-what-should-basic-terms-and-conditions-include',
                'user_account' => 'https://www.iubenda.com/nl/account',
                'amp_permission_support' => 'https://www.iubenda.com/nl/help/1215#amp-permissions'
            )
		);

        foreach ($this->services as $name => $service) {
            $this->services[$name]['status'] = iub_array_get(iubenda()->options, "activated_products.{$service['key']}", 'false');
        }
        $this->quick_generator = get_option(static::IUB_QG_Response) ?: [];

        $user_profile_language = (new LanguageHelper())->get_user_profile_language_code(true);

		// assign links
		$this->links = in_array( $user_profile_language, array_keys( $links ) ) ? $links[$user_profile_language] : $links['en'];

		// handle actions
		if ( ! empty( $_POST['save'] ) ) {
			// update item action
			$this->action = 'save';
		} else {
			$this->action = isset( $_GET['action'] ) && -1 != $_GET['action'] ? esc_attr( $_GET['action'] ) : '';
			$this->action = isset( $_GET['action2'] ) && -1 != $_GET['action2'] ? esc_attr( $_GET['action2'] ) : $this->action;
		}
	}

	/**
	 * Add submenu.
	 *
	 * @return void
	 */
	public function admin_menu_options() {
		if ( iubenda()->options['cs']['menu_position'] === 'submenu' ) {
			// sub menu
			add_submenu_page(
				'options-general.php', 'iubenda', 'iubenda', apply_filters( 'iubenda_cookie_law_cap', 'manage_options' ), 'iubenda', array( $this, 'options_page' )
			);
		} else {
			// top menu
			add_menu_page(
				'iubenda', 'iubenda', apply_filters( 'iubenda_cookie_law_cap', 'manage_options' ), 'iubenda', array( $this, 'options_page' ), 'none'
			);
		}
	}

    private function check_site_is_already_made_setup() {
        $result = array_filter(array_column($this->services, 'status'), function ($service) { return (stripos($service, 'false') === false); });

        if ($result) {
            return true;
        }

        // Check if the services are configured
        $result = array_filter(array_column(iubenda()->options, 'configured'), function ($service) { return (stripos($service, 'false') === false); });

        if ($result) {
            return true;
        }

        return false;
    }

    /**
     * Load admin options page.
     *
     * @return void
     */
    public function options_page() {
        global $pagenow;

        $show_products_page = $this->check_site_is_already_made_setup();

        if ( ! current_user_can( apply_filters( 'iubenda_cookie_law_cap', 'manage_options' ) ) ) {
            wp_die( __( "You don't have permission to access this page.", 'iubenda' ) );
        }
        $default = 'frontpage';

        if($show_products_page){
            $default = 'products-page';
        }elseif(!empty((new QuickGeneratorService())->QG_Response)){
            $default = 'integrate-setup';
        }
        $view = iub_array_get($_GET, 'view', $default);

        switch ($view) {
            case "plugin-settings":
                $pageLabels = [['title' => __('Plugin settings', 'iubenda')]];
                require_once IUBENDA_PLUGIN_PATH . 'views/plugin-settings.php';
                break;
            case "integrate-setup":
                require_once IUBENDA_PLUGIN_PATH . 'views/integrate-setup.php';
                break;
            case 'products-page':
                require_once IUBENDA_PLUGIN_PATH . 'views/products-page.php';
                break;
            case "tc-configuration":
                $pageLabels = [['title' => __('Terms and condition', 'iubenda')]];
                $key = 'tc';
                $service = iub_array_get(iubenda()->settings->services, $key);
                require_once IUBENDA_PLUGIN_PATH . 'views/tc-configuration.php';
                break;
            case "pp-configuration":
                $pageLabels = [['title' => __('Privacy and Cookie Policy', 'iubenda')]];
                $key = 'pp';
                $service = iub_array_get(iubenda()->settings->services, $key);
                require_once IUBENDA_PLUGIN_PATH . 'views/pp-configuration.php';
                break;
            case "cs-configuration":
                $pageLabels = [['title' => __('Cookie Solution', 'iubenda')]];
                $key = 'cs';
                $service = iub_array_get(iubenda()->settings->services, $key);
                require_once IUBENDA_PLUGIN_PATH . 'views/cs-configuration.php';
                break;
            case "cons-configuration":
                $pageLabels = [['title' => __('Consent Solution', 'iubenda')]];
                require_once IUBENDA_PLUGIN_PATH . 'views/cons-configuration.php';
                break;
            case "cons-form-edit":
                $form_id = ! empty( $_GET['form_id'] ) ? absint( $_GET['form_id'] ) : 0;
                $form = ! empty( $form_id ) ? iubenda()->forms->get_form( $form_id ) : false;

                if ( ! $form ){
                    return;
                }
                $pageLabels = [
                    ['title' => __('Consent Solution', 'iubenda'), 'href' => add_query_arg( array( 'view' => 'cons-configuration' ), iubenda()->base_url )],
                    ['title' => $form->post_title]
                ];
                require_once IUBENDA_PLUGIN_PATH . 'views/cons-single-form.php';
                break;
            default:
                if ($show_products_page) {
                    require_once IUBENDA_PLUGIN_PATH . 'views/products-page.php';
                }
                else {
                    require_once IUBENDA_PLUGIN_PATH . 'views/frontpage.php';
                }
        }
    }

    public function admin_enqueue_scripts($page) {
        if ( ! in_array( $page, array( 'toplevel_page_iubenda', 'settings_page_iubenda' ) ) ){
            wp_enqueue_style('iubenda-admin', IUBENDA_PLUGIN_URL . '/assets/css/admin.css', array(), iubenda()->version);
            return;
        }
        wp_enqueue_style('iubenda-admin', IUBENDA_PLUGIN_URL . '/assets/css/style.css', array(), iubenda()->version);
        wp_enqueue_script('iubenda-admin', IUBENDA_PLUGIN_URL . '/assets/js/admin.js', array('jquery'), iubenda()->version,true);

        // Add analytics script to the plugin
        wp_enqueue_script('iubenda-admin-matomo', IUBENDA_PLUGIN_URL . '/assets/js/matomo.js','', iubenda()->version,true);

        // Get radar api status
        $iubendaRadarApiConfiguration = get_option('iubenda_radar_api_configuration', []) ?: [];

        // Localize the script with new data
        $iub_js_vars = [
            'site_url' => get_site_url(),
            'plugin_url' => IUBENDA_PLUGIN_URL,
            'site_language' => iubenda()->lang_current,
            'site_locale' => get_locale(),
            'radar_status' => iub_array_get($iubendaRadarApiConfiguration, 'status'),
            'form_id'		=> iub_array_get($_GET,'form_id', 0),
            'iub_dismiss_notification_alert_nonce'		=> wp_create_nonce( 'iub_dismiss_notification_alert_nonce' ),
        ];

        wp_localize_script( 'iubenda-admin', 'iub_js_vars', $iub_js_vars );
        wp_enqueue_script( 'iubenda-admin-tabs', IUBENDA_PLUGIN_URL . '/assets/js/tabs.js', array( 'jquery' ), iubenda()->version, true );
    }

	/**
	 * Plugin options migration for versions < 1.14.0
	 *
	 * @return void
	 */
	public function update_plugin() {
		if ( ! current_user_can( 'install_plugins' ) )
			return;

		$db_version = get_option( 'iubenda_cookie_law_version' );
		$db_version = ! $db_version ? '1.13.0' : $db_version;

		if ( $db_version != false ) {
			if ( version_compare( $db_version, '1.14.0', '<' ) ) {
				$options = [];

				$old_new = array(
					'iubenda_parse'			 => 'parse',
					'skip_parsing'			 => 'skip_parsing',
					'iubenda_ctype'			 => 'ctype',
					'parser_engine'			 => 'parser_engine',
					'iubenda_output_feed'	 => 'output_feed',
					'iubenda-code-default'	 => 'code_default',
					'default_skip_parsing'	 => '',
					'default_iubendactype'	 => '',
					'default_iubendaparse'	 => '',
					'default_parser_engine'	 => '',
					'iub_code'				 => '',
				);

				foreach ( $old_new as $old => $new ) {
					if ( $new ) {
						$options[$new] = get_option( $old );
					}
					delete_option( $old );
				}

				// multilang support
				if ( ! empty( iubenda()->languages ) ) {
					foreach ( iubenda()->languages as $lang_id => $lang_name ) {
						$code = get_option( 'iubenda-code-' . $lang_id );

						if ( ! empty( $code ) ) {
							$options['code_' . $lang_id] = $code;

							delete_option( 'iubenda-code-' . $lang_id );
						}
					}
				}

				add_option( 'iubenda_cookie_law_solution', $options, '', 'no' );
				add_option( 'iubenda_cookie_law_version', iubenda()->version, '', 'no' );
            }
		}
    }

    public function update_options($data = []){
        $data = $data ?: $_POST;

        $products = [
            'iubenda_privacy_policy_solution' => 'pp',
            'iubenda_cookie_law_solution' => 'cs',
            'iubenda_terms_conditions_solution' => 'tc',
            'iubenda_consent_solution' => 'cons',
        ];

        $result = $this->init_prepare_product_options($products, $data);

        // Validate whether the product (CS) is active or not
        $iubenda_cookie_law_solution_status = iub_array_get($result, 'iubenda_activated_products.iubenda_cookie_law_solution', 'false') ?: 'false';
        if($iubenda_cookie_law_solution_status != 'true'){
            echo json_encode(['status' => 'error', 'responseText' => "( CS ) must be activated."]);
            wp_die();
        }

        // validating Embed Codes of product contains at least one valid code if the product is activated
        foreach (iub_array_get($result, 'iubenda_activated_products', []) ?: [] as $product_name => $product_status) {
            if($product_status == 'false' || $product_name == 'iubenda_consent_solution'){
                continue;
            }

            // Count valid codes per $product_name and return error if doesn't have at least 1 valid code
            if(count(array_filter(iub_array_get($result, "codes_statues.{$product_name}_codes", []) ?: [])) == 0){
                echo json_encode(['status' => 'error', 'responseText' => "( {$product_name} ) At least one code must be valid."]);
                wp_die();
            }
        }

        $this->save_init_prepared_product_options($products, $result);

        $data = [
            'status' => 'done',
        ];
        echo json_encode($data);
        wp_die();
    }

    public function toggle_services(){
        $name = iub_array_get($_POST, 'name');
        $status = iub_array_get($_POST, 'status');

        if($status != 'true'){
            $status = 'false';
        }

        $iubenda_activated_products = get_option( 'iubenda_activated_products');
        $iubenda_activated_products[$name] = $status;

        update_option( 'iubenda_activated_products', $iubenda_activated_products );

        // Reload Options and activated products
        iubenda()->options['activated_products'] = get_option( 'iubenda_activated_products', [] );
        $this->load_defaults();

        $data = ['status' => 'done', 'rating_percentage' => iubenda()->serviceRating->services_percentage()];
        echo json_encode($data);
        wp_die();
    }

    /**
     * Process the bulk actions
     *
     * @return void
     */
    public function process_actions() {
        global $pagenow;

        $page = ! empty( $_POST['option_page'] ) ? esc_attr( $_POST['option_page'] ) : ( ! empty( $_GET['page'] ) ? esc_attr( $_GET['page'] ) : '' );
        $id = isset( $_REQUEST['form_id'] ) ? ( is_array( $_REQUEST['form_id'] ) ? array_map( 'ansint', $_REQUEST['form_id'] ) : absint( $_REQUEST['form_id'] ) ) : false;
        $view_key = ! empty( $_GET['view'] ) ? esc_attr( $_GET['view'] ) : null;

        if ( ! $page )
            return;

        // get redirect url
        if ( iubenda()->options['cs']['menu_position'] === 'submenu' && $pagenow === 'admin.php' ) {
            // sub menu
            $redirect_to = admin_url( 'options-general.php?page=iubenda&view=' . $view_key );
        } else {
            // top menu
            $redirect_to = admin_url( 'admin.php?page=iubenda&view=' . $view_key );
        }

        // add comments cookie option notice
        if ( $view_key == 'cons-configuration' && ! empty( iubenda()->options['cons']['public_api_key'] ) ) {
            $cookies_enabled = get_option( 'show_comments_cookies_opt_in' );
            if ( ! $cookies_enabled ) {
                $this->add_notice( 'iub_comment_cookies_disabled', sprintf( __( 'Please enable comments cookies opt-in checkbox in the <a href="%s" target="_blank">Discussion settings</a>.', 'iubenda' ), esc_url( admin_url( 'options-discussion.php' ) ) ), 'notice' );
            }
        }

        $result = null;

        switch ( $this->action ) {
            case 'autodetect' :
                $result = iubenda()->forms->autodetect_forms();

                // make sure it's current host location
                wp_safe_redirect( $redirect_to );
                exit;

                break;

            case 'save' :
                if ( ! $id )
                    return;

                $form = iubenda()->forms->get_form( $id );

                if ( $form->ID != $id )
                    return;

                $status = isset( $_POST['status'] ) && in_array( $_POST['status'], array_keys( iubenda()->forms->statuses ) ) ? esc_attr( $_POST['status'] ) : 'publish';
                $subject = isset( $_POST['subject'] ) && is_array( $_POST['subject'] ) ? array_map( 'esc_attr', $_POST['subject'] ) : array();
                $preferences = array();
                $exclude = array();
                $legal_notices = array();

                $preferences_raw = isset( $_POST['preferences'] ) && is_array( $_POST['preferences'] ) ? array_map( array( $this, 'array_map_callback' ), $_POST['preferences'] ) : array();
                $exclude_raw = isset( $_POST['exclude'] ) && is_array( $_POST['exclude'] ) ? array_map( array( $this, 'array_map_callback' ), $_POST['exclude'] ) : array();
                $legal_notices_raw = isset( $_POST['legal_notices'] ) && is_array( $_POST['legal_notices'] ) ? array_map( array( $this, 'array_map_callback' ), $_POST['legal_notices'] ) : array();

                // format preferences data
                if ( ! empty( $preferences_raw ) && is_array( $preferences_raw ) ) {
                    foreach ( $preferences_raw as $index => $data ) {
                        if ( ! empty( $data['field'] ) && ( ! is_null( $data['value'] ) || ! "" == $data['value'] ) ) {
                            $preferences[ sanitize_key( $data['field'] ) ] = $data['value'];
                        }
                    }
                }

                // format exclude data
                if ( ! empty( $exclude_raw ) && is_array( $exclude_raw ) ) {
                    foreach ( $exclude_raw as $index => $data ) {
                        if ( ! empty( $data['field'] ) )
                            $exclude[] = $data['field'];
                    }
                }

                // format legal notices data
                if ( ! empty( $legal_notices_raw ) && is_array( $legal_notices_raw ) ) {
                    foreach ( $legal_notices_raw as $index => $data ) {
                        if ( ! empty( $data['field'] ) )
                            $legal_notices[] = $data['field'];
                    }
                }

                // form first save, update status to mapped automatically
                if ( empty( $form->form_subject ) && empty( $form->form_preferences ) ) {
                    $status = 'mapped';
                }

                // echo '<pre>'; print_r( $_POST ); echo '</pre>'; exit;
                $filtered_subjects = array_filter($subject, array(
                    $this,
                    'is_not_empty'
                ));

                // bail if empty fields
                if ( ! count( $filtered_subjects ) ) {
                    $this->add_notice( 'iub_form_fields_missing', __( 'Form saving failed. Please fill the Subject fields.', 'iubenda' ), 'error' );
                    return;
                }

                $args = array(
                    'ID'					=> $form->ID,
                    'status'				=> $status,
                    'object_type'			=> $form->object_type,
                    'object_id'				=> $form->object_id,
                    'form_source'			=> $form->form_source,
                    'form_title'			=> $form->post_title,
                    'form_date'				=> $form->post_modified,
                    'form_fields'			=> $form->form_fields,
                    'form_subject'			=> $subject,
                    'form_preferences'		=> $preferences,
                    'form_exclude'			=> $exclude,
                    'form_legal_notices'	=> $legal_notices
                );

                $result = iubenda()->forms->save_form( $args );

                break;

            case 'delete' :
                if ( ! $id )
                    return;

                $form = iubenda()->forms->get_form( $id );

                if ( empty( $form ) )
                    return;

                $result = iubenda()->forms->delete_form( $id );

                // make sure it's current host location
                wp_safe_redirect( $redirect_to );
                exit;

                break;

            case 'disable_skip_parsing' :

                // disable skip parsing option
                $options = iubenda()->options['cs'];
                $options['skip_parsing'] = false;

                update_option( 'iubenda_cookie_law_solution', $options );

                $this->add_notice( 'iub_settings_updated', __( 'Settings saved.', 'iubenda' ), 'success' );

                // make sure it's current host location
                wp_safe_redirect( $redirect_to );
                exit;

                break;

            default :
                return;
        }

        if ( ! empty ( $result ) ) {
            //
        } else {
            //
        }
    }

    /**
     * Add admin notice.
     *
     * @param mixed $message
     * @param string $notice_type
     */
    public function add_notice( $key, $message, $notice_type = 'notice' ) {
        $key = ! empty( $key ) ? sanitize_key( $key ) : '';
        $message = ! empty( $message ) ? wp_kses_post( $message ) : '';
        $notice_type = ! empty( $notice_type ) && in_array( $notice_type, $this->notice_types ) ? $notice_type : 'notice';

        if ( ! $key || ! $message )
            return;

        $notices = get_transient( 'iubenda_dashboard_notices' ) ?: [];
        $delay = MINUTE_IN_SECONDS * 2;

        // Check notice type is exist before checking the key
        if ( empty( $notices ) || ( isset( $notices[ $notice_type ] ) && ! array_key_exists( $key, $notices[ $notice_type ] ) ) ) {
            $notices[$notice_type][$key] = $message;

            set_transient( 'iubenda_dashboard_notices', $notices, $delay );
        }
    }

    /**
     * Display admin notices.
     *
     * @return mixed
     */
    public function print_notices() {
        $notices = get_transient( 'iubenda_dashboard_notices' );
        foreach ( $this->notice_types as $notice_type ) {
            if ( $this->notice_count( $notices, $notice_type ) > 0 ) {
                require IUBENDA_PLUGIN_PATH . '/views/partials/alert.php';
            }
        }
        delete_transient( 'iubenda_dashboard_notices' );
    }

    public function has_notices() {
        $notices = get_transient( 'iubenda_dashboard_notices' );
        foreach ( $this->notice_types as $notice_type ) {
            if ( $this->notice_count( $notices, $notice_type ) > 0 ) {
                return true;
            }
        }

        return false;
    }

    /**
     * Count notices function.
     *
     * @param string $notice_type
     * @return int
     */
    public function notice_count( $all_notices = array(), $notice_type = '' ) {
        $notice_count = 0;

        if ( isset( $all_notices[$notice_type] ) ) {
            $notice_count = absint( sizeof( $all_notices[$notice_type] ) );
        } elseif ( empty( $notice_type ) ) {
            foreach ( $all_notices as $notices ) {
                $notice_count += absint( sizeof( $all_notices ) );
            }
        }

        return $notice_count;
    }

    /**
     * Perform show notice on plugin installation/upgrade.
     *
     * @return void
     */
    public function maybe_show_notice() {
        if ( ! current_user_can( 'install_plugins' ) )
            return;

        $current_update = 10;
        $activation = (array) get_option( 'iubenda_activation_data', iubenda()->activation );

        // delete_option( 'iubenda_activation_data' );
        // echo '<pre>'; print_r( $activation ); echo '</pre>'; exit;

        // get current time
        $current_time = time();

        if ( $activation['update_version'] < $current_update ) {
            // check version, if update ver is lower than plugin ver, set update notice to true
            $activation = array_merge( $activation, array( 'update_version' => $current_update, 'update_notice' => true ) );

            // set activation date if not set
            if ( $activation['update_date'] == false )
                $activation = array_merge( $activation, array( 'update_date' => $current_time ) );

            update_option( 'iubenda_activation_data', $activation );
        }

        // display current version notice
        if ( $activation['update_notice'] === true ) {
            // include notice js, only if needed
            add_action( 'admin_print_scripts', array( $this, 'admin_inline_js' ), 999 );

            // get activation date
            $activation_date = $activation['update_date'];

            // set delay in seconds
            $delay = WEEK_IN_SECONDS;

            if ( (int) $activation['update_delay_date'] === 0 ) {
                if ( $activation_date + $delay > $current_time )
                    $activation['update_delay_date'] = $activation_date + $delay;
                else
                    $activation['update_delay_date'] = $current_time;

                update_option( 'iubenda_activation_data', $activation );
            }

            if ( ( ! empty( $activation['update_delay_date'] ) ? (int) $activation['update_delay_date'] : $current_time ) <= $current_time ) {
                // add notice
                add_action( 'admin_notices', array( $this, 'show_notice' ) );
            }
        }

        // Display notification to encourage user to verify his account
        $notifications = get_option(iubenda_Settings::IUB_NOTIFICATIONS, []) ?: [];
        if ( iub_array_get($notifications, 'iub_user_needs_to_verify_his_account') ) {
            $url = 'javascript:void(0)';

            if (!empty(iubenda()->settings->links['privacy_policy_generator_edit'])) {
                $url = iubenda()->settings->links['privacy_policy_generator_edit'];
            }elseif(iub_array_get(iubenda()->options['global_options'], 'site_id')){
                $url = iubenda()->settings->links['user_account'];
            }

            iubenda()->settings->add_notice('iub_user_needs_to_verify_his_account', sprintf( __( 'To ensure regular scans and full support, <span class="text-bold">verify your account</span>. Check your mailbox now and validate your email address, or check <a href="%s" target="_blank" class="link-underline">your account</a> on iubenda.com. If you already did that, you can safely <a href="javascript:void(0)" class="notice-dismiss-by-text dismiss-notification-alert link-underline" data-dismiss-key="iub_user_needs_to_verify_his_account">dismiss this reminder</a>.', 'iubenda' ), $url ), 'error');
        }
    }

    /**
     * Display admin notices at iubenda settings.
     */
    public function show_notice() {
        ?>
            <div id="iubenda-rate" class="iubenda-notice notice is-dismissible">
                <div>
                    <p class="step-1">
                        <span class="notice-question"><?php _e( 'Enjoying the iubenda Cookie & Consent Solution Plugin?', 'iubenda' ); ?></span>
                        <span class="notice-reply">
							<a href="#" class="reply-yes"><?php _e( 'Yes', 'iubenda' ); ?></a>
							<a href="#" class="reply-no"><?php _e( 'No', 'iubenda' ); ?></a>
						</span>
                    </p>
                    <p class="step-2 step-yes">
                        <span class="notice-question"><?php _e( "Whew, what a relief!? We've worked countless hours to make this plugin as useful as possible - so we're pretty happy that you're enjoying it. While you here, would you mind leaving us a 5 star rating? It would really help us out.", 'iubenda' ); ?></span>
                        <span class="notice-reply">
							<a href="https://wordpress.org/support/plugin/iubenda-cookie-law-solution/reviews/?filter=5" target="_blank" class="reply-yes"><?php _e( 'Sure!', 'iubenda' ); ?></a>
							<a href="javascript:void(0)" class="reply-no"><?php _e( 'No thanks', 'iubenda' ); ?></a>
						</span>
                    </p>
                    <p class="step-2 step-no">
                        <span class="notice-question"><?php _e( "We're sorry to hear that. Would you mind giving us some feedback?", 'iubenda' ); ?></span>
                        <span class="notice-reply">
							<a href="https://iubenda.typeform.com/to/BXuSMZ" target="_blank" class="reply-yes"><?php _e( 'Ok sure!', 'iubenda' ); ?></a>
							<a href="javascript:void(0)" class="reply-no"><?php _e( 'No thanks', 'iubenda' ); ?></a>
						</span>
                    </p>
                </div>
            </div>
        <?php
    }

    /**
     * Print admin scripts.
     *
     * @return void
     */
    public function admin_inline_js() {
        if ( ! current_user_can( 'install_plugins' ) )
            return;

        $delay = MONTH_IN_SECONDS * 6;
        ?>
        <script type="text/javascript">
            ( function ( $ ) {
                $( document ).ready( function () {
                    // step 1
                    $( '.iubenda-notice .step-1 a' ).on( 'click', function ( e ) {
                        e.preventDefault();

                        $( '.iubenda-notice .step-1' ).slideUp( 'fast' );
                        $( '.iubenda-notice .step-1' ).hide( 'fast' );

                        if ( $( e.target ).hasClass( 'reply-yes' ) ) {
                            $( '.iubenda-notice .step-2.step-yes' ).show( 'fast' );
                        } else {
                            $( '.iubenda-notice .step-2.step-no' ).show( 'fast' );
                        };
                    } );
                    // step 2
                    $( '.iubenda-notice.is-dismissible' ).on( 'click', '.notice-dismiss, .step-2 a', function ( e ) {
                        // console.log( $( e ) );

                        var delay = <?php echo $delay; ?>;

                        if ( $( e.target ).hasClass( 'reply-yes' ) ) {
                            delay = 0;
                        }

                        $.post( ajaxurl, {
                            action: 'iubenda_dismiss_notice',
                            delay: delay,
                            url: '<?php echo admin_url( 'admin-ajax.php' ); ?>',
                            iubenda_nonce: '<?php echo wp_create_nonce( 'iubenda_dismiss_notice' ); ?>'
                        } );

                        $( e.delegateTarget ).slideUp( 'fast' );
                    } );
                } );
            } )( jQuery );
        </script>
        <?php
    }

    /**
     * Dismiss notice.
     *
     * @return void
     */
    public function dismiss_notice() {
        $result = false;

        if ( ! current_user_can( 'install_plugins' ) )
            return $result;

        $nonce = wp_verify_nonce( $_REQUEST['iubenda_nonce'], 'iubenda_dismiss_notice' );

        if ( $nonce ) {
            $delay = ! empty( $_REQUEST['delay'] ) ? absint( $_REQUEST['delay'] ) : 0;
            $activation = (array) get_option( 'iubenda_activation_data', iubenda()->activation );

            // delay notice
            if ( $delay > 0 ) {
                $activation = array_merge( $activation, array( 'update_delay_date' => time() + $delay ) );
                // hide notice permanently
            } else {
                $activation = array_merge( $activation, array( 'update_delay_date' => 0, 'update_notice' => false ) );
            }

            // update activation options
            $result = update_option( 'iubenda_activation_data', $activation );
        }

        echo json_encode( $result );
        exit;
    }

    /**
     * Dismiss alerts inside iubenda plugin.
     *
     * @return void
     */
    public function dismiss_notification_alert() {
        $result = false;

        if ( ! current_user_can( 'install_plugins' ) )
            return $result;

        $nonce = wp_verify_nonce( $_REQUEST['iubenda_nonce'], 'iub_dismiss_notification_alert_nonce' );

        if ( $nonce ) {
            $dismiss_key = $_REQUEST['dismiss_key'] ?: '';

            // Dismiss alert Encourage users to validate their account
            if(iub_array_get(get_option(iubenda_Settings::IUB_NOTIFICATIONS, []) ?: [], $dismiss_key) === true){
                $iub_notifications = get_option(iubenda_Settings::IUB_NOTIFICATIONS, []) ?: [];
                $iub_notifications[$dismiss_key] = false;
                $result = update_option(iubenda_Settings::IUB_NOTIFICATIONS, $iub_notifications);

                $notices = get_transient( 'iubenda_dashboard_notices' );
                if(iub_array_get($notices, "error.{$dismiss_key}") ?: null){
                    unset($notices['error'][$dismiss_key]);
                }
                set_transient( 'iubenda_dashboard_notices' , $notices);

                echo json_encode( $result );
                exit;
            }
        }

        echo json_encode( $result );
        exit;
    }

    /**
     * Sanitize array helper function.
     *
     * @param array $array
     * @return array
     */
    public function array_map_callback( $array ) {
        if ( ! is_array( $array ) )
            return array();

        return array_map( 'esc_attr', $array );
    }

    /**
     * Check the value is not empty and check it contains any value even 0
     *
     * @param $value
     * @return bool
     */
    private function is_not_empty($value) {
        if(is_null($value) || '' === $value){
            return false;
        }

        return true;
    }

    /**
     * Load admin style inline, for menu icon only.
     *
     * @return mixed
     */
    public function admin_print_styles() {
        echo '
		<style>
			a.toplevel_page_iubenda .wp-menu-image {
				background-image: url(data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9Im5vIj8+PCFET0NUWVBFIHN2ZyBQVUJMSUMgIi0vL1czQy8vRFREIFNWRyAxLjEvL0VOIiAiaHR0cDovL3d3dy53My5vcmcvR3JhcGhpY3MvU1ZHLzEuMS9EVEQvc3ZnMTEuZHRkIj48c3ZnIHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIHZpZXdCb3g9IjAgMCAyMzIgNTAzIiB2ZXJzaW9uPSIxLjEiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiIHhtbDpzcGFjZT0icHJlc2VydmUiIHhtbG5zOnNlcmlmPSJodHRwOi8vd3d3LnNlcmlmLmNvbS8iIHN0eWxlPSJmaWxsLXJ1bGU6ZXZlbm9kZDtjbGlwLXJ1bGU6ZXZlbm9kZDtzdHJva2UtbGluZWpvaW46cm91bmQ7c3Ryb2tlLW1pdGVybGltaXQ6MS40MTQyMTsiPiAgICA8ZyB0cmFuc2Zvcm09Im1hdHJpeCgxLDAsMCwxLDEzNi4yNDcsMjY4LjgzMSkiPiAgICAgICAgPHBhdGggZD0iTTAsLTM1LjgxTC0zNi4zLDAuNDg5TC0zNi4zLDE0MC45NzhMMCwxNDAuOTc4TDAsLTM1LjgxWk0tMjAuOTM4LC0xMjkuODAyQy02LjI4NywtMTI5LjgwMiA1LjU4NywtMTQxLjU2NSA1LjU4NywtMTU2LjA2QzUuNTg3LC0xNzAuNTU2IC02LjI4NywtMTgyLjMwOCAtMjAuOTM4LC0xODIuMzA4Qy0zNS42LC0xODIuMzA4IC00Ny40NzQsLTE3MC41NTYgLTQ3LjQ3NCwtMTU2LjA2Qy00Ny40NzQsLTE0MS41NjUgLTM1LjYsLTEyOS44MDIgLTIwLjkzOCwtMTI5LjgwMk04OS4zNiwtMTU0LjQxNkM4OS4zNiwtMTI3LjgyNSA3OS41NzUsLTEwMy40OTkgNjMuMjY5LC04NC42NzJMODYuNjk0LDIyNi42MjhMLTEyMi43MjgsMjI2LjYyOEwtMTAwLjAyNCwtNzkuMjI5Qy0xMTkuMzUxLC05OC42NjggLTEzMS4yNDcsLTEyNS4xNTkgLTEzMS4yNDcsLTE1NC40MTZDLTEzMS4yNDcsLTIxNC4wODYgLTgxLjg3NCwtMjYyLjQzOCAtMjAuOTM4LC0yNjIuNDM4QzM5Ljk5OSwtMjYyLjQzOCA4OS4zNiwtMjE0LjA4NiA4OS4zNiwtMTU0LjQxNiIgc3R5bGU9ImZpbGw6d2hpdGU7ZmlsbC1ydWxlOm5vbnplcm87Ii8+ICAgIDwvZz48L3N2Zz4=);
				background-position: center center;
				background-repeat: no-repeat;
				background-size: 7px auto;
			}
		</style>
		';
    }

    private function services_option() {
        $cs_settings = [];
        if(iub_array_get(iubenda()->options['cs'], 'configuration_type') == 'simplified'){
            $legislation = iub_array_get(iubenda()->options['cs'], 'simplified.legislation') == 'all' ? 'GDPR/CCPA/LGPD' : strtoupper(iub_array_get(iubenda()->options['cs'], 'simplified.legislation'));
            $cs_settings = [
                ['label' => __('Style', 'iubenda'), 'value' => ucwords(iub_array_get(iubenda()->options['cs'], 'simplified.banner_style'))],
                ['label' => __('Position', 'iubenda'), 'value' => ucwords(iub_array_get(iubenda()->options['cs'], 'simplified.position'))],
                ['label' => __('legislation', 'iubenda'), 'value' => $legislation],
            ];
        }else{
            $languages = (new ProductHelper())->get_languages();
            foreach ($languages as $k => $v) {
                $code = iub_array_get(iubenda()->options['cs'], "code_{$k}");
                if($code){
                    $banner = iubenda()->parse_configuration($code, ['mode' => 'banner']);
                    $options = iubenda()->parse_configuration($code);

                    $style = iub_array_get($banner, 'backgroundColor') ? 'White' : 'Dark';
                    if(iub_array_get($options, 'enableGdpr') === null && iub_array_get($options, 'ccpaApplies') == 1 && iub_array_get($options, 'enableLgpd') == 1){
                        $legislation = 'GDPR/CCPA/LGPD';
                    }elseif(iub_array_get($options, 'enableGdpr') === null){
                        $legislation = 'GDPR';
                    }elseif(iub_array_get($options, 'enableLgpd') == 1){
                        $legislation = 'LGPD';
                    }else{
                        $legislation = 'CCPA';
                    }

                    $cs_settings = [
                        ['label' => __('Style', 'iubenda'), 'value' => $style],
                        ['label' => __('Position', 'iubenda'), 'value' => ucwords(iub_array_get($banner, 'position', 'full-top'))],
                        ['label' => __('legislation', 'iubenda'), 'value' => $legislation],
                    ];
                    break;
                }
            }
        }


	    return [
            'pp' => [
                'status' => false,
                'configured' => iub_array_get(iubenda()->options['pp'], 'configured'),
                'label' => __('Privacy and Cookie Policy', 'iubenda'),
                'name' => 'privacy_policy',
                'key' => 'iubenda_privacy_policy_solution',
                'settings' => [
                    ['label' => __('Version', 'iubenda'), 'value' => iub_array_get(iubenda()->options['pp'], 'version')],
                    ['label' => __('Style', 'iubenda'), 'value' => iub_array_get(iubenda()->options['pp'], 'button_style')],
                    ['label' => __('Position', 'iubenda'), 'value' => iub_array_get(iubenda()->options['pp'], 'button_position')]
                ]
            ],
            'cs' => [
                'status' => false,
                'configured' => iub_array_get(iubenda()->options['cs'], 'configured'),
                'label' => __('Cookie Solution', 'iubenda'),
                'name' => 'cookie_law',
                'key' => 'iubenda_cookie_law_solution',
                'settings' => $cs_settings
            ],
            'tc' => [
                'status' => false,
                'configured' => iub_array_get(iubenda()->options['tc'], 'configured'),
                'label' => __('Terms and Conditions', 'iubenda'),
                'name' => 'terms_conditions',
                'key' => 'iubenda_terms_conditions_solution',
                'settings' => [
                    ['label' => __('Version', 'iubenda'), 'value' => '1.5.0'],
                    ['label' => __('Style', 'iubenda'), 'value' => iub_array_get(iubenda()->options['tc'], 'button_style')],
                    ['label' => __('Position', 'iubenda'), 'value' => iub_array_get(iubenda()->options['tc'], 'button_position')]
                ]
            ],
            'cons' => [
                'status' => false,
                'configured' => iub_array_get(iubenda()->options['cons'], 'configured'),
                'label' => __('Consent Solution', 'iubenda'),
                'name' => 'consent',
                'key' => 'iubenda_consent_solution',
            ],
        ];

    }

    /**
     * Return error to appear alert modal
     * @param $index
     * @param $section
     */
    public function return_alert( $index ,$section) {
        $response = $index == 'code_default' ?: "($index)" ;
        echo json_encode(['status' => 'error', 'responseText' => "invalid script {$response}", 'focus' =>  "#{$index}-{$section}_tab" ]);
        wp_die();
    }

    /**
     * Check embed code if empty or not valid
     * @param $index
     * @param $option
     * @param $section
     * @return bool
     */
    public function check_embed_code($index, $option, $section)
    {
        if(substr( $index, 0, 5 ) === "code_" && empty($option)){
            return false;
        }

        if($section == 'iubenda_privacy_policy_solution' || $section == 'iubenda_terms_conditions_solution'){
            if(!iubenda()->parse_tc_pp_configuration(stripslashes_deep($option))){
                return false;
            }
        }

        if($section == 'iubenda_cookie_law_solution' && substr( $index, 0, 5 ) === "code_"){
            return !empty($option);
        }

        return true;
    }

    /**
     * Getting main div in frontpage with updated data
     */
    public function get_frontpage_main_box()
    {
        require_once IUBENDA_PLUGIN_PATH . '/views/partials/frontpage_main_box.php';
        wp_die();
    }

    /**
     * Hide all notices except iubenda notice
     */
    function iubdena_hide_notices_wp()
    {
        ?>
        <style>
            .error, .notice:not(.iubenda-notice) {
                display: none;
            }
        </style>
        <?php
    }

    /**
     * @param $products
     * @param $data
     * @return array
     */
    public function init_prepare_product_options($products, $data)
    {
        $result = [];

        foreach ($products as $product_name => $product_key) {
            $product_option = [];

            if(iub_array_get($data, "{$product_name}_status") && iub_array_get($data, "{$product_name}_status") == 'true'){
                $result['iubenda_activated_products'][$product_name] = 'true';
                $product_option['configured'] = 'true';

                // Check if product is CONS
                if ($product_key == 'cons') {
                    // iubenda_consent_solution saving data
                    if(iub_array_get($data, "{$product_name}.public_api_key") ?: null){
                        $product_option = ['public_api_key' => iub_array_get($data, "{$product_name}.public_api_key")];
                    }else{
                        $result['iubenda_activated_products'][$product_name] = 'false';
                    }
                }

                // Check if product in ['PP', 'CS', 'TC'] to check and validate embed codes
                if (in_array($product_key, ['pp', 'cs', 'tc'])) {
                    $languages = (new ProductHelper())->get_languages();
                    foreach ( $languages as $lang_id => $lang_name ) {
                        $code = iub_array_get($data, "{$product_name}.code_{$lang_id}");

                        //check if code is empty or code is invalid
                        $result['codes_statues']["{$product_name}_codes"][] = $this->check_embed_code("code_{$lang_id}", $code , $product_name);

                        //get public_id & site_id if only the product key is CS and had a valid embed code
                        if ($product_key == 'cs' && $parsed_code = iubenda()->parse_configuration(stripslashes_deep($code))) {
                            //getting site id to save it into Iubenda global option
                            if (iub_array_get($parsed_code, 'siteId') ?: null) {
                                $result['site_id'] = iub_array_get($parsed_code, 'siteId');
                            }

                            //getting public id to save it into Iubenda global option by lang
                            if (iub_array_get($parsed_code, 'cookiePolicyId') ?: null) {
                                $result['public_ids'][$lang_id] = iub_array_get($parsed_code, 'cookiePolicyId');
                            }
                        }

                        if (in_array($product_key, ['pp', 'tc'])) {
                            $parsed_code = iubenda()->parse_tc_pp_configuration(stripslashes_deep($code));

                            //getting public id to save it into Iubenda global option lang
                            if ($parsed_code) {
                                $result['public_ids'][$lang_id] = iub_array_get($parsed_code, 'cookie_policy_id');
                                $product_option['button_style'] = iub_array_get($parsed_code, 'button_style');
                            }

                            //to make tc/pp button appear in footer by default
                            $product_option['button_position'] = 'automatic';

                            // Add a widget in the sidebar
                            iubenda()->assign_legal_block_or_widget();
                        }

                        $product_option["code_{$lang_id}"] =  stripslashes($code);
                        $product_option["manual_code_{$lang_id}"] =  stripslashes($code);
                    }
                }


                if (in_array($product_key, ['pp', 'tc'])) {
                    // Add a widget in the sidebar if the button is positioned automatically
                    iubenda()->assign_legal_block_or_widget();
                }

                //add version if Iubenda privacy policy solution activated
                if ($product_key == 'pp') {
                    $product_option["version"] = 'Manual';
                }

                // Send options to save it
                $result['products_option'][$product_key] = $product_option;
            }else{
                $result['iubenda_activated_products'][$product_name] = 'false';
            }
        }

        return $result;
    }


    /**
     * @param $products
     * @param $data
     * @return array
     */
    public function init_prepare_product_options_while_upgrading($products, $data)
    {
        $result = [];

        foreach ($products as $product_name => $product_key) {
            $product_option = [];

            if(iub_array_get($data, "{$product_name}_status") && iub_array_get($data, "{$product_name}_status") == 'true'){
                $result['iubenda_activated_products'][$product_name] = 'true';
                $product_option['configured'] = 'true';

                // Check if product is CONS
                if ($product_key == 'cons') {
                    // iubenda_consent_solution saving data
                    if(iub_array_get($data, "{$product_name}.public_api_key") ?: null){
                        $product_option = ['public_api_key' => iub_array_get($data, "{$product_name}.public_api_key")];
                    }else{
                        $result['iubenda_activated_products'][$product_name] = 'false';
                    }
                }

                // Check if product in ['PP', 'CS', 'TC'] to check and validate embed codes
                if (in_array($product_key, ['pp', 'cs', 'tc'])) {
                    $languages = (new ProductHelper())->get_languages();
                    foreach ( $languages as $lang_id => $lang_name ) {
                        $code = iub_array_get($data, "{$product_name}.code_{$lang_id}");

                        //check if code is empty or code is invalid
                        $result['codes_statues']["{$product_name}_codes"][] = !empty($code);

                        //get public_id & site_id if only the product key is CS and had a valid embed code
                        if ($product_key == 'cs' && $parsed_code = iubenda()->parse_configuration(stripslashes_deep($code))) {
                            //getting site id to save it into Iubenda global option
                            if (iub_array_get($parsed_code, 'siteId') ?: null) {
                                $result['site_id'] = iub_array_get($parsed_code, 'siteId');
                            }

                            //getting public id to save it into Iubenda global option by lang
                            if (iub_array_get($parsed_code, 'cookiePolicyId') ?: null) {
                                $result['public_ids'][$lang_id] = iub_array_get($parsed_code, 'cookiePolicyId');
                            }
                        }

                        if (in_array($product_key, ['pp', 'tc'])) {
                            $parsed_code = iubenda()->parse_tc_pp_configuration(stripslashes_deep($code));

                            //getting public id to save it into Iubenda global option lang
                            if ($parsed_code) {
                                $result['public_ids'][$lang_id] = iub_array_get($parsed_code, 'cookie_policy_id');
                                $product_option['button_style'] = iub_array_get($parsed_code, 'button_style');
                            }

                            //to make tc/pp button appear in footer by default
                            $product_option['button_position'] = 'automatic';

                            // Add a widget in the sidebar
                            iubenda()->assign_legal_block_or_widget();
                        }

                        $product_option["code_{$lang_id}"] =  stripslashes($code);
                        $product_option["manual_code_{$lang_id}"] =  stripslashes($code);
                    }
                }


                if (in_array($product_key, ['pp', 'tc'])) {
                    // Add a widget in the sidebar if the button is positioned automatically
                    iubenda()->assign_legal_block_or_widget();
                }

                //add version if Iubenda privacy policy solution activated
                if ($product_key == 'pp') {
                    $product_option["version"] = 'Manual';
                }

                // Send options to save it
                $result['products_option'][$product_key] = $product_option;
            }else{
                $result['iubenda_activated_products'][$product_name] = 'false';
            }
        }

        return $result;
    }

    public function save_init_prepared_product_options($products, $result)
    {
        // Getting product option to save it
        foreach ($products as $product_name => $product_key) {
            $product_status = iub_array_get($result, "iubenda_activated_products.{$product_name}", 'false') ?: 'false';
            if($product_status == 'false'){
                continue;
            }

            $product_option = iub_array_get($result, "products_option.{$product_key}", []) ?: [];

            // Merging old $product_name options with new options
            update_option( $product_name, array_merge(iubenda()->options[$product_key] ?: [], $product_option));

            // Update Iubenda instance with new $product_name options
            iubenda()->options[$product_key] = array_merge(iubenda()->options[$product_key] ?: [], $product_option);
        }

        // Merging old iubenda activated products with new
        $old_iubenda_activated_products = iub_array_get(iubenda()->options, 'activated_products', []) ?: [];
        $new_iubenda_activated_products = iub_array_get($result, 'iubenda_activated_products', []) ?: [];
        update_option( 'iubenda_activated_products', array_merge($old_iubenda_activated_products, $new_iubenda_activated_products));

        // Update Iubenda instance with new activated products
        iubenda()->options['activated_products'] = array_merge($old_iubenda_activated_products, $new_iubenda_activated_products);

        // Merging old iubenda global options with new
        $old_iubenda_global_options = iub_array_get(iubenda()->options, 'global_options', []) ?: [];

        $new_iubenda_global_options = [];
        if(iub_array_get($result, 'site_id') ?: null){
            $new_iubenda_global_options['site_id'] = iub_array_get($result, 'site_id');
        }
        if(iub_array_get($result, 'public_ids', []) ?: null){
            $new_iubenda_global_options['public_ids'] = iub_array_get($result, 'public_ids', []);
        }
        update_option( 'iubenda_global_options', array_merge($old_iubenda_global_options, $new_iubenda_global_options));
        iubenda()->options['global_options'] = array_merge($old_iubenda_global_options, $new_iubenda_global_options);

        $this->load_defaults();
    }
}
