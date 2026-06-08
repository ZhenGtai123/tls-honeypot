<?php

if( ! defined( 'ABSPATH' ) ) exit(); // Exit if accessed directly

/**
 * HT CF7 Condition
*/

class Extensions_Cf7_Range_slider{

	/**
     * [$_instance]
     * @var null
    */
    private static $_instance = null;

    /**
     * [instance] Initializes a singleton instance
     * @return [Extensions_Cf7_Pro_Country]
    */
    public static function instance() {
        if ( is_null( self::$_instance ) ) {
            self::$_instance = new self();
        }
        return self::$_instance;
    }

	function __construct(){
        add_filter('extcf7_post_metabox', [$this, 'metabox_options']);
        add_action( 'wpcf7_save_contact_form', [$this, 'styler_save_data'] );
        add_filter( 'wpcf7_contact_form_properties', [$this, 'styler_properties'], 10, 2 );
        add_action('wpcf7_init', [$this, 'wpcf7_tags']);
        add_action('admin_init', [$this, 'wpcf7_tag_generator'], 589);

        add_filter( 'wpcf7_validate_extcf7_range_slider', [$this, 'validation_filter'],10, 2);
        add_filter( 'wpcf7_validate_extcf7_range_slider*', [$this, 'validation_filter'],10, 2);
	}
    public function metabox_options($value) {
        $value['extcf7_range_slider'] = [
            'id'  => 'range_slider',
            'label'  => __( 'Range Slider', 'cf7-extensions-pro' ),
            'fields' => [
                [
                    'name'  => __( 'Slider', 'cf7-extensions-pro' ),
                    'type'  => 'heading',
                    'class' => 'htcf7ext-field-styler group-title-inner',
                    'group' => 'submit_options'
                ],
                [
                    'id'  => 'slider_color',
                    'name'  => __( 'Background Color', 'cf7-extensions-pro' ),
                    'type'  => 'color',
                    'class' => 'htcf7ext-field-styler width-50 admin-width-50',
                ],
                [
                    'id'  => 'slider_selection_color',
                    'name'  => __( 'Background Selection Color', 'cf7-extensions-pro' ),
                    'type'  => 'color',
                    'class' => 'htcf7ext-field-styler width-50 admin-width-50',
                ],
                [
                    'id'  => 'slider_height',
                    'name'  => __( 'Height (px)', 'cf7-extensions-pro' ),
                    'type'  => 'number',
                    'class' => 'htcf7ext-field-styler width-50 admin-width-50',
                ],
                [
                    'id'  => 'slider_radius',
                    'name'  => __( 'Border Radius (px)', 'cf7-extensions-pro' ),
                    'type'  => 'number',
                    'class' => 'htcf7ext-field-styler width-50 admin-width-50',
                ],
                [
                    'id'  => 'slider_border_width',
                    'name'  => __( 'Border Width (px)', 'cf7-extensions-pro' ),
                    'type'  => 'number',
                    'class' => 'htcf7ext-field-styler width-33 admin-width-33',
                    'condition' => [['condition_key' => 'form_styler_enable', 'condition_value' => 'on']],
                    'group' => 'submit_options'
                ],
                [
                    'id'  => 'slider_border_style',
                    'name'  => __( 'Border Style', 'cf7-extensions-pro' ),
                    'type'  => 'select',
                    'default'  => '',
                    'options' => array(
                        '' => __('Select Style', 'cf7-extensions-pro'),
                        'none' => __('None', 'cf7-extensions-pro'),
                        'solid' => __('Solid', 'cf7-extensions-pro'),
                        'dotted' => __('Dotted', 'cf7-extensions-pro'),
                        'dashed' => __('Dashed', 'cf7-extensions-pro'),
                        'double' => __('Double', 'cf7-extensions-pro'),
                    ),
                    'class' => 'htcf7ext-field-styler width-33 admin-width-33',
                    'condition' => [['condition_key' => 'form_styler_enable', 'condition_value' => 'on']],
                    'group' => 'submit_options'
                ],
                [
                    'id'  => 'slider_border_color',
                    'name'  => __( 'Border Color', 'cf7-extensions-pro' ),
                    'type'  => 'color',
                    'class' => 'htcf7ext-field-styler width-33 admin-width-50',
                    'condition' => [['condition_key' => 'form_styler_enable', 'condition_value' => 'on']],
                    'group' => 'submit_options'
                ],
                [
                    'name'  => __( 'Slide Handler', 'cf7-extensions-pro' ),
                    'type'  => 'heading',
                    'class' => 'htcf7ext-field-styler group-title-inner',
                    'group' => 'submit_options'
                ],
                [
                    'id'  => 'handler_color',
                    'name'  => __( 'Background Color', 'cf7-extensions-pro' ),
                    'type'  => 'color',
                    'class' => 'htcf7ext-field-styler width-50 admin-width-50',
                ],
                [
                    'id'  => 'handler_color_hover',
                    'name'  => __( 'Background Color (Hover)', 'cf7-extensions-pro' ),
                    'type'  => 'color',
                    'class' => 'htcf7ext-field-styler width-50 admin-width-50',
                ],
                [
                    'id'  => 'handler_width',
                    'name'  => __( 'Width (px)', 'cf7-extensions-pro' ),
                    'type'  => 'number',
                    'class' => 'htcf7ext-field-styler width-33 admin-width-50',
                ],
                [
                    'id'  => 'handler_height',
                    'name'  => __( 'Height (px)', 'cf7-extensions-pro' ),
                    'type'  => 'number',
                    'class' => 'htcf7ext-field-styler width-33 admin-width-50',
                ],
                [
                    'id'  => 'handler_radius',
                    'name'  => __( 'Border Radius (px)', 'cf7-extensions-pro' ),
                    'type'  => 'number',
                    'class' => 'htcf7ext-field-styler width-33 admin-width-50',
                ],
                [
                    'id'  => 'handler_border_width',
                    'name'  => __( 'Border Width (px)', 'cf7-extensions-pro' ),
                    'type'  => 'number',
                    'class' => 'htcf7ext-field-styler width-50 admin-width-33',
                    'condition' => [['condition_key' => 'form_styler_enable', 'condition_value' => 'on']],
                    'group' => 'submit_options'
                ],
                [
                    'id'  => 'handler_border_style',
                    'name'  => __( 'Border Style', 'cf7-extensions-pro' ),
                    'type'  => 'select',
                    'default'  => '',
                    'options' => array(
                        '' => __('Select Style', 'cf7-extensions-pro'),
                        'none' => __('None', 'cf7-extensions-pro'),
                        'solid' => __('Solid', 'cf7-extensions-pro'),
                        'dotted' => __('Dotted', 'cf7-extensions-pro'),
                        'dashed' => __('Dashed', 'cf7-extensions-pro'),
                        'double' => __('Double', 'cf7-extensions-pro'),
                    ),
                    'class' => 'htcf7ext-field-styler width-50 admin-width-33',
                    'condition' => [['condition_key' => 'form_styler_enable', 'condition_value' => 'on']],
                    'group' => 'submit_options'
                ],
                [
                    'id'  => 'handler_border_color',
                    'name'  => __( 'Border Color', 'cf7-extensions-pro' ),
                    'type'  => 'color',
                    'class' => 'htcf7ext-field-styler width-50 admin-width-50',
                    'condition' => [['condition_key' => 'form_styler_enable', 'condition_value' => 'on']],
                    'group' => 'submit_options'
                ],
                [
                    'id'  => 'handler_border_color_hover',
                    'name'  => __( 'Border Color (Hover)', 'cf7-extensions-pro' ),
                    'type'  => 'color',
                    'class' => 'htcf7ext-field-styler width-50 admin-width-50',
                    'condition' => [['condition_key' => 'form_styler_enable', 'condition_value' => 'on']],
                    'group' => 'submit_options'
                ],
            ],
        ];
        return $value;
    }

