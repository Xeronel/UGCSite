function ugc() {
}

ugc.navSelector = function (element) {
    $('.header > nav > ul > li.active').removeClass('active');
    var e = $(element);
    if (e) {
        e.addClass('active');
    }
};

ugc.alert = function (element, message, type) {
    var alert = $(element).parent().find('.alert');
    alert.removeClass(function (idx, cls) {
        return (cls.match(/alert-(?!dismissible).+/) || []).join(' ');
    });
    alert.addClass('alert' + '-' + type);
    alert.show();
    alert.find('p').html(message);
};

ugc.alert.danger = function (element, message) {
    ugc.alert(element, message, 'danger');
};

ugc.alert.success = function (element, message) {
    ugc.alert(element, message, 'success');
};