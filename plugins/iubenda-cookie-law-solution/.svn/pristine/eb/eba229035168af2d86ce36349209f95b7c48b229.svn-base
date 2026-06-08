<?php
/*
  Plugin Name: Cookie and Consent Solution for the GDPR & ePrivacy
  Plugin URI: https://www.iubenda.com
  Description: The iubenda plugin is an <strong>all-in-one</strong>, extremely easy to use 360° compliance solution, with text crafted by actual lawyers, that quickly <strong>scans your site and auto-configures to match your specific setup</strong>.  It supports the GDPR (DSGVO, RGPD), UK-GDPR, ePrivacy, LGPD, CCPA, CalOPPA, PECR and more.
  Version: 3.3.2
  Author: iubenda
  Author URI: https://www.iubenda.com
  License: MIT License
  License URI: http://opensource.org/licenses/MIT
  Text Domain: iubenda
  Domain Path: /languages

  Cookie and Consent Solution for the GDPR & ePrivacy
  Copyright (C) 2018-2020, iubenda s.r.l

  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

// exit if accessed directly
if ( ! defined( 'ABSPATH' ) )
	exit;

// define contants
define( 'IUB_DEBUG', false );

/**
 * iubenda final class.
 *
 * @property-read iubenda_Settings $settings
 * @property IubendaLegalWidget $widget
 * @property IubendaLegalBlock $block
 *
 * @class iubenda
 * @version	3.3.2
 */
class iubenda {

    /**
     * @var ServiceRating
     */
    public $serviceRating;

	private static $instance;
	public $options = array();
	public $defaults = array(
		'cs' => array(
			'parse'				=> true, // iubenda_parse
			'skip_parsing'		=> false, // skip_parsing
            'ctype'				=> true, // iubenda_ctype
            'parser_engine'		=> 'new', // parser_engine
            'output_feed'		=> true, // iubenda_output_feed
            'output_post'		=> true,
			'code_default'		=> false, // iubenda-code-default,
			'menu_position'		=> 'topmenu',
			'amp_support'		=> false,
			'amp_source'		=> 'local',
			'amp_template_done' => false,
			'amp_template'		=> '',
			'custom_scripts'	=> array(),
			'custom_iframes'	=> array(),
			'deactivation'		=> false,
			'configuration_type'=> 'manual',
			'simplified'        => [
                'position'              => 'float-top-center',
			    'background_overlay'    => false,
			    'banner_style'          => 'dark',
			    'legislation'           => 'gdpr',
			    'require_consent'       => 'worldwide',
			    'explicit_accept'       => true,
			    'explicit_reject'       => true,
            ]
		),
        'pp' => array(
			'version'			=> '', // Simplified / Embed Code
			'parse'				=> false, // iubenda_parse
			'deactivation'		=> false,
			'button_style'		=> 'white',
			'button_position'	=> 'automatic'
		),
        'tc' => array(
			'parse'				=> false, // iubenda_parse
			'deactivation'		=> false,
            'button_style'		=> 'white',
			'button_position'   => 'automatic'
		),
		'cons' => array(
			'public_api_key' => '',
			'cons_endpoint' => 'https://consent.iubenda.com/public/consent',
		)
	);
	public $base_url;
	public $version = '3.3.2';
	public $activation = array(
		'update_version'	=> 0,
		'update_notice'		=> true,
		'update_date'		=> '',
		'update_delay_date'	=> 0
	);
	public $no_html = false;
	public $multilang = false;
	public $languages = array();
	public $languages_locale = array();
	public $lang_default = '';
	public $lang_current = '';
    public $lang_mapping = [
        //wordpress language    //iubenda language
        'nl_NL'                 =>'nl',
        'en_US'                 =>'en',
        'en_UK'                 =>'en',
        'en_GB'                 =>'en-GB',
        'fr_FR'                 =>'fr',
        'de_DE'                 =>'de',
        'it_IT'                 =>'it',
        'pt_BR'                 =>'pt-BR',
        'pt_PT'                 =>'pt',
        'ru_RU'                 =>'ru',
        'es_ES'                 =>'es',
    ];
    public $supported_languages = [
        'nl'        => 'Dutch',
        'en'        => 'English (US)',
        'en-GB'     => 'English (UK)',
        'fr'        => 'French',
        'de'        => 'German',
        'it'        => 'Italian',
        'pt-BR'     => 'Portuguese (BR)',
        'pt'        => 'Portuguese',
        'ru'        => 'Russian',
        'es'        => 'Spanish',
    ];

	/**
	 * Disable object clone.
	 */
	public function __clone() {
		throw new Exception( 'Cloning is not allowed for ' . __CLASS__ );
	}

	/**
	 * Disable unserializing of the class.
	 */
	public function __wakeup() {
		throw new Exception( 'Serializing is disabled for class ' . __CLASS__ );
	}

	/**
	 * Main plugin instance,
	 * Insures that only one instance of the plugin exists in memory at one time.
	 *
	 * @return object
	 */
	public static function instance() {
		if ( ! isset( self::$instance ) && ! ( self::$instance instanceof iubenda ) ) {

			self::$instance = new iubenda;
			self::$instance->define_constants();

			add_action( 'plugins_loaded', array( self::$instance, 'load_textdomain' ) );
			add_action( 'plugins_loaded', array( self::$instance, 'init' ) );

			self::$instance->includes();
            self::$instance->serviceRating = new ServiceRating();

			self::$instance->AMP = new iubenda_AMP();
			self::$instance->forms = new iubenda_Forms();
			self::$instance->settings = new iubenda_Settings();
			self::$instance->widget = new IubendaLegalWidget();
			self::$instance->block = new IubendaLegalBlock();
		}

		return self::$instance;
	}

