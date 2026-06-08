<?php
if( !class_exists('Extensions_Cf7_list') ){
    return;
}

$eamil_list_table = new Extensions_Cf7_list();
$eamil_list_table->set_data();  
$eamil_list_table->prepare_items();
$contact_form_title = !empty($_GET['cf7_id']) ? "Of - "  . get_the_title($_GET['cf7_id']) : ''; //phpcs:ignore WordPress.Security.NonceVerification.Recommended	
ob_start();
?>
<div class="wrapp htcf7ext-submissions">
    <div><?php esc_html_e("Email List ", "cf7-extensions"); echo esc_html($contact_form_title); ?></div>
    <ul class="subsubsub">
        <li class="all">
            <a href="#" aria-current="page"><?php esc_html_e('All','cf7-extensions');?></a>
        </li>
    </ul>
    <form method="post" action="" enctype="multipart/form-data">
        <?php
            $eamil_list_table->search_box('search','search_id');  
            $eamil_list_table->display();
        ?>
    </form>
</div><!-- .wrap -->


<?php
echo ob_get_clean(); //phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped