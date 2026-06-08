<?php
/**
 *  @phpcs:disable WordPress.DB.PreparedSQL.InterpolatedNotPrepared, WordPress.DB.DirectDatabaseQuery.DirectQuery, WordPress.DB.DirectDatabaseQuery.NoCaching
 */

/**
 * [extcf7_clean]
 * @param  [JSON] $var
 * @return [array]
 */
function extcf7_clean( $varr ) {
    if ( is_array( $varr ) ) {
        return array_map( 'extcf7_clean', $varr );
    } else {
        return is_scalar( $varr ) ? sanitize_text_field( $varr ) : $varr;
    }
}

/**
 * Get option value
 * 
 * Look at the new option name first
 * if does not exists that option, then look the old option key
 *
 * @return string
 */
if( !function_exists('htcf7ext_get_option') ){
    function htcf7ext_get_option( $section = '', $option_key = '', $default = '' ){
        $new_options = array();
    
        if( $section === 'htcf7ext_opt' ){
            $new_options = get_option('htcf7ext_opt');
        }
    
        if( $section === 'htcf7ext_opt_extensions' ){
            $new_options = get_option('htcf7ext_opt_extensions');
        }
    
        // 1. look for new settings data
        // 2. look for old settings data
        // 3. look for default param
    
        if( isset($new_options[$option_key]) ){
            return $new_options[$option_key];
        } elseif( get_option($option_key) ) {
            return get_option($option_key);
        } elseif( $default ){
            return $default;
        }
    
        return '';
    }
}

/**
 * Get module option value
 * @input section, option_id, option_key, default
 * @return mixed
 */
if( !function_exists('htcf7ext_get_module_option') ) {
    function htcf7ext_get_module_option( $section = '', $option_id = '', $option_key = '', $default = null ){

        $module_settings = get_option( $section );
        
        if( $option_id && is_array( $module_settings ) && count( $module_settings ) > 0 ) {


            if( isset ( $module_settings[ $option_id ] ) && '' != $module_settings[ $option_id ] ) {

                $option_value = json_decode( $module_settings[ $option_id ], true );

                if( $option_key && is_array( $option_value  ) && count( $option_value  ) > 0 ) {

                    if ( isset($option_value[$option_key] ) && '' != $option_value[$option_key] ) {
                        return $option_value[$option_key];
                    } else {
                        return $default;
                    }
                } else {
                    return $module_settings[ $option_id ];
                }
                
            } else {
                return $default;;
            }

        } else {
            return $module_settings;
        }

    }
}

function htcf7ext_update_menu_badge() {
    
    global $menu, $submenu, $wpdb;
    $slug        = 'contat-form-list';
    $capability  = 'manage_options';
    $table_name  = $wpdb->prefix.'extcf7_db';

    $total = $wpdb->get_var($wpdb->prepare("SELECT COUNT(*) FROM $table_name WHERE status = %s ", 'unread'));

    // Update Menu badge
    foreach ( $menu as $key => $menu_item ) {
        if ( $menu_item[2] === $slug && current_user_can( $capability ) ) {
            $menu[$key][0] = sprintf( '%1$s <span class="awaiting-mod count-%2$d"><span class="pending-count" aria-hidden="true">%2$d</span><span class="comments-in-moderation-text screen-reader-text">%2$d %3$s</span></span>', $menu_item[3], $total, __('Unread Message', 'cf7-extensions') );
            break;
        }
    }

    // Update Submenu badge
    foreach ( $submenu as $key => $items ) {
        if ( $key === $slug && current_user_can( $capability ) ) {
            foreach ($items as $index => $value) {
                if ( $value[2] === 'admin.php?page=contat-form-list#/entries' ) {
                    $submenu[$key][$index][0] = sprintf( '%1$s <span class="awaiting-mod count-%2$d"><span class="pending-count" aria-hidden="true">%2$d</span><span class="comments-in-moderation-text screen-reader-text">%2$d %3$s</span></span>', __('Submissions', 'cf7-extensions'), $total, __('Unread Message', 'cf7-extensions') );
                    break;
                }
            }
            break;
        }
    }

}