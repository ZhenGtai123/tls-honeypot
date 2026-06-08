<?php
// exit if accessed directly
if (!defined('ABSPATH'))
    exit;

/**
 * Class QuickGeneratorService
 */
class QuickGeneratorService
{
    public $QG_Response = [];

    public function __construct(){
        $this->QG_Response = get_option(iubenda_Settings::IUB_QG_Response, []) ?: [];
    }

    protected function get_mapped_language_on_local($iub_lang_code)
    {
        $result = [];
        $iub_lang_code = strtolower(str_replace('-', '_', $iub_lang_code));

        foreach (iubenda()->languages_locale as $wordpress_locale => $lang_code) {
            // lower case and replace - with underscore
            $lower_wordpress_locale = strtolower(str_replace('-', '_', $wordpress_locale));
            // Map after all both codes becomes lower case and underscore

            // Map en iubenda language to wordpress languages en_us
            if ($iub_lang_code == 'en' && $lower_wordpress_locale == 'en_us') {
                $result[] =  $lang_code;
                continue;
            }

            // Map iubenda language to wordpress languages
            if ($iub_lang_code == $lower_wordpress_locale) {
                $result[] =  $lang_code;
                continue;
            }

            // Map pt iubenda language to pt-pt
            if ($iub_lang_code == 'pt' && $lower_wordpress_locale == 'pt_pt') {
                $result[] =  $lang_code;
                continue;
            }

            // Cases iubenda languages without _ mapped to
            if ($iub_lang_code == strstr($lower_wordpress_locale, '_', true) && $iub_lang_code != 'pt') {
                $result[] =  $lang_code;
                continue;
            }
            // Map any XX_ iubenda language to any wordpress languages starts with XX_
            if ((strpos($iub_lang_code, '_') === 0 && strstr($iub_lang_code, '_', true)) && (strpos($lower_wordpress_locale, '_') === 0 && strstr($lower_wordpress_locale, '_', true))) {
                $result[] =  $lang_code;
                continue;
            }

            if ($lower_wordpress_locale == $iub_lang_code) {
                $result[] =  $lang_code;
                continue;
            }
        }

        return $result;
    }

    public function quick_generator_api()
    {
        $public_ids = [];
        $privacy_policies = [];
        $site_id = null;

        $body = iub_array_get($_POST, 'payload');
        $user = iub_array_get($body, 'user');

        $multi_lang = boolval(iubenda()->multilang && !empty(iubenda()->languages));

        foreach (iub_array_get($body, 'privacy_policies', []) ?? [] as $key => $privacy_policy) {
            //getting site id to save it into Iubenda global option
            if(!$site_id){
                $site_id = iub_array_get($privacy_policy, 'site_id');
            }

            if($multi_lang){
                if($local_lang_codes = $this->get_mapped_language_on_local($privacy_policy['lang'])){
                    foreach ($local_lang_codes as $local_lang_code){
                        $privacy_policies[$local_lang_code] = $privacy_policy;

                        //getting public id to save it into Iubenda global option default lang
                        $public_ids[$local_lang_code] = iub_array_get($privacy_policy, 'public_id');
                    }
                }

                // Getting supported local languages intersect with iubenda supported languages
                $iubenda_intersect_supported_langs = (new ProductHelper())->get_local_supported_language();

                // Fallback to default language if no supported local languages intersect with iubenda supported languages
                if (empty($iubenda_intersect_supported_langs)) {
                    $public_ids[iubenda()->lang_default] = iub_array_get($privacy_policy, 'public_id');
                }
            }else{
                $privacy_policies['default'] = $privacy_policy;

                //getting public id to save it into Iubenda global option default lang
                $public_ids['default'] = iub_array_get($privacy_policy, 'public_id');
            }
        }

        $configuration = [
            'website' => iub_array_get($_POST, 'website'),
            'user' => [
                'id' => iub_array_get($user, 'id'),
                'email' => iub_array_get($user, 'email'),
            ],
            'privacy_policies' => $privacy_policies,
        ];

        update_option(iubenda_Settings::IUB_QG_Response, $configuration);
        update_option( 'iubenda_global_options', ['site_id' => $site_id, 'public_ids' => $public_ids] );

        iubenda()->settings->add_notice( 'iub_integrated_success', __( 'Your website has been created and your legal documents have been generated. Setup your cookie banner and privacy policy button to complete the integration.', 'iubenda' ), 'success' );

        echo json_encode([
            'status' => 'done',
            'redirect' =>  admin_url( 'admin.php?page=iubenda&view=integrate-setup') ,
        ]);
        wp_die();
    }

