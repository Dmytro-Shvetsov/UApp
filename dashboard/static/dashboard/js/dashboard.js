let ajaxRequestIsLoading = false;

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


function saveForm(formSelector, requiredFieldsFunc, btnSpinnerSelector, url = "", additional_data = "", additional_params = {}) {
    let data = new FormData($(formSelector).get(0));
    if (ajaxRequestIsLoading == false) {
        let $form = $(formSelector);
        let params = {
            method: "POST",
            url: url,
            data: data,
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
                    let msg;
                    if (response.form_errors === undefined || response.form_errors === null || response.form_errors === "") {
                        create_fancybox_alert('fail', response.alert_title, response.alert_message, 'Помилка!');
                    } else {
                        // msg = "Під час обробки профілю щось пішло не так. Спробуйте пізніше";
                        // create_fancybox_alert('fail', response.alert_title, msg, 'Помилка!');
                        let msg;
                        if (response.form_errors === undefined || response.form_errors === null || response.form_errors === "") {
                            create_fancybox_alert('fail', response.alert_title, response.alert_message, 'Error!');
                        } else {
                            msg = "<ul class='errorlist'>";
                            for (error_key in response.form_errors) {
                                if (response.form_errors[error_key].length > 1) {
                                    for (index in response.form_errors[error_key]) {
                                        list_value = "<li class='error'>" + response.form_errors[error_key][index] + "</li>";
                                        msg += list_value;
                                    }
                                } else {
                                    list_value = '<li class=\'error\'>' + response.form_errors[error_key] + '</li>';
                                    msg += list_value;
                                }
                            }
                            msg += "</ul>";
                            create_fancybox_alert('fail', response.alert_message, msg, response.alert_title);
                        }
                    }
                }
            }
        };
        $.extend(params, additional_params);

        if (requiredFieldsFunc()) {
            $.ajax(params);
            ajaxRequestIsLoading = false;
        }
    }
}

function requiredFieldsClosure() {
    return true;
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

