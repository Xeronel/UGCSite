var editPostForm = $('#edit-post-form');
var alert = $('.alert');

editPostForm.validate({
    rules: {
        title: {
            required: true
        }
    }
});

editPostForm.submit(function (e) {
    alert.hide();
    if (editPostForm.valid())
    {
        $.ajax({
            type: 'POST',
            data: editPostForm.serialize(),
            error: function (data) {
                ugc.alert.danger(editPostForm, data.responseText);
            },
            success: function (data) {
                location.reload();
            }
        });
    }
    e.preventDefault();
});