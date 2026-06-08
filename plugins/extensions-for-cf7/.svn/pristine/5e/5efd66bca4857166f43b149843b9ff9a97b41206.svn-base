<?php

if( ! defined( 'ABSPATH' ) ) exit(); // Exit if accessed directly

/**
 * HT CF7 Condition
*/

class Extensions_Cf7_Column{

	/**
     * [$_instance]
     * @var null
    */
    private static $_instance = null;

    /**
     * [instance] Initializes a singleton instance
     * @return [Extensions_Cf7_Column]
    */
    public static function instance() {
        if ( is_null( self::$_instance ) ) {
            self::$_instance = new self();
        }
        return self::$_instance;
    }

	function __construct(){
        add_action('wpcf7_init', [$this, 'wpcf7_tags']);
        add_action('admin_init', [$this, 'wpcf7_tag_generator'], 589);

        add_filter( 'wpcf7_contact_form_properties', [$this, 'row_properties'], 9999, 1 );
        add_filter( 'wpcf7_contact_form_properties', [$this, 'col_properties'], 9999, 1 );
	}
	public function wpcf7_tags() {
        if (function_exists('wpcf7_add_form_tag')) {
            wpcf7_add_form_tag('extcf7_column', [$this, 'column_shortcode'], true);
        } else {
            throw new Exception(esc_html__('functions wpcf7_add_form_tag not found.', 'cf7-extensions'));
        }
    }
    public function column_shortcode($tag){
        $tag = new WPCF7_FormTag($tag);
        return $tag->content;
    }

    public function row_properties($form_properties) {
        if (!is_admin() || ( class_exists( '\Elementor\Plugin' ) && ( \Elementor\Plugin::$instance->editor->is_edit_mode() || \Elementor\Plugin::$instance->preview->is_preview_mode() ) )) {
            $form = $form_properties['form'];

            $form_parts = preg_split('/(\[\/?extcf7_row(?:\]|\s.*?\]))/',$form, -1,PREG_SPLIT_NO_EMPTY | PREG_SPLIT_DELIM_CAPTURE);

            ob_start();
            foreach ($form_parts as $form_part) {
                if ($form_part == '[extcf7_row]') {
                    echo '<div class="extcf7-row">';
                } else if ($form_part == '[/extcf7_row]') {
                    echo '</div>';
                } else {
                    echo $form_part; //phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
                }
            }
            $form_properties['form'] = ob_get_clean();
        }
        return $form_properties;
    }
    public function col_properties($form_properties) {
        if (!is_admin() || ( class_exists( '\Elementor\Plugin' ) && ( \Elementor\Plugin::$instance->editor->is_edit_mode() || \Elementor\Plugin::$instance->preview->is_preview_mode() ) )) {
            $form = $form_properties['form'];

            $form_parts = preg_split('/(\[\/?extcf7_col(?:\]|\s.*?\]))/',$form, -1,PREG_SPLIT_NO_EMPTY | PREG_SPLIT_DELIM_CAPTURE);
            ob_start();
            foreach ($form_parts as $form_part) {
                if ($form_part == '[extcf7_col col:12]') {
                    echo '<div class="extcf7-col extcf7-col-12">';
                } else if ($form_part == '[extcf7_col col:6]') {
                    echo '<div class="extcf7-col extcf7-col-6">';
                } else if ($form_part == '[extcf7_col col:4]') {
                    echo '<div class="extcf7-col extcf7-col-4">';
                } else if ($form_part == '[extcf7_col col:3]') {
                    echo '<div class="extcf7-col extcf7-col-3">';
                } else if ($form_part == '[/extcf7_col]') {
                    echo '</div>';
                } else {
                    echo $form_part; //phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
                }
            }
            $form_properties['form'] = ob_get_clean();
        }
        return $form_properties;
    }

