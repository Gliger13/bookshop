function display_error(error) {
    $("#error-message-banner").removeClass("visually-hidden").addClass("opacity-85");
    $("#error-message").html(error);
}

function login_user(data) {
    $.ajax('/login', {
        data: JSON.stringify(data),
        contentType: 'application/json',
        beforeSend: function (xhr) {
            xhr.setRequestHeader('Authorization', `Bearer ${window.localStorage.getItem('AuthToken')}`);
        },
        type: 'POST',
        success: function(data, textStatus) {
            window.location.href = data;
        },
        error: function(request, status, error) {
            display_error("Can not login user. Something went wrong (┳‸┳)");
        }
    });
}

function authenticate(login, password) {
    var authData = btoa(unescape(encodeURIComponent(`${login}:${password}`)))
    $.ajax('/api/generate_token', {
        contentType: 'application/json',
        beforeSend: function (xhr) {
            xhr.setRequestHeader('Authorization', `Basic ${authData}`);
        },
        type: 'GET',
        success: function(data) {
            window.localStorage.setItem('AuthToken', data.AuthToken);
            login_user({'login': login});
        },
        error: function(request, status, error) {
            display_error("Invalid credentials");
        }
    });
}

$(document).ready(function(){
    $("#login-form").on("submit", function (e) {
        e.preventDefault();
        var login = $(this).find('#login').val();
        var password = $(this).find('#password').val()
        authenticate(login, password);
    });
    $("#registration-form").on("submit", function (e) {
        e.preventDefault();
        var login = $(this).find('#login').val();
        var password = $(this).find('#password').val();
        var request_json = {
            "login": login,
            "password": password,
            "email": $(this).find('#email').val()
        };
        var name = $(this).find('#name').val();
        if (name != "" ) {
            request_json["name"] = name
        }

        var phone = $(this).find('#phone').val();
        if (phone != "" ) {
            request_json["phone"] = phone
        }

        var address = $(this).find('#address').val();
        if (address != "" ) {
            request_json["address"] = address
        }

        $.ajax('/api/user', {
            contentType: 'application/json',
            data: JSON.stringify(request_json),
            type: 'POST',
            success: function() {
                authenticate(login, password);
            },
            error: function(request, status, error) {
                display_error(jQuery.parseJSON(request.responseText).error);
            }
        });
    });
});