    public function integrate_setup()
    {
        // Saving iubenda plugin settings
        $this->plugin_settings_save_options();

        if(iub_array_get($_POST, 'cookie_law') == 'on'){
            // Saving CS data with CS function
            $this->cs_save_options();
        }

        if(iub_array_get($_POST, 'privacy_policy') == 'on'){
            // Saving PP data with PP function
            $this->pp_save_options();
        }
        
        if (iub_array_get($_POST, 'cookie_law') == 'on' || iub_array_get($_POST, 'privacy_policy') == 'on') {
            //add notice that`s notice user the integrate has been done successfully
            iubenda()->settings->add_notice('iub_integrated_success', __('Our products has been integrated successfully, now customize all products to increase the compliance rating and make your website fully compliant.', 'iubenda'), 'success');
        }

        // Encourage user to verify his account
        $iub_notifications = get_option(iubenda_Settings::IUB_NOTIFICATIONS, []) ?: [];
        $iub_notifications['iub_user_needs_to_verify_his_account'] = true;
        update_option(iubenda_Settings::IUB_NOTIFICATIONS, $iub_notifications);

        echo json_encode(['status' => 'done']);
        wp_die();
    }

    public function save_public_api_key()
    {
        if(empty(iub_array_get($_POST, 'public_api_key'))){
            echo json_encode(['status' => 'error', 'responseText' => "invalid public API key"  ]);
            wp_die();
        }
        update_option('iubenda_consent_solution', ['public_api_key' => iub_array_get($_POST, 'public_api_key')]);

        $iubenda_activated_products = get_option('iubenda_activated_products');
        $iubenda_activated_products['iubenda_consent_solution'] = 'true';
        update_option('iubenda_activated_products', $iubenda_activated_products);

        echo json_encode(['status' => 'done']);
        wp_die();
    }

    public function auto_detect_forms()
    {
        iubenda()->forms->autodetect_forms();

        require_once IUBENDA_PLUGIN_PATH . 'views/partials/auto_detect_forms.php';
        wp_die();

    }

    public function add_footer()
    {
        if(iub_array_get(iubenda()->settings->services, 'pp.status') == 'true' && iub_array_get(iubenda()->options['pp'], 'button_position') == 'automatic'){
            echo $this->pp_button();
        }
        if(iub_array_get(iubenda()->settings->services, 'tc.status') == 'true' && iub_array_get(iubenda()->options['tc'], 'button_position') == 'automatic'){
            echo $this->tc_button();
        }
    }

    public function tc_button_shortcode(){
        if ((iub_array_get(iubenda()->settings->services, 'tc.status') == 'true') && (iub_array_get(iubenda()->options['tc'], 'button_position') == 'manual')) {
            return $this->tc_button();
        }
        return "[iub-tc-button]";
    }

    public function tc_button(){
        if ( iubenda()->multilang && ! empty( iubenda()->lang_current ) ) {
            $code = iub_array_get(iubenda()->options, 'tc.code_'.iubenda()->lang_current) ?? null;
        } else {
            $code = iub_array_get(iubenda()->options, 'tc.code_default') ?? null;
        }

        return $code;
    }

    public function pp_button_shortcode(){
        if (iub_array_get(iubenda()->settings->services, 'pp.status') == 'true' && iub_array_get(iubenda()->options['pp'], 'button_position') != 'automatic') {
            return $this->pp_button();
        }
        return "[iub-pp-button]";
    }

