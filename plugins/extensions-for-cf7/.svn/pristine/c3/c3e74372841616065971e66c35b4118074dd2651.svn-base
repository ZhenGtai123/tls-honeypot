<?php
/**
 * @phpcs:disable WordPress.Security.NonceVerification.Recommended, WordPress.Security.NonceVerification.Missing
 */
if( ! defined( 'ABSPATH' ) ) exit(); // Exit if accessed directly

/**
 * HT CF7 Popup
*/

class Extensions_Cf7_Mailchimp_Map{

	/**
     * [$_instance]
     * @var null
    */
    private static $_instance = null;

    /**
     * [instance] Initializes a singleton instance
     * @return [Extensions_Cf7_Mailchimp_Map]
    */
    public static function instance(){
        if ( is_null( self::$_instance ) ){
            self::$_instance = new self();
        }
        return self::$_instance;
    }

    function __construct(){
        add_filter( 'wpcf7_editor_panels', array( $this, 'mail_chimp_panel' ) );
        add_action( 'wp_ajax_extcf7_mailchimp_map', array( $this, 'mailchimp_map' ) );
        add_action( 'wpcf7_after_save', array( $this, 'extcf7_mailchimp_save' ) );
    }

    public function mail_chimp_panel($panels){
        if ( current_user_can( 'wpcf7_edit_contact_form' ) ) {
            $panels['extcf7_pro-mailchimp-panel'] = array(
                'title'    => esc_html__( 'HT MailChimp', 'cf7-extensions' ),
                'callback' => array( $this, 'add_mailchimp_pannel' ),
            );
        }
        return $panels;
    }

    public function add_mailchimp_pannel($form){

        $form_saved = isset($_GET['post']) ? absint($_GET['post']) : false;

        if (false === $form_saved ){
            ?>
            <div class="extcf7-inner-container">
                <h2><?php echo esc_html__( 'Conditional fields', 'cf7-extensions' ); ?></h2>
                <p><?php echo esc_html__( 'Please save your form first.', 'cf7-extensions' ); ?></p>
            </div>
            <?php
            return;
        }

        $cf7_list_tag         = $this->get_cf7_form_tag();
        $extcf7_mcmp_defaults = array();
        $extcf7_mcmp          = get_option( 'extcf7_mcmp_'.$form->id(), $extcf7_mcmp_defaults );
        include CF7_EXTENTIONS_PL_PATH.'admin/template/mailchimp-pannel-layout.php';
    }

    public function mailchimp_map(){
        $ajax_nonce = sanitize_text_field($_POST['ajax_nonce']);

        if(wp_verify_nonce($ajax_nonce, 'extcf7_mailchimp_map_active_nonce')) {
            
            $extcf7_mcmp_defaults = array();
            $mcmp_idform = 'extcf7_mcmp_'. wp_unslash( sanitize_text_field($_POST['mcmp_idform']) );
            $mceapi      = isset( $_POST['mcmpapi'] ) ? sanitize_text_field($_POST['mcmpapi']) : 0 ;
            
            $extcf7_mcmp = get_option( $mcmp_idform, $extcf7_mcmp_defaults );
            $tempost     = $extcf7_mcmp;

            unset( $tempost['api'], $tempost['valid_api'], $tempost['lisdata'], $tempost['listfields']);

            $temp        = $this->mailchimp_api_validation( $mceapi );
            $apivalid    = $temp['valid_api'];

            $tempost     = $tempost + $temp;

            $temp 	     = $this->get_mailchimp_list( $mceapi, $apivalid );
            $listdata    = $temp['lisdata'];

            $tempost     = $tempost + $temp;

            if( $apivalid ){
                $listfields = $this->get_mailchimp_field( $listdata['lists'][0]['id'], $mceapi);
                $tempost    = $tempost + array( 'listfields' => $listfields );
                $chimp = array('map_fields'=>$this->mailchimp_map_field_html( $apivalid, $listfields ));
            }

            $tempost     = $tempost + array( 'api' => $mceapi );

            update_option( $mcmp_idform, $tempost );

            $chimp ['list_mail'] = $this->mailchimp_html_listmail( $apivalid, $listdata);
        
            echo wp_json_encode( $chimp );
            die();
        }
    }

