<?php
use HTCf7Ext\Admin\Options_Field;
/**
 * Contact Form Database Inialiaze
*/
class Extensions_Cf7_Metabox {
    private static $_instance = null;
    private $metabox = [];

    /**
     * [instance] Initializes a singleton instance
     * @return [Docus]
     */
    public static function instance() {
        if (is_null( self::$_instance )) {
            self::$_instance = new self();
        }
        return self::$_instance;
    }

	function __construct(){
        $this->metabox = apply_filters('extcf7_post_metabox', $value = [] );
        if(empty($this->metabox)) {
            return;
        }
        add_action( 'wpcf7_admin_footer', [$this, 'styler_meta_box_content'], 20 );
        add_action('admin_enqueue_scripts', [$this, 'admin_enqueue_scripts']);
        add_action('admin_head-toplevel_page_wpcf7', [$this, 'activate_color_picker']);
	}
    public function admin_enqueue_scripts($hook) {
		if ( $hook === 'toplevel_page_wpcf7' ) {
			wp_enqueue_script( 'wp-color-picker' );
			wp_enqueue_style( 'wp-color-picker' );
		}
	}
    function activate_color_picker() {
        echo "<script defer>
            jQuery.noConflict();
            (function($) {
                $(function() {
                    $('.rwp-color-picker').wpColorPicker({defaultColor: false});
                });
            })(jQuery);
        </script>";
    }
    
