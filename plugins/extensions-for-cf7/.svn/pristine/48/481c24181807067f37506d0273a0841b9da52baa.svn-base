<?php
global $wpdb;
$cf7_data   = [];

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
    $total_email = $wpdb->get_var("SELECT COUNT(*) FROM $table_name WHERE form_id = $cf7_post_id");
    $link  = "<a href=admin.php?page=contat-form-list&cf7_id=$cf7_post_id>%s</a>";
    $cf7_value['id']  = $cf7_post_id;
    $cf7_value['name']  = $title;
    $cf7_value['count'] = $total_email;
    $cf7_data[] = $cf7_value;
}

ob_start();
?>
 <div class="htcf7ext-list-area">
    <table>
        <thead>
            <tr>
            <th>ID</th>
            <th>Form Name</th>
            <th>Submissions</th>
            </tr>
        </thead>
        <tbody>

            <?php foreach ($cf7_data as $value): ?>
                <tr>
                    <td><?php echo ($value['id']); ?></td>
                    <td><?php echo ($value['name']); ?></td>
                    <td><a href="<?php echo esc_url(admin_url('admin.php?page=contat-form-list&cf7_id='. $value['id'] .'#/entries')) ?>">View <span>(<?php echo ($value['count']); ?>)</span></a></td>
                </tr>
            <?php endforeach ?>

        </tbody>
    </table>
</div>
<?php echo apply_filters('htcf7ext_dashboard_general', ob_get_clean() ); ?>