<?php
/**
 * @phpcs:disable WordPress.Security.NonceVerification.Recommended, WordPress.Security.NonceVerification.Missing
 */
if( ! defined( 'ABSPATH' ) ) exit(); // Exit if accessed directly

/**
 * HT CF7 Condition
*/

class Extensions_Cf7_Conditional {

	/**
     * [$_instance]
     * @var null
    */
    private static $_instance = null;

    /**
     * [instance] Initializes a singleton instance
     * @return [Extensions_Cf7_Conditional]
    */
    public static function instance() {
        if ( is_null( self::$_instance ) ) {
            self::$_instance = new self();
        }
        return self::$_instance;
    }

	function __construct(){
		// Register shortcodes
        add_action('wpcf7_init', array($this, 'extcf7_add_shortcodes'));

        // Tag generator
        add_action('admin_init', array($this, 'extcf7_tag_generator'), 589);

        //add editor pannel
        add_filter('wpcf7_editor_panels', array($this,'extcf7_add_conditional_panel'));
        //save conditional setup
        add_action( 'wpcf7_after_save', array( $this, 'extcf7_save_conditional_setup' ) );
	}


	public function extcf7_add_shortcodes() {
        if (function_exists('wpcf7_add_form_tag'))
            wpcf7_add_form_tag('fields_group', array($this, 'extcf7_shortcode_handler'), true);
        else if (function_exists('wpcf7_add_shortcode')) {
            wpcf7_add_shortcode('fields_group', array($this, 'extcf7_shortcode_handler'), true);
        }else{
            throw new Exception(esc_html__('functions wpcf7_add_form_tag and wpcf7_add_shortcode not found.', 'cf7-extensions'));
        }
    }

    public function extcf7_shortcode_handler($tag) {
        $tag = new WPCF7_FormTag($tag);
        return $tag->content;
    }

	public function extcf7_tag_generator() {
        if (! function_exists( 'wpcf7_add_tag_generator'))
            return;
        //echo "contact form 7 tag generator";
        wpcf7_add_tag_generator('fields_group',
            esc_html__('Conditional Fields', 'cf7-extensions'),
            'wpcf7-tg-fields-group',
            array($this, 'extcf7_tg_layout')
        );

    }

    public function extcf7_tg_layout($contact_form, $args = ''){
    	$args = wp_parse_args( $args, array() );
        $type = 'fields_group';

        $description = esc_html__( "Generate a fields_group tag to unite form elements that can be shown conditionally.", 'cf7-extensions' );
        include CF7_EXTENTIONS_PL_PATH.'admin/template/fields-group-layout.php';
    }

    public function extcf7_add_conditional_panel($panels){
    	if ( current_user_can( 'wpcf7_edit_contact_form' ) ) {
			$panels['extcf7-conditional-panel'] = array(
				'title'    => esc_html__( 'Conditional fields Settings', 'cf7-extensions' ),
				'callback' => array( $this, 'extcf7_editor_panel_conditional'),
			);
		}
		return $panels;
    }

    function extcf7_all_group_options($post){
    	$all_groups = $post->scan_form_tags(array('type'=>'fields_group'));
    	ob_start();
		?>
		<option value="" selected disabled><?php echo esc_html__( '-- Select group --', 'cf7-extensions' ); ?></option>
		<?php
		foreach ($all_groups as $tag) {
			?>
			<option value="<?php echo esc_attr($tag->name); ?>"><?php echo esc_html($tag->name); ?></option>
			<?php
		}
		return ob_get_clean();
    }

    function extcf7_all_field_options($post){
    	$all_fields = $post->scan_form_tags();

    	ob_start();
		?>
		<option value="" selected disabled><?php echo esc_html__( '-- Select field --', 'cf7-extensions' ); ?></option>
		<?php
		foreach ($all_fields as $tag) {
			if ($tag['type'] == 'fields_group' || $tag['name'] == '') continue;
			?>
			<option value="<?php echo esc_attr($tag['name']); ?>"><?php echo esc_html($tag['name']); ?></option>
			<?php
		}
		return ob_get_clean();
    }

    public function extcf7_editor_panel_conditional($form){

    	$form_id = isset($_GET['post']) ? absint($_GET['post']) : false;
    	$extcf7_entries = Extensions_Cf7_Condition_Setup::get_conditions_value($form_id);

		if (false === $form_id ) {
			?>
		    <div class="extcf7-inner-container">
				<h2><?php echo esc_html__( 'Conditional fields', 'cf7-extensions' ); ?></h2>
				<p><?php echo esc_html__( 'Please save your form first before adding condition.', 'cf7-extensions' ); ?></p>
			</div>
			<?php
			return;
		}
        include CF7_EXTENTIONS_PL_PATH.'admin/template/conditional-field-layout.php';
    }

    public function extcf7_save_conditional_setup($cf7){
		if ( ! isset( $_POST ) || empty( $_POST ) || ! isset( $_POST['extcf7-settings-text'] ) ) {
			return;
		}

		$post_id = $cf7->id();
		if ( ! $post_id ) {
			return;
		}
		
		$str = sanitize_textarea_field($_POST['extcf7-settings-text']);
		$extcf7_conditions_string = stripslashes($str);
		$extcf7_conditions = Extensions_Cf7_Condition_Setup::setup_conditions_string_to_array($extcf7_conditions_string);
		Extensions_Cf7_Condition_Setup::set_conditions_value($post_id, $extcf7_conditions);
	}
}

Extensions_Cf7_Conditional::instance();