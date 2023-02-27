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
            alert("Authentication failed, please try again.");
        }
    });
}


$(document).ready(function(){
    $("#login-form").on("submit", function (e) {
        e.preventDefault();
        var login = $(this).find('#login').val();
        var password = $(this).find('#password').val()
        var authData = btoa(unescape(encodeURIComponent(`${login}:${password}`)))
        $.ajax('/api/generate_token', {
            contentType: 'application/json',
            beforeSend: function (xhr) {
                xhr.setRequestHeader('Authorization', `Basic ${authData}`);
            },
            type: 'GET',
            success: function(data) {
                window.localStorage.setItem('AuthToken', data.AuthToken);
                login_user({'login': login})
            },
            error: function(request, status, error) {
                alert("Authentication failed, please try again.");
            }
        });
    });
});
