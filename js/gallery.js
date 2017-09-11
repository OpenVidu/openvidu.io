$(document).ready(function(){

    $("[data-fancybox]").fancybox({
        infobar : true,
        arrows : false,
        loop: true,
        buttons : [
            'close'
        ],
        clickOutside : 'close',
        clickSlide   : 'close',
        touch : {
			vertical : false
		}
    });

});