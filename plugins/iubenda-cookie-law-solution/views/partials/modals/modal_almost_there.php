<div class="modalAlmostThere">

    <div class="text-center">
        <img src="<?php echo IUBENDA_PLUGIN_URL ?>/assets/images/modals/modal_almost_there.svg" alt="" />
        <h2 class="text-lg"><?php _e('Nice! We are almost there.', 'iubenda') ?></h2>
        <p class="text-regular pb-3"><?php _e('Since you already activated some products for this website, we just ask you to copy and paste the embedding code of the product you already have to syncronize your iubenda acount with WP plugin.', 'iubenda') ?></p>
    </div>

    <form class="ajax-form">
        <input hidden name="action" value="update_options">
        <input hidden name="_redirect" value="<?php echo esc_url(add_query_arg(['view' => 'products-page'], iubenda()->base_url)) ?>">

        <h4 class="mb-3"><?php _e('Select products you have already activated', 'iubenda') ?></h4>
        <div class="radio-cards pb-3 mb-4">

            <?php foreach(iubenda()->settings->services as $key => $service): ?>
                <label for="radio-card-<?php echo $key; ?>" class="radio-card">
                    <input type="checkbox" name="iubenda_<?php echo $service['name']; ?>_solution_status" class="select-product-checkbox section-checkbox-control<?php if($key == 'cs'): echo ' required-control'; endif;?>" data-section-name="#section-<?php echo $key; ?>" <?php if($key == 'cs'): echo 'data-required-control="#submit-btn"'; endif;?> value="true" id="radio-card-<?php echo $key; ?>" <?php echo $service['status']=='true' ? 'checked':''; ?>/>
                    <span class="check-icon"></span>

                    <div>
                        <img src="<?php echo IUBENDA_PLUGIN_URL ?>/assets/images/checkboxes/<?php echo $key; ?>_icon.svg" alt="<?php echo $service['label']; ?>" />
                        <span>
                            <?php echo $service['label']; ?>
                            <?php if ($key == 'cs'): ?>
                                <span style="color: rgb(207, 116, 99);"><?php _e('(required)', 'iubenda') ?></span>
                            <?php endif; ?>
                        </span>
                    </div>
                </label>

            <?php endforeach; ?>

        </div>

        <?php foreach(iubenda()->settings->services as $key => $service): ?>
            <?php if ($key == 'cons'): ?>
                <section id="section-<?php echo $key; ?>" class="<?php echo $service['status']=='true' ? '':'hidden'; ?>">
                    <h4 class="mb-3"><?php _e('Consent Solution API key', 'iubenda') ?></h4>
                    <fieldset class="paste_embed_code">
                        <input name="public_api_key" class="form field-input" type="text" value="<?php echo iubenda()->options['cons']['public_api_key'] ?>" placeholder="<?php _e('Paste your API key here', 'iubenda') ?>">
                    </fieldset>
                    <div class="text-right mt-2">
                        <a target="_blank" href="<?php echo iubenda()->settings->links['how_generate_cons']; ?>" class="link link-helper"><span class="tooltip-icon mr-2">?</span><?php _e('Where can I find this code?', 'iubenda') ?></a>
                    </div>
                </section>
            <?php else: ?>
                <section id="section-<?php echo $key; ?>" class="<?php echo $service['status']=='true' ? '':'hidden'; ?>">
                    <h4 class="mb-3"><?php echo $service['label']; ?></h4>
                    <?php
                    // Check if we support current theme to attach legal
                    if (!iubenda()->check_if_we_support_current_theme_to_attach_legal()) {
                        $url = 'javascript:void(0)';

                        if(iubenda()->widget->check_current_theme_supports_widget()){
                            $url = admin_url( 'widgets.php' );
                        }elseif(iubenda()->block->check_current_theme_supports_blocks()){
                            $url = admin_url( 'site-editor.php' );
                        }

                        ?>
                        <div class="notice notice--warning mt-2 mb-4 p-3 d-flex align-items-center text-warning text-xs">
                            <img class="mr-2" style="width: 3rem !important" src="<?php echo IUBENDA_PLUGIN_URL ?>/assets/images/warning-icon.svg">
                            <p><?php echo sprintf( __( 'We were not able to add a "Legal" widget/block to the footer as your theme is not compatible, you can position the "Legal" widget/block manually from <a href="%s" target="_blank">here</a>.', 'iubenda' ), esc_url( $url ) ) ?></p>
                        </div>
                        <?php
                    }
                    ?>
                    <?php require IUBENDA_PLUGIN_PATH . '/views/partials/languagesTabs.php'; ?>
                </section>
            <?php endif; ?>

        <?php endforeach; ?>

        <div class="text-center">
            <button type="submit" class="btn btn-green-primary btn-sm mt-5 hidden" id="submit-btn" onclick="_paq.push(['trackEvent', 'Click', 'Synchronize products']);">
                <span class="button__text"><?php _e('Synchronize products', 'iubenda') ?></span>
            </button>
        </div>

    </form>

</div>