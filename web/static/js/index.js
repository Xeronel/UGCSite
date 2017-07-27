function delete_post(post_id) {
    if (confirm("Are you sure?")) {
        $.ajax({
            type: 'POST',
            url: '/delete_post',
            data: {'post-id': post_id},
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-Xsrftoken', Cookies.get('_xsrf'));
            },
            success: function () {
                location.reload();
            }
        });
    }
}