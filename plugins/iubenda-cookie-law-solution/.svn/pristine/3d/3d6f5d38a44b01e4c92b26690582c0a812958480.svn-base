<?php
// exit if accessed directly
if (!defined('ABSPATH')) exit;

/**
 * Class ProductHelper
 */
class ProductHelper
{

    /**
     * @param $lang_id
     * @return string
     */
    public function get_cs_embed_code_by_lang($lang_id): string
    {
        $code = iub_array_get(iubenda()->options['cs'], "manual_code_{$lang_id}");
        if (!$code) {
            $code = iub_array_get(iubenda()->options['cs'], "code_{$lang_id}");
        }

        return html_entity_decode(iubenda()->parse_code($code));
    }

    /**
     * @param $lang_id
     * @return string
     */
    public function get_pp_embed_code_by_lang($lang_id): string
    {
        return $this->get_embed_code('pp', $lang_id);
    }

    /**
     * @param $lang_id
     * @return string
     */
    public function get_tc_embed_code_by_lang($lang_id): string
    {
        return $this->get_embed_code('tc', $lang_id);
    }

    /**
     * Get all languages if website is multilingual and return default if website is single language
     *
     * @return array|string[]
     */
    public function get_languages(): array
    {
        if (iubenda()->multilang && !empty(iubenda()->languages)) {
            return iubenda()->languages;
        }

        return ['default' => 'default_language'];
    }


    /**
     * @param $key
     * @param $lang_id
     * @return string
     */
    private function get_embed_code($key, $lang_id): string
    {
        $code = iub_array_get(iubenda()->options[$key], "code_{$lang_id}");

        return html_entity_decode(iubenda()->parse_code($code));
    }

    /**
     * Check Iubenda CS code exists on current lang or not
     *
     * @return bool
     */
    public function check_iub_cs_code_exists_current_lang(): bool
    {
        return $this->check_iub_code_exists_current_lang('cs');
    }

    /**
     * Check Iubenda $key code exists on current lang or not
     *
     * @param $key
     * @return bool
     */
    private function check_iub_code_exists_current_lang($key): bool
    {
        // Check if there is multi language plugin installed and activated
        if ( iubenda()->multilang === true && defined( 'ICL_LANGUAGE_CODE' ) && isset( iubenda()->options['cs']['code_' . ICL_LANGUAGE_CODE] ) ) {
            $iubenda_code = iubenda()->options[$key]['code_' . ICL_LANGUAGE_CODE];

            // no code for current language, use default
            if ( ! $iubenda_code ){
                $iubenda_code = iubenda()->options[$key]['code_default'];
            }
        } else{
            $iubenda_code = iubenda()->options[$key]['code_default'];
        }

        return boolval(trim($iubenda_code ?: ''));
    }

    /**
     * Getting public id for current language if stored in database
     * @return array|ArrayAccess|false|mixed
     */
    public function get_public_id_for_current_language(){
        // Checking if there is no public id for current language
        if ( iubenda()->multilang && ! empty( iubenda()->lang_current ) ) {
            $lang_id = iubenda()->lang_current;
        } else {
            $lang_id = 'default';
        }

        return iub_array_get(iubenda()->options['global_options'], "public_ids.{$lang_id}", false) ?: false;
    }

    /**
     * Check privacy policy and terms and condition services status and position and codes
     *
     * @return bool
     */
    public function check_pp_tc_status_and_position(){
        $ppStatus = iub_array_get(iubenda()->settings->services, 'pp.status') == 'true';
        $ppPosition = iub_array_get(iubenda()->options['pp'], 'button_position') == 'automatic';

        $tcStatus = iub_array_get(iubenda()->settings->services, 'tc.status') == 'true';
        $tcPosition = iub_array_get(iubenda()->options['tc'], 'button_position') == 'automatic';
        $quickGeneratorService = new QuickGeneratorService();

        if (!($ppStatus && $ppPosition && boolval($quickGeneratorService->pp_button())) && !($tcStatus && $tcPosition && boolval($quickGeneratorService->tc_button()))) {
            return false;
        }

        return true;
    }

    /**
     * Get intersect supported local languages intersect with iubenda supported languages
     *
     */
    public function get_local_supported_language(){
        if (iubenda()->multilang && !empty(iubenda()->languages)) {
            $local_languages = array_keys(iubenda()->languages_locale) ?: [];
            $local_languages = iubenda()->language_unification_locale_to_iub($local_languages);

            $iubenda_intersect_supported_langs = array_intersect($local_languages, array_keys(iubenda()->supported_languages)) ?: [];
        }
        else {
            $iubenda_intersect_supported_langs = array_intersect([iub_array_get(iubenda()->lang_mapping, get_locale())], array_values(iubenda()->lang_mapping)) ?: [];
        }

        return $iubenda_intersect_supported_langs;
    }

    /**
     * Check if iubenda service is enabled
     *
     * @param $service
     * @return bool
     */
    private function is_iub_service_enabled($service): bool {
        return boolval(iub_array_get(iubenda()->settings->services, "{$service}.status") == 'true');
    }

    /**
     * Check if CS service is enabled
     *
     */
    public function is_cs_service_enabled(): bool {
        return $this->is_iub_service_enabled('cs');
    }

    /**
     * Check if PP service is enabled
     *
     */
    public function is_pp_service_enabled(): bool {
        return $this->is_iub_service_enabled('pp');
    }

    /**
     * Check if TC service is enabled
     *
     */
    public function is_tc_service_enabled(): bool {
        return $this->is_iub_service_enabled('tc');
    }

    /**
     * Check if CONS service is enabled
     *
     */
    public function is_cons_service_enabled(): bool {
        return $this->is_iub_service_enabled('cons');
    }

    /**
     * Check if iubenda service is configured
     *
     * @param $service
     * @return bool
     */
    private function is_iub_service_configured($service): bool {
        return boolval(iub_array_get(iubenda()->settings->services, "{$service}.configured") == 'true');
    }

    /**
     * Check if CS service is configured
     *
     */
    public function is_cs_service_configured(): bool {
        return $this->is_iub_service_configured('cs');
    }

    /**
     * Check if PP service is configured
     *
     */
    public function is_pp_service_configured(): bool {
        return $this->is_iub_service_configured('pp');
    }

    /**
     * Check if TC service is configured
     *
     */
    public function is_tc_service_configured(): bool {
        return $this->is_iub_service_configured('tc');
    }

    /**
     * Check if CONS service is configured
     *
     */
    public function is_cons_service_configured(): bool {
        return $this->is_iub_service_configured('cons');
    }
}