	/**
	 * Class constructor.
	 */
	public function __construct() {
		register_activation_hook( __FILE__, array( $this, 'activation' ) );
		register_deactivation_hook( __FILE__, array( $this, 'deactivation' ) );

		// settings
		$cs_options = (array) get_option( 'iubenda_cookie_law_solution', $this->defaults['cs'] );
		$pp_options = (array) get_option( 'iubenda_privacy_policy_solution', $this->defaults['pp'] );
		$tc_options = (array) get_option( 'iubenda_terms_conditions_solution', $this->defaults['tc'] );
		$cons_options = (array) get_option( 'iubenda_consent_solution', $this->defaults['cons'] );

		// activate AMP if not available before
		if ( function_exists( 'is_amp_endpoint' ) || function_exists( 'ampforwp_is_amp_endpoint' ) ) {
			if ( ! isset( $cs_options['amp_support'] ) )
				$this->defaults['cs']['amp_support'] = true;
		}

		$this->options['cs'] = array_merge( $this->defaults['cs'], $cs_options );
		$this->options['pp'] = array_merge( $this->defaults['pp'], $pp_options );
		$this->options['tc'] = array_merge( $this->defaults['tc'], $tc_options );
		$this->options['cons'] = array_merge( $this->defaults['cons'], $cons_options );
		$this->options['activated_products'] = get_option( 'iubenda_activated_products', [] ) ?: [];
		$this->options['global_options'] = get_option( 'iubenda_global_options', [] ) ?: [];

		$this->base_url = esc_url_raw( add_query_arg( 'page', 'iubenda', admin_url( $this->options['cs']['menu_position'] === 'submenu' ? 'options-general.php' : 'admin.php' ) ) );

		// actions
		add_action( 'after_setup_theme', array( $this, 'register_shortcode' ) );
		add_action( 'wp_head', array( $this, 'wp_head_cs' ), 0 );
		add_action( 'wp_head', array( $this, 'wp_head_cons' ), 1 );
		add_action( 'template_redirect', array( $this, 'output_start' ), 0 );
		add_action( 'shutdown', array( $this, 'output_end' ), 100 );
		add_action( 'template_redirect', array( $this, 'disable_jetpack_tracking' ) );
		add_action( 'admin_init', array( $this, 'maybe_do_upgrade' ) );
		add_action( 'admin_init', array( $this, 'check_iubenda_version' ) );
		add_action( 'upgrader_process_complete', array( $this, 'upgrade' ), 10, 2 );
		add_filter( 'plugin_action_links', array($this, 'plugin_action_links'), 10, 5 );
        add_action( 'upgrader_overwrote_package', array( $this, 'do_upgrade_processes' ) );
        add_action( 'after_switch_theme', array($this, 'assign_legal_block_or_widget'));
    }

	/**
	 * Append settings to plugin action link
	 *
	 * @param $actions
	 * @param $plugin_file
	 *
	 * @return array|mixed
	 */
	public function plugin_action_links( $actions, $plugin_file ) {
		static $plugin;
		if ( ! isset( $plugin ) ) {
			$plugin = plugin_basename( __FILE__ );
		}

		if ( $plugin === $plugin_file ) {
			$menu_page = esc_url_raw( add_query_arg( 'page', 'iubenda', admin_url( $this->options['cs']['menu_position'] === 'submenu' ? 'options-general.php' : 'admin.php' ) ) );
			$settings = array( 'settings' => "<a href='{$menu_page}'>" . esc_html__( 'Settings', 'iubenda' ) . '</a>' );
			$actions  = array_merge( $actions, $settings );
		}

		return $actions;
	}

	/**
	 * Setup plugin constants.
	 *
	 * @return void
	 */
	private function define_constants() {
		define( 'IUBENDA_PLUGIN_URL', plugins_url( '', __FILE__ ) );
		define( 'IUBENDA_PLUGIN_REL_PATH', dirname( plugin_basename( __FILE__ ) ) . '/' );
		define( 'IUBENDA_PLUGIN_PATH', plugin_dir_path( __FILE__ ) );
	}

	/**
	 * Include required files.
	 *
	 * @return void
	 */
	private function includes() {
		include_once( IUBENDA_PLUGIN_PATH . 'includes/settings.php' );
		include_once( IUBENDA_PLUGIN_PATH . 'includes/forms.php' );
        include_once( IUBENDA_PLUGIN_PATH . 'includes/amp.php' );
        include_once( IUBENDA_PLUGIN_PATH . 'includes/QuickGeneratorService.php' );
        include_once( IUBENDA_PLUGIN_PATH . 'includes/RadarService.php' );
        include_once( IUBENDA_PLUGIN_PATH . 'includes/CookieSolutionGenerator.php' );
        include_once( IUBENDA_PLUGIN_PATH . 'includes/PrivacyPolicyGenerator.php' );
        include_once( IUBENDA_PLUGIN_PATH . 'includes/ServiceRating.php' );
        include_once( IUBENDA_PLUGIN_PATH . 'includes/widget/IubendaLegalWidget.php' );
        include_once( IUBENDA_PLUGIN_PATH . 'includes/block/IubendaLegalBlock.php' );
        include_once( IUBENDA_PLUGIN_PATH . 'includes/ProductHelper.php' );
        include_once( IUBENDA_PLUGIN_PATH . 'includes/LanguageHelper.php' );
    }

