<?php
// exit if accessed directly
if (!defined('ABSPATH')) exit;

/**
 * Class LanguageHelper
 */
class LanguageHelper {

    /**
     * Get the language code of logged in user profile
     *
     * @param bool $lower_case
     * @return string
     */
    public function get_user_profile_language_code($lower_case = false): string {
        $iub_supported_languages = iubenda()->supported_languages;
        $user_profile_language = get_bloginfo("language");

        // Check if the current user language is supported by iubenda
        if (iub_array_get($iub_supported_languages, $user_profile_language) ?: null) {
            $result = $user_profile_language;
        }
        // Remove the country from the language code to check if iubenda supports the current user language without the country
        else{
            $locale = explode('-', $user_profile_language) ?: [];
            $result = iub_array_get($iub_supported_languages, $locale[0]) ? $locale[0] : null;
        }

        // Fallback to EN if current user language is not supported
        if(!$result){
            $result = 'en';
        }

        return $lower_case ? strtolower($result) : $result;
    }

    /**
     * Get the site's default language code
     *
     * @param bool $lower_case
     * @return string
     */
    public function get_default_website_language_code($lower_case = false): string {
        if ((is_plugin_active('polylang/polylang.php') || is_plugin_active('polylang-pro/polylang.php')) && function_exists('PLL')) {
            $default_language_local_code = pll_default_language('locale');
            $website_language_code = iub_array_get(iubenda()->lang_mapping, $default_language_local_code);
        }
        elseif (is_plugin_active('sitepress-multilingual-cms/sitepress.php') && class_exists('SitePress')) {
            global $sitepress;
            $website_language_code = $sitepress->get_default_language();

            // Special handling if the default language is pt-pt
            if($website_language_code == 'pt-pt'){
                $website_language_code = 'pt';
            }
        }
        else {
            $website_language_code = iub_array_get(iubenda()->lang_mapping, get_locale());
        }

        return $lower_case ? strtolower($website_language_code) : $website_language_code;
    }

}