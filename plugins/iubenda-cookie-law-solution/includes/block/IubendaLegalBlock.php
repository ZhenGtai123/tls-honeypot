<?php


class IubendaLegalBlock
{
    const IUB_LEGAL_BLOCK_NAME = 'iubenda/legal-block';  // IUB legal block Name
    const IUB_LEGAL_BLOCK_SHORTCODE = 'iub-wp-block-buttons';  // IUB legal block Shortcode

    /**
     * IubendaLegalBlock constructor.
     */
    public function __construct()
    {
        add_action('iubenda_attach_block_in_footer', [$this, 'attach_legal_block_into_footer']);

        // Change preregistered default footer content
        add_action('init', [$this, 'change_pre_registered_default_footer_content'], 10, 0);

        // Attach IUB legal block into WP blocks area
        add_action('admin_init', [$this, 'attach_legal_block_into_block_area'], 10, 0);

        // Register IUB Legal block shortcode
        add_action('after_setup_theme', [$this, 'register_shortcode']);
    }

    /**
     * Register IUB Legal block shortcode function.
     *
     * @return void
     */
    public function register_shortcode() {
        add_shortcode(static::IUB_LEGAL_BLOCK_SHORTCODE, [$this, 'render_iub_legal_block']);
    }

    /**
     * Attach iubenda legal block in footer
     */
    public function attach_legal_block_into_footer()
    {
        // if current theme doesn't supports blocks -> return
        if (!$this->check_current_theme_supports_blocks()) {
            return;
        }

        // Check if IUB short code exist in footer
        if ($this->check_iub_block_shortcode_exists_in_the_footer()) {
            return;
        }

        $this->force_append_legal_block_in_footer();
    }

    /**
     * Detach iubenda legal block from footer
     */
    public function detach_legal_block_from_footer()
    {
        // if current theme doesn't supports blocks -> return
        if (!$this->check_current_theme_supports_blocks()) {
            return;
        }

        // Check if IUB short code exist in footer
        if ($this->check_iub_block_shortcode_exists_in_the_footer()) {
            $this->force_detach_legal_block_from_footer();
            return;
        }
    }

    /**
     * Attach iubenda legal block in WP blocks area
     */
    public function attach_legal_block_into_block_area()
    {
        // Register IUB js block
        wp_register_script('iubenda-block-editor', IUBENDA_PLUGIN_URL . '/assets/js/legal_block.js', ['wp-blocks', 'wp-block-editor'], iubenda()->version);
        register_block_type(static::IUB_LEGAL_BLOCK_NAME, ['editor_script' => 'iubenda-block-editor',]);

        // Send iub vars from backend to JS file
        wp_localize_script('iubenda-block-editor', 'iub_block_js_vars', [
            'block_name' => 'iubenda/legal-block',
            'iub_legal_block_shortcode' => static::IUB_LEGAL_BLOCK_SHORTCODE,
            'iub_legal_block_short_title' => __('Legal', 'iubenda'),
        ]);
    }

    /**
     * Render iubenda legal block and apply filters
     * @return mixed
     */
    public function render_iub_legal_block()
    {
        $html = '';
        $html = apply_filters('before_iub_legal_block_section', $html);
        $html .= '<section>' . $this->iub_legal_block_html($html) . '</section>';
        $html = apply_filters('after_iub_legal_block_section', $html);

        return $html;
    }

    /**
     * Check if the current theme support WP blocks or not
     * @return bool
     */
    public function check_current_theme_supports_blocks()
    {
        // Condition if there is no sidebar and the activated theme is working by WP blocks
        global $wp_registered_sidebars;

        if (!boolval(iub_array_get($wp_registered_sidebars, 'sidebar-1'))) {
            return true;
        }

        return false;
    }

