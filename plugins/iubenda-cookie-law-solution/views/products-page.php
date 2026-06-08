<?php require_once IUBENDA_PLUGIN_PATH . '/views/partials/header.php'; ?>
<div class="main-box">
    <?php require_once IUBENDA_PLUGIN_PATH . '/views/partials/siteInfo.php'; ?>
    <div class="p-3 m-3">
        <?php
            $result = array_filter(array_column($this->services, 'status'), function ($service) {
                return (stripos($service, 'false') === false);
            });
            if (!$result) {
                ?>
                <div class="alert alert--failure is-dismissible m-4">
                    <div class="alert__icon p-4">
                        <img src="<?php echo IUBENDA_PLUGIN_URL . '/assets/images/banner_failure.svg' ?>">
                    </div>
                    <p id="products-page-alert-text" class="text-regular"><?php _e('It seems that you have not activated any of our services, we recommend you to activate them and increase your level of compliance and avoid risking fines.', 'iubenda') ?></p>
                    <button class="btn-close mr-3 notice-dismiss">×</button>
                </div>
                <?php
            }

            if(iubenda()->settings->print_notices()){
                iubenda()->settings->print_notices();
            }
        ?>
        <div class="configure-services-cards">
            <?php
            foreach (iubenda()->settings->services as $serviceKey => $serviceOptions) :
                require IUBENDA_PLUGIN_PATH . '/views/partials/product-card.php';
            endforeach;
            ?>
        </div>
    </div>
</div>
<?php require_once IUBENDA_PLUGIN_PATH . 'views/partials/footer.php'; ?>