    private function mailchimp_api_validation($api){

    	if ( !isset( $api ) or trim ( $api ) =="" ) {

	      $tmp = array( 'valid_api' => 0 );

	      return $tmp ;
	    }

	    $account = ( isset( $api )  ) ? substr_count( $api, "-" ) : "" ;

	    if ( $account == 0  ) {

	      $tmp = array( 'valid_api' => 0 );

	      return $tmp ;

	    }

	    $dc      = explode("-",$api);
    	$url   	 = "https://anystring:$dc[0]@$dc[1].api.mailchimp.com/3.0/ping";
	    $headers = array( "Content-Type" => "application/json" ) ;

	    $opts = array(
            'headers' => $headers,
            'method'  => 'GET',
            'timeout' => 10000
        );

	    $response = wp_remote_get( $url, $opts );

	    if ( is_wp_error ( $response ) ) {
	        $tmp = array( 'valid_api' => 0 );
	        return $tmp;
	    }

	    $response_body = wp_remote_retrieve_body( $response );

    	$validate_api_key_response = json_decode( $response_body, true );

    	if ( isset ( $validate_api_key_response["status"] ) ) {
	        if ( $validate_api_key_response["status"] >=400  ) {
	            $tmp = array( 'valid_api' => 0 );
	            return $tmp;
	        }
	    }

	    $tmp = array( 'valid_api' => 1 );

	    return $tmp;
    }

    private function get_mailchimp_list($apikey,$validapi){

    	if ( $validapi == 0    ) {

	        $list_data 	= array(
			    'id'  => 0,
				'name' => esc_html__('empty list','cf7-extensions'),
		    );

	       $tmp = array( 'lisdata' => array('lists' => $list_data ));

	       return $tmp ;
	    }

	    $api   	 = $apikey;
	    $dc    	 = explode("-",$api);
	    $url   	 = "https://anystring:$dc[0]@$dc[1].api.mailchimp.com/3.0/lists?count=9999";
	    $headers = array( "Content-Type" => "application/json" ) ;

	    $opts = array(
            'headers' => $headers,
            'method'  => 'GET',
            'timeout' => 10000
        );

        $response 	 = wp_remote_get( $url, $opts );

	    if ( is_wp_error ( $response ) ) {

	        $list_data 	= array(
		    	'id'   => 0,
				'name' => esc_html__('empty list','cf7-extensions'),
		    );

	        $tmp = array( 'lisdata' => array('lists' => $list_data ));

	        return $tmp;
	    }

	    $reapose_body = wp_remote_retrieve_body( $response );

	    $list_datanew = json_decode( $reapose_body, true );

	    $tmp = array( 'lisdata' => $list_datanew );

	    return $tmp;
	}

	private function get_mailchimp_field( $module, $apikey ){

        $api     = $apikey;
        $dc      = explode("-",$api);
        $url     = "https://anystring:$dc[0]@$dc[1].api.mailchimp.com/3.0/lists/".$module."/merge-fields?count=200";
        $headers = array( "Content-Type" => "application/json" ) ;

        $opts = array(
            'headers' => $headers,
            'method'  => 'GET',
            'timeout' => 10000
        );

        $response       = wp_remote_get( $url, $opts ); 

        $reapose_body   = wp_remote_retrieve_body( $response );

        $list_field_tag = json_decode( $reapose_body, true );

        $tmp            = $this->map_mailchimp_field( $list_field_tag );

        return $tmp;        

	}