    /**
     * Iubenda legal block html
     * @param $html
     * @return mixed|string
     */
    private function iub_legal_block_html($html)
    {
        $quick_generator_service = new QuickGeneratorService();

        $pp_status = iub_array_get(iubenda()->settings->services, 'pp.status') == 'true';
        $pp_position = iub_array_get(iubenda()->options['pp'], 'button_position') == 'automatic';
        $tc_status = iub_array_get(iubenda()->settings->services, 'tc.status') == 'true';
        $tc_position = iub_array_get(iubenda()->options['tc'], 'button_position') == 'automatic';

        if ($pp_status && $pp_position) {
            $html .= $quick_generator_service->pp_button();
        }

        if (($pp_status && $pp_position) && ($tc_status && $tc_position)) {
            $html .= '<br>';
        }

        if (($tc_status == 'true') && ($tc_position == 'automatic')) {
            $html .= $quick_generator_service->tc_button();
        }

        return $html;
    }

    /**
     * Get footer post from database
     * @return mixed|null
     */
    private function get_footer_from_database()
    {
        // Default arguments
        $args = [
            'post_type'      => 'wp_template_part',
            'post_status'    => 'publish',
            'tax_query'      => [
                [
                    'taxonomy' => 'wp_theme',
                    'field'    => 'slug',
                    'terms'    => [ get_stylesheet() ],
                ],
            ],
            'posts_per_page' => 1,
            'no_found_rows'  => true,
        ];

        // Search for footer in database
        $args['name'] = 'footer';

        // Run WP Query with new args
        $footer_query = new WP_Query($args);
        $footer = $footer_query->have_posts() ? $footer_query->next_post() : null;

        // Footer exist in database
        if ($footer) {
            return $footer;
        }

        // Search if it is inserted as a default footer in the database
        $args['name'] = 'default-footer';

        // Run WP Query with new args
        $footer_query = new WP_Query($args);
        $footer = $footer_query->have_posts() ? $footer_query->next_post() : null;

        return $footer;
    }

    /**
     * Check if IUB short code exist in footer
     * @return bool
     */
    private function check_iub_block_shortcode_exists_in_the_footer()
    {
        $footer = $this->get_footer_from_database();

        if ($footer && $this->check_iub_block_shortcode_exists_in_the_footer_content($footer->post_content)) {
            return true;
        }

        return false;
    }

    /**
     * Force append IUB legal block in footer
     */
    private function force_append_legal_block_in_footer()
    {
        $footer = $this->get_footer_from_database();

        if ($footer) {
            $footer->post_content = $this->insert_iub_block_shortcode_into_footer_by_dom($footer->post_content);

            $this->update_the_footer_into_database($footer);
        }

        // There is no footer stored in database then
        // Attach legal block into WP_Block_Patterns as WP default footer and insert this footer into database
        $this->change_pre_registered_default_footer_content(true);
    }

    /**
     * Insert Legal block into WP content by php DOMDocument
     *
     * @param $footer_content
     * @return false|string
     */
    private function insert_iub_block_shortcode_into_footer_by_dom($footer_content)
    {
        if($this->check_iub_block_shortcode_exists_in_the_footer_content($footer_content)){
            return $footer_content;
        }

        $dom = new DOMDocument();
        $previous_value = libxml_use_internal_errors(TRUE);
        $dom->loadHTML((string)$footer_content, LIBXML_HTML_NOIMPLIED | LIBXML_HTML_NODEFDTD);
        libxml_clear_errors();
        libxml_use_internal_errors($previous_value);

        $target_div = $dom->getElementsByTagName('div')->item(1);

        if(!$target_div){
            return '';
        }

        // insert End of Iubenda legal block before start
        $template = $dom->createDocumentFragment();
        $template->appendXML(' <!-- /wp:'. static::IUB_LEGAL_BLOCK_NAME .' --> ');
        $target_div->insertBefore($template, $target_div->firstChild);

        // Create container div with class 'wp-block-iubenda-legal-block'
        $div = $dom->createElement("div");
        $div->setAttribute("class", "wp-block-iubenda-legal-block");

        // Append the block title
        $div->appendChild($dom->createElement('p', __('Legal', 'iubenda')));

        // Append the block content
        $div->appendChild($dom->createElement('p', '[iub-wp-block-buttons]'));

        // Insert the block into the footer
        $target_div->insertBefore($div, $target_div->firstChild);

        // Append Start of Iubenda legal block
        $template = $dom->createDocumentFragment();
        $template->appendXML(' <!-- wp:'. static::IUB_LEGAL_BLOCK_NAME .' --> ');
        $target_div->insertBefore($template, $target_div->firstChild);

        return $dom->saveHTML();
    }

