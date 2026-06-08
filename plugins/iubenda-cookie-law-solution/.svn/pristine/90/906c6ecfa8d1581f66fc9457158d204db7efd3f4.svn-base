<?php
// exit if accessed directly
if ( ! defined( 'ABSPATH' ) )
	exit;

/**
 * Class CookieSolutionGenerator
 */
class CookieSolutionGenerator {

    /**
     * @param $language
     * @param $siteId
     * @param $cookiePolicyId
     * @param array $args
     * @return string
     */
	public function handle($language, $siteId, $cookiePolicyId, $args = []) {
        // Return if there is no public ID or site ID
	    if(!$cookiePolicyId || !$siteId){
	        return null;
	    }

        // Handle if the website is single language
	    if($language == 'default'){
            $language = iubenda()->lang_current ?: iubenda()->lang_default;
	    }

        // Special handling if the language is pt-pt
        if(strtolower($language) == 'pt-pt'){
            $language = 'pt';
        }

        // Special handling if the language has a country to replace the country code with capital letters
        if(strpos($language, '-')){
            $language = explode('-', $language);
            $language[1] = strtoupper($language[1]);
            $language = implode('-', $language);
        }

        $beforeConfiguration = '
            <script type="text/javascript">
            var _iub = _iub || [];
            _iub.csConfiguration =';
        $afterConfiguration = '</script>';

        $csConfiguration = [
            'floatingPreferencesButtonDisplay' => 'bottom-right',
            'lang' => $language,
            'siteId' => $siteId,
            'cookiePolicyId' => $cookiePolicyId,
            'whitelabel' => false,
            'invalidateConsentWithoutLog' => true,
        ];
        $csConfiguration['banner']['closeButtonDisplay'] = false;

        $legislation = iub_array_get($args, 'legislation');

        // If legislation is GDPR or LGPD or All
        if ($legislation == 'gdpr' || $legislation == 'lgpd' || $legislation == 'all'){
            $csConfiguration['consentOnContinuedBrowsing'] = false;
            $csConfiguration['perPurposeConsent'] = true;
            $csConfiguration['banner']['listPurposes'] = true;
            $csConfiguration['banner']['explicitWithdrawal'] = true;

            $explicit_reject = iub_array_get($args, 'explicit_reject');
            if ($explicit_reject || true == iub_array_get($args, 'tcf')) {
                $csConfiguration['banner']['rejectButtonDisplay'] = true;
            }

            $explicit_accept = iub_array_get($args, 'explicit_accept');
            if ($explicit_accept || true == iub_array_get($args, 'tcf')) {
                $csConfiguration['banner']['acceptButtonDisplay'] =  true;
                $csConfiguration['banner']['customizeButtonDisplay'] =  true;
            }

            // If Require Consent is EU Only
            if(iub_array_get($args, 'require_consent') == 'eu_only'){
                $csConfiguration['countryDetection'] = true;
                $csConfiguration['gdprAppliesGlobally'] = false;
            }
        }

        // If legislation is CCPA or All
        if ($legislation == 'ccpa' || $legislation == 'all'){
            $csConfiguration['enableCcpa'] = true;

            // If Require Consent is Worldwide
            if(iub_array_get($args, 'require_consent') == 'worldwide'){
                $csConfiguration['ccpaApplies'] = true;
            }
            $afterConfiguration .= '
                <script type="text/javascript" src="//cdn.iubenda.com/cs/ccpa/stub.js"></script>
            ';
        }

        // If legislation is LGDP or All
        if ($legislation == 'lgpd' || $legislation == 'all'){
            $csConfiguration['enableLgpd'] = true;
        }

        // If legislation is CCPA or LGPD
        if ($legislation == 'ccpa' || $legislation == 'lgpd'){
            // If Require Consent is Worldwide
            if(iub_array_get($args, 'require_consent') == 'worldwide'){
                $csConfiguration['enableGdpr'] = false;
            }
        }

        // conditions on TCF is enabled
        if (($legislation == 'gdpr' || $legislation == 'all') && true == iub_array_get($args, 'tcf')){
            $csConfiguration['enableTcf'] = true;
            $csConfiguration['banner']['closeButtonRejects'] = true;
            $csConfiguration['tcfPurposes']['1'] = true;
            $csConfiguration['tcfPurposes']['2'] = 'consent_only';
            $csConfiguration['tcfPurposes']['3'] = 'consent_only';
            $csConfiguration['tcfPurposes']['4'] = 'consent_only';
            $csConfiguration['tcfPurposes']['5'] = 'consent_only';
            $csConfiguration['tcfPurposes']['6'] = 'consent_only';
            $csConfiguration['tcfPurposes']['7'] = 'consent_only';
            $csConfiguration['tcfPurposes']['8'] = 'consent_only';
            $csConfiguration['tcfPurposes']['9'] = 'consent_only';
            $csConfiguration['tcfPurposes']['10'] = 'consent_only';

            $afterConfiguration .= '
                <script type="text/javascript" src="//cdn.iubenda.com/cs/tcf/stub-v2.js"></script>
                <script type="text/javascript" src="//cdn.iubenda.com/cs/tcf/safe-tcf-v2.js"></script>
            ';
        }
        $csConfiguration['banner']['position'] = str_replace('full-', '', iub_array_get($args, 'position'));

        $bannerStyle = iub_array_get($args, 'banner_style');
        if ('light' == $bannerStyle) {
            $csConfiguration['banner']['style'] = 'light';
            $csConfiguration['banner']['textColor'] = '#000000';
            $csConfiguration['banner']['backgroundColor'] = '#FFFFFF';
            $csConfiguration['banner']['customizeButtonCaptionColor'] = '#4D4D4D';
            $csConfiguration['banner']['customizeButtonColor'] = '#DADADA';
        }else{
            $csConfiguration['banner']['style'] = 'dark';
        }

        $background_overlay = iub_array_get($args, 'background_overlay');
        if ($background_overlay) {
            $csConfiguration['banner']['backgroundOverlay'] = true;
        }

        $afterConfiguration .= '
            <script type="text/javascript" src="//cdn.iubenda.com/cs/iubenda_cs.js" charset="UTF-8" async></script>
        ';

        return $beforeConfiguration.json_encode($csConfiguration)."; ".$afterConfiguration;
	}
}