    private function map_mailchimp_field($listdata){

        $res=array();
        $address=array(
            'addr1'=> esc_html__('Street Line 1','cf7-extensions'),
            'addr2'=> esc_html__('Street Line 2','cf7-extensions'),
            'city'=> esc_html__('City','cf7-extensions'),
            'state'=> esc_html__('State','cf7-extensions'),
            'zip'=> esc_html__('Zip','cf7-extensions'),
            'country'=> esc_html__('Country','cf7-extensions'),
        );

        if(!empty($listdata['merge_fields'])){
            $res['PHONE']=array(
                'name'=>esc_html__('PHONE','cf7-extensions'),
                'label'=>esc_html__('Phone Number','cf7-extensions'),
                'type'=>'phone'
            );

            foreach($listdata['merge_fields'] as $k=>$v){
                $merge_id=intval($v['merge_id']);
                if($v['type'] == 'address'){
                    foreach($address as $i=>$r){
                        $field=array('label'=>$v['name'].'-'.$r,'name'=>$v['tag'].'-'.$i,'type'=>'address'); 
                        if($v['required'] == true){
                          $field['req']='true';    
                        }  
                        $res[$v['tag'].'-'.$i]=$field; 
                    }   
                }else{
                    $field=array('label'=>$v['name'],'name'=>$v['tag'],'type'=>$v['type']);
                    if(in_array($v['type'],array('dropdown','radio'))){
                        if(!empty($v['options']['choices'])){ 
                            $field['eg']=implode(',',$v['options']['choices']); 
                            $field['options']=$v['options']['choices'];
                        }
                    }else if($v['type'] == 'date'){
                      if(!empty($v['options']['date_format'])){ $field['eg']=$v['options']['date_format'];  }   
                    }else if($v['type'] == 'birthday'){
                      $field['eg']='MM/DD';   
                    }
                    if($v['required'] == true){ $field['req']='true';    } 
                    $res[$v['tag']]=$field;   
                } 
            }
        }

        return $res; 
    }

	private function mailchimp_html_listmail($validapi,$listdata){
        ob_start();
    	?>
    		<small><input type="hidden" id="valid-api" name="extcf7-mailchimp[valid_api]" value="<?php echo( isset( $validapi ) ) ? esc_attr( $validapi ) : ''; ?>" /></small>

    	<?php
    	if ( isset( $validapi ) && '1' == $validapi ):
    	?>
            <div class="extcf7_p_lr_tb">
    		<label class="extcf7-mailchimp-label" for="extcf7-mailchimp-list"><?php echo esc_html( __( 'Your mailchimp lists: ','cf7-extensions' ) ); ?></label>
		    <select id="extcf7-mailchimp-list" name="extcf7-mailchimp[list]" style="width:45%;">
			    <?php
			    foreach ( $listdata['lists'] as $list ) {
			      ?>
			      <option value="<?php echo esc_attr( $list['id'] ) ?>">
			        <?php echo esc_html( $list['name'] ); ?></option>
			      <?php
			    }
			    ?>
		    </select>
            </div>
    	<?php
    	endif; 
        return ob_get_clean();
    }

    private function get_cf7_form_tag(){
    	$tag_instance = WPCF7_FormTagsManager::get_instance();
		$form_tags 	  = $tag_instance->get_scanned_tags();
		return $form_tags;
    }