    /**
     * Remove Legal block from WP content
     *
     * @param $footer_content
     * @return false|string
     */
    private function remove_iub_block_shortcode_from_footer($footer_content)
    {
        $start_of_iub_legal_block = '<!-- wp:'. static::IUB_LEGAL_BLOCK_NAME .' -->';
        $end_of_iub_legal_block = '<!-- /wp:'. static::IUB_LEGAL_BLOCK_NAME .' -->';

        return $this->iub_delete_in_between($start_of_iub_legal_block, $end_of_iub_legal_block, $footer_content);
    }

    /**
     * Update the current footer
     *
     * @param $footer
     */
    private function update_the_footer_into_database($footer)
    {
        return wp_update_post($footer);
    }

    /**
     * Attach legal block into WP_Block_Patterns as WP default footer
     * if $insert_into_database is true insert default footer into database
     *
     * @param bool $insert_into_database
     * @return void
     */
    public function change_pre_registered_default_footer_content($insert_into_database = false)
    {
        $public_id = (new ProductHelper())->get_public_id_for_current_language();

        // Return false if there is no public id for current language
        if (!($public_id)) {
            return;
        }

        // Check for PP & TC service status and codes
        if (!(new ProductHelper())->check_pp_tc_status_and_position()) {
            return;
        }

        // Check if WP_Block_Patterns_Registry is exist
        if (!class_exists('WP_Block_Patterns_Registry', false)) {
            return;
        }

        $block_registry = WP_Block_Patterns_Registry::get_instance();

        foreach ( $block_registry->get_all_registered() as $block) {
            $block_name = iub_array_get($block, 'name') ?: null;

            if (strpos($block_name, 'footer-default') !== false) {
                // Unregister default footer
                $block_registry->unregister(iub_array_get($block, 'name'));

                // Attach Iubenda legal block in footer content
                $block['content'] = $this->insert_iub_block_shortcode_into_footer_by_dom(iub_array_get($block, 'content'));

                // Register footer after attached Iubenda legal block on it
                $block_registry->register(iub_array_get($block, 'name'), $block);

                if ($insert_into_database) {
                    // Insert the footer into database
                    $this->insert_default_footer_into_database($block);
                }
            }
        }
    }

    /**
     * Insert default footer into database
     *
     * @param $block
     * @return int|WP_Error
     */
    private function insert_default_footer_into_database($block)
    {
        // taxonomies
        $taxonomies = [
            'wp_template_part_area' => 'footer',
            'wp_theme' => get_stylesheet(), // Current active theme slug
        ];

        // New footer data
        $footer = [
            'post_title'    => 'Footer',
            'post_content'  => $block['content'],
            'post_status'   => 'publish',
            'post_author'   => 1,
            'post_type'     => 'wp_template_part',
            'post_category' => [ 'footer' ],
            'tax_input'     => $taxonomies
        ];

        // Insert the new footer into the database
        wp_insert_post($footer);
    }

    /**
     * Force detach IUB legal block from footer
     */
    private function force_detach_legal_block_from_footer()
    {
        $footer = $this->get_footer_from_database();

        if ($footer) {
            $footer->post_content = $this->remove_iub_block_shortcode_from_footer($footer->post_content);

            $this->update_the_footer_into_database($footer);
        }
    }

    private function iub_delete_in_between($beginning, $end, $string) {
        $beginning_pos = strpos($string, $beginning);
        $end_pos = strpos($string, $end);
        if ($beginning_pos === false || $end_pos === false) {
            return $string;
        }

        $text_to_delete = substr($string, $beginning_pos, ($end_pos + strlen($end)) - $beginning_pos);

        return $this->iub_delete_in_between($beginning, $end, str_replace($text_to_delete, '', $string)); // recursion to ensure occurrences are removed
    }

    /**
     * Check IUB block shortcode exists in the footer content
     * @param $footer_content
     * @return bool
     */
    private function check_iub_block_shortcode_exists_in_the_footer_content($footer_content)
    {
        return strpos($footer_content, '[iub-wp-block-buttons]') !== false;
    }

}