    public function styler_meta_box_content($form) {
        ?>
        <div id="extcf7-metabox" class="extcf7-metabox">
            <div class="extcf7-metabox-header">
                <h3 class="extcf7-metabox-title"><?php esc_html_e('Extensions for CF7 Options', 'cf7-extensions-pro')?></h3>
            </div>
            <div class="extcf7-metabox-sidebar">
                <div class="extcf7-metabox-sidebar-tab">
                    <?php foreach ($this->metabox as $key => $metabox) {
                        printf(
                            '<button data-toggle="extcf7-metabox-tab-%s" type="button">%s</button>',
                            esc_attr($metabox['id']),
                            esc_html($metabox['label'])
                        );
                    } ?>
                </div>
            </div>
            <div class="extcf7-metabox-tab-content">
                <?php
                    foreach ($this->metabox as $key => $metabox) { ?>
                        <div id="extcf7-metabox-tab-<?php echo esc_attr($metabox['id']) ?>" class="extcf7-metabox-tab-pane" style="display: none;">
                            <div class="htcf7ext-form-fields" style="flex-direction: column;">
                                <?php if(!empty($metabox['tabs'])) { ?>
                                    <div class="htcf7ext-form-fields">
                                        <?php foreach ($metabox['fields'] as $field) {
                                            $field_classes = [
                                                'htcf7ext-admin-option',
                                                'htcf7ext-admin-option-'. $field['type']
                                            ];
                                            if(!empty($field['class'])) {
                                                $field_classes = array_merge($field_classes, explode(' ', $field['class']));
                                            }
                                            if (!isset($field['group'])) {
                                                printf(
                                                    '<div class="%s">',
                                                    esc_attr(implode(' ', $field_classes))
                                                );
                                                    echo $this->field($field, $form, $metabox);
                                                echo '</div>';
                                            }
                                        }?>
                                    </div>
                                    <div class="htcf7ext-tab-nav">
                                        <?php foreach ($metabox['tabs'] as $tab) {
                                            printf(
                                                '<button class="%s" data-toggle="extcf7-tab-%s" type="button">%s</button>',
                                                !empty($tab['active']) ? 'active' : '',
                                                esc_attr($tab['id']),
                                                esc_html($tab['label'])
                                            );
                                        } ?>
                                    </div>
                                    <div class="extcf7-tab-content">
                                        <?php foreach ($metabox['tabs'] as $tab) { ?>
                                            <div id="extcf7-tab-<?php echo esc_attr($tab['id']) ?>" class="extcf7-tab-pane"  style="<?php echo !empty($tab['active']) ? 'display: block;' : 'display: none;'; ?>">
                                                <div class="htcf7ext-form-fields">
                                                    <?php foreach ($metabox['fields'] as $field) {
                                                        $field_classes = [
                                                            'htcf7ext-admin-option',
                                                            'htcf7ext-admin-option-'. $field['type']
                                                        ];
                                                        if(!empty($field['class'])) {
                                                            $field_classes = array_merge($field_classes, explode(' ', $field['class']));
                                                        }
                                                        if (!empty($field['group']) && $field['group'] === $tab['id']) {
                                                            printf(
                                                                '<div class="%s">',
                                                                esc_attr(implode(' ', $field_classes))
                                                            );
                                                                echo $this->field($field, $form, $metabox);
                                                            echo '</div>';
                                                        }
                                                    }?>
                                                </div>
                                            </div>
                                        <?php } ?>
                                    </div>
                                <?php } else { ?>
                                    <div class="htcf7ext-form-fields">
                                        <?php foreach ($metabox['fields'] as $field) {
                                            $field_classes = [
                                                'htcf7ext-admin-option',
                                                'htcf7ext-admin-option-'. $field['type']
                                            ];
                                            if(!empty($field['class'])) {
                                                $field_classes = array_merge($field_classes, explode(' ', $field['class']));
                                            }
                                            printf(
                                                '<div class="%s">',
                                                esc_attr(implode(' ', $field_classes))
                                            );
                                                echo $this->field($field, $form, $metabox);
                                            echo '</div>';
                                        }?>
                                    </div>
                                <?php } ?>
                            </div>
                        </div>
                    <?php }
                ?>
            </div>
        </div>
        <?php
    }
    public function field($field, $form, $metabox) {
        echo $this->field_label($field);
        if($field['type'] !== 'heading') {
            echo '<div class="htcf7ext-admin-option-field">';
            if($field['type'] === 'number' || $field['type'] === 'text' || $field['type'] === 'email') {
                echo $this->field_input($field, $form, $metabox);
            }
            if($field['type'] === 'select') {
                echo $this->field_select($field, $form, $metabox);
            }
            if($field['type'] === 'color') {
                echo $this->field_color($field, $form, $metabox);
            }
            if($field['type'] === 'swatch') {
                echo $this->field_swatch($field, $form, $metabox);
            }
            echo '</div>';
        }
    }
    public function field_label($field) {
        ?>
            <div class="htcf7ext-admin-option-content">
                <?php if(!empty($field['name'])) printf('<h6 class="htcf7ext-admin-option-label">%s</h6>', esc_html($field['name'])); ?>
                <?php if(!empty($field['desc'])) printf('<p class="htcf7ext-admin-option-desc">%s</p>', esc_html($field['desc'])); ?>
            </div>
        <?php
    }
    public function field_input($field, $form, $metabox) {
        printf(
        '<input class="htcf7ext-admin-field-input" name="extcf7_%s[%s]" type="%s" value="%s" placeholder="%s" />',
            esc_attr($metabox['id']),
            esc_attr($field['id']),
            esc_attr($field['type']),
            esc_attr($this->value($field, $form, $metabox)),
            !empty($field['placeholder']) ? esc_attr($field['placeholder']) : ''
        );
    }
    public function field_swatch($field, $form, $metabox) {
        printf(
            '<input id="%1$s" class="htcf7ext-admin-field-swatch" name="extcf7_%2$s[%1$s]" type="checkbox" %3$s />',
            esc_attr($field['id']),
            esc_attr($metabox['id']),
            checked($this->value($field, $form, $metabox) === 'on', true, false)
        );
        printf(
            '<label for="%1$s" class="htcf7ext-admin-field-swatch-label">%2$s %3$s <span class="indicator"></span></label>',
            esc_attr($field['id']),
            !empty($field['label_on']) ? '<span class="on">'.esc_attr($field['label_on']).'</span>' : '',
            !empty($field['label_off']) ? '<span class="off">'.esc_attr($field['label_off']).'</span>' : ''

        );
    }
    public function field_color($field, $form, $metabox) {
        printf(
        '<input class="htcf7ext-admin-field-input rwp-color-picker" name="extcf7_%s[%s]" type="text" value="%s" />',
            esc_attr($metabox['id']),
            esc_attr($field['id']),
            esc_attr($this->value($field, $form, $metabox))
        );
    }
    public function field_select($field, $form, $metabox) {
        echo '<select class="htcf7ext-admin-field-select" name="extcf7_'.esc_attr($metabox['id']).'[' . esc_attr($field['id']) . ']">';
        if (!empty($field['options']) && is_array($field['options'])) {
            foreach ($field['options'] as $value => $label) {
                printf(
                    '<option value="%s" %s>%s</option>',
                    esc_attr($value),
                    selected($this->value($field, $form, $metabox) == $value, true, false),
                    esc_html($label)
                );
            }
        }
        echo '</select>';
    }
    private function value( $field, $form, $metabox) {
		if ( metadata_exists( 'post', $form->id(), 'extcf7_'.$metabox['id'] ) ) {
			$meta = get_post_meta( $form->id(), 'extcf7_'.$metabox['id'], true );
            if( !empty($meta[$field['id']]) ) {
                return $meta[$field['id']];
            } else {
                return '';
            }
		} else if ( !empty( $field['default'] ) ) {
			return $field['default'];
		} else {
			return '';
		}
	}
}
Extensions_Cf7_Metabox::instance();