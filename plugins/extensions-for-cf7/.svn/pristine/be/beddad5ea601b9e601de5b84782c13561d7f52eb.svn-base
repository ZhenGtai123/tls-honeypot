(function ($) {
	"use strict";

	var extcf7_animaion_enable = extcf7_animation_info.animitation_status;
	
	extcf7_animation_status(extcf7_animaion_enable);

    // Settings panel
    $(document).ready(function(){

        // Define a function to initialize datepicker
        function initializeDatepicker() {
            if ($("#form-data").length > 0) {
                $("#form-data, #to-date").datepicker({
                    dateFormat : 'yy-mm-dd'
                });
            }
        }

        // Call initializeDatepicker() when a navigation menu item is clicked
        $("body").on('click', '.htcf7ext-navigation-menu li a', function(e) {
            initializeDatepicker();
        });

        // Initialize datepicker for #form-data and #to-date
        initializeDatepicker();

        // Event handler for #form-data
        $("body").on('click', '#form-data', function(e) {
            $(this).datepicker({
                dateFormat : 'yy-mm-dd'
            });
        });

        // Event handler for #to-date
        $("body").on('click', '#to-date', function(e) {
            
            $(this).datepicker({
                dateFormat : 'yy-mm-dd'
            });
        });
        

        $("body").on('click','.contact_forms .view a', function(e) {
            e.preventDefault();
            const $this = $(this);
            let params = new URLSearchParams($this.attr('href'));
            let entry_id = parseInt(params.get('cf7em_id'));
            let form_id = parseInt(params.get('cf7_id'));

            const $modalFrame = $(`
                <div class="htcf7ext-modal">
                    <div class="htcf7ext-modal-content">
                        <span class="htcf7ext-modal-close">&times;</span>
                        <div class="htcf7ext-modal-content-inner"></div>
                    </div>
                </div>
            `);
                
            $.ajax({
                url: htcf7ext_params.ajax_url,
                type: 'POST',
                data: {
                    'action': 'htcf7ext_view_formdata',
                    'entry_id': entry_id,
                    'form_id': form_id,
                    'nonce' : htcf7ext_params.nonce
                },
        
                beforeSend:function(){
                    trigger_modal($modalFrame, 'Loading...');
                },
        
                success:function(response) {
                    trigger_modal($modalFrame, $(response.data.html));
                    $this.closest('td').find('.status').addClass('read').removeClass('unread').html('read');
                    if(response.data.total !== '0') {
                        $('#toplevel_page_contat-form-list .awaiting-mod .pending-count').html(response.data.total);
                        $('#toplevel_page_contat-form-list .awaiting-mod .screen-reader-text').html(response.data.total + ' ' + response.data.message);
                    } else {
                        $('#toplevel_page_contat-form-list .awaiting-mod').remove()
                    }
                },
        
                complete:function( response ){
                    
                },
        
                error: function(errorThrown){
                    console.log(errorThrown);
                }
            });
        });
    });

    function trigger_modal( $modal = '', $content = '' ){

        // Check if alreay a modal is open
        if( $('body').find('.htcf7ext-modal').length ){
            $modal = $('body').find('.htcf7ext-modal');
        }
        
        if($content){
            $modal.find('.htcf7ext-modal-content-inner').html($content)
        }
        
        $('body').append($modal);

        // Get the <span> element that closes the modal
        let $close = $modal.find('.htcf7ext-modal-close');

        // open the modal 
        $modal.addClass('open');

        // When the user clicks on (x), close the modal
        $close.on('click', () => {
            $modal.removeClass('open');
        });

        // When the user clicks anywhere outside of the modal, close it
        $(window).on('click', (e) => {
            if ($(e.target).hasClass('htcf7ext-modal')) {
                $modal.removeClass('open');
            }
        });
    }

	$('#extcf7-animation-enable').on('change',function(){
		extcf7_animation_enable($(this).prop("checked"));
	});

	function extcf7_animation_status(animation_status){
        if('on' == animation_status){
            extcf7_animation_enable(true);   
        }else{
            extcf7_animation_enable(false);
        }
    }

    function extcf7_animation_enable(animation_enable){
        if(true == animation_enable){
            $('.extcf7-animation-time').show();
        }else{
            $('.extcf7-animation-time').hide();
        }
    }

})(jQuery);