    public function pp_button(){
        $privacy_policy_generator = new PrivacyPolicyGenerator();

        if ( iubenda()->multilang && ! empty( iubenda()->lang_current ) ) {
            $code = iub_array_get(iubenda()->options, 'pp.code_'.iubenda()->lang_current) ?? null;
        } else {
            $code = iub_array_get(iubenda()->options, 'pp.code_default') ?? null;
        }

        if (!$code){
            if ( iubenda()->multilang && ! empty( iubenda()->lang_current ) ) {
                $public_id = iub_array_get(iubenda()->options['global_options'], 'public_ids.'.iubenda()->lang_current);
            } else {
                $public_id = iub_array_get(iubenda()->options['global_options'], 'public_ids.default');
            }

            $code = $privacy_policy_generator->handle('default', $public_id, iub_array_get(iubenda()->options, 'pp.button_style'));
        }

        return $code;
    }

    public function ajax_save_options()
    {
        $iubenda_section_name = iub_array_get($_POST, 'iubenda_section_name');
        $iubenda_section_key = iub_array_get($_POST, 'iubenda_section_key');

        // If section == CS save by CS function
        if($iubenda_section_key == 'cs'){
            $this->cs_save_options(false);
        }

        // Elseif section == Plugin-settings save by plugin settings function
        elseif($iubenda_section_key == 'plugin-settings'){
            $this->plugin_settings_save_options(false);
        }

        else{
            $codes_statues = [];
            $global_options = iubenda()->options['global_options'];

            $section_new_option = iub_array_get($_POST, $iubenda_section_name);
            $old_section_options = iubenda()->options[$iubenda_section_key];

            if($iubenda_section_name == 'iubenda_terms_conditions_solution') {
                foreach($section_new_option as $index => $option) {
                    if(substr( $index, 0, 5 ) === "code_"){
                        $parsed_code = iubenda()->parse_tc_pp_configuration(stripslashes_deep($option));

                        if ($parsed_code) {
                            $codes_statues["{$iubenda_section_name}_codes"][] = true;
                            $global_options['public_ids'][substr($index, 5)] = iub_array_get($parsed_code, 'cookie_policy_id');
                        }else{
                            $codes_statues["{$iubenda_section_name}_codes"][] = false;
                        }
                    }
                }

                // validating Embed Codes of TC contains at least one valid code
                if(count(array_filter($codes_statues["{$iubenda_section_name}_codes"])) == 0){
                    echo json_encode(['status' => 'error', 'responseText' => "( {$iubenda_section_name} ) At least one code must be valid."]);
                    wp_die();
                }
            }

            // Update buttons style & position
            // Privacy policy Button
            if($iubenda_section_name == 'iubenda_privacy_policy_solution') {
                // Add a widget in the sidebar if the button is positioned automatically
                if('automatic' === iub_array_get($section_new_option, 'button_position')){
                    iubenda()->assign_legal_block_or_widget();
                }

                // Merge old old PP options with new options to update codes with new style
                $old_section_options = $old_section_options ? $this->stripslashes_deep($old_section_options) : [];
                $section_new_option = array_merge($old_section_options, $section_new_option);

                // Update PP codes with new button style
                $section_new_option = $this->update_button_style($section_new_option, 'pp');
            }

            // Terms and conditions Button
            if($iubenda_section_name == 'iubenda_terms_conditions_solution') {
                // Add a widget in the sidebar if the button is positioned automatically
                if('automatic' === iub_array_get($section_new_option, 'button_position')){
                    iubenda()->assign_legal_block_or_widget();
                }

                // Update TC codes with new button style
                $section_new_option = $this->update_button_style($section_new_option, 'tc');
            }

            //set the product configured option true
            $section_new_option['configured'] = 'true';

            $iubenda_activated_products = get_option('iubenda_activated_products');
            $iubenda_activated_products[$iubenda_section_name] = 'true';
            update_option('iubenda_activated_products', $iubenda_activated_products);

            $section_new_option = $this->stripslashes_deep($section_new_option);
            if($old_section_options){
                $old_section_options = $this->stripslashes_deep($old_section_options);
                $section_new_option = array_merge($old_section_options, $section_new_option);
            }
            update_option($iubenda_section_name, $section_new_option);

            //update iubenda global options (public_ids)
            update_option( 'iubenda_global_options', $global_options );
        }

        echo json_encode(['status' => 'done']);
        wp_die();
    }

