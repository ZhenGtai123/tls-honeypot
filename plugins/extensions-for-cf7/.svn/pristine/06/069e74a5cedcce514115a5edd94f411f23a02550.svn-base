<?php
if( !class_exists('Extensions_Cf7_list') ){
    return;
}

$eamil_list_table = new Extensions_Cf7_list();
$eamil_list_table->set_data();  
$eamil_list_table->prepare_items();
$contact_form_title = !empty($_GET['cf7_id']) ? "Of - "  . get_the_title($_GET['cf7_id']) : '';
ob_start();
?>
<div class="wrapp htcf7ext-submissions">
    <div><?php _e("Email List $contact_form_title","cf7-extensions") ?></div>
    <ul class="subsubsub">
        <li class="all">
            <a href="#" aria-current="page">All</a>
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
echo ob_get_clean();