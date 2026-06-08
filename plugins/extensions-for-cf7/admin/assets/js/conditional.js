(function ($) {
    "use strict";

    var extcf7_single_and_entries = $('#extcf7-new-entry .extcf7-and-rules-container').find('.extcf7-and-rule')[0];
    var extcf7_single_and_rule = extcf7_single_and_entries ? extcf7_single_and_entries.innerHTML : '';
    var extcf7_single_conditon_rule = $('#extcf7-new-entry').html();
    var extcf7_ui_mode = $('#extcf7-entries-ui');
    var extcf7_text_mode = $('#extcf7-text-entries');
    var extcf7_only_text = $('#extcf7-text-only-checkbox');
    var extcf7_form_editor = $('#wpcf7-admin-form-element').eq(0);
    var extcf7_current_ui_mode = extcf7_conditional_mode.conditional_mode;
    var extcf7_condition_type = `<select class="extcf7-condition-type_input">
                        <option value="and">And</option>
                        <option value="or">Or</option>
                    </select>`;

    $('#extcf7-add-button').on('click', function(){
    	var extcf7_entry = $('<div class="extcf7-entry">'+extcf7_single_conditon_rule+'</div>');
    	extcf7_entry.appendTo('#extcf7-entries');
    });

    $(document).on('click','.extcf7-and-button',function(){
    	$(this).before('<div class="extcf7-and-rule">'+extcf7_condition_type+extcf7_single_and_rule+'</div>');
    });

    $(document).on('click','.extcf7-remove-condition-btn',function(){
    	var extcf7_condition_and_rule = $(this).closest('.extcf7-entry');
    	extcf7_condition_and_rule.remove();
    });

    $(document).on('click','.extcf7-delete-button',function(){
    	var extcf7_and_rule = $(this).closest('.extcf7-and-rule');
    	if (extcf7_and_rule.siblings().length > 1) {
            extcf7_and_rule.remove();
        }else{
            extcf7_and_rule[0].closest('.extcf7-entry').remove();
        }
    });

    function extcf7_convert_conditions_from_string_to_array_of_Objects(str){
        var condition_as_object = [];
        if(str){
            var object_process = str.split('show ');
            for (var i =0; i < object_process.length; i++){
                if(i > 0){
                    var set_condition = object_process[i].split(/\n /);
                    for(var j =0; j < set_condition.length; j++){
                        var condition_string = set_condition[j];
                        if(j == 0){
                            var rule_conditon_field = condition_string.match(/\[(.*?)\]/g);
                            var condition_object = {
                                rule_applied_field: rule_conditon_field[0].replace("[", "").replace("]", ""),
                                and_condition_rules: [{
                                    if_field_input : rule_conditon_field[1].replace("[", "").replace("]", ""),
                                    if_type_input  : '',
                                    operator_input : condition_string.match(/equal|not-equal/) ? condition_string.match(/equal|not-equal/)[0] : "equal",
                                    if_value_input : condition_string.match(/".*?"/g)[0].replace('"', '').replace('"', ''),
                                }],
                            };
                            continue;
                        }

                        condition_object.and_condition_rules.push({
                            if_field_input : condition_string.match(/\[(.*?)\]/)[0].replace("[", "").replace("]", ""),
                            if_type_input  : condition_string.match(/and|or/g)[0],
                            operator_input : condition_string.match(/equal|not-equal/) ? condition_string.match(/equal|not-equal/)[0] : "equal",
                            if_value_input : condition_string.match(/".*?"/g)[0].replace('"', '').replace('"', ''),
                        });
                    }
                    condition_as_object.push(condition_object);
                }
            }
            return condition_as_object;
        }
    }

    function extcf7_convert_conditions_from_array_of_objects_to_field_elements(conditions){

        if(conditions){
            jQuery('#extcf7-entries').html('');

            var group_entries = [];

            for (var i = 0; i<conditions.length; i++) {

                var condition = conditions[i];
                var id=0;

                // setup then_field
                var group_entry = $( '<div class="extcf7-entry">' + extcf7_single_conditon_rule + '</div>' );
                $('.extcf7-and-rule',group_entry).remove();
                $('.extcf7-then-field', group_entry).val(condition.rule_applied_field);

                for (var j = 0; j < condition.and_condition_rules.length; j++) {

                    var condition_rule;
                    var and_rule = condition.and_condition_rules[j];

                    if(!and_rule.if_type_input){
                        condition_rule = $('<div class="extcf7-and-rule">'+extcf7_single_and_rule+'</div>');
                    }else{
                        condition_rule = $('<div class="extcf7-and-rule">'+extcf7_condition_type+extcf7_single_and_rule+'</div>');
                        $('.extcf7-condition-type_input', condition_rule).val(and_rule.if_type_input);
                    }

                    $('.extcf7-if-field-select', condition_rule).val(and_rule.if_field_input);
                    $('.extcf7-condition-operator_input', condition_rule).val(and_rule.operator_input);
                    $('.extcf7-if-field-value', condition_rule).val(and_rule.if_value_input);
                    $('.extcf7-and-button', group_entry).before(condition_rule);
                }

                group_entries.push(group_entry);
            }

            $('#extcf7-entries').html(group_entries);
        }
    }

    function extcf7_convert_conditions_from_fields_to_array_bjects(){
    	var group_entries = $('#extcf7-entries .extcf7-entry');
    	var conditional_objects = [];
    	group_entries.each(function(){
            
    		var rule_applied_field = $(this).find('.extcf7-then-field').val() ?? '';
        
	        var conditional_object = {
	            rule_applied_field: rule_applied_field,
	            and_condition_rules: [],
	        };

            var if_type_input,
                operator_input,
                if_field_input,
                if_value_input;

	        $(this).find('.extcf7-and-rule').each(function(i){
                if_type_input  = $(this).find('.extcf7-condition-type_input').val();
                operator_input = $(this).find('.extcf7-condition-operator_input').val();
                if_field_input = $(this).find('.extcf7-if-field-select').val();
                if_value_input = $(this).find('.extcf7-if-field-value').val();
	            conditional_object.and_condition_rules.push({
                    if_type_input  : if_type_input ?? '',
	                operator_input : operator_input ?? '',
	                if_field_input : if_field_input ?? '',
	                if_value_input : if_value_input?? '',
	            });
	        });

        	conditional_objects.push(conditional_object);
    	});

    	return conditional_objects;
    }

    function extcf7_convert_conditions_from_array_objects_to_string(conditions){
    	return conditions.map(function(condition){
	        var space =' ';
	        return `show [${condition.rule_applied_field}] if`+condition.and_condition_rules.map(function(condition_rule, i){
	            return ( i>0 ? space+condition_rule.if_type_input:'' ) + `-[${condition_rule.if_field_input}]-${condition_rule.operator_input}-"${condition_rule.if_value_input}"`
	        }).join('\n');
	    }).join('\n');
    }

    function extcf7_copy_text_to_fields(){
        var str = $('#extcf7-settings-text').val();
        var obj = extcf7_convert_conditions_from_string_to_array_of_Objects(str);
        extcf7_convert_conditions_from_array_of_objects_to_field_elements(obj);
    }

    function extcf7_copy_fields_to_text(){
    	var obj = extcf7_convert_conditions_from_fields_to_array_bjects();
	    var str = extcf7_convert_conditions_from_array_objects_to_string(obj);
	    $('#extcf7-settings-text').val(str);
    }

    function extcf7_get_number_of_entries(){
    	return $('#extcf7-entries').find('.extcf7-entry').length;
    }

    function extcf7_set_ui_mode(is_text_only,event_mode){
    	if(is_text_only){
            extcf7_current_ui_mode = 'text';
    		extcf7_ui_mode.hide();
    		extcf7_text_mode.show();
            extcf7_only_text.prop('checked', true);
    		if(extcf7_get_number_of_entries() > 0){
    			extcf7_copy_fields_to_text();
    		}else{
                if('change' == event_mode){
                    $('#extcf7-settings-text').val("");
                }
            }
    	}else{
            extcf7_current_ui_mode = 'normal';
    		extcf7_text_mode.hide();
    		extcf7_ui_mode.show();
            extcf7_only_text.prop('checked', false);
            extcf7_copy_text_to_fields();
    	}
    }

    function extcf7_conditional_mode_status(current_ui_status){
        if('text' === current_ui_status){
            extcf7_set_ui_mode(true,'reload');
        }else{
            extcf7_set_ui_mode(false,'reload'); 
        }
    }

    extcf7_conditional_mode_status( extcf7_current_ui_mode );

    extcf7_only_text.on('change',function(){
    	extcf7_set_ui_mode($(this).is(':checked'),'change');
    });

    extcf7_form_editor.on('submit', function() {
        if (extcf7_current_ui_mode == 'normal'){
            if(extcf7_get_number_of_entries() > 0){
                extcf7_copy_fields_to_text();
            }else{
               $('#extcf7-settings-text').val(""); 
            }
        }
    });

    var extcf7_auto_complete_tag = wpcf7.taggen.compose;
    wpcf7.taggen.compose = function(tagType, $form)
    {
        var tag = extcf7_auto_complete_tag.apply(this, arguments);
        if (tagType== 'fields_group') tag += "[/fields_group]";
        return tag;
    };

})(jQuery);