    public function styler_save_data($form) {
        if(empty($_POST['extcf7_range_slider'])) {
            return;
        }
        update_post_meta($form->id, 'extcf7_range_slider', htcf7extopt_data_clean($_POST['extcf7_range_slider']));
    }
    public function styler_properties($form_properties, $current_form) {
        if (!is_admin() || ( class_exists( '\Elementor\Plugin' ) && ( \Elementor\Plugin::$instance->editor->is_edit_mode() || \Elementor\Plugin::$instance->preview->is_preview_mode() ) )) {
            $form = $form_properties['form'];
            if('on' == htcf7ext_get_option( 'htcf7ext_opt_extensions', 'range_extension', 'off' )){
                $form_styler_meta = [];
                if(metadata_exists('post', $current_form->id(), 'extcf7_range_slider')) {
                    $form_styler_meta = get_post_meta( $current_form->id(), 'extcf7_range_slider', true );
                }
                ob_start();
                echo $this->get_style($form_styler_meta, $current_form->id());
                echo '<div class="extcf7-cf7-style extcf7-cf7-style-' . esc_attr( $current_form->id() ) . '">' . $form . '</div>';
                $form_properties['form'] = ob_get_clean();
            }
        }
        return $form_properties;
    }
    public function get_style ($options, $id){
        ob_start();
        ?>
        <style>
            .extcf7-cf7-style-<?php echo esc_attr($id); ?> .ui-widget.ui-widget-content {
                <?php
                    $slider_color = $options['slider_color'] ?? '';
                    $slider_height = $options['slider_height'] ?? '';
                    $slider_radius = $options['slider_radius'] ?? '';
                    $slider_border_width = $options['slider_border_width'] ?? '';
                    $slider_border_style = $options['slider_border_style'] ?? '';
                    $slider_border_color = $options['slider_border_color'] ?? '';
                    $margin_block = '';
                    if(!empty($handler_height) && !empty($slider_height)) {
                        $margin_block = ($handler_height - $slider_height) / 2;
                    } elseif (!empty($handler_height) && empty($slider_height)) {
                        $margin_block = ($handler_height - 10) / 2;
                    } elseif (empty($handler_height) && !empty($slider_height)) {
                        $margin_block = (20 - $slider_height) / 2;
                    }

                    // Slider CSS
                    echo !empty($slider_color) ? $this->get_css('background', $slider_color) : '';
                    echo !empty($slider_height) ? $this->get_css('height', $slider_height, 'px') : '';
                    echo !empty($slider_radius) ? $this->get_css('border-radius', $slider_radius, 'px') : '';
                    echo !empty($slider_border_width) ? $this->get_css('border-width', $slider_border_width, 'px') : '';
                    echo !empty($slider_border_style) ? $this->get_css('border-style', $slider_border_style) : '';
                    echo !empty($slider_border_color) ? $this->get_css('border-color', $slider_border_color) : '';
                    $margin_block;
                    if(!empty($handler_height) && !empty($slider_height)) {
                        $margin_block = ($handler_height - $slider_height) / 2;
                    } elseif (!empty($handler_height) && empty($slider_height)) {
                        $margin_block = ($handler_height - 10) / 2;
                    } elseif (empty($handler_height) && !empty($slider_height)) {
                        $margin_block = (20 - $slider_height) / 2;
                    }
                    echo !empty($margin_block) ? $this->get_css('margin-block', $margin_block, 'px') : '';
                ?>
            }
            .extcf7-cf7-style-<?php echo esc_attr($id); ?> .ui-widget.ui-widget-content .ui-slider-range {
                <?php
                    $slider_selection_color = $options['slider_selection_color'] ?? '';
                    // Range Selection CSS
                    echo !empty($slider_selection_color) ? $this->get_css('background', $slider_selection_color) : '';
                ?>
            }
            .extcf7-cf7-style-<?php echo esc_attr($id); ?> .ui-widget.ui-widget-content .ui-slider-handle {
                <?php
                    $handler_color = $options['handler_color'] ?? '';
                    $handler_width = $options['handler_width'] ?? '';
                    $handler_height = $options['handler_height'] ?? '';
                    $handler_radius = $options['handler_radius'] ?? '';
                    $handler_border_width = $options['handler_border_width'] ?? '';
                    $handler_border_style = $options['handler_border_style'] ?? '';
                    $handler_border_color = $options['handler_border_color'] ?? '';
                    
                    // Handler CSS
                    echo !empty($handler_color) ? $this->get_css('background', $handler_color) : '';
                    echo !empty($handler_width) ? $this->get_css('width', $handler_width, 'px') : '';
                    echo !empty($handler_height) ? $this->get_css('height', $handler_height, 'px') : '';
                    echo !empty($handler_radius) ? $this->get_css('border-radius', $handler_radius, 'px') : '';
                    echo !empty($handler_border_width) ? $this->get_css('border-width', $handler_border_width, 'px') : '';
                    echo !empty($handler_border_style) ? $this->get_css('border-style', $handler_border_style) : '';
                    echo !empty($handler_border_color) ? $this->get_css('border-color', $handler_border_color) : '';
                    if(!empty($handler_width)) {
                        $this->get_css('margin-left', '-' . $handler_width / 2, 'px');
                    }
                    if(!empty($handler_height)) {
                        $this->get_css('margin-top', '-' . $handler_height / 2, 'px');
                    }
                ?>
            }
            .extcf7-cf7-style-<?php echo esc_attr($id); ?> .ui-widget.ui-widget-content .ui-slider-handle.ui-state-active,
            .extcf7-cf7-style-<?php echo esc_attr($id); ?> .ui-widget.ui-widget-content .ui-slider-handle.ui-state-hover {
                <?php
                    $handler_color_hover = $options['handler_color_hover'] ?? '';
                    $handler_border_color_hover = $options['handler_border_color_hover'] ?? '';
                    // Handler Hover CSS
                    echo !empty($handler_color_hover) ? $this->get_css('background', $handler_color_hover) : '';
                    echo !empty($handler_border_color_hover) ? $this->get_css('border-color', $handler_border_color_hover) : '';
                ?>
            }
        </style>
        <?php return ob_get_clean();
    }
    public function get_css ( $property, $value, $suffix = '') {
        return esc_attr($property) . ': ' . esc_attr($value) . esc_attr($suffix) . ';';
    }
	public function wpcf7_tags() {
        if (function_exists('wpcf7_add_form_tag')) {
            wpcf7_add_form_tag(['extcf7_range_slider', 'extcf7_range_slider*'], [$this, 'range_slider_shortcode'], true);
        } else {
            throw new Exception(esc_html__('functions wpcf7_add_form_tag not found.', 'cf7-extensions-pro'));
        }
    }
    public function range_slider_shortcode($tag){
        if ( empty( $tag->name ) ) {
            return '';
        }
        $validation_error = wpcf7_get_validation_error( $tag->name );
        $class = wpcf7_form_controls_class( 'extcf7_range_slider' );
        $atts = [];
        if ( $validation_error ) {
            $class .= ' wpcf7-not-valid';
        }
        if ( $tag->is_required() ) {
            $atts['aria-required'] = 'true';
        }
        $atts['name'] = $tag->name;
        $atts['class'] = $tag->get_class_option( $class );
        $atts['aria-invalid'] = $validation_error ? 'true' : 'false';
        if($tag->has_option('show_value')) {
            $atts['data-show'] = $tag->get_option( 'show_value', '', true);
        }
        if($tag->has_option('slider_type')) {
            $atts['data-type'] = $tag->get_option( 'slider_type', '', true);
        }
        $atts['data-min'] = ( $tag->has_option ( 'minimum_value' ) ) ? $tag->get_option ( 'minimum_value', '', true ) : '0';
        
        $atts['data-max'] = ( $tag->has_option ( 'maximum_value' ) ) ? $tag->get_option ( 'maximum_value', '', true ) : '100';

        $atts['data-default'] = ( $tag->has_option ( 'default_value' ) ) ? $tag->get_option ( 'default_value', '', true ) : '50';

        if($tag->has_option('range_step')) {
            $atts['data-step'] = $tag->get_option( 'range_step', '', true);
        }

        $valueContainer = sprintf(
            '<div class="wpcf7-extcf7-range-slider-amount" %s ></div>',
            !empty($atts['data-show']) && $atts['data-show'] === 'on' ? '' : 'style="display:none;"'
        );

        $atts = wpcf7_format_atts( $atts );
        return sprintf('<div id="%1$s" class="wpcf7-form-control-wrap wpcf7-extcf7-range-slider">
            %2$s
            <div class="wpcf7-extcf7-range-slider-wrapper"><input type="hidden" %3$s /></div>
            %4$s
        </div>', 
        esc_attr( $tag->name ),
        $valueContainer,
        $atts,
        wp_kses_post($validation_error) );
    }

