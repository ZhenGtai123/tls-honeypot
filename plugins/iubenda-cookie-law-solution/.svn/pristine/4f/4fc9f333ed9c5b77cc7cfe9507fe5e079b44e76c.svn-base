<div id="alert-div-container" class="hidden">
    <div id="alert-div" class="alert is-dismissible m-4" >
        <div class="alert__icon p-4">
            <img id="alert-image" src="<?php echo IUBENDA_PLUGIN_URL ?>/assets/images/banner_failure.svg">
        </div>
        <p id="alert-message" class="text-regular text-left"></p>
        <button class="btn-close mr-3 notice-dismiss">×</button>
    </div>
</div>

<?php require_once (IUBENDA_PLUGIN_PATH . 'views/partials/welcomeScreenHeader.php'); ?>

<?php
$radar = new RadarService();

if (!empty($radar->apiConfiguration) && iub_array_get($radar->apiConfiguration, 'status') == 'completed') {
    require_once IUBENDA_PLUGIN_PATH . '/views/partials/header_scanned.php';
} else {
    ?>
    <div class="p-4 my-5 text-center">
        <span class="inline-spinner lg text-gray"></span>
        <p class="m-0 mt-3 text-md"><?php _e('Analyzing your website', 'iubenda') ?>...</p>
    </div>

    <div class="mt-4 pt-4">
        <h2 class="text-md m-0 mb-4"><?php _e('This is what you may need to be compliant', 'iubenda') ?>:</h2>
    </div>
    <?php
}
?>


<div>
    <ul class="list_radar m-0 mt-4 px-4">
        <?php foreach (iubenda()->serviceRating->rating_calculation_components() as $key => $service) : ?>
            <li class="list_radar__item my-5 my-lg-0 mx-lg-3 list_radar__item--<?php echo iub_array_get($radar->apiConfiguration, 'status') == 'completed' ? iub_array_get($service, 'status') == true ? 'on':'off' : null; ?> iubenda-<?php echo $key ?>-item">
                <figure><img src="<?php echo IUBENDA_PLUGIN_URL ?>/assets/images/list_radar_<?php echo $key; ?>.svg"></figure>
                <p class="text-bold m-0 mx-4"><?php echo $service['label']; ?></p>
            </li>
        <?php endforeach; ?>
    </ul>
</div>
