// main function
var _iub = _iub || [];


function circularBar(el) {
    el.innerHTML = `
  <svg xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 32 32" >
  <circle class="circle1" cy="16" cx="16" r="13" />
  <circle class="circle2" cy="16" cx="16" r="13" />
  </svg>
  <span></span>
  `;

    var perc = parseInt(el.dataset.perc);
    var circle = el.querySelector('.circle2');
    var color = '#CF7463';

    el.querySelector('span').innerHTML = perc + '<b>%</b>';

    if (perc >= 50)
        color = '#F5B350';
    if (perc > 80)
        color = '#1CC691';

    var strokeDashArray = parseInt(getComputedStyle(circle, null).getPropertyValue("stroke-dasharray"));
    var strokeDashOffset = strokeDashArray - ((strokeDashArray * perc) / 100);

    circle.style.strokeDashoffset = strokeDashOffset;
    el.style.color = color;

}
document.addEventListener("DOMContentLoaded", function () {
    // search all .circularBar and initialize them
    document.querySelectorAll(".circularBar").forEach(function (el) {
        circularBar(el);
    });
});

;(function (global, $) {
    //es5 strict mode
    "use strict";

    var IUB = global.IUB = global.IUB || {};

    $(document).ready(function () {
        IUB.ELEMS = {body: $('body')};
        IUB.ELEMS.body.on('click', '.show-modal', showModal);
        IUB.ELEMS.body.on('click', '.show-rating-modal', showRatingModal);
        IUB.ELEMS.body.on('click', '.hide-modal', hideModal);
        IUB.ELEMS.body.on('click', hideAllModals);
        IUB.ELEMS.body.on('click', '.section-checkbox-control', sectionCheckboxShowAndHide);
        IUB.ELEMS.body.on('click', '.section-radio-control', sectionRadioControl);
        IUB.ELEMS.body.on('click', '.active-class-control', activeClassControl);
        IUB.ELEMS.body.on('click', '.show-class-control', showClassControl);
        IUB.ELEMS.body.on('submit', '.ajax-form', submitAjaxForm);
        IUB.ELEMS.body.on('submit', '.ajax-form-to-options', submitAjaxFormToOptions);
        IUB.ELEMS.body.on('click', '.service-checkbox', toggleServiceSetting);
        IUB.ELEMS.body.on('click', '#alert-close', hideAlertDiv);
        IUB.ELEMS.body.on('click', '#public_api_button', savePublicApiKey);
        IUB.ELEMS.body.on('click', '.auto-detect-forms', reloadAutoDetectForms);
        IUB.ELEMS.body.on('click', '.add-custom-section', addCustomSection);
        IUB.ELEMS.body.on('click', '.remove-custom-section', removeCustomSection);
        IUB.ELEMS.body.on('click', '.required-control', requiredControl);
        IUB.ELEMS.body.on('click', '.update-button-style', updateButtonStyle);
        IUB.ELEMS.body.on('change keyup past', '.iub-embed-code-tc', syncEmbedCode);
        IUB.ELEMS.body.on('change click', '.iub-toggle-elements-status', toggleCheckboxes);
    });

    function showModal(evt) {
        $(".modal").removeClass('shown');
        var elId = $(evt.target).data('modal-name');
        $(elId).addClass('shown');
    }

    function showRatingModal() {
        $('#modal-rating').addClass('shown')
    }

    function hideModal(evt) {
        var elId = $(evt.target).data('modal-name');
        $(elId).removeClass('shown');
    }

    function hideAllModals(evt) {
        if (
            !evt.target.matches(".show-modal") &&
            !evt.target.closest(".modal__window") &&
            !evt.target.closest(".show-rating-modal")
        ) {
            $(".modal").removeClass('shown');
        }
    }

    function sectionCheckboxShowAndHide(evt) {
        if ($(evt.target).is(':checked')) {
            $($(evt.target).data('section-name')).show();
        } else {
            $($(evt.target).data('section-name')).hide();
        }
    }

    function sectionRadioControl(evt) {
        if ($(evt.target).is(':checked')) {
            $($(evt.target).data('section-group')).hide();
            $($(evt.target).data('section-name')).show();
        }
    }

    function activeClassControl(evt) {
        $($(evt.target).data('element-name')).removeClass('inactive');
    }

    function showClassControl(evt) {
        $($(evt.target).data('section-name')).show();
    }


    function submitAjaxForm(evt){
        evt.stopImmediatePropagation();
        evt.preventDefault();

        var formData= $($(evt.target)).serialize();
        var formButton= $($(evt.target)).find('button[type=submit]');

        var redirect= $($(evt.target)).find('input[name="_redirect"]').val();
        var showModal= $($(evt.target)).find('input[name="show_modal"]').val();

        $.ajax({
            type: "POST",
            dataType: "json",
            url: iub_js_vars['site_url'] + "/wp-admin/admin-ajax.php",
            data : formData,
            beforeSend: function() {
                formButton.addClass("btn-loading");
                formButton.prop('disabled', true);
            },
            success: function(response){
                formButton.removeClass("btn-loading");
                formButton.prop('disabled', false);
                if (response.status === 'done') {
                    if(typeof(showModal) != "undefined" && showModal !== null) {
                        $(".modal").removeClass('shown');
                        $(showModal).addClass('shown');
                    } else {
                        window.location = redirect
                    }
                }else{
                    if(response.focus && $(response.focus).length){
                        $(response.focus).trigger('click');
                        $([document.documentElement, document.body]).animate({
                            scrollTop: $(response.focus).offset().top
                        }, 500);
                    }
                    _paq.push(['trackEvent', 'Error', 'No website found with this embed code.']);
                    $('#modal-no-website-found').addClass('shown')
                }
            },
            error: function(response) { // if error occured

                $("#alert-div").addClass("alert--failure");
                $("#alert-image").attr('src',iub_js_vars['plugin_url'] + '/assets/images/banner_failure.svg');
                $("#alert-message").text(response.responseText);


                $("#alert-div").removeClass("hidden");
                formButton.removeClass("btn-loading");
                formButton.prop('disabled', false);
            },
            complete: function() {
                formButton.removeClass("btn-loading");
                formButton.prop('disabled', false);
            },

        });
        return false;
    }

    function submitAjaxFormToOptions(evt){
        evt.preventDefault();
        var formData= $($(evt.target)).serialize();
        var formButton= $($(evt.target)).find('button[type=submit]');

        var redirect= $($(evt.target)).find('input[name="_redirect"]').val();

        $.ajax({
            type: "POST",
            dataType: "json",
            url: iub_js_vars['site_url'] + "/wp-admin/admin-ajax.php",
            data : formData,
            beforeSend: function() {
                formButton.addClass("btn-loading");
                formButton.prop('disabled', true);
            },
            success: function(response){
                formButton.removeClass("btn-loading");
                formButton.prop('disabled', false);
                if (response.status === 'done') {
                    window.location = redirect
                }else{
                    if(response.focus){
                        $(response.focus).trigger('click');
                        $([document.documentElement, document.body]).animate({
                            scrollTop: $(response.focus).offset().top
                        }, 500);
                    }
                    _paq.push(['trackEvent', 'Error', 'No website found with this embed code.']);
                    $('#modal-no-website-found').addClass('shown')
                }
            },
            error: function(response) { // if error occured

                console.log(response.responseText)
                $("#alert-div").addClass("alert--failure");
                $("#alert-image").attr('src',iub_js_vars['plugin_url'] + '/assets/images/banner_failure.svg');
                $("#alert-message").text(response.responseText);


                $("#alert-div").removeClass("hidden");
                formButton.removeClass("btn-loading");
                formButton.prop('disabled', false);
            },
            complete: function() {
                formButton.removeClass("btn-loading");
                formButton.prop('disabled', false);
            },

        });
        return false;
    }

    function toggleServiceSetting(evt){
        const serviceName = $(evt.target).data('service-name')
        const serviceKey = $(evt.target).data('service-key')
        const status = $(evt.target).is(":checked")
        if(status === true){
            evt.stopImmediatePropagation();
            evt.preventDefault();
            window.location = $(evt.target).data('redirect')
            return
        }
        jQuery.ajax({
            type: "post",
            dataType: "json",
            url: iub_js_vars['site_url'] + "/wp-admin/admin-ajax.php",
            data : {action: "toggle_services", name: serviceName, status: status},
            success: function(response){
                if (response.status === 'done') {
                    $('.'+serviceKey+'-item').removeClass("list_radar__item--on").addClass("list_radar__item--off");
                    $('#configiration-'+serviceKey).toggle();

                    // Update service status label
                    let service_status_label = $('#'+serviceKey+'-status-label');
                    if(service_status_label != undefined){
                        service_status_label.html(service_status_label.data('status-label-off'));
                    }

                    // Update rating circular bar if rating percentage is not equal undefined
                    if(response.rating_percentage != undefined){
                        document.querySelectorAll(".circularBar").forEach(function (el) {
                            $(el).attr('data-perc', response.rating_percentage);
                            circularBar(el);
                        });
                    }
                }
            },
            error: function (jqXHR, exception) {
                var msg = '';
                if (jqXHR.status === 0) {
                    msg = 'Not connect.\n Verify Network.';
                } else if (jqXHR.status == 404) {
                    msg = 'Requested page not found. [404]';
                } else if (jqXHR.status == 500) {
                    msg = 'Internal Server Error [500].';
                } else if (exception === 'parsererror') {
                    msg = 'Requested JSON parse failed.';
                } else if (exception === 'timeout') {
                    msg = 'Time out error.';
                } else if (exception === 'abort') {
                    msg = 'Ajax request aborted.';
                } else {
                    msg = 'Uncaught Error.\n' + jqXHR.responseText;
                }
                console.log(msg);
            },
        });
    }

    function hideAlertDiv(evt){
        $(evt.target).parents('#alert-div').fadeOut();
    }

    function savePublicApiKey(evt){
        evt.preventDefault();
        document.querySelector('#public_api_key').reportValidity();
        var public_api_key = $('#public_api_key').val();

        var formButton= $('#public_api_button');

        $.ajax({
            type: "post",
            dataType: "json",
            url: iub_js_vars['site_url'] + "/wp-admin/admin-ajax.php",
            data : {action: "save_public_api_key", public_api_key: public_api_key},
            beforeSend: function() {
                formButton.addClass("btn-loading");
                formButton.prop('disabled', true);
            },
            success: function(response){
                formButton.removeClass("btn-loading");
                formButton.prop('disabled', false);
                if (response.status === 'done') {
                    $.ajax({
                        type: "post",
                        url: iub_js_vars['site_url'] + "/wp-admin/admin-ajax.php",
                        data : {action: "auto_detect_forms", public_api_key: public_api_key},
                        success: function(response) {
                            $("#auto-detect-forms").html(response);
                            $("#public-api-key-div").show();
                        },
                    });

                }else{
                    _paq.push(['trackEvent', 'Error', 'No website found with this embed code.']);
                    $('#modal-no-website-found').addClass('shown')
                }
            },
            error: function (jqXHR, exception) {
                var msg = '';
                if (jqXHR.status === 0) {
                    msg = 'Not connect.\n Verify Network.';
                } else if (jqXHR.status == 404) {
                    msg = 'Requested page not found. [404]';
                } else if (jqXHR.status == 500) {
                    msg = 'Internal Server Error [500].';
                } else if (exception === 'parsererror') {
                    msg = 'Requested JSON parse failed.';
                } else if (exception === 'timeout') {
                    msg = 'Time out error.';
                } else if (exception === 'abort') {
                    msg = 'Ajax request aborted.';
                } else {
                    msg = 'Uncaught Error.\n' + jqXHR.responseText;
                }
                console.log(msg);
            },
        });
    }


    function reloadAutoDetectForms(evt){
        evt.preventDefault();
        var auto_detect_forms = $("#auto-detect-forms")
        var auto_detect_parent_div = $("#auto-detect-parent-div")
        auto_detect_parent_div.addClass("loader");
        auto_detect_forms.css('visibility', 'hidden');


        var public_api_key = $('input[name="public_api_key"]').val();

        $.ajax({
            type: "post",
            url: iub_js_vars['site_url'] + "/wp-admin/admin-ajax.php",
            data : {action: "auto_detect_forms", public_api_key: public_api_key},
            success: function(result) {
                auto_detect_parent_div.removeClass("loader");
                $("#auto-detect-forms").html(result);
                $("#auto-detect-forms").css('visibility', 'visible');
            },
            error: function (jqXHR, exception) {
                var msg = '';
                if (jqXHR.status === 0) {
                    msg = 'Not connect.\n Verify Network.';
                } else if (jqXHR.status == 404) {
                    msg = 'Requested page not found. [404]';
                } else if (jqXHR.status == 500) {
                    msg = 'Internal Server Error [500].';
                } else if (exception === 'parsererror') {
                    msg = 'Requested JSON parse failed.';
                } else if (exception === 'timeout') {
                    msg = 'Time out error.';
                } else if (exception === 'abort') {
                    msg = 'Ajax request aborted.';
                } else {
                    msg = 'Uncaught Error.\n' + jqXHR.responseText;
                }
                console.log(msg);
            },
        });
    }

    function addCustomSection(evt){
        evt.preventDefault();
        const append_section = $($(evt.target).data('append-section'));
        const cloned_section = $($(evt.target).data('clone-section'));

        cloned_section.clone().each(function(){
            this.id = Math.random(); // to keep it unique
            $(this).find('input, textarea, button, select').prop('disabled', false);
        }).appendTo(append_section).hide().fadeIn(300);
    }

    function removeCustomSection(evt){
        evt.preventDefault();
        $($(evt.target)).closest($(evt.target).data('remove-section')).remove();
        $("#parent-selector :input").attr("disabled", true);
    }

    function requiredControl(evt){
        if ($(evt.target).is(':checked')) {
            $($(evt.target).data('required-control')).show();
        } else {
            $($(evt.target).data('required-control')).hide();
        }
    }

    function updateButtonStyle(evt){
        $('.iub-pp-code, .iub-tc-code').each(function() {
            var text = $(this).html();
            $(this).html(text.replace('white', $(evt.target).val()).replace('black', $(evt.target).val()));
        });
        $('.iub-language-code').each(function() {
            var text = $(this).val();
            $(this).val(text.replace('white', $(evt.target).val()).replace('black', $(evt.target).val()));
        });
    }

    // Sync embed code between TC live code and Readonly code
    function syncEmbedCode(evt){
        var ele = $($(evt.target));

        if($('#iub-tc-code-'+ele.data('language')).length > 0){
            $('#iub-tc-code-'+ele.data('language')).text(ele.val())
            $('#iub-embed-code-readonly-'+ele.data('language')).trigger('click')
        }
    }

    // Toggle elements status
    function toggleCheckboxes(evt){
        $($($(evt.target)).data('group')).each(function() {
            // Prevent uncheck if they already checked
            if($(evt.target).is(':checked')){
                $(this).prop('checked', $(evt.target).is(':checked'));
            }
            $(this).attr('disabled', $(evt.target).is(':checked'));
        });
    }

    // Start banner position script
    $( document ).on( 'click', '.position-select > div > label', function ( e ) {
        if (!$(this).closest('.position-select > div').hasClass('open')) {
            $(this).closest('.position-select > div').addClass('open');
        }
    })

    $(document).on('mousedown', function (e) {
        var positionDropdown = $('.position-select > div.open');

        if (positionDropdown.length &&
            !positionDropdown.is(e.target) &&
            positionDropdown.has(e.target).length === 0 &&
            $('.pcr-app').has(e.target).length === 0
        ) {
            positionDropdown.removeClass('open');
        }
    });
    // End banner position script

    // Preferences fields
    // Add new preferences field
    $( document ).on( 'click', '.add-preferences-field', function ( e ) {
        e.preventDefault();

        $( '#postbox-container-2' ).change();

        var html = $( '#preferences-field-template' ).html();
        html = html.replace( /__PREFERENCE_ID__/g, $( '.preferences-field' ).length++ );

        $( '.preferences-table .add-preferences-field' ).closest( 'tr' ).before( '<tr class="preferences-field options-field" style="display: none;">' + html + '</tr>' );

        var last = $( '.preferences-field' ).last();

        last.find('.preferences-inputs').prop('disabled',false)
        last.fadeIn( 300 );
    } );

    // Remove preferences field
    $( document ).on( 'click', '.remove-preferences-field', function ( e ) {
        e.preventDefault();

        $( '#postbox-container-2' ).change();

        $( this ).closest( '.preferences-field' ).fadeOut( 300, function () {
            $( this ).remove();
        } );
    } );

    // Exclude fields
    var excludeID = $( '.exclude-field' ).length;

    // Add new preferences field
    $( document ).on( 'click', '.add-exclude-field', function ( e ) {
        e.preventDefault();

        $( '#postbox-container-2' ).change();

        var html = $( '#exclude-field-template' ).html();
        html = html.replace( /__EXCLUDE_ID__/g, excludeID++ ).replace( 'disabled', '' );

        $( '.exclude-table .add-exclude-field' ).closest( 'tr' ).before( '<tr class="exclude-field options-field" style="display: none;">' + html + '</tr>' );

        var last = $( '.exclude-field' ).last();

        last.fadeIn( 300 );
    } );

    // Remove exclude field
    $( document ).on( 'click', '.remove-exclude-field', function ( e ) {
        e.preventDefault();

        $( '#postbox-container-2' ).change();

        $( this ).closest( '.exclude-field' ).fadeOut( 300, function () {
            $( this ).remove();
        } );
    } );

    $( function () {
        $('.cs-configuration-type').on('change', function() {
            if($("input[name='iubenda_cookie_law_solution[configuration_type]']:checked").val() == 'simplified'){
                $('.iub-language-code').attr("disabled", true)
            } else {
                $('.iub-language-code').attr("disabled", false)
            }
        }).trigger('change');

    } );

    // Legal notices fields
    var legalNoticesID = $( '.legal_notices-field' ).length;

    // Add new preferences field
    $( document ).on( 'click', '.add-legal_notices-field', function ( e ) {
        e.preventDefault();

        $( '#postbox-container-2' ).change();

        var html = $( '#legal_notices-field-template' ).html();
        html = html.replace( /__LEGAL_NOTICE_ID__/g, legalNoticesID++ );

        console.log( html );

        $( '.legal_notices-table .add-legal_notices-field' ).closest( 'tr' ).before( '<tr class="legal_notices-field options-field" style="display: none;">' + html + '</tr>' );

        var last = $( '.legal_notices-field' ).last();

        last.find('.legal-notices-inputs').prop('disabled',false)
        last.fadeIn( 300 );
    } );

    // Remove legal notices field
    $( document ).on( 'click', '.remove-legal_notices-field', function ( e ) {
        e.preventDefault();

        $( '#postbox-container-2' ).change();

        $( this ).closest( '.legal_notices-field' ).fadeOut( 300, function () {
            $( this ).remove();
        } );
    } );

    // Handle form fields data
    $( document ).on( 'change', '#postbox-container-2', function() {
        var fields = {},
            fieldsTypes = [ 'subject', 'preferences', 'exclude' ];

        if ( iub_js_vars['form_id'] > 0 ) {
            // get all fields
            fields.all = $( '.subject-fields-select.select-id option:not([value=""])' ).map( function() { return $( this ).val(); } ).get();

            // get specific fields
            $.each( fieldsTypes, function( index, fieldType ) {
                fields[fieldType] = [];

                var fieldItems = $( '.' + fieldType + '-field select' );

                // get selected values
                $.each( fieldItems, function( index, item ) {
                    if ( $( item ).val() != '' )
                        fields[fieldType].push( $( item ).val() );
                } );

                fields.fieldType = $.unique( fields[fieldType] );

                // remove available fields if needed
                if ( fields[fieldType].length > 0 ) {

                    // get options count
                    var templateItemsCount = $( '.template-field .' + fieldType + '-fields-select option:disabled' ).length;

                    // update if options count changed
                    if ( templateItemsCount !== 0 && fields[fieldType].length != templateItemsCount ) {
                        // console.log( fields[fieldType] );
                    }

                    // disable add button if needed
                    if ( fields.all.length == fields[fieldType].length ) {
                        $( '.add-' + fieldType + '-field' ).attr( 'disabled', 'disabled' );
                    } else {
                        $( '.add-' + fieldType + '-field' ).attr( 'disabled', false );
                    }

                    // adjust disabled options
                    $.each( fields.all, function( index, fieldName ) {
                        if ( $.inArray( fieldName, fields[fieldType] ) < 0 ) {
                            // options field
                            $( '.' + fieldType + '-fields-select option:not(:checked)[value="' + fieldName + '"]' ).attr( 'disabled', false );
                            // template field
                            $( '.template-field .' + fieldType + '-fields-select option[value="' + fieldName + '"]' ).attr( 'disabled', false );
                        } else {
                            $( '.' + fieldType + '-fields-select option:not(:checked)[value="' + fieldName + '"]' ).attr( 'disabled', 'disabled' );
                            $( '.template-field .' + fieldType + '-fields-select option[value="' + fieldName + '"]' ).attr( 'disabled', 'disabled' );
                        }
                    } );
                }
            } );

            // console.log( fields );
        }

    } );

    // Force trigger change on document ready
    $( function() {
        $( '#postbox-container-2' ).change();
    } );

    $( document ).on( 'mouseenter mouseleave', '#postbox-container-2 .options-field, #postbox-container-2 .submit-field', function() {
        $( '#postbox-container-2' ).change();
    } );

    // Update _iub.quick_generator selected language
    $(function($) {
        $('#iub-website-language').on('change', function() {
            try {
                _iub.quick_generator.input.privacy_policy.langs = [$(this).val()]
            }
            catch(err) {
                console.log(err)
            }
        }).trigger('change');
    });

    $( document ).on( 'click', '.notice-dismiss, .notice-dismiss-by-text', function ( e ) {
        e.preventDefault();
        $(this).closest('div.is-dismissible').slideUp();
    });

    $( document ).on( 'click', '.dismiss-notification-alert', function ( e ) {
        $.ajax({
            type: "post",
            dataType: "json",
            url: iub_js_vars['site_url'] + "/wp-admin/admin-ajax.php",
            data : {
                action: "iubenda_dismiss_notification_alert",
                iubenda_nonce: iub_js_vars['iub_dismiss_notification_alert_nonce'],
                dismiss_key: $(e.target).data('dismiss-key')
            },

        })
    });
}(window, jQuery));

