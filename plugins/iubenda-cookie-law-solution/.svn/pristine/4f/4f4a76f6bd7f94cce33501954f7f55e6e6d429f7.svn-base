<ul class="breadcrumb text-gray">
  <li class="breadcrumb__item"><a href="<?php echo add_query_arg( array('view' => 'products-page'), iubenda()->base_url ); ?>"><?php _e('Products', 'iubenda') ?></a></li>
  <?php
     foreach($pageLabels as $pageLabel){
        if(end($pageLabels) === $pageLabel){
            $textStyle = 'text-bold';
        }else{
            $textStyle = '';
        }

        $href = iub_array_get($pageLabel, 'href') ?? 'javascript:void(0)';
       echo "<li class='breadcrumb__item {$textStyle}'><a href='{$href}'>".iub_array_get($pageLabel, 'title')."</a></li>";
     }
  ?>
</ul>

<?php if(iubenda()->settings->print_notices()): ?>
    <div class="p-3 m-3">
        <?php iubenda()->settings->print_notices() ?>
    </div>
<?php endif; ?>