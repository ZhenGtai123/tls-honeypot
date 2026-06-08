(function ($) {
	"use strict";

    $('.wpcf7-extcf7_range_slider').each(function() {
        const type = this?.dataset?.type,
            value = this?.dataset?.default,
            min = this?.dataset?.min,
            max = this?.dataset?.max,
            step = this?.dataset?.step;
        const params = {};
        if (type === "double") {
            params.range = true;
            params.values = value?.includes(',') ? value?.split(',')?.map(Number) : [+value, max];
        } else {
            params.value = +value;
        }
        if (min) { params.min = +min; }
        if (max) { params.max = +max; }
        if (step) { params.step = +step; }

        const amountContainer = $(this).closest('.wpcf7-extcf7-range-slider').find('.wpcf7-extcf7-range-slider-amount');
        if(amountContainer && params.values) { amountContainer.html(params.values.join(' - ')) }
        if(amountContainer && params.value) { amountContainer.html(params.value) }
        
        $( this.parentElement ).slider({
            ...params,
            slide: function( event, ui ) {
                if(ui?.values) {
                    $(event?.target).find('input.wpcf7-extcf7_range_slider').val( ui.values );
                    if(amountContainer) {amountContainer.html(ui.values.join(' - '))}
                } else {
                    $(event?.target).find('input.wpcf7-extcf7_range_slider').val( ui.value );
                    if(amountContainer) {amountContainer.html(ui.value)}
                }
            }
        });
    });
})(jQuery);