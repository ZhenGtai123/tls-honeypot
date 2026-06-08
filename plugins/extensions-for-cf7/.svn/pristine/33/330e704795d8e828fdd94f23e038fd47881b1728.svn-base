<?php

if( ! defined( 'ABSPATH' ) ) exit(); // Exit if accessed directly

/**
 * HT CF7 Store Form Data
 */
class Extensions_Cf7_Store_Data
{
	
	function __construct(){
		add_action( 'wpcf7_submit', array($this,'extcf7_submit'), 10, 2 );
	}

    /**
     * Save the email data on email submit
     * @return void
    */
	function extcf7_submit($extcf7_info, $result){
        global $wpdb;
        if ( empty($result['status']) || 'mail_sent' !== $result['status'] ) {
            return;
        }
        $submission = WPCF7_Submission::get_instance();
        if($submission){
            $cf7_data               = $submission->get_posted_data(); 
            $cf7_file_upload_dir    = wp_upload_dir();
            $cf7_file_dirname       = $cf7_file_upload_dir['basedir'].'/extcf7_uploads';
            $current_time           = time();
            $cf7_files              = $submission->uploaded_files();
            $cf7_uploaded_files     = array();
            $posted_fields_value    = array();

            foreach ($_FILES as $file_key => $file) { //phpcs:ignore WordPress.Security.NonceVerification.Missing
                array_push($cf7_uploaded_files, $file_key);
            }

            foreach ($cf7_files as $file_key => $file) {
                $file = is_array( $file ) ? reset( $file ) : $file;
                if( empty($file) ) continue;
                copy($file, $cf7_file_dirname.'/'.$current_time.'-'.$file_key.'-'.basename($file));
            }

            foreach ($cf7_data  as $key => $value){
                if(!in_array($key, $cf7_uploaded_files )){
                    $dataKey = esc_html($key);
                    $posted_fields_value[$dataKey] = $value;
                }
                if ( in_array($key, $cf7_uploaded_files ) ){
                    $dataKey = esc_html($key);
                    $file = is_array( $cf7_files[ $key ] ) ? reset( $cf7_files[ $key ] ) : $cf7_files[ $key ];
                    $file_name = empty( $file ) ? '' : $current_time.'-'.$key.'-'.basename( $file ); 
                    $posted_fields_value[$dataKey] = $file_name;
                }
            }

            $mail_template = $extcf7_info->prop( 'mail' );
            $mail = wpcf7_mail_replace_tags(
                $mail_template,
                array(
                    'html' => $mail_template['use_html'],
                    'exclude_blank' => $mail_template['exclude_blank'],
                )
            );

            $posted_fields_value['mail_recipient'] = $mail['recipient'];

            $posted_fields_value['server_http_referer'] = sanitize_text_field( $_SERVER['HTTP_REFERER'] );
            $posted_fields_value['server_remote_addr']  = sanitize_text_field( $_SERVER['REMOTE_ADDR'] );

            $cf7_post_id = $extcf7_info->id();
            $cf7_value   = serialize( $posted_fields_value );
            $cf7_date    = current_time('Y-m-d H:i:s');

            $data  = [
                'form_id'      => $cf7_post_id,
                'form_value'   => $cf7_value,
                'form_date'    => $cf7_date,
            ];

            $table_name = $wpdb->prefix . 'extcf7_db';

            $wpdb->insert( $table_name, $data ); //phpcs:ignore WordPress.DB.DirectDatabaseQuery.DirectQuery
        }
    }
}

new Extensions_Cf7_Store_Data();