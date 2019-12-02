$(function () {
    jQuery.each($('[data-load]'), function () {
        // this refers to the element
        $(this).load("/pages/" + $(this).data("load"))
    })
})

$(function () {
    $(document).scroll(function () {
        // toggle if greater than height of screen
        $(".navbar").toggleClass('navbar-dark bg-dark see-through transition', $(window).scrollTop() > $(window).height() * .8);
    });
});