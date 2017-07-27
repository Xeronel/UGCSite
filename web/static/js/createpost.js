tinymce.init({
    plugins: 'image imagetools paste media',
    paste_as_text: true,
    selector: 'textarea',
    menubar: true,
    skin: 'light',
    forced_root_block: false,
    theme_advanced_resizing: true,
    theme_advanced_resize_horizontal: false,
    theme_advanced_statusbar_location: 'bottom',
    toolbar: 'undo,redo,bold,italic,alignleft,aligncenter,' +
    'alignright,alignjustify,bullist,numlist,outdent,indent,image,media',
    setup: function (ed) {
        ed.on('change', function () {
            tinymce.triggerSave();
            $("#" + ed.id).valid();
        })
    },
    automatic_uploads: true,
    file_picker_types: 'image',
    file_picker_callback: function (cb, value, meta) {
        var input = document.createElement('input');
        input.setAttribute('type', 'file');
        input.setAttribute('accept', 'image/*');

        input.onchange = function () {
            var file = this.files[0];

            var reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = function () {
                var id = 'blobid' + (new Date()).getTime();
                var blobCache = tinymce.activeEditor.editorUpload.blobCache;
                var base64 = reader.result.split(',')[1];
                var blobInfo = blobCache.create(id, file, base64);
                blobCache.add(blobInfo);
                cb(blobInfo.blobUri(), {title: file.name});
            };
        };

        input.click();
    },
    images_upload_handler: function (blobInfo, success, failure) {
        var formData = new FormData();
        formData.append('file', blobInfo.blob(), blobInfo.filename());
        $.ajax({
            type: 'POST',
            url: 'image_upload',
            data: formData,
            async: true,
            contentType: false,
            processData: false,
            timeout: 60000,
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-Xsrftoken', Cookies.get('_xsrf'));
            },
            success: function (data) {
                success(data);
            },
            error: function (data) {
                failure('HTTP Error: ' + data.responseText);
            }
        });
    }
});

var createPostForm = $('#create-post-form');
var alert = $('.alert');

createPostForm.validate({
    rules: {
        title: {
            required: true
        }
    }
});

createPostForm.submit(function (e) {
    alert.hide();
    if (createPostForm.valid())
    {
        $.ajax({
            type: 'POST',
            data: createPostForm.serialize(),
            error: function (data) {
                ugc.alert.danger(createPostForm, data.responseText);
            },
            success: function (data) {
                createPostForm[0].reset();
                ugc.alert.success(createPostForm, data);
            }
        });
    }
    e.preventDefault();
});