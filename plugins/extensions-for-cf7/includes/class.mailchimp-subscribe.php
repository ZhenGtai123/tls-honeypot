<?php

if( ! defined( 'ABSPATH' ) ) exit(); // Exit if accessed directly

/**
 * HT CF7 Store Form Data
 */
class Extensions_Cf7_Pro_Mailchimp_Subscribe{

  /**
   * [$_instance]
   * @var null
  */
  private static $_instance = null;

  /**
   * [instance] Initializes a singleton instance
   * @return [Extensions_Cf7_Pro_Mailchimp_Subscribe]
  */
  public static function instance(){
    if ( is_null( self::$_instance ) ){
      self::$_instance = new self();
    }
    return self::$_instance;
  }
	
  function __construct(){
  	add_action( 'wpcf7_before_send_mail', array($this,'extcf7_pro_mailchimp_subscribe') );
  }

  public function extcf7_pro_mailchimp_subscribe($form_obj){


  $extcf7_mcmp = get_option( 'extcf7_mcmp_'.$form_obj->id() );
	$idform = 'extcf7_mcmp_'.$form_obj->id() ;

	if ( empty($extcf7_mcmp['valid_api']) || $extcf7_mcmp['valid_api'] != 1 ){
    return;
  }

	$chimp_api   = isset( $extcf7_mcmp['api'] ) ? $extcf7_mcmp['api'] : '';
	$pos  = strpos($chimp_api,"-");

	if ($pos === false ) return ;

	if( !$extcf7_mcmp ) return;

	$regex = '/\[\s*([a-zA-Z][0-9a-zA-Z_-]*)\s*\]/';

	$submission = WPCF7_Submission::get_instance();

	$email = $this->extcf7_pro_tag_replace($regex, $extcf7_mcmp['email'], $submission->get_posted_data());
	$name  = $this->extcf7_pro_tag_replace($regex, $extcf7_mcmp['name'], $submission->get_posted_data());
	$lists = $this->extcf7_pro_tag_replace($regex, $extcf7_mcmp['list'], $submission->get_posted_data());

	$merge_field=array('FNAME'=>$name);

    $parts = explode(" ", $name);
    if(count($parts)>1) {

      $lastname = array_pop($parts);
      $firstname = implode(" ", $parts);
      $merge_field=array('FNAME'=>$firstname, 'LNAME'=>$lastname);

    } else {

      $merge_field=array('FNAME'=>$name);

    }

    if(isset($extcf7_mcmp['chimp-customfield'])){
      if( isset($extcf7_mcmp['cf7tag']) && !empty($extcf7_mcmp['cf7tag']) ){
      	foreach ($extcf7_mcmp['cf7tag'] as $key => $cf7_field_val) {
      		$name_field = $extcf7_mcmp['mailchimp-tag'][$key];
      		$merge_field = $merge_field + array($name_field => $this->extcf7_pro_tag_replace($regex, $cf7_field_val, $submission->get_posted_data()));
      	}
      }
    }

    $chmp_subcribe = 'subscribed';

    if(isset($extcf7_mcmp['chimp-active']) && $extcf7_mcmp['chimp-active'] == '1'){
    	$chmp_subcribe = '';
    }else{
    	if ( isset($extcf7_mcmp['confirm-subs']) && strlen($extcf7_mcmp['confirm-subs']) != 0 ){
    		$confirm_subs = $this->extcf7_pro_tag_replace($regex, $extcf7_mcmp['confirm-subs'], $submission->get_posted_data());
    		if ( strlen( trim($confirm_subs) ) != 0  ) {
            	$chmp_subcribe = 'subscribed';
	        }else {
	          	$chmp_subcribe = '';
	        }
    	}else{
    		$chmp_subcribe = 'subscribed';
    	}
    }

    if($chmp_subcribe == '') return;

    $chimp_mergefields = "";

    foreach($merge_field as $chmp_fname=>$chmp_fvalue) {
        $chmpvar= '"'.$chmp_fname.'":"' .$chmp_fvalue. '", ';
        $chimp_mergefields = $chimp_mergefields . $chmpvar ;
    }

    $chimp_mergefields = substr($chimp_mergefields,0,strlen($chimp_mergefields) -2);

    $strform      	= explode("-",$chimp_api);
    $list  		= $lists;
	$urlcmp_v3  = "https://anystring:$strform[0]@$strform[1].api.mailchimp.com/3.0";
    $headers 	= array( "Content-Type" => "application/json" ) ;

    $url_get_merge_fields = "$urlcmp_v3/lists/$list/merge-fields";

    $opts = array(
        'headers' => $headers,
        'method'  => 'GET',
        'timeout' => 10000
    );

    $merge_field = wp_remote_get( $url_get_merge_fields, $opts );
    $mergresbody = wp_remote_retrieve_body( $merge_field );
    $arraymerger = json_decode( $mergresbody, True );

    if ( isset($arraymerger['merge_fields'])  )  { 
    	$columnes_require = $this->required_columns($arraymerger['merge_fields'],'required','merge_id');

    	foreach($columnes_require as $merge_id=>$value) {
            if ($value) {
                $chmp_req = '{"required":false}';
                $url_edit   = "$urlcmp_v3/lists/$list/merge-fields/$merge_id";

                $opts = array(
                          'method' => 'PATCH',
                          'headers' => $headers,
                          'body' => $chmp_req,
                        );

                $resp_merg_res = wp_remote_post( $url_edit, $opts );
            }
        }
    }

    $url_put   = "$urlcmp_v3/lists/$list"; 
    $info  = '{"members": [

                { "email_address": "'. $email .'",
                  "status": "'.$chmp_subcribe.'",
                  "merge_fields":{ '. $chimp_mergefields .' }
                }

              ],
              "update_existing": true}';

    $opts = array(
              'method' => 'POST',
              'headers' => $headers,
              'body' => $info,
            );

    $respsubs = wp_remote_post( $url_put, $opts );
    $resp 	  = wp_remote_retrieve_body( $respsubs );


  }

  private function extcf7_pro_tag_replace($pattern,$object,$posted_data){
  	if( preg_match($pattern,$object,$matches) > 0) {
  		if ( isset( $posted_data[$matches[1]] ) ) {

  			$submitted_field = $posted_data[$matches[1]];

  			if ( is_array( $submitted_field ) ){
		        $replaced_field = join( ', ', $submitted_field );
		    }
	        else{
		        $replaced_field = $submitted_field;
		    }

	    	return stripslashes( $replaced_field );
  		}

  		return $matches[0];
  	}
  	return $object;
  }

  private function required_columns(array $input_fields, $column_required, $merge_id = null){
    $array = array();
    foreach ($input_fields as $value) {
        if ( !array_key_exists($column_required, $value) ) {
            trigger_error("Key \"$column_required\" does not exist in array");
            return false;
        }
        if (is_null($merge_id)) {
            $array[] = $value[$column_required];
        }
        else {
            if ( !array_key_exists($merge_id, $value)) {
                trigger_error("Key \"$merge_id\" does not exist in array");
                return false;
            }
            if ( ! is_scalar($value[$merge_id])) {
                trigger_error("Key \"$merge_id\" does not contain scalar value");
                return false;
            }
            $array[$value[$merge_id]] = $value[$column_required];
        }
    }
    return $array;
  }

}

Extensions_Cf7_Pro_Mailchimp_Subscribe::instance();