    private function prepare_custom_scripts_iframes($data, $flag ) {
        return array_combine(
            iub_array_get($data, $flag),
            iub_array_get($data, 'type')
        );
    }

    private function stripslashes_deep($value)
    {
        $value = is_array($value) ?
            array_map('stripslashes_deep', $value) :
            stripslashes($value);

        return $value;
    }

    /**.
     * Update button style in options
     *
     * @param $options
     * @param $service
     * @return array
     */
    public function update_button_style($options, $service): array
    {
        if($service == 'pp'){
            $privacy_policy_generator = new PrivacyPolicyGenerator();
        }

        $new_options = [];
        $button_style = iub_array_get($options, 'button_style');

        foreach($options as $key => $index){
            $new_options[$key] = $index;

            if(substr( $key, 0, 5 ) === "code_"){
                if($service == 'pp'){
                    // Get public_id for this language
                    $public_id = iub_array_get(iubenda()->options['global_options'], "public_ids.".substr( $key, 5 ), false) ?: false;

                    if ((!$index || empty($index)) && $public_id) {
                        $index = $privacy_policy_generator->handle(substr( $key, 5 ), $public_id, iubenda()->options['pp']);
                    }
                }
                
                $new_code = str_replace(['iubenda-black', 'iubenda-white'], "iubenda-{$button_style}",$index);
                $new_options[$key] = $new_code;
            }
        }
        return $new_options;
    }

