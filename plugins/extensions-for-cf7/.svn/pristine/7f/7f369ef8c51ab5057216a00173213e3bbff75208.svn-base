<?php
/**
 * @phpcs:disable WordPress.DB.DirectDatabaseQuery.DirectQuery, WordPress.DB.DirectDatabaseQuery.NoCaching
 */
if( ! defined( 'ABSPATH' ) ) exit(); // Exit if accessed directly

/**
 * CF7 Post List
*/
class Extensions_Cf7_Post_List implements Extensions_Cf7_Form_Datalist_Render
{
	
    /**
     * Contact Form 7 post list
     * @return postlist data
    */
	function contact_form_list(){
        global $wpdb;
        $cf7_data    = [];

        $args = array(
            'post_type'=> 'wpcf7_contact_form',
            'order'    => 'ASC',
            'posts_per_page' => -1
        );

        $the_query = new WP_Query( $args );

        while ( $the_query->have_posts() ){ 
            $the_query->the_post();
            $cf7_post_id = get_the_id();
            $title = get_the_title();
            $table_name = $wpdb->prefix . 'extcf7_db';
            $total_email = $wpdb->get_var($wpdb->prepare("SELECT COUNT(*) FROM $table_name WHERE form_id = %d ", $cf7_post_id));//phpcs:ignore WordPress.DB.PreparedSQL.InterpolatedNotPrepared
            $link  = "<a href=admin.php?page=contat-form-list&cf7_id=$cf7_post_id>%s</a>";
            $cf7_value['name']  = sprintf( $link, $title );
            $cf7_value['count'] = sprintf( $link, $total_email );
            $cf7_data[] = $cf7_value;
        }
        return $cf7_data;
    }

    /**
     * Contact Form 7 post list layout
     * @return postlist layout
    */
    function cf7_layout_render(){
        $form_data = $this->contact_form_list();
        ob_start();
        ?>
        <h2><?php echo esc_html__('Contact Form List','cf7-extensions') ?></h2>
        <div class="ht-cf7-formlist-info">
            <table class="ht-cf7-formlist-table">
                <tr>
                    <th><?php echo esc_html__('Form Name','cf7-extensions') ?></th>
                    <th><?php echo esc_html__('Submission Count','cf7-extensions');?></th>
                </tr>
                <tbody>
                    <?php foreach ($form_data as $value): ?>
                        <tr>
                            <td><?php echo wp_kses_post($value['name']); ?></td>
                            <td><?php echo wp_kses_post($value['count']); ?></td>
                        </tr>
                    <?php endforeach ?>
                </tbody>
            </table>
        </div>
        <?php
        return ob_get_clean();
    }
}