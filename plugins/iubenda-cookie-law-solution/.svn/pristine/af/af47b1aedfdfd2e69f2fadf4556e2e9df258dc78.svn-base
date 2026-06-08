<?php
if (isset($notices) || isset($notice_type)):
    foreach ($notices[$notice_type] as $key => $notice) {
        ?>
        <div class="alert alert--<?php echo($notice_type === 'error' ? 'failure' : 'success'); ?> is-dismissible m-4">
            <div class="alert__icon p-4">
                <img src="<?php echo IUBENDA_PLUGIN_URL ?>/assets/images/banner_<?php echo($notice_type === 'error' ? 'failure' : 'success'); ?>.svg">
            </div>
            <?php
            echo '<p class="text-regular">' . wp_kses_post($notice) . '</p> </br>';
            ?>
            <button class="btn-close mr-3 notice-dismiss dismiss-notification-alert" data-dismiss-key="<?php echo $key ?>"> ×</button>
        </div>
        <?php
    }
endif; ?>