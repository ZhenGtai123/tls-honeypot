<div class="mb-3 p-0">

  <fieldset class="paste_embed_code tabs tabs--style2">

    <ul class="tabs__nav">
      <?php foreach(iubenda()->languages as $k => $v): ?>
        <li id="<?php echo "code_{$k}-iubenda_{$service['name']}_solution_tab" ?>" class="tabs__nav__item <?php echo $k == iubenda()->lang_default?'active':false ; ?>" data-target="tab-<?php echo $k ; ?>"  data-group="language-tabs">
          <?php echo strtoupper($k) ; ?>
        </li>
      <?php endforeach; ?>
    </ul>

    <?php
    $product_helper = new ProductHelper();

    foreach($product_helper->get_languages() as $lang_id => $v):
        $method = "get_{$key}_embed_code_by_lang";
        $code = $product_helper->{$method}($lang_id);
    ?>
        <div data-target="tab-<?php echo $lang_id ; ?>" class="tabs__target <?php echo $lang_id == iubenda()->lang_default || $lang_id == 'default'? 'active': '' ; ?>" data-group="language-tabs">
            <textarea class='form-control text-sm m-0 iub-language-code iub-embed-code-<?php echo $key; ?>' data-language="<?php echo $lang_id; ?>" placeholder='<?php _e('Paste your embed code here', 'iubenda') ?>' name='iubenda_<?php echo $service['name']; ?>_solution[code_<?php echo $lang_id ; ?>]' rows='4'><?php echo $code ?></textarea>
        </div>
    <?php endforeach; ?>

  </fieldset>
  <div class="text-right mt-2">
    <a target="_blank" href="<?php echo iubenda()->settings->links["how_generate_{$key}"]; ?>" class="link link-helper"><span class="tooltip-icon mr-2">?</span><?php _e('Where can I find this code?', 'iubenda') ?></a>
  </div>
</div>