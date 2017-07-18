var createUserForm = $('#create-user-form');
var alert = $('.alert');

createUserForm.validate({
    rules: {
        verify_password: {
            equalTo: '#password'
        }
    }
});

createUserForm.submit(function (e) {
    alert.hide();
    $.ajax({
        type: 'POST',
        data: createUserForm.serialize(),
        error: function (data) {
            ugc.alert.danger(createUserForm, data.responseText);
        },
        success: function (data) {
            createUserForm[0].reset();
            ugc.alert.success(createUserForm, data);
        }
    });
    e.preventDefault();
});