<?php

$positions = [
  'float-top-left',
  'float-top-center',
  'float-top-right',
  'float-bottom-left',
  'float-bottom-center',
  'float-bottom-right',
  'full-top',
  'full-bottom',
  'float-center'
];

?>
<div class="cs_banner_choices mb-5 mb-lg-0">
  
  <div class="cs_banner_choices__position mr-4 pr-4">

    <h4><?php _e('Position', 'iubenda') ?></h4>

    <div class="position-select">

      <div id="dropdown">

          <?php foreach($positions as $v): ?>
              <input type="radio" class="position-select-radio" name="iubenda_cookie_law_solution[simplified][position]" value="<?php echo $v; ?>" id="<?php echo $v ; ?>" <?php
              checked( $v, iub_array_get(iubenda()->options['cs'], 'simplified.position'), true);
              ?> >
          <label for="<?php echo $v ; ?>">
            <div>
              <div class="<?php echo str_replace('-', ' ', $v) ; ?>"><span></span></div>
            </div>
          </label>
        <?php endforeach; ?>

        <div class="overlaybox p-0">
          <div class="p-3">
              <label class="checkbox-regular">
              <input type="checkbox" class="mr-2" name="iubenda_cookie_law_solution[simplified][background_overlay]" <?php echo checked( true, (bool) iub_array_get(iubenda()->options['cs'], 'simplified.background_overlay'), false); ?>>
              <span><?php _e('Background-overlay', 'iubenda') ?></span>
            </label>
          </div>
        </div>

      </div>

    </div>

  </div>

</div>