	/**
	 * Initialize plugin.
	 *
	 * @return void
	 */
	public function init() {
		// check if WPML or Polylang is active
		include_once( ABSPATH . 'wp-admin/includes/plugin.php' );

		// Polylang support
		if ( ( is_plugin_active( 'polylang/polylang.php' ) || is_plugin_active( 'polylang-pro/polylang.php' ) ) && function_exists( 'PLL' ) ) {
			$this->multilang = true;

			// get registered languages
			$registered_languages = PLL()->model->get_languages_list();

			if ( ! empty( $registered_languages ) ) {
				foreach ( $registered_languages as $language ){
                    $this->languages[$language->slug] = $language->name;
                    $this->languages_locale[$language->locale] = $language->slug;
				}
			}

			// get default language
			$this->lang_default = pll_default_language();
			// get current language
			$this->lang_current = pll_current_language();

			// WPML support
		} elseif ( is_plugin_active( 'sitepress-multilingual-cms/sitepress.php' ) && class_exists( 'SitePress' ) ) {
			$this->multilang = true;

			global $sitepress;

			// get registered languages
			$registered_languages = icl_get_languages();

			if ( ! empty( $registered_languages ) ) {
                foreach ( $registered_languages as $language ){
                    $this->languages[$language['code']] = $language['display_name'];
                    $this->languages_locale[$language['default_locale']] = $language['code'];
                }
            }

			// get default language
			$this->lang_default = $sitepress->get_default_language();
			// get current language
			$this->lang_current = $sitepress->get_current_language();
		}else{
            // if no plugin for multi lang installed
            $this->lang_default = iub_array_get(iubenda()->lang_mapping, get_locale(), 'en');
            $this->lang_current = iub_array_get(iubenda()->lang_mapping, get_locale());
        }

		// load iubenda parser
		include_once( dirname( __FILE__ ) . '/iubenda-cookie-class/iubenda.class.php' );
	}

	/**
	 * Plugin activation.
	 *
	 * @return void
	 */
	public function activation() {
        // Check Iubenda version on plugin activation
        $this->check_iubenda_version();

		set_transient( 'iub_activation_completed', 1, 3600 );

        add_option( 'iubenda_cookie_law_solution', $this->options['cs'], '', 'no' );
        add_option( 'iubenda_cookie_law_solution', $this->options['cons'], '', 'no' );
        update_option( 'iubenda_cookie_law_version', $this->version, 'no' );
		add_option( 'iubenda_activation_data', $this->activation, '', 'no' );

        // Send a radar request on plugin activation.
        $radar = new RadarService;
        $radar->ask_radar_to_send_request();
	}

	/**
	 * Plugin deactivation.
	 *
	 * @return void
	 */
	public function deactivation() {
		// remove options from database?
		if ( $this->options['cs']['deactivation'] ) {
            delete_option( 'iubenda_activated_products' );
            delete_option( 'iubenda_activation_data' );
            delete_option( 'iubenda_consent_forms' );
            delete_option( 'iubenda_consent_solution' );
            delete_option( 'iubenda_cookie_law_solution' );
            delete_option( 'iubenda_cookie_law_version' );
            delete_option( 'iubenda_cs_page_configuration' );
            delete_option( 'iubenda_pp_page_configuration' );
            delete_option( 'iubenda_privacy_policy_solution' );
            delete_option( 'iubenda_quick_generator_response' );
            delete_option( 'iubenda_tc_page_configuration' );
            delete_option( 'iubenda_terms_conditions_solution' );
            delete_option( iubenda_Settings::IUB_NOTIFICATIONS );

            // Detach iubenda legal block from footer
            $this->block->detach_legal_block_from_footer();
		}

        // remove radar options from database
        delete_option( 'iubenda_radar_api_configuration' );
        delete_option( 'iubenda_radar_api_response' );
	}

	/**
	 * Plugin upgrae.
	 *
	 * @return void
	 */
	public function upgrade( $upgrader_object, $options ) {
		// if an update has taken place and the updated type is plugins and the plugins element exists
		if ( 'update' == $options['action']  &&  'plugin' == $options['type'] ) {
			$this->set_transient_flag_on_plugin_upgrade( $options );
		}
	}

	/**
	 * Set the transient flag on the plugin upgrade/update
	 *
	 * @param array $options
	 *
	 * @return void
	 */
	private function set_transient_flag_on_plugin_upgrade( $options ) {
		// the path to our plugin's main file
		$our_plugin = plugin_basename( __FILE__ );

		// Check our plugin is there and being updated
		if ( isset( $options['plugins'] ) && is_array( $options['plugins'] ) && in_array( $our_plugin, $options['plugins'] ) ) {

			// set a transient to record that our plugin has just been updated
			set_transient( 'iub_upgrade_completed', 1, 3600 );
			return;
		}

		// Check our plugin is there and being updated
		if ( isset( $options['plugin'] ) && __FILE__ == $options['plugin'] ) {
			set_transient( 'iub_upgrade_completed', 1, 3600 );
		}
	}

	/**
	 * Load textdomain.
	 *
	 * @return void
	 */
	public function load_textdomain() {
		load_plugin_textdomain( 'iubenda', false, IUBENDA_PLUGIN_REL_PATH . 'languages/' );
	}

	/**
	 * Register shortcode function.
	 *
	 * @return void
	 */
	public function register_shortcode() {
		add_shortcode( 'iub-cookie-policy', array( $this, 'block_shortcode' ) );
		add_shortcode( 'iub-cookie-block', array( $this, 'block_shortcode' ) );
		add_shortcode( 'iub-cookie-skip', array( $this, 'skip_shortcode' ) );
	}

	/**
	 * Handle block shortcode function.
	 *
	 * @param array $atts
	 * @param mixed $content
	 * @return mixed
	 */
	public function block_shortcode( $atts, $content = '' ) {
		return '<!--IUB-COOKIE-BLOCK-START-->' . do_shortcode( $content ) . '<!--IUB-COOKIE-BLOCK-END-->';
	}

