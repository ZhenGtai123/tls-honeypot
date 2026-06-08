<?php

if( ! defined( 'ABSPATH' ) ) exit(); // Exit if accessed directly

/**
 * HT CF7 Condition Setup
*/

class Extensions_Cf7_Condition_Setup{

	/**
     * [$_instance]
     * @var null
    */
    private static $_instance = null;

    /**
     * [instance] Initializes a singleton instance
     * @return [Extensions_Cf7_Condition_Setup]
    */
    public static function instance() {
        if ( is_null( self::$_instance ) ) {
            self::$_instance = new self();
        }
        return self::$_instance;
    }

    /**
     * save the conditions to the post_meta
     * @param string form_id
    */
    public static function set_conditions_value($form_id, $conditions) {
        return update_post_meta($form_id,'extcf7_conditional_options',$conditions); 
    }

    /**
     * load the conditions from the post_meta
     * @param string $form_id
    */
    public static function get_conditions_value($form_id) {
        // make sure conditions are an array.
        $options = get_post_meta($form_id,'extcf7_conditional_options',true);
        return is_array($options) ? $options : array();
    }

    public static function setup_conditions_string_to_array($condition_string){
        
    	$conditions = [];

    	$condition_process = explode("show ", $condition_string);

    	foreach ($condition_process as $k => $value_process){
    		if($k > 0){
    			$set_condition = preg_split("/\n /",$value_process);
    			foreach ($set_condition as $j => $c_str) {

                    preg_match('/equal|not-equal/i', $c_str, $operator_input_value);
                    preg_match('/".*?"/', $c_str, $if_conditions_value);

    				if( 0 == $j){
                        preg_match_all("/\[(.*?)\]/", $c_str, $rule_applied_field);
    					$condition_rules['rule_applied_field']  = str_replace( array('[',']'), '', $rule_applied_field[0][0] );
    					$condition_rules['and_condition_rules'] = [
                            [
                                'if_field_input' => str_replace( array('[',']'), '', $rule_applied_field[0][1] ),
                                'if_type_input'  => '',
                                'operator_input' => $operator_input_value[0],
                                'if_value_input' => str_replace('"', '', $if_conditions_value[0]),
                            ]
                        ];
    					continue;
    				}

    				preg_match('/\[(.*?)\]/', $c_str, $if_field_input_value);
                    preg_match('/and|or/i', $c_str, $if_type_input_value);
    				$condition_rules['and_condition_rules'][] = [
    					'if_field_input' => str_replace( array('[',']'), '', $if_field_input_value[0] ),
                        'if_type_input'  => $if_type_input_value[0],
    					'operator_input' => $operator_input_value[0],
    					'if_value_input' => str_replace('"', '', $if_conditions_value[0]),
    				];
    			}
    			array_push($conditions, $condition_rules);
    			$condition_rules['and_condition_rules'] = [];
    		}
    	}

    	return $conditions;
    }

    public static function serialize_conditions_value($array){

    	$conditions_lines = [];

        foreach ($array as $entry) {
            $rule_applied_field = $entry['rule_applied_field'];
            $and_condition_rules = $entry['and_condition_rules'];

            foreach ($and_condition_rules as $i => $rule) {
                $if_field_input = $rule['if_field_input'];
                $if_type_input  = isset($rule['if_type_input']) ? $rule['if_type_input'] : 'and';
                $operator_input = $rule['operator_input'];
                $if_value_input = $rule['if_value_input'];

                if ($i == 0){
                    $conditions_lines[] = "show [{$rule_applied_field}] if-[{$if_field_input}]-{$operator_input}-\"{$if_value_input}\"";
                }else{
                    $conditions_lines[] =" {$if_type_input}-[{$if_field_input}]-{$operator_input}-\"{$if_value_input}\"";
                }
            }
        }
        
        return implode("\n", $conditions_lines);
    }

}

Extensions_Cf7_Condition_Setup::instance();

add_filter( 'wpcf7_contact_form_properties', 'extcf7_properties', 10, 1 );

function extcf7_properties($form_properties) {

	if (!is_admin() || ( class_exists( '\Elementor\Plugin' ) && ( \Elementor\Plugin::$instance->editor->is_edit_mode() || \Elementor\Plugin::$instance->preview->is_preview_mode() ) )) {

        $cf7_form = $form_properties['form'];

	    $cf7_form_parts = preg_split('/(\[\/?fields_group(?:\]|\s.*?\]))/',$cf7_form, -1,PREG_SPLIT_NO_EMPTY | PREG_SPLIT_DELIM_CAPTURE);

	    ob_start();

	    foreach ($cf7_form_parts as $cf7_form_part) {
	    	if (substr($cf7_form_part,0,14) == '[fields_group ') {
	    		$form_tag_parts = explode(' ',rtrim($cf7_form_part,']'));

	    		array_shift($form_tag_parts);

	    		$form_tag_id = $form_tag_parts[0];

                if(in_array('clear_field_on_hide' , $form_tag_parts)){
                    $clear_on_hide = ' data-clear= clear_field_on_hide';
                 }else{
                    $clear_on_hide = '';
                }

			    echo '<div data-id="'.esc_attr($form_tag_id).'"'.esc_attr($clear_on_hide).' data-class="extcf7_group">';
		    } else if ($cf7_form_part == '[/fields_group]') {
	    		echo '</div>';
		    } else {
	    		echo $cf7_form_part; //phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
		    }
	    }

        $form_properties['form'] = ob_get_clean();
    }
    return $form_properties;
}

add_action('wpcf7_form_hidden_fields', 'extcf7_conditional_form_hidden_fields',10,1);

function extcf7_conditional_form_hidden_fields($form_hidden_fields) {

    $current_form = wpcf7_get_current_contact_form();
    $current_form_id = $current_form->id();
    $conditions = Extensions_Cf7_Condition_Setup::get_conditions_value($current_form_id);
    foreach ($conditions as $k1 => $condition) {
        foreach ($condition['and_condition_rules'] as $k2 => $cnd_props) {
            if(!isset($cnd_props['if_type_input'])){
                if($k2 > 0){
                    $conditions[$k1]['and_condition_rules'][$k2]['if_type_input'] = 'and';
                }else{
                    $conditions[$k1]['and_condition_rules'][$k2]['if_type_input'] = '';
                }
            } 
        }
    }
    $options = array(
        'form_id' => $current_form_id,
        'conditions' => $conditions
    );

	return array_merge($form_hidden_fields, array(
        '_extcf7_conditional_options' => ''.wp_json_encode($options),
    ));
}