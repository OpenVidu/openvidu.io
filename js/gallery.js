$(document).ready(function(){

    $("[data-fancybox]").fancybox({
        infobar : true,
        arrows : false,
        loop: true,
        protect: true,
        transitionEffect: 'slide',
        buttons : [
            'close'
        ],
        clickOutside : 'close',
        clickSlide   : 'close',
    });

});