	/**
	 * Handle skip shortcode function.
	 *
	 * @param array $atts
	 * @param mixed $content
	 * @return mixed
	 */
	public function skip_shortcode( $atts, $content = '' ) {
		return '<!--IUB-COOKIE-BLOCK-SKIP-START-->' . do_shortcode( $content ) . '<!--IUB-COOKIE-BLOCK-SKIP-END-->';
	}

	/**
	 * Add wp_head cookie solution content.
	 *
	 * @return mixed
	 */
	public function wp_head_cs() {
        if (!$this->is_cs_service_enabled_and_configured()) {
	        return;
	    }

		// check content type
		if ( (bool) $this->options['cs']['ctype'] == true ) {
			$iub_headers = headers_list();
			$destroy = true;

			foreach ( $iub_headers as $header ) {
				if ( strpos( $header, "Content-Type: text/html" ) !== false || strpos( $header, "Content-type: text/html" ) !== false ) {
					$destroy = false;
					break;
				}
			}

			if ( $destroy )
				$this->no_html = true;
		}

		// is post or not html content type?
		if ( ( $_POST && $this->options['cs']['output_post'] ) || $this->no_html )
			return;

        // bail if current page is page builder of Divi by elegant themes
        if ( function_exists( 'et_fb_is_enabled' ) && et_fb_is_enabled() ) {
            return;
        }

        // bail if current page is builder frame of (Fusion/Avada) theme
        if ( function_exists( 'fusion_is_builder_frame' ) && fusion_is_builder_frame() ) {
            return;
        }

		// initial head output
		$iubenda_code = '';

        // Check if there is multi language plugin installed and activated
        if ( $this->multilang === true && defined( 'ICL_LANGUAGE_CODE' ) && isset( $this->options['cs']['code_' . ICL_LANGUAGE_CODE] ) ) {
            $iubenda_code .= $this->options['cs']['code_' . ICL_LANGUAGE_CODE];

            // no code for current language, use default
            if ( ! $iubenda_code )
                $iubenda_code .= $this->options['cs']['code_default'];
        } else{
            $iubenda_code .= $this->options['cs']['code_default'];
        }

		$iubenda_code = $this->parse_code( $iubenda_code, true );

		if ( $iubenda_code !== '' ) {
			$iubenda_code .= "\n
			<script>
				var iCallback = function() {};
				var _iub = _iub || {};

				if ( typeof _iub.csConfiguration != 'undefined' ) {
					if ( 'callback' in _iub.csConfiguration ) {
						if ( 'onConsentGiven' in _iub.csConfiguration.callback )
							iCallback = _iub.csConfiguration.callback.onConsentGiven;

						_iub.csConfiguration.callback.onConsentGiven = function() {
							iCallback();

							/* separator */
							jQuery('noscript._no_script_iub').each(function (a, b) { var el = jQuery(b); el.after(el.html()); });
						}
					}
				}
			</script>";

			echo '<!--IUB-COOKIE-SKIP-START-->' . $iubenda_code . '<!--IUB-COOKIE-SKIP-END-->';
		}
	}

	/**
	 * Add wp_head consent solution content.
	 *
	 * @return mixed
	 */
	public function wp_head_cons() {
		if ( ! empty( $this->options['cons']['public_api_key'] ) ) {

			$parameters = apply_filters( 'iubenda_cons_init_parameters', array(
				'log_level'			 => 'error',
				'logger'			 => 'console',
				'send_from_local'	 => true
			) );

			echo '<!-- Library initialization -->
			<script type="text/javascript">
				var _iub = _iub || { };

				_iub.cons_instructions = _iub.cons_instructions || [ ];
				_iub.cons_instructions.push(
					[ "init", {
							api_key: "' . $this->options['cons']['public_api_key'] . '",
							log_level: "' . $parameters['log_level'] . '",
							logger: "' . ( ! empty( $parameters['logger'] ) && in_array( $parameters['logger'], array( 'console', 'none' ) ) ? $parameters['logger'] : 'console' ) . '",
							sendFromLocalStorageAtLoad: ' . ( (bool) ( $parameters['send_from_local'] ) ? 'true' : 'false' ) . '
						}, function ( ) {
							// console.log( "init callBack" );
						}
					]
				);
			</script>
			<script type="text/javascript" src="//cdn.iubenda.com/cons/iubenda_cons.js" async></script>';
		}
	}

	/**
	 * Initialize html output.
	 *
	 * @return void
	 */
	public function output_start() {
		if ( ! is_admin() )
			ob_start( array( $this, 'output_callback' ) );
	}

	/**
	 * Finish html output.
	 *
	 * @return void
	 */
	public function output_end() {
		if ( ! is_admin() && ob_get_level() )
			ob_end_flush();
	}

