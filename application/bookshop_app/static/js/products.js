function display_error(modal_id, response) {
    $("#" + modal_id + "_error-message-banner").removeClass("visually-hidden").addClass("opacity-85");
    $("#" + modal_id + "_error-message").html(jQuery.parseJSON(response.responseText).detail);
};


$(document).ready(function() {
    $("#create_product_form").on("submit", function(event) {
        event.preventDefault();
        var form_data = new FormData($(this)[0]);
        $.ajax("/api/product", {
            data: form_data,
            type: "POST",
            cache: false,
            contentType: false,
            processData: false,
            beforeSend: function(xhr) {
                xhr.setRequestHeader("Authorization", `Bearer ${window.localStorage.getItem("AuthToken")}`);
            },
            success: function(data) {
                history.go(0);
            },
            error: function(request, status, error) {
                display_error("create_product", request);
            }
        });
    });

    $("#update_product_form").on("submit", function(event) {
        event.preventDefault();
        var id = $(this).find("#update_product_id").val();
        var form_data = new FormData($(this)[0]);
        $.ajax("/api/product/" + id, {
            data: form_data,
            type: "PUT",
            cache: false,
            contentType: false,
            processData: false,
            beforeSend: function(xhr) {
                xhr.setRequestHeader("Authorization", `Bearer ${window.localStorage.getItem("AuthToken")}`);
            },
            success: function(data) {
                history.go(0);
            },
            error: function(request, status, error) {
                display_error("update_product", request);
            }
        });
    });

    $("#delete_product_form").on("submit", function(event) {
        event.preventDefault();
        var id = $(this).find("#delete_product_id").val();
        $.ajax("/api/product/" + id, {
            contentType: "application/json",
            type: "DELETE",
            beforeSend: function(xhr) {
                xhr.setRequestHeader("Authorization", `Bearer ${window.localStorage.getItem("AuthToken")}`);
            },
            success: function(data) {
                history.go(0);
            },
            error: function(request, status, error) {
                display_error("delete_product", request);
            }
        });
    });
});
