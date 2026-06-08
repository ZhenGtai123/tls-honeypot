<div>

    <div class="text-center mb-5">

        <h1 class="text-xl">
            <?php _e('Your rating', 'iubenda') ?>
        </h1>

        <div class="circularBar" id="iubendaRadarCircularBar" data-perc="<?php echo iubenda()->serviceRating->services_percentage() ?>"></div>

        <p class="text-gray text-md"><?php _e('Here’s how we calculate your rating.', 'iubenda') ?></p>

    </div>


    <ul class="list_radar list_radar--block">
        <?php foreach (iubenda()->serviceRating->rating_calculation_components() as $rating_calculation_component_key => $rating_calculation_component_value) : ?>
            <li class="list_radar__item mb-4 list_radar__item--<?php echo $rating_calculation_component_value['status']?'on':'off'; ?> iubenda-<?php echo $rating_calculation_component_key == 'cons' ? 'cs' : $rating_calculation_component_key ?>-item">
                <figure><img src="<?php echo IUBENDA_PLUGIN_URL ?>/assets/images/list_radar_<?php echo $rating_calculation_component_key; ?>.svg"></figure>
                <div>
                    <h2 class="m-0 mb-2"><?php echo $rating_calculation_component_value['label']; ?></h2>
                    <p><?php echo $rating_calculation_component_value['paragraph']; ?> <a target="_blank" href="<?php echo iubenda()->settings->links["how_{$rating_calculation_component_key}_rate"]; ?>" class="link-underline"><?php _e('Learn More', 'iubenda') ?></a></p>
                </div>

            </li>
        <?php endforeach; ?>
    </ul>

</div>