	/**
	 * Handle final html output.
	 *
	 * @param mixed $output
	 * @return mixed
	 */
	public function output_callback( $output ) {
		// check whether to run parser or not
		// bail on ajax, xmlrpc or iub_no_parse request
		if (
		( defined( 'XMLRPC_REQUEST' ) && XMLRPC_REQUEST ) || ( defined( 'DOING_AJAX' ) && DOING_AJAX ) || isset( $_SERVER["HTTP_X_REQUESTED_WITH"] ) || isset( $_GET['iub_no_parse'] )
		)
			return $output;

        if (!$this->is_cs_service_enabled_and_configured()) {
            return $output;
        }

		// bail on admin side
		if ( is_admin() )
			return $output;

		// bail on rss feed
		if ( is_feed() && $this->options['cs']['output_feed'] )
			return $output;

		if ( strpos( $output, "<html" ) === false )
			return $output;
		elseif ( strpos( $output, "<html" ) > 200 )
			return $output;

		// bail if skripts blocking disabled
		if ( ! $this->options['cs']['parse'] )
			return $output;

		// bail if consent given and skip parsing enabled
		if ( iubendaParser::consent_given() && $this->options['cs']['skip_parsing'] )
			return $output;

		// bail on POST request
		if ( $_POST && $this->options['cs']['output_post'] )
			return $output;

		// bail if bot detectd, no html in output or it's a post request
		if ( iubendaParser::bot_detected() || $this->no_html )
			return $output;

		// bail if current page is page builder of Divi by elegant themes
		if ( function_exists( 'et_fb_is_enabled' ) && et_fb_is_enabled() ) {
			return $output;
		}

        // bail if current page is builder frame of (Fusion/Avada) theme
        if ( function_exists( 'fusion_is_builder_frame' ) && fusion_is_builder_frame() ) {
            return $output;
        }

        // bail if the current page is page builder for any theme
        if (is_customize_preview()) {
            return $output;
        }

		// google recaptcha v3 compatibility
		if ( class_exists( 'WPCF7' ) && (int) WPCF7::get_option( 'iqfix_recaptcha' ) === 0 && ! iubendaParser::consent_given() )
			$this->options['cs']['custom_scripts']['grecaptcha'] = 2;

		// Jetpack compatibility
		if ( class_exists( 'Jetpack' ) )
			$this->options['cs']['custom_scripts']['stats.wp.com'] = 5;

		$startime = microtime( true );
		$output = apply_filters( 'iubenda_initial_output', $output );

		// prepare scripts and iframes
		$scripts = $this->prepare_custom_data( $this->options['cs']['custom_scripts'] );
		$iframes = $this->prepare_custom_data( $this->options['cs']['custom_iframes'] );

        // Check if the current language have a valid CS code or not
        if (!(new ProductHelper())->check_iub_cs_code_exists_current_lang()) {
            return $output;
        }

		// experimental class
		if ( $this->options['cs']['parser_engine'] == 'new' ) {
			$iubenda = new iubendaParser( mb_convert_encoding( $output, 'HTML-ENTITIES', 'UTF-8' ), array(
				'type' => 'faster',
				'amp' => $this->options['cs']['amp_support'],
				'scripts' => $scripts,
				'iframes' => $iframes
			) );

			// render output
			$output = $iubenda->parse();

			// append signature
			$output .= '<!-- Parsed with iubenda experimental class in ' . round( microtime( true ) - $startime, 4 ) . ' sec. -->';
			// default class
		} else {
			$iubenda = new iubendaParser( $output, array(
				'type' => 'page',
				'amp' => $this->options['cs']['amp_support'],
				'scripts' => $scripts,
				'iframes' => $iframes
			) );

			// render output
			$output = $iubenda->parse();

			// append signature
			$output .= '<!-- Parsed with iubenda default class in ' . round( microtime( true ) - $startime, 4 ) . ' sec. -->';
		}

		return apply_filters( 'iubenda_final_output', $output );
	}

	/**
	 * Prepare scripts/iframes.
	 *
	 * @param array $data
	 * @return array
	 */
	public function prepare_custom_data( $data ) {
		$newdata = array();

		foreach ( $data as $script => $type ) {
			if ( ! array_key_exists( $type, $newdata ) )
				$newdata[$type] = array();

			$newdata[$type][] = $script;
		}

		return $newdata;
	}

	/**
	 * Parse iubenda code.
	 *
	 * @param string $source
	 * @param bool $display
	 * @return string
	 */
	public function parse_code( $source, $display = false ) {
		// return $source;
        $source = trim( $source ?: '' );

		preg_match_all( '/(\"(?:html|content)\"(?:\s+)?\:(?:\s+)?)\"((?:.*?)(?:[^\\\\]))\"/s', $source, $matches );

		// found subgroup?
		if ( ! empty( $matches[1] ) && ! empty( $matches[2] ) ) {
			foreach ( $matches[2] as $no => $match ) {
				$source = str_replace( $matches[0][$no], $matches[1][$no] . '[[IUBENDA_TAG_START]]' . $match . '[[IUBENDA_TAG_END]]', $source );
			}

			// kses it
			$source = wp_kses( $source, $this->get_allowed_html() );

			preg_match_all( '/\[\[IUBENDA_TAG_START\]\](.*?)\[\[IUBENDA_TAG_END\]\]/s', $source, $matches_tags );

			if ( ! empty( $matches_tags[1] ) ) {
				foreach ( $matches_tags[1] as $no => $match ) {
					$source = str_replace( $matches_tags[0][$no], '"' . ( $display ? str_replace( '</', '<\/', $matches[2][$no] ) : $matches[2][$no] ) . '"', $source );
				}
			}
		}

		return $source;
	}

	/**
	 * Disable Jetpack tracking on AMO cached pages.
	 *
	 * @return void
	 */
	public function disable_jetpack_tracking() {
		// bail no Jetpack active
		if ( ! class_exists( 'Jetpack' ) )
			return;

		// disable if it's not AMP cached request
		if ( ! class_exists( 'Jetpack_AMP_Support' ) || ! Jetpack_AMP_Support::is_amp_request() )
			return;

		// if ( is_feed() || is_robots() || is_trackback() || is_preview() || jetpack_is_dnt_enabled() )
		// bail if skripts blocking disabled
		if ( ! $this->options['cs']['parse'] )
			return;

		// bail if consent given and skip parsing enabled
		if ( iubendaParser::consent_given() && $this->options['cs']['skip_parsing'] )
			return;

		remove_action( 'wp_head', 'stats_add_shutdown_action' );
		remove_action( 'wp_footer', 'stats_footer', 101 );
	}

