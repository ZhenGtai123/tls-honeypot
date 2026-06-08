<?php

if( ! defined( 'ABSPATH' ) ) exit(); // Exit if accessed directly

/**
 * HT CF7 Email List
*/
class Extensions_Cf7_Detail_Page implements Extensions_Cf7_Form_Datalist_Render
{

	private $form_id;
	private $form_mail_id;

	function __construct(){
		$this->form_id = isset( $_GET['cf7_id'] ) ? absint($_GET['cf7_id']) : 0;
		$this->form_mail_id = isset( $_GET['cf7em_id'] ) ? absint($_GET['cf7em_id']) : 0;
	}

    /**
     * Email details informaion page
     * @return void
    */
	function cf7_layout_render(){
		global $wpdb;
		$table_name   		= $wpdb->prefix.'extcf7_db';
		$current_form_id    = $this->form_id;
		$mail_form_id   	= $this->form_mail_id;
		$cf7_upload_dir 	= wp_upload_dir();
        $cfdb7_dirname  	= $cf7_upload_dir['baseurl'].'/extcf7_uploads';

		if(isset($_GET['action']) && sanitize_text_field($_GET['action']) =='delete'){

            if(isset($_GET['n']) && !empty($_GET['n'])){

                $nonce = sanitize_text_field($_GET['n']);

                if ( !wp_verify_nonce( $nonce, "cf7_email_delete" ) ){

                    wp_die(__('Sorry you are not authorised to do this','cf7_email_delete'));
                }
            }

            $delete_row     = $wpdb->get_results( "SELECT * FROM $table_name WHERE id = '$mail_form_id' LIMIT 1", OBJECT );
            $del_row_value  = $delete_row[0]->form_value;
            $del_row_values = unserialize($del_row_value);

            foreach ($del_row_values as $key => $result) {

                if ( ( strpos($key, 'file') !== false ) &&
                    file_exists($cfdb7_dirname.'/'.$result) ) {
                    unlink($cfdb7_dirname.'/'.$result);
                }

            }
			$wpdb->delete("{$table_name}",['id' => $mail_form_id]);
			$url = admin_url("?page=contat-form-list&cf7_id=").$current_form_id;
			wp_redirect($url);
			exit;
		}


        $mail_form_data = $wpdb->get_results( "SELECT * FROM $table_name WHERE 	form_id = '$current_form_id' AND id = '$mail_form_id' LIMIT 1", OBJECT );
        

        if ( empty($mail_form_data) ) {
            wp_die( $message = 'Not valid contact form' );
        }


		ob_start();
		?>
		<div class="wrap">
			<h2><?php echo esc_html__("Email Information","cf7-extensions") ?></h2>
            <table class="extcf7-form-data-details">
                <tbody>
                    <tr>
                        <th><?php echo esc_html('Date :') ?></th>
                        <td><?php echo date_format(date_create($mail_form_data[0]->form_date),"F j, Y, g:i a"); ?></td>
                    </tr>
                    <?php $form_data  = unserialize( $mail_form_data[0]->form_value );
                    foreach ($form_data as $key => $data):

                        if(false !== strpos($key,'server')) continue;

                        if ( strpos($key, 'file') !== false ){
                            $key_value = str_replace('your-', '', $key);
                            $key_value = str_replace( array('-','_'), ' ', $key_value);
                            $key_value = ucwords( $key_value );
                            echo '<tr><th>Attachment :</th> <td><a href="'.$cfdb7_dirname.'/'.$data.'">'
                            .$data.'</a></td></tr>';
                        }else{
                            if(is_array($data)){
                                $key_value = str_replace('your-', '', $key);
                                $key_value = str_replace( array('-','_'), ' ', $key_value);
                                $key_value = ucwords( $key_value );
                                $array_data =  implode(', ',$data);
                                $array_data =  esc_html( $array_data );
                                echo '<tr><th>'.$key_value.' :</th><td>'.nl2br($array_data).'</td></tr>';
                            }else{
                                $key_value = str_replace('your-', '', $key);
                                $key_value = str_replace( array('-','_'), ' ', $key_value);
                                $key_value = ucwords( $key_value );
                                $data    = esc_html( $data );
                                echo '<tr><th>'.$key_value.' :</th><td>'.nl2br($data).'</td></tr>';
                            }
                        }
                    endforeach;
                    ?>
                </tbody>
            </table>
            <?php 
                $ip_address   =  htcf7ext_get_option('htcf7ext_opt', 'ip_address_enable', 'on');
                $referer_link =  htcf7ext_get_option('htcf7ext_opt', 'reffer_link_enable', 'on');
                if('on' == $ip_address || 'on' == $referer_link):
            ?>
                    <hr>
                    <h2><?php echo esc_html__("Submission Details","cf7-extensions") ?></h2>
                    <table class="extcf7-form-data-details">
                        <tbody>
                            <?php if('on' == $referer_link): ?>
                                <tr>
                                    <th><?php echo esc_html__("Referer :","cf7-extensions"); ?></th>
                                    <td><?php echo esc_url($form_data['server_http_referer']); ?></td>
                                </tr>
                            <?php endif; ?>
                            <?php if('on' == $ip_address): ?>
                                <tr>
                                    <th><?php echo esc_html__("IP Address :","cf7-extensions"); ?></th>
                                    <td><?php
                                        if(false !== strpos( $form_data['server_remote_addr'], '.' )){
                                            $ip_address = sprintf(
                                                '<a href="'.esc_url('http://whois.arin.net/rest/ip/%s').'" target="_blank">%s</a>',
                                                esc_attr( $form_data['server_remote_addr'] ),
                                                esc_html( $form_data['server_remote_addr'] )
                                            );
                                        }else{
                                           $ip_address = esc_html( $form_data['server_remote_addr'] );  
                                        } 
                                        echo $ip_address ? $ip_address : 'Invalid Ip';
                                    ?></td>
                                </tr>
                            <?php endif; ?>
                        </tbody>
                    </table>
                <?php endif; ?>
        </div>
		<?php
		return ob_get_clean();
	}
}
