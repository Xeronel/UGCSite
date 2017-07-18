$(function () {
    var loginForm = $('#login-form');
    var alert = $('.alert');

    loginForm.submit(function (e) {
        alert.hide();
        $.ajax({
            type: 'POST',
            data: loginForm.serialize(),
            error: function (data) {
                ugc.alert.danger(loginForm, data);
            },
            success: function () {
                document.location.reload();
            }
        });
        e.preventDefault();
    })
});