<?php
/**
 * @phpcs:disable WordPress.Security.NonceVerification.Recommended, WordPress.DB.PreparedSQL.InterpolatedNotPrepared, WordPress.DB.DirectDatabaseQuery.DirectQuery, WordPress.DB.DirectDatabaseQuery.NoCaching
 */
    global $wpdb;
    $entry_id   = !empty($_REQUEST['entry_id']) ? sanitize_text_field($_REQUEST['entry_id']) : 0;
    $form_id    = !empty($_REQUEST['form_id']) ? sanitize_text_field($_REQUEST['form_id']) : 0;

    $table_name   		= $wpdb->prefix.'extcf7_db';
    $current_form_id    = $form_id;
    $mail_form_id   	= $entry_id;
    $cf7_upload_dir 	= wp_upload_dir();
    $cfdb7_dirname  	= $cf7_upload_dir['baseurl'].'/extcf7_uploads';

    $mail_form_data = $wpdb->get_results( $wpdb->prepare("SELECT * FROM $table_name WHERE id = %d LIMIT 1", $mail_form_id ), OBJECT );

    if( !$mail_form_data ){
        echo "<span>".esc_html__('No data found!','cf7-extensions')."</span>";
        return;
    }
?>

<h2><?php echo esc_html__("Email Information","cf7-extensions") ?></h2>
<table class="extcf7-form-data-details">
    <tbody>
        <tr>
            <th><?php echo esc_html__('Date :','cf7-extensions'); ?></th>
            <td><?php echo esc_html(date_format(date_create($mail_form_data[0]->form_date),"F j, Y, g:i a")); ?></td>
        </tr>
        <?php $form_data  = unserialize( $mail_form_data[0]->form_value );
        foreach ($form_data as $key => $data):

            if(false !== strpos($key,'server')) continue;

            if ( strpos($key, 'file') !== false ){
                continue;
                $key_value = str_replace('your-', '', $key);
                $key_value = str_replace( array('-','_'), ' ', $key_value);
                $key_value = ucwords( $key_value );
                echo '<tr><th>'.esc_html__('Attachment :','cf7-extensions').'</th> <td><a href="'.esc_url($cfdb7_dirname.'/'.$data).'">'.esc_html($data).'</a></td></tr>';
            }else{
                if(is_array($data)){
                    $key_value = str_replace('your-', '', $key);
                    $key_value = str_replace( array('-','_'), ' ', $key_value);
                    $key_value = ucwords( $key_value );
                    $array_data =  implode(', ',$data);
                    $array_data =  esc_html( $array_data );
                    echo '<tr><th>'.esc_html($key_value).' :</th><td>'.nl2br(wp_kses_post($array_data)).'</td></tr>';
                }else{
                    $key_value = str_replace('your-', '', $key);
                    $key_value = str_replace( array('-','_'), ' ', $key_value);
                    $key_value = ucwords( $key_value );
                    $data    = esc_html( $data );
                    echo '<tr><th>'.esc_html($key_value).' :</th><td>'.nl2br(wp_kses_post($data)).'</td></tr>';
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
                            echo $ip_address ? esc_html($ip_address) : esc_html__('Invalid Ip','cf7-extensions');
                        ?></td>
                    </tr>
                <?php endif; ?>
            </tbody>
        </table>
    <?php endif; ?>