	public function wpcf7_tag_generator() {
        if (! function_exists( 'wpcf7_add_tag_generator')) { 
            return;
        }
        wpcf7_add_tag_generator(
			'extcf7_range_slider',
			esc_html__('HT Range Slider', 'cf7-extensions-pro'),
            'wpcf7-tg-extcf7-range-slider',
            [$this, 'range_slider_layout']
        );
    }
    public function range_slider_layout($contact_form, $args = '') {
        $args = wp_parse_args( $args, [] );
        $type = 'extcf7_range_slider';
        ?>
            <div class="control-box">
                <table class="form-table">
                    <tbody>
                        <tr>
                            <th scope="row"><?php echo esc_html__( 'Field type', 'cf7-extensions-pro' ); ?></th>
                            <td>
                                <fieldset>
                                    <legend class="screen-reader-text"><?php echo esc_html__( 'Field type', 'cf7-extensions-pro' ); ?></legend>
                                    <label><input type="checkbox" name="required" /> <?php echo esc_html__( 'Required field', 'cf7-extensions-pro' ); ?></label>
                                </fieldset>
                            </td>
                        </tr>
                        <tr>
                            <th scope="row"><label for="<?php echo esc_attr( $args['content'] . '-name' ); ?>"><?php echo esc_html__( 'Name', 'cf7-extensions-pro' ); ?></label></th>
                            <td><input type="text" name="name" class="tg-name" id="<?php echo esc_attr( $args['content'] . '-name' ); ?>" /></td>
                        </tr>
                        <tr>
                            <th scope="row"><label><?php echo esc_html__( 'Show Values', 'cf7-extensions-pro' ); ?></label></th>
                            <td>
                                <label for="show_value_on"><input type="radio" name="show_value" class="option" id="show_value_on" value="on" />On</label>
                                <label for="show_value_off"><input type="radio" name="show_value" class="option" id="show_value_off" value="off" />Off</label>
                            </td>
                        </tr>
                        <tr>
                            <th scope="row"><label><?php echo esc_html__( 'Slider Type', 'cf7-extensions-pro' ); ?></label></th>
                            <td>
                                <label for="slider_type_single"><input type="radio" name="slider_type" class="option" id="slider_type_single" value="single" />Single Handle</label>
                                <label for="slider_type_double"><input type="radio" name="slider_type" class="option" id="slider_type_double" value="double" />Double Handle</label>
                            </td>
                        </tr>
                        <tr>
                            <th scope="row"><label for="<?php echo esc_attr( $args['content'] . '-minimum-value' ); ?>"><?php echo esc_html__( 'Minimum Value', 'cf7-extensions-pro' ); ?></label></th>
                            <td>
                                <input type="text" name="minimum_value" class="minimum-value oneline option" placeholder="10" id="<?php echo esc_attr( $args['content'] . '-minimum-value' ); ?>" />
                            </td>
                        </tr>
                        <tr>
                            <th scope="row"><label for="<?php echo esc_attr( $args['content'] . '-maximum-value' ); ?>"><?php echo esc_html__( 'Maximum Value', 'cf7-extensions-pro' ); ?></label></th>
                            <td>
                                <input type="text" name="maximum_value" class="maximum-value oneline option" placeholder="100" id="<?php echo esc_attr( $args['content'] . '-maximum-value' ); ?>" />
                            </td>
                        </tr>
                        <tr>
                            <th scope="row"><label for="<?php echo esc_attr( $args['content'] . '-default-value' ); ?>"><?php echo esc_html__( 'Default Value', 'cf7-extensions-pro' ); ?></label></th>
                            <td>
                                <input type="text" name="default_value" class="default-value oneline option" placeholder="50" id="<?php echo esc_attr( $args['content'] . '-default-value' ); ?>" />
                                <p><?php echo esc_html__( 'For the "Double Handle" slider type, you can set two values separated by a comma (","). If you only set one value, the other will default to the maximum value.','cf7-extensions-pro' ) ?></p>
                            </td>
                        </tr>
                        <tr>
                            <th scope="row"><label for="<?php echo esc_attr( $args['content'] . '-range-step' ); ?>"><?php echo esc_html__( 'Range Step', 'cf7-extensions-pro' ); ?></label></th>
                            <td>
                                <input type="text" name="range_step" class="range-step oneline option" placeholder="1" id="<?php echo esc_attr( $args['content'] . '-range-step' ); ?>" />
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="insert-box">
                <input type="text" name="<?php echo esc_attr( $type ); ?>" class="tag code" readonly="readonly" onfocus="this.select()" />
                <div class="submitbox">
                    <input type="button" class="button button-primary insert-tag" value="<?php esc_html_e( 'Insert Tag', 'cf7-extensions-pro' ); ?>" />
                </div>
                <br class="clear" />
            </div>
        <?php
    }

    public function validation_filter($result, $tag){
        $name = $tag->name;
        $value = ( isset( $_POST[ $name ] ) && !empty( $_POST[ $name ] ) ) ? sanitize_text_field($_POST[ $name ]) : null ; //phpcs:ignore WordPress.Security.NonceVerification.Missing
        if( empty( $value ) && $tag->is_required() ) {
            $result->invalidate( $tag, wpcf7_get_message( 'invalid_required' ) );
            return $result;
        }
        return $result;
    }
}

Extensions_Cf7_Range_slider::instance();