<?php


class IubendaLegalWidget extends WP_Widget
{
    private $widget_id = 'iubenda_legal_widget';

    private $default_widget_title = 'Legal';

    public function __construct()
    {
        parent::__construct(

            // Base ID of your widget
            $this->widget_id,

            // Widget name will appear in UI
            __('Iubenda legal', 'iubenda'),

            // Widget description
            ['description' => __('Iubenda legal widget for Privacy Policy and Terms & Conditions', 'iubenda'),]
        );

        add_action( 'iubenda_assign_widget_to_first_sidebar', [$this, 'assign_iubenda_widget'] );
        $this->init();
    }

    /**
     * Register HOOKS
     *
     * @return void
     */
    private function init() {
        add_action('widgets_init', [$this, 'register_widget']);
    }

    /**
     * Set default value for the first Iubenda Legal widget
     * @return array|array[]|ArrayIterator|ArrayObject|false
     */
    public function get_settings()
    {
        $settings = parent::get_settings();
        // Set default value for the first widget
        if (!$settings) {
            return [1 => []];
        }

        return $settings;
    }

    /**
     * Override display callback
     *
     * @param $args
     * @param $widget_args
     * @return void
     */
    public function display_callback( $args, $widget_args = 1 ) {

        if ( is_numeric( $widget_args ) ) {
            $widget_args = array( 'number' => $widget_args );
        }

        $widget_args = wp_parse_args( $widget_args, array( 'number' => -1 ) );
        $this->_set( $widget_args['number'] );
        $instances = $this->get_settings();

        // Additional code to add default title widget title if it's not set yet
        if (!$instances) {
            $instances[$this->number] = ['title' => __($this->default_widget_title ,'iubenda')];
        }

        if ( isset( $instances[ $this->number ] ) ) {
            $instance = $instances[ $this->number ];

            /**
             * Filters the settings for a particular widget instance.
             *
             * Returning false will effectively short-circuit display of the widget.
             *
             * @since 2.8.0
             *
             * @param array     $instance The current widget instance's settings.
             * @param WP_Widget $widget   The current widget instance.
             * @param array     $args     An array of default widget arguments.
             */
            $instance = apply_filters( 'widget_display_callback', $instance, $this, $args );

            if ( false === $instance ) {
                return;
            }

            $was_cache_addition_suspended = wp_suspend_cache_addition();
            if ( $this->is_preview() && ! $was_cache_addition_suspended ) {
                wp_suspend_cache_addition( true );
            }

            $this->widget( $args, $instance );

            if ( $this->is_preview() ) {
                wp_suspend_cache_addition( $was_cache_addition_suspended );
            }
        }
    }


    // Creating widget front-end
    public function widget($args, $instance)
    {
        $ppStatus = iub_array_get(iubenda()->settings->services, 'pp.status') == 'true';
        $ppPosition = iub_array_get(iubenda()->options['pp'], 'button_position') == 'automatic';

        $tcStatus = iub_array_get(iubenda()->settings->services, 'tc.status') == 'true';
        $tcPosition = iub_array_get(iubenda()->options['tc'], 'button_position') == 'automatic';

        // Checking if there is no public id for current language
        if ( iubenda()->multilang && ! empty( iubenda()->lang_current ) ) {
            $lang_id = iubenda()->lang_current;
        } else {
            $lang_id = 'default';
        }

        $public_id = iub_array_get(iubenda()->options['global_options'], "public_ids.{$lang_id}", false) ?: false;

        // Return false if there is no public id for current language
        if (!($public_id)) {
            return false;
        }
        $quickGeneratorService = new QuickGeneratorService();

        if (!($ppStatus && $ppPosition && boolval($quickGeneratorService->pp_button())) && !($tcStatus && $tcPosition && boolval($quickGeneratorService->tc_button()))) {
            return false;
        }

        $title = apply_filters('widget_title', iub_array_get($instance, 'title') ?? 'Legal');

        // before and after widget arguments are defined by themes
        echo $args['before_widget'];
        if (!empty($title)) echo $args['before_title'] . $title . $args['after_title'];

        // Display TC or PP if activated
        if (($ppStatus && $ppPosition) || ($tcStatus && $tcPosition)) {

            $legal = '<section>';

            if($ppStatus && $ppPosition){
                $legal .= $quickGeneratorService->pp_button();
            }
            if(($ppStatus && $ppPosition) && ($tcStatus && $tcPosition)){
                $legal .= '<br>';
            }
            if($tcStatus && $tcPosition){
                $legal .= $quickGeneratorService->tc_button();
            }

            $legal .= '</section>';

            echo $legal;
        }
        echo $args['after_widget'];
    }

    // Widget Backend
    public function form($instance)
    {
        $title = __('Legal', 'iubenda');

        if (isset($instance['title'])) {
            $title = $instance['title'];
        }

        // Widget admin form
        ?>
        <p>
            <label for="<?php echo $this->get_field_id('title'); ?>"><?php _e('Title:'); ?></label>
            <input class="widefat" id="<?php echo $this->get_field_id('title'); ?>" name="<?php echo $this->get_field_name('title'); ?>" type="text" value="<?php echo esc_attr($title); ?>"/>
        </p>
        <?php
    }

    // Updating widget replacing old instances with new
    public function update($new_instance, $old_instance)
    {
        $instance = [];
        $instance['title'] = (!empty($new_instance['title'])) ? strip_tags($new_instance['title']) : '';
        return $instance;
    }

    /**
     * Assign iubenda widget to registered sidebar if exists and not registered before
     *
     * @return bool
     */
    public function assign_iubenda_widget()
    {
        global $wp_registered_sidebars;

        // Check if iubenda widget activated in any sidebar
        if (is_active_widget(false, false, $this->widget_id)) {
            return;
        }

        // If sidebar-1 not registered or not activated
        if (!iub_array_get($wp_registered_sidebars, 'sidebar-1')) {
            return;
        }

        // Check if wp_assign_widget_to_sidebar is exist
        if (!function_exists('wp_assign_widget_to_sidebar')) {
            return;
        }

        // Iubenda widget in not activated in sidebar and sidebar-1 is registered and activated
        wp_assign_widget_to_sidebar("{$this->widget_id}-1", 'sidebar-1');
    }

    /**
     * Register current widget in WP
     *
     * @return void
     */
    public function register_widget() {
        register_widget(__CLASS__);
    }

    /**
     * Check current theme supports widget
     */
    public function check_current_theme_supports_widget()
    {
        global $wp_registered_sidebars;

        // If sidebar-1 registered and activated
        if (iub_array_get($wp_registered_sidebars, 'sidebar-1')) {
            return true;
        }

        return false;
    }
}



