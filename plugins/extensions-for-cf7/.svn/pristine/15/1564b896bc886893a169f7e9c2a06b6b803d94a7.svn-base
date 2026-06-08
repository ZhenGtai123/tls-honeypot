;(function ($) {
    'use strict';
	$(document).on( 'click', '.extcf7-column-select', function(e){
        e.preventDefault();
        const form = document.getElementById("wpcf7-form"),
            curPos = form.selectionStart,
            formData = form.value,
            code = this?.dataset?.code;
        form.value = formData.slice(0, curPos) + code + formData.slice(curPos);
        const newPos = curPos + code.length;
        form.setSelectionRange(newPos, newPos);
        form.focus();
        tb_remove();
	});
})(jQuery);