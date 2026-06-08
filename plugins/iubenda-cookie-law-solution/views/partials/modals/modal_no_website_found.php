<div id="modal-no-website-found" class="modal" style="z-index: 999999 !important;">
    <div class="modal__window modal__window--md p-4 p-lg-5">
        <div class="modalSync">
            <img class="ml-4" src="<?php echo IUBENDA_PLUGIN_URL ?>/assets/images/modals/modal_no_website_found.svg" alt="" />
            <h1 class="text-lg">
                <?php _e('Ooops! <br> No website found with this embed code.', 'iubenda') ?>
            </h1>
            <p class="mb-4"><?php _e('It seems that it is not possible to access your data with the code you pasted, do you want to try again or do you prefer to start configuring your website from scratch?', 'iubenda') ?></p>

            <button class="btn btn-gray-lighter btn-block btn-sm mb-3 hide-modal" data-modal-name="#modal-no-website-found" href="javascript:void(0)" onclick="_paq.push(['trackEvent', 'Click', 'Try again']);"><?php _e('Try again', 'iubenda') ?></button>
            <div class="btn btn-gray-lighter btn-block btn-sm show-modal" data-modal-name="#modal-setup-screen" onclick="_paq.push(['trackEvent', 'Click', 'I want to start from scratch']);"> <?php _e('I want to start from scratch', 'iubenda') ?></div>
        </div>
    </div>
</div>