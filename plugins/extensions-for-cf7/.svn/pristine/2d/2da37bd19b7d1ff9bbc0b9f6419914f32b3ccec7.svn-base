;(function($){
"use strict";

	// Tab Menu
    function recemendation_admin_tabs( $tabmenus, $tabpane ){
        $tabmenus.on('click', 'a', function(e){
            e.preventDefault();
            var $this = $(this),
                $target = $this.attr('href');
            $this.addClass('ext-active').parent().siblings().children('a').removeClass('ext-active');
            $( $tabpane + $target ).addClass('ext-active').siblings().removeClass('ext-active');
        });
    }
    recemendation_admin_tabs( $(".recomendation-admin-tabs"), '.riecomendation-admin-tab-pane' );

})(jQuery);