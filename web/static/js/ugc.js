function ugc() {
}

ugc.navSelector = function (element) {
    $('.header > nav > ul > li.active').removeClass('active');
    $(element).addClass('active');
};

ugc.alert = function (element, message) {
    var alert = $(element).parent().find('.alert');
    alert.show();
    alert.find('p').html(message.responseText);
};