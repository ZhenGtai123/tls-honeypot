<div class="service-card">

  <div class="flex-fill d-flex flex-direction-column">

    <div class="d-flex justify-content-end p-3">
      <a target="_blank" href="<?php echo iubenda()->settings->links["about_{$serviceKey}"]; ?>" class="tooltip-icon">?</a>
    </div>

    <div class="text-center pb-4 flex-fill d-flex align-items-center justify-content-center flex-direction-column">
      <img src="<?php echo IUBENDA_PLUGIN_URL ?>/assets/images/service_cards/<?php echo $serviceKey; ?>_icon.svg">
      <h3 class="text-regular text-bold text-gray m-0"><?php echo $serviceOptions['label']; ?></h3>
    </div>

    <?php
        //Check if the site_id is not entered before
        $site_id = iub_array_get(iubenda()->options['global_options'], 'site_id') ?: null;
        if(isset($serviceOptions['settings']) && $site_id):
     ?>
      <ul id="configiration-iubenda-<?php echo $serviceKey ?>" class="service-on text-gray text-xs " <?php echo $serviceOptions['status']!='true' ? 'style="display: none;"':''; ?> id="toggleServiceOn">
        <?php
        foreach (iub_array_get($serviceOptions, 'settings', []) ?: [] as $setting) :
            $value = '';
            if ($setting['label'] === 'Version') {
                continue;
            }

            if($setting['value'] == 'black'){
                $value = 'Dark';
            }elseif($setting['value'] == 'white'){
                $value = 'Light';
            }else{
                $value = $setting['value'];
            }
          ?>
            <li class="mr-3"><span class="text-bold"><?php echo ucfirst($setting['label']); ?>:</span> <?php echo ucfirst($value); ?></li>
        <?php endforeach; ?>
      </ul>
    <?php endif; ?>

    <hr>

    <div class="d-flex align-items-center justify-content-between p-3">
      <div class="switch align-items-center">
        <input type="checkbox" class="service-checkbox" data-redirect="<?php echo add_query_arg(array('view' => "$serviceKey-configuration"), iubenda()->base_url ); ?>" data-service-key="iubenda-<?php echo $serviceKey; ?>" data-service-name="iubenda_<?php echo $serviceOptions['name']; ?>_solution" id="toggle-<?php echo $serviceKey; ?>" <?php echo $serviceOptions['status']=='true' ? 'checked':' '; ?> />
        <label for="toggle-<?php echo $serviceKey; ?>"></label>
          <p class="notification text-xs text-bold text-gray-lighter ml-2" id="<?php echo "iubenda-{$serviceKey}-status-label" ?>" data-status-label-off="<?php _e('Service off', 'iubenda') ?>"><?php $serviceOptions['status']=='true' ? _e('Service on', 'iubenda') : _e('Service off', 'iubenda') ?></p>
      </div>
        <a class="btn btn-gray-lighter btn-xs" href="<?php echo add_query_arg(array('view' => "$serviceKey-configuration"), iubenda()->base_url ); ?>" onclick="_paq.push(['trackEvent', 'Click', '<?php echo $serviceOptions['label']. " configuration" ?>']);"><?php _e('Configure', 'iubenda') ?></a>
    </div>

  </div>
</div>