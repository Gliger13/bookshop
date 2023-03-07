function display_error(modal_id, response) {
    $("#" + modal_id + "_error-message-banner").removeClass("visually-hidden").addClass("opacity-85");
    $("#" + modal_id + "_error-message").html(jQuery.parseJSON(response.responseText).detail);
};


$(document).ready(function() {
    $("#book_product_by_id_form").on("submit", function(event) {
        event.preventDefault();
        var request_json = {
            "product_id": parseInt($(this).find("#book_product_by_id_product_id").val()),
            "user_id": parseInt($(this).find("#book_product_by_id_user_id").val()),
            "delivery_address": $(this).find("#book_product_by_id_delivery_address").val(),
            "quantity": parseInt($(this).find("#book_product_by_id_quantity").val()),
        }

        $.ajax("/api/booking", {
            data: JSON.stringify(request_json),
            contentType: "application/json",
            type: "POST",
            beforeSend: function(xhr) {
                xhr.setRequestHeader("Authorization", `Bearer ${window.localStorage.getItem("AuthToken")}`);
            },
            success: function(data) {
                location.href = "/bookings";
            },
            error: function(request, status, error) {
                display_error("book_product_by_id", request);
            }
        });
    });

    $("#update_product_by_id_form").on("submit", function(event) {
        event.preventDefault();
        var id = $(this).find("#update_product_by_id_id").val();
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
                display_error("update_product_by_id", request);
            }
        });
    });

    $("#delete_product_by_id").on("submit", function(event) {
        event.preventDefault();
        var id = $(this).find("#delete_product_by_id_id").val();
        $.ajax("/api/product/" + id, {
            contentType: "application/json",
            type: "DELETE",
            beforeSend: function(xhr) {
                xhr.setRequestHeader("Authorization", `Bearer ${window.localStorage.getItem("AuthToken")}`);
            },
            success: function(data) {
                location.href = "/products";
            },
            error: function(request, status, error) {
                display_error("delete_product_by_id", request);
            }
        });
    });
});