	/**
	 * Perform actions on plugin installation/upgrade.
	 *
	 * @return void
	 */
	public function maybe_do_upgrade() {
		if ( ! current_user_can( 'install_plugins' ) )
			return;

		// bail if no activation or upgrade transient is set
		if ( ! get_transient( 'iub_upgrade_completed' ) && ! get_transient( 'iub_activation_completed' ) )
			return;

		// delete the activation transient
		delete_transient( 'iub_activation_completed' );
		// delete the upgrade transient
		delete_transient( 'iub_upgrade_completed' );

		// bail if activating from network, or bulk, or within an iFrame
		if ( is_network_admin() || isset( $_GET['activate-multi'] ) || defined( 'IFRAME_REQUEST' ) )
			return;

		// generate AMP template file if AMP plugins available
		if ( function_exists( 'is_amp_endpoint' ) || function_exists( 'ampforwp_is_amp_endpoint' ) ) {
			$this->regenerate_amp_templates();
		}

        // Sending a radar request when installing the plugin for the first time
        $radar = new RadarService;
        $radar->ask_radar_to_send_request();
	}


	/**
	 * Compare Iubenda plugin versions and
     * do functions if compare result false (DB_version < Current version of plugin files ).
	 *
	 */
    public function check_iubenda_version() {
        if ($this->compare_iub_plugin_versions()){
            // Upgrade processes
            $this->do_upgrade_processes();

            // Update Iubenda plugin version
            $this->update_iubenda_version();
        }
	}

	/**
	 * update Iubenda version in Database.
     *
     * @return void
     */
    private function update_iubenda_version() {
        update_option( 'iubenda_cookie_law_version', $this->version, 'no' );
	}


	/**
	 * Perform processes on plugin upgrade.
	 *
	 * @return void
	 */
	public function do_upgrade_processes() {
        $db_version = get_option( 'iubenda_cookie_law_version' ) ?: '2.5.91';

        // Version 3.0.0 and above
        if ( version_compare( $db_version, '3.0.6', '<' ) ) {
            $this->upgrading_to_ver_3_process();
        }
	}

	/**
	 * Get configuration data parsed from iubenda code
	 *
	 * @param type $iubenda_code
	 * @param type $args
	 * @return type
	 */
	public function parse_configuration( $code, $args = array() ) {
        // Check if the embed code have Callback Functions inside it or not
        if (strpos($code, 'callback') !== false) {
            $code = $this->replace_the_callback_functions_to_parse_configuration($code);
        }

		$configuration = array();
		$defaults = array(
			'mode'	 => 'basic',
			'parse' => false
		);

		// parse incoming $args into an array and merge it with $defaults
		$args = wp_parse_args( $args, $defaults );

		if ( empty( $code ) )
			return $configuration;

		// parse code if needed
		$parsed_code = $args['parse'] === true ? $this->parse_code( $code, true ) : $code;

		// get script
		$parsed_script = '';

		preg_match_all( '/src\=(?:[\"|\'])(.*?)(?:[\"|\'])/', $parsed_code, $matches );

		// find the iubenda script url
		if ( ! empty( $matches[1] ) ) {
			foreach ( $matches[1] as $found_script ) {
				if ( wp_http_validate_url( $found_script ) && strpos( $found_script, 'iubenda_cs.js' ) ) {
					$parsed_script = $found_script;
					continue;
				}
			}
		}

		// strip tags
		$parsed_code = wp_kses( $parsed_code, array() );

		// get configuration
		preg_match( '/_iub.csConfiguration *= *{(.*?)\};/', $parsed_code, $matches );

		if ( ! empty( $matches[1] ) )
			$parsed_code = '{' . $matches[1] . '}';

		// decode
		$decoded = json_decode( $parsed_code, true );

		if ( ! empty( $decoded ) && is_array( $decoded ) ) {

			$decoded['script'] = $parsed_script;

			// basic mode
			if ( $args['mode'] === 'basic' ) {
				if ( isset( $decoded['banner'] ) )
					unset( $decoded['banner'] );
				if ( isset( $decoded['callback'] ) )
					unset( $decoded['callback'] );
				if ( isset( $decoded['perPurposeConsent'] ) )
					unset( $decoded['perPurposeConsent'] );
			// Banner mode to get banner configuration only
			} else if ( 'banner' == $args['mode'] ) {
				if ( isset( $decoded['banner'] ) ) {
					return $decoded['banner'];
				}

				return array();
			}

			$configuration = $decoded;
		}

		return $configuration;
	}

    /**
     * Get configuration data parsed from TC & PP iubenda code
     * @param $code
     * @return array|false
     */
	public function parse_tc_pp_configuration($code) {
        if (empty($code)) {
            return false;
        }

        preg_match_all('/<a[^>]+href=([\'"])(?<href>.+?)\1[^>]*>/i', $code, $result);
        $url = iub_array_get($result, 'href.0');

        if (!$url) {
            return false;
        }


        $button_style = strpos(stripslashes($code), 'iubenda-white') !== false ? 'white' : 'black';
        $cookie_policy_id = basename($url);

        return ['button_style' => $button_style, 'cookie_policy_id' => $cookie_policy_id];
	}

	/**
	 * Domain info helper function.
	 *
	 * @param type $domainb
	 * @return type
	 */
	public function domain( $domainb ) {
		$bits = explode( '/', $domainb );
		if ( $bits[0] == 'http:' || $bits[0] == 'https:' ) {
			$domainb = $bits[2];
		} else {
			$domainb = $bits[0];
		}
		unset( $bits );
		$bits = explode( '.', $domainb );
		$idz = 0;
		while ( isset( $bits[$idz] ) ) {
			$idz += 1;
		}
		$idz -= 3;
		$idy = 0;
		while ( $idy < $idz ) {
			unset( $bits[$idy] );
			$idy += 1;
		}
		$part = array();
		foreach ( $bits AS $bit ) {
			$part[] = $bit;
		}
		unset( $bit );
		unset( $bits );
		unset( $domainb );
		$domainb = '';

		if ( strlen( $part[1] ) > 3 ) {
			unset( $part[0] );
		}
		foreach ( $part AS $bit ) {
			$domainb .= $bit . '.';
		}
		unset( $bit );

		return preg_replace( '/(.*)\./', '$1', $domainb );
	}

