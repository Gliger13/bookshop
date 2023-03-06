function display_error(modal_id, response) {
    $("#" + modal_id + "_error-message-banner").removeClass("visually-hidden").addClass("opacity-85");
    $("#" + modal_id + "_error-message").html(jQuery.parseJSON(response.responseText).detail);
};


$(document).ready(function() {
    $("#user_form").on("submit", function(event) {
        event.preventDefault();

        var id = $(this).find("#id").val();
        var login = $(this).find("#login").val();
        var password = $(this).find("#password").val();
        var email = $(this).find("#email").val();
        var name = $(this).find("#name").val();
        var phone = $(this).find("#phone").val();
        var address = $(this).find("#address").val();
        var role_id = $(this).find("#role_id").val();

        var request_data = {
            "login": login,
            "password": password,
            "email": email,
            "name": name,
            "phone": phone,
            "address": address,
            "role_id": role_id != "" ? parseInt(role_id) : role_id
        };
        var filtered_data = Object.fromEntries(Object.entries(request_data).filter(([_, v]) => v != ""));

        $.ajax("/api/user/" + id, {
            data: JSON.stringify(filtered_data),
            contentType: "application/json",
            type: "PUT",
            beforeSend: function(xhr) {
                xhr.setRequestHeader("Authorization", `Bearer ${window.localStorage.getItem("AuthToken")}`);
            },
            success: function(data) {
                history.go(0);
            },
            error: function(request, status, error) {
                display_error("user_form", request);
            }
        });
    });

    $("#delete_user_button").on("click", function(event) {
        event.preventDefault();
        var id = $("#user_form").find("#id").val();
        $.ajax("/api/user/" + id, {
            contentType: "application/json",
            type: "DELETE",
            beforeSend: function(xhr) {
                xhr.setRequestHeader("Authorization", `Bearer ${window.localStorage.getItem("AuthToken")}`);
            },
            success: function(data) {
                $.ajax("/log-out", {
                    type: "POST",
                });
                location.href = "/products";
            },
            error: function(request, status, error) {
                display_error("user_form", request);
            }
        });
    });
});
