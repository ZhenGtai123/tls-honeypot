<?php
// exit if accessed directly
if ( ! defined( 'ABSPATH' ) )
    exit;


/**
 * Class Radar_API
 */
class RadarService {

    private $authorization = [
        'username' => 'devops',
        'password' => 'orIDiVvPVdHvwyjM4',
    ];
    private $serviceRating = '';

    private $url = [
        'match-async' => 'https://radar.iubenda.com/api/match-async',
        'match-progress' => 'https://radar.iubenda.com/api/match-progress',
    ];

    public $apiConfiguration = [];

    private $updateMessage = "Please, make also sure the plugin is updated to the <a target='_blank' href='https://wordpress.org/plugins/iubenda-cookie-law-solution/'><u> latest version.</u></a>";

    public function __construct(){
        $this->serviceRating = new ServiceRating();
        $this->apiConfiguration = get_option('iubenda_radar_api_configuration', []) ?: [];
    }

    public function ask_radar_to_send_request(){
        if (!empty($this->apiConfiguration)) {
            return $this->send_radar_progress_request();
        }

        return $this->send_radar_sync_request();
    }

    public function force_delete_radar_configuration(){
        delete_option('iubenda_radar_api_configuration');
        return true;
    }

    public function calculate_radar_percentage(){
        $services['pp'] = $this->serviceRating->is_privacy_policy_activated();
        $services['cs'] = $this->serviceRating->is_cookie_solution_activated();
        $services['cons'] = boolval($this->serviceRating->is_cookie_solution_activated() && $this->serviceRating->is_cookie_solution_automatically_parse_enabled());
        $services['tc'] = $this->serviceRating->is_terms_conditions_activated();

        return [
            'percentage' => (count(array_filter($services)) / count($services)) * 100,
            'services' => $services
        ];
    }

    private function send_radar_sync_request()
    {
        $website = get_site_url();
        $data = ['timeout' => 30,
            'redirection' => 5,
            'httpversion' => '1.0',
            'headers' => ['Authorization' => 'Basic ' . base64_encode($this->authorization['username'] . ':' . $this->authorization['password'])],
            'body' => ['url' => $website, 'detectLegalDocuments' => 'true'],
        ];

        $response = wp_remote_get(iub_array_get($this->url, 'match-async'), $data);
        $responseCode = wp_remote_retrieve_response_code($response);

        //check response code
        $this->check_response($response, $responseCode);

        $body = json_decode(iub_array_get($response, 'body'), true);

        $body['trial_num'] = 1;
        $body['next_trial'] = time();

        update_option('iubenda_radar_api_configuration', $body);

        if (defined('DOING_AJAX') && DOING_AJAX) {
            wp_send_json(['code' => $responseCode, 'status' => 'progress',]);
            wp_die();
        }

        return true;
    }

    private function send_radar_progress_request()
    {
        $iubendaRadarApiConfiguration = $this->apiConfiguration;


        if (iub_array_get($iubendaRadarApiConfiguration, 'status') == 'completed') {
            if (defined('DOING_AJAX') && DOING_AJAX) {
                wp_send_json(['code' => '200', 'status' => 'complete', 'data' => $this->calculate_radar_percentage(),]);
                wp_die();
            }

            return true;
        }

        // Check if the next trial is not now
        if(intval(iub_array_get($iubendaRadarApiConfiguration, 'next_trial')) > time()){
            if (defined('DOING_AJAX') && DOING_AJAX) {
                $nextRequestInSec = intval(iub_array_get($iubendaRadarApiConfiguration, 'next_trial')) - (time());

                wp_send_json(['code' => '200', 'status' => 'timeout', 'data' => $nextRequestInSec,]);
                wp_die();
            }

            return true;
        }

        $nextTrial = time();
        $trialNum = intval(iub_array_get($iubendaRadarApiConfiguration, 'trial_num', 1) ?? 1);

        // Check if 3 trials were made in this round
        if(is_int($trialNum / 3)){
            $rounds = $trialNum / 3 ;
            $nextTrial = time() + (pow(30, $rounds));
        }
        $trialNum++;

        $id = iub_array_get($iubendaRadarApiConfiguration, 'id');

        $data = [
            'timeout' => 30,
            'redirection' => 5,
            'httpversion' => '1.0',
            'headers' => ['Authorization' => 'Basic ' . base64_encode($this->authorization['username'] . ':' . $this->authorization['password'])],
            'body' => ['id' => $id],
        ];

        $response = wp_remote_get(iub_array_get($this->url, 'match-progress'), $data);
        $responseCode = wp_remote_retrieve_response_code($response);

        //check response code
        $this->check_response($response, $responseCode);

        $body = json_decode(iub_array_get($response, 'body'), true);
        $body['trial_num'] = $trialNum;
        $body['next_trial'] = $nextTrial;

        update_option('iubenda_radar_api_configuration', $body);

        if (defined('DOING_AJAX') && DOING_AJAX) {
            wp_send_json(['code' => $responseCode, 'status' => 'progress',]);
            wp_die();
        }

        return true;
    }

    private function check_response($response, $responseCode)
    {
        if (is_wp_error($response) || $responseCode != 200) {
            if (!is_numeric($responseCode)) {
                $message = $this->updateMessage;
            } elseif ($responseCode == 408) {
                //408 error code it`s mean request timeout
                $message = $this->updateMessage;
            } elseif (is_numeric(substr($responseCode, 0, 1)) == 4) {
                //4xx error codes
                $message = $this->updateMessage;
            } else {
                $message = "Something went wrong: " . $response->get_error_message();
            }

            if (defined('DOING_AJAX') && DOING_AJAX) {
                wp_send_json(['code' => $responseCode, 'status' => 'error', 'message' => $message]);
                wp_die();
            }
            return true;
        }
    }
}
