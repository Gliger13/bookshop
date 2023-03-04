function add_record_to_table(data) {
    $("#users_table tr:last").after(
        "<tr>" +
        "<td class='id_cell'>" + data.id + "</td>" +
        "<td class='login_cell'>" + data.login + "</td>" +
        "<td class='email_cell'>" + data.email + "</td>" +
        "<td class='name_cell'>" + data.name + "</td>" +
        "<td class='address_cell'>" + data.name + "</td>" +
        "<td class='phone_cell'>" + data.phone + "</td>" +
        "<td class='role_cell'>" + data.role.name + "</td>" +
        "</tr>");
    $("#add_user").modal("hide");
};


function update_record_in_table(data) {
    $('#users_table td.id_cell:contains('+data['id']+')').parent().replaceWith(
        "<tr>" +
        "<td class='id_cell'>" + data.id + "</td>" +
        "<td class='login_cell'>" + data.login + "</td>" +
        "<td class='email_cell'>" + data.email + "</td>" +
        "<td class='name_cell'>" + data.name + "</td>" +
        "<td class='address_cell'>" + data.name + "</td>" +
        "<td class='phone_cell'>" + data.phone + "</td>" +
        "<td class='role_cell'>" + data.role.name + "</td>" +
        "</tr>");
    $('#update_user').modal('hide');
};


function delete_record_from_table(id) {
    $('#users_table td.id_cell:contains('+id+')').parent().remove();
    $("#update_user").modal("hide");
};


function display_error(error) {
    $("#error-message-banner").removeClass("visually-hidden").addClass("opacity-85");
    $("#error-message").html(error);
};


$(document).ready(function(){
    $(document).on("click", '#users_table tbody tr', function() {
        $(this).addClass('bg-light-subtle').siblings().removeClass('bg-light-subtle');
    });

    $("#add_user_form").on("submit", function (event) {
        event.preventDefault();
        var login = $(this).find("#create_user_login").val();
        var password = $(this).find("#create_user_password").val();
        var request_json = {
            "login": login,
            "password": password,
            "email": $(this).find("#create_user_email").val()
        };
        var name = $(this).find("#create_user_name").val();
        if (name != "" ) {
            request_json.name = name;
        }

        var phone = $(this).find("#create_user_phone").val();
        if (phone != "" ) {
            request_json.phone = phone;
        }

        var address = $(this).find("#create_user_address").val();
        if (address != "" ) {
            request_json.address = address;
        }

        var role_id = $(this).find("#create_user_role_id").val();
        if (role_id != "" ) {
            request_json.role_id = parseInt(role_id);
        }

        $.ajax("/api/user", {
            data: JSON.stringify(request_json),
            contentType: "application/json",
            beforeSend: function (xhr) {
                xhr.setRequestHeader("Authorization", `Bearer ${window.localStorage.getItem("AuthToken")}`);
            },
            type: "POST",
            success: function(data) {
                add_record_to_table(data);
                $("#add_user").modal("hide");
            },
            error: function(request, status, error) {
                display_error(jQuery.parseJSON(request.responseText).error);
            }
        });
    });

    $("#delete_user_form").on("submit", function (event) {
        event.preventDefault();
        var id = $(this).find("#delete_user_id").val();
        $.ajax("/api/user/" + id, {
            contentType: "application/json",
            type: "DELETE",
            beforeSend: function (xhr) {
                xhr.setRequestHeader("Authorization", `Bearer ${window.localStorage.getItem("AuthToken")}`);
            },
            success: function(data) {
                delete_record_from_table(id);
                $("#delete_user").modal("hide");
            },
            error: function(request, status, error) {
                display_error(request.responseText);
            }
        });
    });

    $("#delete_user").on("shown.bs.modal", function (event) {
        var id = $("tr.bg-light-subtle td:eq(0)").text();
        $(this).find("#delete_user_id").val(id);
    });

    $("#update_user").on("shown.bs.modal", function (event) {
        var id = $('tr.bg-light-subtle td:eq(0)').text();
        var login = $('tr.bg-light-subtle td:eq(1)').text();
        var email = $('tr.bg-light-subtle td:eq(2)').text();
        var name = $('tr.bg-light-subtle td:eq(3)').text();
        var address = $('tr.bg-light-subtle td:eq(4)').text();
        var phone = $('tr.bg-light-subtle td:eq(5)').text();
        var role_name = $('tr.bg-light-subtle td:eq(6)').text();

        $(this).find('#update_user_id').val(id);
        $(this).find('#update_user_login').val(login);
        $(this).find('#update_user_email').val(email);
        $(this).find('#update_user_name').val(name);
        $(this).find('#update_user_address').val(address);
        $(this).find('#update_user_phone').val(phone);
        var role_map = {"Admin": 1, "Manager": 2, "Customer": 3};
        $(this).find('#update_user_role_id').val(role_map[role_name]);
    });

    $("#update_user_form").on("submit", function (event) {
        event.preventDefault();
        var id = $(this).find("#update_user_id").val();
        var request_json = {};

        var login = $(this).find("#update_user_login").val();
        if (login != "" ) {
            request_json.login = login;
        }

        var password = $(this).find("#update_user_password").val();
        if (password != "" ) {
            request_json.password = password;
        }

        var email = $(this).find("#update_user_email").val();
        if (email != "" ) {
            request_json.email = email;
        }

        var name = $(this).find("#update_user_name").val();
        if (name != "" ) {
            request_json.name = name;
        }

        var phone = $(this).find("#update_user_phone").val();
        if (phone != "" ) {
            request_json.phone = phone;
        }

        var address = $(this).find("#update_user_address").val();
        if (address != "" ) {
            request_json.address = address;
        }

        var role_id = $(this).find("#update_user_role_id").val();
        if (role_id != "" ) {
            request_json.role_id = parseInt(role_id);
        }
        $.ajax('/api/user/' + id, {
            data: JSON.stringify(request_json),
            contentType: 'application/json',
            beforeSend: function (xhr) {
                xhr.setRequestHeader('Authorization', `Bearer ${window.localStorage.getItem('AuthToken')}`);
            },
            type: 'PUT',
            success: function(data) {
                update_record_in_table(data);
                $('#update_user').modal('hide');
            },
            error: function(request, status, error) {
                display_error(request.responseText);
            }
        });
    });
});
