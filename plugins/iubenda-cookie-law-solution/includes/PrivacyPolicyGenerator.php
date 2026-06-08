<?php
// exit if accessed directly
if ( ! defined( 'ABSPATH' ) )
	exit;

/**
 * Class PrivacyPolicyGenerator
 */
class PrivacyPolicyGenerator {

    /**
     * @param $language
     * @param $cookiePolicyId
     * @param $buttonStyle
     * @return string
     */
	public function handle($language, $cookiePolicyId, $buttonStyle) {
        // Return if there is no public id
        if(!$cookiePolicyId){
            return null;
        }
        $privacyTitle = 'Privacy Policy';

        // Handle if the website is single language
        if ($language == 'default') {
            $language = iubenda()->lang_current ?: iubenda()->lang_default;
        }

        // If the language has translation in iubenda plugin
        $language_code = array_search(strtolower($language), array_map('strtolower', iubenda()->lang_mapping)) ?: null;
        if($language_code){
            $privacyTitle = __iub_trans('Privacy Policy', $language_code);
        }

        $ppConfiguration = '
        <a href="https://www.iubenda.com/privacy-policy/'.$cookiePolicyId.'" class="iubenda-'.$buttonStyle.' no-brand iubenda-noiframe iubenda-embed iubenda-noiframe " title="'.$privacyTitle.'">'.$privacyTitle.'</a><script type="text/javascript">(function (w,d) {var loader = function () {var s = d.createElement("script"), tag = d.getElementsByTagName("script")[0]; s.src="https://cdn.iubenda.com/iubenda.js"; tag.parentNode.insertBefore(s,tag);}; if(w.addEventListener){w.addEventListener("load", loader, false);}else if(w.attachEvent){w.attachEvent("onload", loader);}else{w.onload = loader;}})(window, document);</script>
        ';

        return $ppConfiguration;
	}
}
