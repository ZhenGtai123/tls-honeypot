(function ($) {
    "use strict";

    if(typeof extcf7_redirect_settings == 'undefined'){
        return;
    }

    if(extcf7_redirect_settings){
        var extcf7_redirect_fields_enable = extcf7_redirect_settings.redirection_enable ?? 'off';
        var extcf7_redirection_url_show   = extcf7_redirect_settings.custom_url_enable ?? 'off';
        var extcf7_javascript_fire_show   = extcf7_redirect_settings.js_action ?? 'off';
    }

    //Redirect field show/hide
    extcf7_redirect_field_status(extcf7_redirect_fields_enable);
    $('#extcf7-redirection-enable').on('change',function(){
    	extcf7_redirect_field_show($(this).prop("checked"));
    });

    function extcf7_redirect_field_status(field_status){
    	if('on' == field_status){
    		extcf7_redirect_field_show(true);
    	}else{
    		extcf7_redirect_field_show(false);	
    	}
    }

    function extcf7_redirect_field_show(field_show){
    	if(true == field_show){
    		$('.extcf7-redirect-fields').show();
    		extcf7_redirect_fields_enable = 'on';
    		extcf7_redirection_url_status(extcf7_redirection_url_show);
    	}else{
    		$('.extcf7-redirect-fields').hide();
    		extcf7_redirect_fields_enable = 'off';
    		extcf7_redirection_url_status(extcf7_redirection_url_show);
    	}
    }

    //Custom paeg url field show/hide 
    extcf7_redirection_url_status(extcf7_redirection_url_show);
    $('#extcf7-custom-url-enable').on('change',function(){
    	extcf7_redirection_url_enable($(this).prop("checked"));
    });

    function extcf7_redirection_url_status(url_status){
    	if('on' == extcf7_redirect_fields_enable){
	    	if('on' == url_status){
	    		extcf7_redirection_url_enable(true);
	    	}else{
	    		extcf7_redirection_url_enable(false);
	    	}
    	}
    }

    function extcf7_redirection_url_enable(custom_url){
    	if(true == custom_url){
    		$('.extcf7-custom-page-url').show();
            $('.extcf7-page-url').hide();
        }else{
        	 $('.extcf7-page-url').show();
        	$('.extcf7-custom-page-url').hide();
        }
    }

    //javascript acrion feild show/hide
    extcf7_javascript_fire_status(extcf7_javascript_fire_show);
    $('#extcf7-js-acction').on('change',function(){
    	extcf7_javascript_fire_enable($(this).prop("checked"));
    });

	function extcf7_javascript_fire_status(js_fire_status){
		if('on' == js_fire_status){
			extcf7_javascript_fire_enable(true);
		}else{
			extcf7_javascript_fire_enable(false);
		}
	}    

    function extcf7_javascript_fire_enable(js_action){
    	if(true == js_action){
    		$('.extcf7-js-code').show();
    	}else{
    		$('.extcf7-js-code').hide();
    	}
    }

})(jQuery);