	/**
	 * Check if file exists helper function.
	 *
	 * @param type $file
	 */
	public function file_exists( $file ) {
		$file_headers = @get_headers( $file );

		if ( ! $file_headers || $file_headers[0] == 'HTTP/1.1 404 Not Found' ) {
			$exists = false;
		} else {
			$exists = true;
		}
	}

	/**
	 * Get allowed iubenda script HTML.
	 *
	 * @return array
	 */
	public function get_allowed_html() {
		// Jetpack fix
		remove_filter( 'pre_kses', array( 'Filter_Embedded_HTML_Objects', 'filter' ), 11 );

		$html = array_merge(
		wp_kses_allowed_html( 'post' ), array(
			'script'	 => array(
				'type'		 => array(),
				'src'		 => array(),
				'charset'	 => array(),
				'async'		 => array()
			),
			'noscript'	 => array(),
			'style'		 => array(
				'type' => array()
			),
			'iframe'	 => array(
				'src'				 => array(),
				'height'			 => array(),
				'width'				 => array(),
				'frameborder'		 => array(),
				'allowfullscreen'	 => array()
			)
		)
		);

		return apply_filters( 'iub_code_allowed_html', $html );
	}

	/**
	 * Re-generate the amp templates
	 */
	private function regenerate_amp_templates() {
		// For multi-language
		if ( iubenda()->multilang && ! empty( iubenda()->languages ) ) {
			foreach ( iubenda()->languages as $lang_id => $lang_name ) {
				// get code for the language
				$code = '';
				if ( ! empty( iubenda()->options['cs'][ 'code_' . $lang_id ] ) ) {
					$code = html_entity_decode( iubenda()->parse_code( iubenda()->options['cs'][ 'code_' . $lang_id ] ) );
				}

				// handle default, if empty
				if ( empty( $code ) && $lang_id == iubenda()->lang_default ) {
					$code = iubenda()->parse_code( iubenda()->options['cs']['code_default'] );
				}

				// Generate code if it was set for the selected language
				if ( ! empty( $code ) ) {
					iubenda()->AMP->generate_amp_template( $code, $lang_id );
				}
			}

			return;
		}

		// For one language
		$code = iubenda()->options['cs']['code_default'];
		iubenda()->AMP->generate_amp_template( $code );
	}

    /**
     * unification all languages from locale to iub language
     *
     * @param array $locale_languages
     * @return array
     */
    public function language_unification_locale_to_iub(array $locale_languages): array
    {
        $iub_languages = [];

        // Workaround to solve return languages if has 'pt' language
        if($key = array_search('pt_PT', $locale_languages)){
            unset($locale_languages[$key]);
            $iub_languages[] = 'pt';
        }
        if($key = array_search('pt_BR', $locale_languages)){
            unset($locale_languages[$key]);
            $iub_languages[] = 'pt-BR';
        }
        if($key = array_search('en_GB', $locale_languages)){
            unset($locale_languages[$key]);
            $iub_languages[] = 'en-GB';
        }

        if($key = array_search('en_US', $locale_languages)){
            unset($locale_languages[$key]);
            $iub_languages[] = 'en';
        }

        if($key = array_search('en_AU', $locale_languages)){
            unset($locale_languages[$key]);
            $iub_languages[] = 'en';
        }

        if($key = array_search('en_CA', $locale_languages)){
            unset($locale_languages[$key]);
            $iub_languages[] = 'en';
        }

        foreach ($locale_languages as $language){
            if(strpos($language, '_')){
                $iub_languages[] = strstr($language, '_', true);
            }
        }

        return $iub_languages;
    }

    private function upgrading_to_ver_3_process()
    {
        $products = [
            'iubenda_cookie_law_solution' => 'cs',
            'iubenda_consent_solution' => 'cons',
        ];

        $old_data = [
            'iubenda_cookie_law_solution' => iubenda()->options['cs'],
            'iubenda_cookie_law_solution_status' => 'true',
            'iubenda_consent_solution' => iubenda()->options['cons'],
            'iubenda_consent_solution_status' => 'true',
        ];
        $result = $this->settings->init_prepare_product_options_while_upgrading($products, $old_data);

        // Count valid codes for iubenda cookie law solution codes and set the service inactive
        if(count(array_filter(iub_array_get($result, "codes_statues.iubenda_cookie_law_solution_codes", []) ?: [])) == 0){
            $result['iubenda_activated_products']['iubenda_cookie_law_solution'] = 'false';
        }

        $this->settings->save_init_prepared_product_options($products, $result);

        // Reload Options
        $this->settings->load_defaults();
    }

    /**
     * Workaround to replace the callback functions with empty json array to parse configuration
     *
     * @param $code
     * @return string|string[]
     */
    private function replace_the_callback_functions_to_parse_configuration($code)
    {
        $callback_position = strpos($code, 'callback');
        $opened_callback_braces = strpos($code, '{', $callback_position);
        $closing_callback_braces = $this->find_closing_bracket($code, $opened_callback_braces);

        return substr_replace($code, '{', $opened_callback_braces, $closing_callback_braces - $opened_callback_braces);
    }