jQuery(document).ready(function($){
    let activeRequest = false;
    let completed = false;
    setTimeout(ajax, 10);

    function ajax(){
        if((activeRequest) || (iub_js_vars['radar_status'] == 'completed'))
        {
            return;
        }
        activeRequest = true;
        jQuery.ajax({
            type: "post",
            dataType: "json",
            url: iub_js_vars['site_url'] + "/wp-admin/admin-ajax.php",
            data : {action: "radar_percentage_reload"},
            success: function(result){
                if (result.status === 'timeout'){
                    activeRequest = false;
                    setTimeout(ajax, (parseInt(result.data) * 1000));
                    return
                }

                if (result.status === 'progress'){
                    activeRequest = false;
                    completed = true;
                    setTimeout(ajax, 10000);
                    return
                }

                if (result.status === 'error'){
                    $("#alert-div").addClass("alert--failure");
                    $("#alert-image").attr('src',iub_js_vars['plugin_url'] + '/assets/images/banner_failure.svg');
                    $("#alert-message").html(result.message);
                    $("#alert-div-container").fadeIn( 300 );
                }

                if (result.status === 'complete' && completed){
                    if($('#frontpage-main-box').length){
                        $.ajax({
                            type: "post",
                            url: iub_js_vars['site_url'] + "/wp-admin/admin-ajax.php",
                            data : {action: "frontpage_main_box"},
                            success: function(response) {
                                _paq.push(['trackEvent', 'Event', 'End of scan and report rating']);
                                $('#frontpage-main-box').html(response)
                                document.querySelectorAll(".circularBar").forEach(function (el) {
                                    $(el).attr('data-perc', result.data.percentage);
                                    circularBar(el);
                                });
                            },
                        });
                    }
                }
            }
        })
        setTimeout(ajax, 10000);
    }
});