	public function wpcf7_tag_generator() {
        if (! function_exists( 'wpcf7_add_tag_generator')) { 
            return;
        }
        wpcf7_add_tag_generator(
			'extcf7_column',
			esc_html__('HT Column', 'cf7-extensions'),
            'wpcf7-tg-extcf7-column',
            [$this, 'column_layout']
        );

    }
    public function column_layout($contact_form, $args = '') {
        $args = wp_parse_args( $args, [] );
        $type = 'extcf7_column';
        ?>
            <div class="control-box">
                <table class="form-table">
                    <tbody>
                        <tr class="extcf7-column-item">
                            <th scope="row">
                                <?php echo esc_html__( '1 Column', 'cf7-extensions' ); ?>
                                <span class="button extcf7-column-select" data-code="[extcf7_row]
    [extcf7_col col:12] --Put your code here-- [/extcf7_col]
[/extcf7_row]"><?php echo esc_html__( 'Insert tag', 'cf7-extensions' ); ?></span>
                            </th>
                            <td>
								<pre class="extcf7-column-code">
[extcf7_row]
    [extcf7_col col:12] --Put your code here-- [/extcf7_col]
[/extcf7_row]
</pre>
                            </td>
                        </tr>
                        <tr class="extcf7-column-item">
                            <th scope="row">
                                <?php echo esc_html__( '2 Column', 'cf7-extensions' ); ?>
                                <span class="button extcf7-column-select" data-code="[extcf7_row]
    [extcf7_col col:6] --Put your code here-- [/extcf7_col]
    [extcf7_col col:6] --Put your code here-- [/extcf7_col]
[/extcf7_row]"><?php echo esc_html__( 'Insert tag', 'cf7-extensions' ); ?></span>
                            </th>
                            <td>
								<pre class="extcf7-column-code">
[extcf7_row]
    [extcf7_col col:6] --Put your code here-- [/extcf7_col]
    [extcf7_col col:6] --Put your code here-- [/extcf7_col]
[/extcf7_row]
</pre>
                            </td>
                        </tr>
                        <tr class="extcf7-column-item">
                            <th scope="row">
                                <?php echo esc_html__( '3 Column', 'cf7-extensions' ); ?>
                                <span class="button extcf7-column-select" data-code="[extcf7_row]
    [extcf7_col col:4] --Put your code here-- [/extcf7_col]
    [extcf7_col col:4] --Put your code here-- [/extcf7_col]
    [extcf7_col col:4] --Put your code here-- [/extcf7_col]
[/extcf7_row]"><?php echo esc_html__( 'Insert tag', 'cf7-extensions' ); ?></span>
                            </th>
                            <td>
								<pre class="extcf7-column-code">
[extcf7_row]
    [extcf7_col col:4] --Put your code here-- [/extcf7_col]
    [extcf7_col col:4] --Put your code here-- [/extcf7_col]
    [extcf7_col col:4] --Put your code here-- [/extcf7_col]
[/extcf7_row]
</pre>
                            </td>
                        </tr>
                        <tr class="extcf7-column-item">
                            <th scope="row">
                                <?php echo esc_html__( '4 Column', 'cf7-extensions' ); ?>
                                <span class="button extcf7-column-select" data-code="[extcf7_row]
    [extcf7_col col:3] --Put your code here-- [/extcf7_col]
    [extcf7_col col:3] --Put your code here-- [/extcf7_col]
    [extcf7_col col:3] --Put your code here-- [/extcf7_col]
    [extcf7_col col:3] --Put your code here-- [/extcf7_col]
[/extcf7_row]"><?php echo esc_html__( 'Insert tag', 'cf7-extensions' ); ?></span>
                            </th>
                            <td>
								<pre class="extcf7-column-code">
[extcf7_row]
    [extcf7_col col:3] --Put your code here-- [/extcf7_col]
    [extcf7_col col:3] --Put your code here-- [/extcf7_col]
    [extcf7_col col:3] --Put your code here-- [/extcf7_col]
    [extcf7_col col:3] --Put your code here-- [/extcf7_col]
[/extcf7_row]
</pre>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="insert-box sr-only">
                <input type="text" name="<?php echo esc_attr( $type ); ?>" class="tag code extcf7-column-insert" readonly="readonly" onfocus="this.select()" />
                <div class="submitbox">
                    <input type="button" class="button button-primary extcf7-column-insert-button insert-tag" value="<?php esc_html_e( 'Insert Tag', 'cf7-extensions' ); ?>" />
                </div>
                <br class="clear" />
            </div>
        <?php
    }
}

Extensions_Cf7_Column::instance();