    private function cf7_form_tag_html( $formfield, $form_tag_list, $extcf7_mcmp, $filter_txt, $merge_tag ){

    	if('email' !== $formfield){
    		$tag_list = array_filter( $form_tag_list, function($item) use ($filter_txt){
    			return ($item['basetype'] !==  'email' && $item['basetype'] !== 'submit' ) ||  'textarea' == $item['basetype'];
    		});
    	}else{
    		$tag_list = array_filter( $form_tag_list, function($item) use ($filter_txt){
    			return $item['basetype'] ==  $filter_txt;
    		});
    	}

        if($merge_tag){
            $formtype       = "cf7tag";
            $custom_value   = !is_array($extcf7_mcmp) ? $extcf7_mcmp : ' ';
            $formname       = "extcf7-mailchimp[".$formtype."][]";
        }else{
           $formtype        =  $formfield;
           $custom_value    = ( isset( $extcf7_mcmp[$formtype] ) ) ? $extcf7_mcmp[$formtype] : ' ' ;
           $formname        = "extcf7-mailchimp[".$formtype."]";
        }

    	$custom_vlaue = ( ( $formfield =='email' && $custom_value == ' ' )  ? '[your-email]':$custom_value );
    	?>
            <?php if ( $formfield != 'email'  ): ?>
    		<select class="extcf7-mailchimp-select" id="extcf7-mailchimp-<?php echo esc_attr( $formtype );?>" name="<?php echo esc_attr($formname); ?>" style="width: 95%;">
    			<option <?php  if ( $custom_value == ' ' ) { echo 'selected="selected"'; } ?> disabled>
                     <?php echo (($custom_value=='email') ? esc_html__( 'Required by MailChimp','cf7-extensions') : esc_html__( 'Choose','cf7-extensions' )); ?>
    			</option>
    		    <?php 
    			foreach ( $tag_list as $list ) {
	              $field = '['. trim( $list['name'] ) . ']' ;
	              ?>
	                <option value="<?php echo esc_attr( $field ) ?>" <?php if (  trim( $custom_value ) == $field ){ echo 'selected="selected"'; } ?> >
                      <?php echo '[' . esc_html( $list['name'] ) . ']' ?>
	                </option>
	              <?php
		        }
    			?>
    		</select>
            <?php else: 
                foreach ( $tag_list as $list ) {
            ?>
                <input type="text" name="<?php echo esc_attr($formname); ?>" value="<?php echo esc_attr('['.$list['name'].']') ?>" style="width: 80%;">
            <?php
              } 
              endif; 
            ?>
    	<?php
    }

    private function mailchimp_map_field_html($validapi, $listfields){
        if ( isset( $validapi ) && '1' == $validapi ):
            ob_start();
            ?>
                <label class="extcf7-mailchimp-label" ><strong><?php echo esc_html__('Select Mailchimp Field','cf7-extensions') ?></strong></label>
                <select name="extcf7-mailchimp[mailchimp-tag][]" style="width:95%;">
                    <?php foreach ( $listfields as $field ): ?>
                        <option value="<?php echo esc_attr($field['name']) ?>"><?php echo esc_html($field['label']); ?></option>
                    <?php endforeach; ?>
                </select>
            <?php
            return ob_get_clean();
        endif;
    }

    public function extcf7_mailchimp_save($args){
        if ( ! isset( $_POST ) || empty( $_POST['extcf7-mailchimp'] ) ) {
            return;
        }

        $default = array () ;
        $extcf7_mcmp = get_option ( 'extcf7_mcmp_'.$args->id(), $default  ) ;
        $globalarray = extcf7_clean($_POST['extcf7-mailchimp']) ;

        if(isset( $extcf7_mcmp['valid_api'])){

           $apivalid       = $extcf7_mcmp['valid_api'];
           $check_apivalid = $this->mailchimp_api_validation( $globalarray['api'] );
           $apivalid       = $check_apivalid['valid_api'];

           if(!$apivalid){
               $globalarray['valid_api'] = $apivalid;
           }

        }else{
            $apivalid = 0;
        }

        $listdata   = ( isset( $extcf7_mcmp['lisdata'] ) ) ? $extcf7_mcmp['lisdata'] : 0 ;
        $listfields = ( isset( $extcf7_mcmp['listfields'] ) ) ? $extcf7_mcmp['listfields'] : 0 ;

        if ( !isset( $_POST['extcf7-mailchimp']['valid_api'] ) )
            $globalarray += array ('valid_api' => $apivalid  ) ;

        if ( !isset( $_POST['extcf7-mailchimp']['lisdata'] )  ) {
            $globalarray += array ('lisdata' => $listdata  ) ;
        }

        if ( !isset( $_POST['extcf7-mailchimp']['listfields'] )  ) {
            $globalarray += array ('listfields' => $listfields  ) ;
        }

        update_option( 'extcf7_mcmp_'.$args->id(), $globalarray );
    }

}

Extensions_Cf7_Mailchimp_Map::instance();