    /**
     * @param $string
     * @param $open_position
     * @return mixed
     */
    private function find_closing_bracket($string, $open_position)
    {
        $close_pos = $open_position;
        $counter = 1;
        while ($counter > 0) {

            // To Avoid the infinity loop
            if (!isset($string[$close_pos + 1])) {
                break;
            }

            $c = $string[++$close_pos];
            if ($c == '{') {
                $counter++;
            } else if ($c == '}') {
                $counter--;
            }
        }

        return $close_pos;
    }

    /**
     * Compare between Iubenda DB version and This version and
     *
     * return true if DB version is lower than this version
     * return false if DB version is equal or more than this version
     *
     * @return bool|int
     */
    private function compare_iub_plugin_versions()
    {
        $db_version = get_option( 'iubenda_cookie_law_version' ) ?: '2.5.91';
        return version_compare( $db_version, $this->version, '<' );
    }

    /**
     * Decide which will be included into footer (Block or Widget)
     */
    public function assign_legal_block_or_widget()
    {
        $pp_status = iub_array_get(iubenda()->settings->services, 'pp.status') == 'true';
        $pp_position = iub_array_get(iubenda()->options['pp'], 'button_position') == 'automatic';

        // Privacy Policy button should appear
        $pp_should_appear = ($pp_status && $pp_position);

        $tc_status = iub_array_get(iubenda()->settings->services, 'tc.status') == 'true';
        $tc_position = iub_array_get(iubenda()->options['tc'], 'button_position') == 'automatic';

        // Terms and conditions button should appear
        $tc_should_appear = ($tc_status && $tc_position);

        if(!($pp_should_appear || $tc_should_appear)){
            return;
        }

        // If current theme supports widget
        if ($this->widget->check_current_theme_supports_widget()) {
            do_action('iubenda_assign_widget_to_first_sidebar');
        }

        // if current theme supports blocks
        if ($this->block->check_current_theme_supports_blocks()) {
            do_action('iubenda_attach_block_in_footer');
        }
    }

    /**
     * Check if we support current theme to attach legal
     */
    public function check_if_we_support_current_theme_to_attach_legal()
    {
        if ($this->widget->check_current_theme_supports_widget() || $this->block->check_current_theme_supports_blocks()) {
            return true;
        }

        return false;
    }

    /**
     * Check if cookie solution service is activated and configured
     */
    private function is_cs_service_enabled_and_configured(): bool {
        $product_helper = new ProductHelper();

        return ($product_helper->is_cs_service_enabled() && $product_helper->is_cs_service_configured());
    }

}

if (!function_exists('iub_array_get')) {
    function iub_array_get($array, $key, $default = null) {
        if (!(is_array($array) || $array instanceof ArrayAccess)) {
            return $default instanceof Closure ? $default() : $default;
        }

        if (is_null($key)) {
            return $array;
        }

        if (array_key_exists($key, $array)) {
            return $array[$key];
        }

        if (strpos($key, '.') === false) {
            return $array[$key] ?? ($default instanceof Closure ? $default() : $default);
        }

        foreach (explode('.', $key) as $segment) {
            if ((is_array($array) || $array instanceof ArrayAccess) && (array_key_exists($segment, $array))) {
                $array = $array[$segment];
            } else {
                return $default instanceof Closure ? $default() : $default;
            }
        }

        return $array;
    }
}

if (!function_exists('__iub_trans')) {
    /**
     * @param $string
     * @param $textDomain
     * @param $locale
     * @return string|void
     */
    function __iub_trans($string, $locale, $textDomain = 'iubenda' ): string
    {
        global $l10n;
        // Take a backup of textDomain
        if (isset($l10n[$textDomain])) {
            $backup = $l10n[$textDomain];
        }
        load_textdomain($textDomain, IUBENDA_PLUGIN_PATH . 'languages/'.$textDomain.'-'. $locale . '.mo');
        $translation = __($string,$textDomain);

        // update back the backup of textDomain if isset
        if (isset($backup)) {
            $l10n[$textDomain] = $backup;
        }
        return $translation;
    }
}

/**
 * add stars in iubenda plugin meta
 */
add_filter('plugin_row_meta' , 'iubenda_add_plugin_meta_links', 10, 2);
if ( ! function_exists('iubenda_add_plugin_meta_links') ) {
    function iubenda_add_plugin_meta_links($meta_fields, $file) {
        if ( plugin_basename(__FILE__) == $file ) {
            $plugin_url = "https://wordpress.org/support/plugin/iubenda-cookie-law-solution/reviews/?rate=5#new-post";
            $meta_fields[] = "<a href='" . esc_url($plugin_url) ."' target='_blank' title='" . esc_html__('Rate', 'iubenda') . "'>
            <i class='iubenda-rate-stars'>"
                . "<svg xmlns='http://www.w3.org/2000/svg' width='15' height='15' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' class='feather feather-star'><polygon points='12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2'/></svg>"
                . "<svg xmlns='http://www.w3.org/2000/svg' width='15' height='15' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' class='feather feather-star'><polygon points='12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2'/></svg>"
                . "<svg xmlns='http://www.w3.org/2000/svg' width='15' height='15' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' class='feather feather-star'><polygon points='12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2'/></svg>"
                . "<svg xmlns='http://www.w3.org/2000/svg' width='15' height='15' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' class='feather feather-star'><polygon points='12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2'/></svg>"
                . "<svg xmlns='http://www.w3.org/2000/svg' width='15' height='15' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' class='feather feather-star'><polygon points='12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2'/></svg>"
                . "</i></a>";

        }

        return $meta_fields;
    }
}
/**
 * Initialise iubenda Cookie Solution
 *
 * @return iubenda
 */
function iubenda() {
	static $instance;

	// first call to instance() initializes the plugin
	if ( $instance === null || ! ( $instance instanceof iubenda ) )
		$instance = iubenda::instance();

	return $instance;
}

$iubenda = iubenda();