    /**
     * saving Iubenda cookie law solution options
     * @param bool $default_options
     */
    private function cs_save_options($default_options = true)
    {
        $iubenda_cookie_solution_generator = new CookieSolutionGenerator;
        $global_options = iubenda()->options['global_options'];

        $codes_statues = [];
        $site_id = null;
        $new_cs_option = iub_array_get($_POST, 'iubenda_cookie_law_solution');

        if (!$default_options) {
            //CS plugin general options
            $new_cs_option['parse'] = (bool)isset($new_cs_option['parse']);
            $new_cs_option['parser_engine'] = isset($new_cs_option['parser_engine']) && in_array($new_cs_option['parser_engine'], ['default', 'new']) ? $new_cs_option['parser_engine'] : iubenda()->defaults['cs']['parser_engine'];
            $new_cs_option['skip_parsing'] = (bool)isset($new_cs_option['skip_parsing']);
            $new_cs_option['amp_support'] = iub_array_get($new_cs_option, 'amp_support', false) ?: false;
        }

        if(isset($new_cs_option['custom_scripts'])){
            $new_cs_option['custom_scripts'] = $this->prepare_custom_scripts_iframes( iub_array_get($new_cs_option, 'custom_scripts'), 'script');

            // Set all selected values Int to not break compatibility with old version
            $new_cs_option['custom_scripts'] = array_map('intval' , $new_cs_option['custom_scripts']);
        }else{
            $new_cs_option['custom_scripts'] = [];
        }

        if(isset($new_cs_option['custom_iframes'])){
            $new_cs_option['custom_iframes'] = $this->prepare_custom_scripts_iframes( iub_array_get($new_cs_option, 'custom_iframes'), 'iframe');

            // Set all selected values Int to not break compatibility with old version
            $new_cs_option['custom_iframes'] = array_map('intval' , $new_cs_option['custom_iframes']);
        }else{
            $new_cs_option['custom_iframes'] = [];
        }

        if ('simplified' === iub_array_get($new_cs_option, 'configuration_type')) {
            // Check explicit accept & reject forced on if TCF is on
            if(true == iub_array_get($new_cs_option, 'simplified.tcf')){
                $new_cs_option['simplified']['explicit_accept'] = 'on';
                $new_cs_option['simplified']['explicit_reject'] = 'on';
            }
            $languages = (new ProductHelper())->get_languages();
            // loop on iubenda->>language
            foreach ($languages as $lang_id => $lang_name) {
                $privacy_policy_id = iub_array_get($global_options, "public_ids.{$lang_id}");

                if(!$privacy_policy_id){
                    continue;
                }

                $site_id = iub_array_get(iubenda()->options, 'global_options.site_id') ?: null;

                // Generating CS Simplified code
                $cs_embed_code = $iubenda_cookie_solution_generator->handle($lang_id, $site_id, $privacy_policy_id, iub_array_get($new_cs_option, 'simplified'));

                $new_cs_option["code_{$lang_id}"] = $this->stripslashes_deep($cs_embed_code);

                // generate amp template file if the code is valid
                if($cs_embed_code){
                    // generate amp template file
                    if ($new_cs_option['amp_support']) {
                        $template_done[$lang_id] = false;

                        $template_done[$lang_id] = (bool)iubenda()->AMP->generate_amp_template($cs_embed_code, $lang_id);

                        // Check if AMP is checked and the auto generated option is selected
                        if ("1" == $new_cs_option['amp_support'] && 'local' == $new_cs_option['amp_source']) {

                            if (is_bool($template_done[$lang_id]) && false === $template_done[$lang_id]) {
                                $this->add_amp_permission_error();
                            }
                        }

                        $new_cs_option['amp_template_done'] = $template_done;

                        // TODO need to checked with AMP files url
                        if (is_array($new_cs_option['amp_template'])) {
                            foreach ($new_cs_option['amp_template'] as $lang => $template) {
                                $new_cs_option['amp_template'][$lang] = esc_url($template);
                            }
                        } else {
                            $new_cs_option['amp_template'] = esc_url($new_cs_option['amp_template']);
                        }
                    }
                }
            }
        }
        elseif('manual' === iub_array_get($new_cs_option, 'configuration_type')){
            foreach($new_cs_option as $index => $option) {
                //check code if valid or not
                if (substr($index, 0, 5) === "code_" && !empty($option)) {
                    // Getting data from embed code
                    $parsed_code = iubenda()->parse_configuration(stripslashes_deep($option));

                    // if code parsed correctly
//                    if(!$parsed_code){
//                        $codes_statues[substr($index, 5)] = false;
//                        continue;
//                    }
                    $new_cs_option['manual_'."$index"] =  $option;
                    $codes_statues[substr($index, 5)] = true;

                    //getting cookiePolicyId to save it into Iubenda global option
                    if(iub_array_get($parsed_code, 'cookiePolicyId') ?: null){
                        $global_options['public_ids'][substr($index, 5)] = iub_array_get($parsed_code, 'cookiePolicyId');
                    }

                    //getting site id to save it into Iubenda global option
                    if(!$site_id && iub_array_get($parsed_code, 'siteId') ?: null){
                        $site_id = iub_array_get($parsed_code, 'siteId');
                    }

                    // generate amp template file
                    if ($new_cs_option['amp_support']) {
                        $lang_id = substr($index, 5);
                        $template_done[$lang_id] = false;

                        $template_done[$lang_id] = (bool)iubenda()->AMP->generate_amp_template(stripslashes_deep($option), $lang_id);

                        // Check if AMP is checked and the auto generated option is selected
                        if ("1" == $new_cs_option['amp_support'] && 'local' == $new_cs_option['amp_source']) {

                            if (is_bool($template_done[$lang_id]) && false === $template_done[$lang_id]) {
                                $this->add_amp_permission_error();
                            }
                        }

                        $new_cs_option['amp_template_done'] = $template_done;

                        // TODO need to checked with AMP files url
                        if (is_array($new_cs_option['amp_template'])) {
                            foreach ($new_cs_option['amp_template'] as $lang => $template) {
                                $new_cs_option['amp_template'][$lang] = esc_url($template);
                            }
                        } else {
                            $new_cs_option['amp_template'] = esc_url($new_cs_option['amp_template']);
                        }
                    }
                }
            }
            // validating Embed Codes of CS contains at least one valid code
            if(count(array_filter($codes_statues)) == 0){
                echo json_encode(['status' => 'error', 'responseText' => "( Iubenda cookie law solution ) At least one code must be valid."]);
                wp_die();
            }
        }

        //set the product configured option true
        $new_cs_option['configured'] = 'true';

        // update only cs make it activated service
        iubenda()->options['activated_products']['iubenda_cookie_law_solution'] = 'true';
        update_option('iubenda_activated_products', iubenda()->options['activated_products']);

        // saving new options merged by old options
        $new_cs_option = $this->stripslashes_deep($new_cs_option);
        $old_cs_options = $this->stripslashes_deep(iubenda()->options['cs']);

        $new_cs_option = array_merge($old_cs_options, $new_cs_option);
        update_option('iubenda_cookie_law_solution', $new_cs_option);

        // save site ID into Iubenda global option
        if($site_id){
            $global_options['site_id'] = $site_id;
        }

        //update iubenda global options (site_id & public_ids)
        iubenda()->options['global_options'] = $global_options;
        update_option( 'iubenda_global_options', $global_options );
    }

