<?php
/**
 * @phpcs:disable WordPress.Security.NonceVerification.Recommended, WordPress.Security.NonceVerification.Missing
 */
if( ! defined( 'ABSPATH' ) ) exit(); // Exit if accessed directly

/**
 * HT CF7 Redirection
*/

class Extensions_Cf7_Redirection{

	/**
     * [$_instance]
     * @var null
    */
    private static $_instance = null;

    /**
     * [instance] Initializes a singleton instance
     * @return [Extensions_Cf7_Redirection]
    */
    public static function instance() {
        if ( is_null( self::$_instance ) ) {
            self::$_instance = new self();
        }
        return self::$_instance;
    }

    function __construct(){
    	add_filter( 'wpcf7_editor_panels', array( $this, 'add_redirection_panel' ) );
        add_action( 'wpcf7_after_save', array( $this, 'store_redirection_value' ) );
    	add_action( 'wpcf7_form_hidden_fields', array( $this, 'extcf7_redirection_form_hidden_fields' ) );
    }

    public function add_redirection_panel($panels){
    	if ( current_user_can( 'wpcf7_edit_contact_form' ) ) {
	    	$panels['extcf7-redirect-panel'] = array(
				'title'    => esc_html__( 'Redirect Actions', 'cf7-extensions' ),
				'callback' => array( $this, 'redirection_pannel' ),
			);
		}

		return $panels;
    }

    public function redirection_pannel($form){
    	$form_id = isset($_GET['post']) ? absint($_GET['post']) : false;
    	if (false === $form_id ) {
			?>
		    <div class="extcf7-inner-container">
				<h2><?php echo esc_html__( 'Redirection Options', 'cf7-extensions' ); ?></h2>
				<p><?php echo esc_html__( 'Please save your form first', 'cf7-extensions' ); ?></p>
			</div>
			<?php
			return;
		}
        include CF7_EXTENTIONS_PL_PATH.'admin/template/redierect-options-layout.php';
    }

    public function store_redirection_value($cf7){
    	if ( ! isset( $_POST ) || empty( $_POST['redirect_options'] ) ) {
			return;
		}

		$form_id = $cf7->id();
        $options_values = array();
        if(is_array($_POST['redirect_options'])){
            foreach($_POST['redirect_options'] as $key => $redirect_val) {
                if('javascript_code' == $key){
                    $options_values[$key] = sanitize_textarea_field($redirect_val);
                }else{
                   $options_values[$key] = sanitize_text_field($redirect_val); 
                }
            }
        }

		update_post_meta($form_id,'extcf7_redirect_options', $options_values);
    }

    public function extcf7_redirection_form_hidden_fields($hidden_fields){
        $current_form = wpcf7_get_current_contact_form();
        $current_form_id = $current_form->id();

        $options = array(
            'form_id' => $current_form_id,
            'redirect_options' => get_post_meta($current_form_id,'extcf7_redirect_options',true)
        );

        return array_merge($hidden_fields, array(
            '_extcf7_redirect_options' => ''.wp_json_encode($options),
        ));
    }

}

Extensions_Cf7_Redirection::instance();

?>