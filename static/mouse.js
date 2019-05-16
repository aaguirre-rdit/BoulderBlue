// TODO: break this into multiple files, create objects instead of functions

$(function global() {
    $('[data-toggle="tooltip"]').tooltip();

    $('.expand-all').click(function() {
        $('.collapse').collapse('show');
    });

    $('.collapse-all').click(function() {
        $('.collapse').collapse('hide');
    });
});


// ***************************************************************************


$(function editInPlace() {
    var enableEIP = function() {
        $('body').addClass('editing');
        $.inplaceeditform.methods.enableInplaceEditAction();
        $('.inplaceedit').tooltip('enable');
        $('#edit-mode input').prop('checked', true);
        window.location.hash = '#edit';
    }
    var disableEIP = function() {
        $('body').removeClass('editing');
        $.inplaceeditform.methods.disableInplaceEditAction();
        $('.inplaceedit').tooltip('disable');
        $('#edit-mode input').prop('checked', false);
        window.location.hash = '';
    };

    if (window.location.hash == '#edit') {
        enableEIP();
    } else {
        disableEIP();
    }

    $('#edit-mode').on('change', 'input', function(e) {
        e.stopPropagation();
        if ($(e.target).is(':checked')) {
            if (confirm('WARNING: This course may be live!')) {
                enableEIP();
            } else {
                e.target.checked = false;
            }
        } else {
            disableEIP();
        }
    });
});


// ***************************************************************************


$(function contentUploader() {

    var resetForm = function(form) {
        var input = form.siblings('.file-input');
        input.replaceWith(input.val('').clone(true));
        form.siblings('.dropzone').removeClass('dragover uploading uploaded processing').addClass('empty');
        form.find('input[type="submit"]').prop('disabled', true);
    };

    var uploadFile = function uploadFile(file, s3_signature, bucket_url, form) {
        var postData = new FormData();
        for(field in s3_signature){
            postData.append(field, s3_signature[field]);
        }
        postData.append('file', file);

        $.ajax({
            type: 'POST',
            url: bucket_url,
            data: postData,
            contentType: false,
            processData: false,
            success: function(response) {
                form.find('input[type="submit"]').prop('disabled', false);
                form.find('input[name="location"]').val(file.name);
                form.siblings('.dropzone').removeClass('uploading').addClass('uploaded');
            },
            error: function() {
                alert("Could not upload file.");
                resetForm(form);
            }
        });
    };

    var getSignedRequest = function getSignedRequest(file, form) {
        $.ajax({
            type: 'GET',
            url: location.pathname + "/sign_s3?file_name=" + file.name + "&file_type=" + file.type,
            dataType: 'json',
            success: function(response) {
                uploadFile(file, response.data, response.bucket_url, form);
            },
            error: function() {
                alert("Could not get signed URL.");
                resetForm(form);
            }
        });
    };

    var handleFile = function handleFile(dropzone, file) {
        if (confirm('Are you sure you want to upload this file?')) {
            dropzone.removeClass('empty').addClass('uploading');
            dropzone.find('.file-msg').text(file.name);
            getSignedRequest(file, dropzone.siblings('form'));
        } else {
            resetForm($(this).siblings('form'));
        }
    };

    $('.file-input').on('change', function(e) {
        e.preventDefault();
        var file = e.target.files[0];
        if (file) {
            var dropzone = $(this).siblings('.dropzone');
            handleFile(dropzone, file);
        }
    });

    $('.dropzone').on('drag dragstart dragend dragover dragenter dragleave drop click', function(e) {
        e.preventDefault();
        e.stopPropagation();
    }).on('dragover dragenter dragstart', function() {
        $(this).addClass('dragover');
    }).on('dragleave dragend drop', function() {
        $(this).removeClass('dragover');
    }).on('drop', function(e) {
        file = e.originalEvent.dataTransfer.files[0];
        handleFile($(this), file);
    }).on('click', function (e) {
        var target = window[this.htmlFor];
        target.checked = !target.checked;
        $(target).trigger('click');
    });

    $('.content-upload-form').on('submit', function(e) {
        var self = $(this);
        var dropzone = self.siblings('.dropzone');
        dropzone.removeClass('uploaded').addClass('processing');
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: self.attr('action'),
            data: self.serialize(),
            success: function(data) {
                var locationField = self.parent().siblings('.location');
                locationField.addClass('text-success').text(data.location);
                setTimeout(function() {
                    locationField.removeClass('text-success');
                }, 1500);
                resetForm(self);
            },
            error: function(data) {
                console.error(data);
                resetForm(self);
            }
        });
    });

});


// ***************************************************************************

$(function ajaxFormSubmit() {
    $('body').on('submit', 'form.ajax-submit', function(e) {
        e.preventDefault();
        var form = $(e.target);
        $.ajax({
            type: 'POST',
            url: form.attr('action'),
            data: form.serialize(),
            success: function(response) {
                window.location.reload(true);
            },
            error: function(response) {
                console.error(response);
                alert('Something went wrong.' + response);
            }
        });
    });
});


$(function addForms() {
    var body = $('body');
    var topicsNode = $('#topics');

    var addBtnNodes = $('.add-btn');
    var addTopicNode = $('#add-topic');
    var addChapterNodes = $('.add-chapter');

    var getAndRenderForm = function(url, parentNode) {
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response) {
                parentNode.after(response);
                addBtnNodes.hide();
            },
            error: function(response) {
                console.error(response);
                alert('Something went wrong. ' + response);
            }
        });
    }

    addTopicNode.on('click', function() {
        var url = location.pathname + '/add/topic';
        getAndRenderForm(url, topicsNode);
    });

    addChapterNodes.on('click', function() {
        var self = $(this);
        var topicId = self.parents('.topic').data('id');
        var url = location.pathname + '/' + topicId + '/add/chapter';

        getAndRenderForm(url, self);
    });

    body.on('click', '.add-cancel', function(e) {
        e.preventDefault();
        var form = $(e.target).parents('form');
        form.remove();
        addBtnNodes.show();
    });
});