    /**
     * Saving iubenda plugin settings
     * @param bool $default_options
     */
    private function plugin_settings_save_options($default_options = true)
    {
        $new_options = iub_array_get($_POST, 'iubenda_plugin_settings', []) ?: [];

        if (!$default_options) {
            $new_options['ctype']           = (bool)isset($new_options['ctype']);
            $new_options['output_feed']     = (bool)isset($new_options['output_feed']);
            $new_options['output_post']     = (bool)isset($new_options['output_post']);
            $new_options['menu_position']   = (bool)isset($new_options['menu_position']) ? $new_options['menu_position'] : iubenda()->defaults['cs']['menu_position'];
            $new_options['deactivation']    = (bool)isset($new_options['deactivation']);
        }

        $old_cs_options = $this->stripslashes_deep(iubenda()->options['cs']);
        $new_cs_option = array_merge($old_cs_options, $new_options);
        update_option('iubenda_cookie_law_solution', $new_cs_option);
    }

    /**
     * saving Iubenda privacy policy solution options
     */
    private function pp_save_options()
    {
        // TODO enhance more
        $privacy_policy_generator = new PrivacyPolicyGenerator();
        $global_options = iubenda()->options['global_options'];

        $languages = (new ProductHelper())->get_languages();
        // loop on iubenda->>language
        foreach ($languages as $lang_id => $v) {
            $privacy_policy_id = null;

            // getting privacy policy id from saved QG response
            $privacy_policy_id = iub_array_get($global_options, "public_ids.{$lang_id}");

            if(!$privacy_policy_id){
                continue;
            }

            // Insert PP Simplified code into options
            $pp_embed_code = $privacy_policy_generator->handle($lang_id, $privacy_policy_id, iub_array_get($_POST, 'iubenda_privacy_policy_solution.button_style'));

            $pp_data["code_{$lang_id}"] = $pp_embed_code;

            //getting public id to save it into Iubenda global option for each lang
            $global_options['public_ids'][$lang_id] = $privacy_policy_id;
        }

        // Add a widget in the sidebar if the button is positioned automatically
        if('automatic' === iub_array_get($_POST, 'iubenda_privacy_policy_solution.button_position')){
            iubenda()->assign_legal_block_or_widget();
        }

        // Set the version of PP service as Simplified
        $pp_data["version"] = 'Simplified';

        // Set the configured status as true
        $pp_data["configured"] = 'true';

        update_option("iubenda_privacy_policy_solution", array_merge($pp_data, iub_array_get($_POST, 'iubenda_privacy_policy_solution')));

        // update only pp make it activated service
        iubenda()->options['activated_products']['iubenda_privacy_policy_solution'] = 'true';
        update_option('iubenda_activated_products', iubenda()->options['activated_products']);

        //update iubenda global options (site_id & public_ids)
        iubenda()->options['global_options'] = $global_options;
        update_option( 'iubenda_global_options', $global_options );
    }

    private function add_amp_permission_error()
    {
        $file_path = IUBENDA_PLUGIN_PATH . 'templates' . DIRECTORY_SEPARATOR;
        $message = sprintf( __( 'Currently, you do not have write permission for <i class="text-bold">%s</i>. For instructions on how to fix this, please read <a class="link-underline" target="_blank" href="%s">our guide</a>.', 'iubenda' ), $file_path, iubenda()->settings->links['amp_permission_support']);

        add_settings_error('cs_settings_errors', 'iub_cs_settings_updated', $message, 'error');
        iubenda()->settings->add_notice( 'iub_integrated_success', $message, 'error' );
    }
}
