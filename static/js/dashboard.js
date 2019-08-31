let ajaxRequestIsLoading = false;

$(document).ready(function () {
    $('.content').load('profile/');
    $('.list-group-item a').click(function (event) {
        if (ajaxRequestIsLoading == false) {
            event.preventDefault();
            $(this).parent().addClass('active').siblings().removeClass('active');
            let page = $(this).text();
            let data = {
                'page': page
            };
            $.ajax({
                url: page.toLowerCase() + '/',
                method: 'GET',
                data: data,
                dataType: 'html',
                beforeSend: function () {
                    ajaxRequestIsLoading = true;
                    let loadingText = '<i class="fa fa-circle-o-notch fa-spin"></i> working...';
                    if ($(".content").html() !== loadingText) {
                        $(".content").data('original-text', $(".content").html());
                        $(".content").html(loadingText);
                    }
                },
                success: function (response) {
                    $('.content').html($("#btnSignIn").data('original-text'));
                    $('.content').html(response);
                },
                error: function (error) {
                    $('.content').html($("#btnSignIn").data('original-text'));
                    $('.content').html('<h1>404. Not Found!</h1>');
                }
            });
            ajaxRequestIsLoading = false;
        }
    });
});

function create_fancybox_alert(type, title, message, footer) {
    let alert_class;
    if (type === 'success') {
        alert_class = 'alert-success';
    } else {
        alert_class = 'alert-danger';
    }

    $.fancybox.open("<div style=\"padding:0; width: 400px; border-radius:8px;\">" +
        "<div class=\"m-0 alert " + alert_class + "\" role=\"alert\">\n" +
        "  <h4 class=\"alert-heading\">" + title + "</h4>\n" +
        "  <p>" + message + "</p>\n" +
        "  <hr>\n" +
        "  <p class=\"mb-0\">" + footer + "</p>\n" +
        "</div>" +
        "</div>");
}

function saveForm(formSelector, requiredFieldsFunc, btnSpinnerSelector, url = "", additional_data = "") {
    if (ajaxRequestIsLoading == false) {
        let $form = $(formSelector);
        if (requiredFieldsFunc()) {
            $.ajax({
                method: "POST",
                url: url,
                data: $form.serialize() + additional_data,
                cache: false,
                dataType: "json",
                beforeSend: function () {
                    ajaxRequestIsLoading = true
                    let loadingText = '<i class="fa fa-circle-o-notch fa-spin"></i> working...';
                    if ($(btnSpinnerSelector).html() !== loadingText) {
                        $(btnSpinnerSelector).data('original-text', $(btnSpinnerSelector).html());
                        $(btnSpinnerSelector).html(loadingText);
                    }
                },
                success: function (response) {
                    $(btnSpinnerSelector).html($(btnSpinnerSelector).data('original-text')); //stop animation and switch back to original text
                    if (response.alert_type == 'success') {
                        create_fancybox_alert('success', response.alert_title, response.alert_message, 'Well Done!');
                        setTimeout(function () {
                            window.location.reload()
                        }, 2500);
                    } else {
                        create_fancybox_alert('fail', response.alert_title, response.alert_message, 'Error!');
                    }
                }
            });
            ajaxRequestIsLoading = false;
        }
    }
}

function passwordChangeRequiredFieldsPass() {
    let old_password = $("#id_old_password").val()
    let id_new_password1 = $("#id_new_password1").val();
    let id_new_password2 = $("#id_new_password2").val();

    if (old_password === undefined || old_password === null || old_password === "") {
        create_fancybox_alert("fail", "Old Password is Required!", "Please enter your old password.", "Error");
        $("#id_old_password").focus();
        return false;
    }

    if (id_new_password1 === undefined || id_new_password1 === null || id_new_password1 === "") {
        create_fancybox_alert("fail", "New password is Required!", "Please enter your new password.", "Error!");
        $("#id_new_password1").focus();
        return false;
    }

    if (id_new_password2 === undefined || id_new_password2 === null || id_new_password2 === "") {
        create_fancybox_alert("fail", "Confirm password is Required!", "Please confirm your new password.", "Error!")
        $("#id_new_password2").focus();
        return false;
    }

    if (id_new_password1 != id_new_password2) {
        create_fancybox_alert("fail", "Password Not Match", "Passwords do not match, please try again.", "Error!");
        $("#id_new_password2").focus();
        return false;
    }

    return true;
}
