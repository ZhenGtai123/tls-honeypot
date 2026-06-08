(function ($) {
    "use strict";

    if(typeof init_valid_api == 'undefined'){
        return;
    }

    mailchimp_api_response_handler(init_valid_api,true);
    mailchimp_custom_field_visible(custom_field_visible);
    $(document).on('click','#extcf7-mailchimp-activate',function(event){
        event.preventDefault();
        $.ajax({
            type: "POST",
            url: ajaxurl,
            data: {
                action : 'extcf7_mailchimp_map',
                mcmp_idform : $("#malichimp-formid").val(),
                mcmpapi: $("#extcf7-mailchimp-api-key").val(),
                ajax_nonce: extcf7_mailchimp_map_data.nonce,
            },

            beforeSend: function() {
                $(".extcf7-mailchimp-pannel-wraper .spinner").css('visibility', 'visible');
            },

            success: function(response){
                var chimp_html = JSON.parse(response);
                $(".extcf7-mailchimp-pannel-wraper .spinner").css('visibility', 'hidden');
                $("#extcf7-listmail").html(chimp_html.list_mail);
                $("#extcf7-mailchimp-field").html(chimp_html.map_fields);
                var validapi = $("#valid-api").val();
                mailchimp_api_response_handler(validapi,false);
            },
        });
    });

    $(document).on('click','#extcf7-add-custom-field',function(event){
        event.preventDefault();
        var custom_field = $(".extcf7-custom-fields").find('.extcf7-mailchimp-custom-fields')[0];
        var custome_field_saved = custom_field.dataset.mcmp_csmfield;
        if('yes' === custome_field_saved){
            $(".extcf7-custom-button-align").before('<div class="extcf7-mailchimp-custom-fields">'+custom_field.innerHTML+'</div>');
        }else{
            $(".extcf7-custom-button-align").before('<div class="extcf7-mailchimp-custom-fields">'+custom_field.innerHTML+'<button id="extcf7-custom-field-delete" class="button">remove</button></div>');
        }
    });

    $(document).on('click','#extcf7-custom-field-delete',function(event){
        event.preventDefault();
        $(this).parent().remove();
    });

    function mailchimp_api_response_handler( valid_api, window_loading ){
        if(valid_api == '1'){

            $(".extcf7-mailchimp-activate-btn").css('visibility', 'visible')
                                               .removeClass("key-invalid")
                                               .addClass("key-valid");
            $(".extcf7-mailchimp-activate-btn #extcf7-mailchimp-activate").val("Connected")
                                                                          .prop('disabled', true);
            $(".dashicons").removeClass("dashicons-no")
                           .addClass("dashicons-yes");

            $(".invalid-api-message").css('display','none');

            $(".extcf7-mailchimp-activated").removeClass("extcf7-mailchimp-inactive")
                                            .addClass("extcf7-mailchimp-active");

        }else{

            $(".extcf7-mailchimp-activate-btn").css('visibility', 'visible')
                                               .removeClass("key-valid")
                                               .addClass("key-invalid");

            $(".extcf7-mailchimp-activate-btn #extcf7-mailchimp-activate").val("Try Again");

            $(".dashicons").removeClass("dashicons-yes")
                           .addClass("dashicons-no");

            if(window_loading === false){
                $(".invalid-api-message").css('display','block');
            }else{
                mailchimp_connect_btn_reset();
            }

            $(".extcf7-mailchimp-activated").removeClass("extcf7-mailchimp-active")
                                            .addClass("extcf7-mailchimp-inactive");
        }
    }

    $('div.extcf7-tooltip-item').mouseenter(function() {
       $(this).children("div.tooltip").css({'display':'block'}); 
    }).mouseleave(function() {
       $(this).children("div.tooltip").animate({"opacity": "hide"}, "fast");
    });

    $("#extcf7-mailchimp-custom-field").on('change', function(){
        if ($(this).prop('checked')==true){ 
            mailchimp_custom_field_visible('1');
        }else{
           mailchimp_custom_field_visible('0'); 
        }
    });

    function mailchimp_custom_field_visible(state){
        if('1' == state){
            $(".extcf7-chimp-customfield").slideDown();
        }else{
            $(".extcf7-chimp-customfield").slideUp();
        }
    }

    $("#extcf7-mailchimp-api-key").on('keyup',function(){
        mailchimp_connect_btn_reset();
    });

    function mailchimp_connect_btn_reset(){

        $(".extcf7-mailchimp-activate-btn #extcf7-mailchimp-activate").prop('disabled', false);

        $(".extcf7-mailchimp-activate-btn").removeClass("key-valid")
                                           .removeClass("key-invalid");

        $(".extcf7-mailchimp-activate-btn #extcf7-mailchimp-activate").val("Connect With MailChimp");

        $(".dashicons").removeClass("dashicons-yes")
                       .removeClass("dashicons-no");  

    }

})(jQuery);