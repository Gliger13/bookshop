function add_record_to_table(data) {
    $("#store_items_table tr:last").after(
        "<tr>" +
        "<td class='id_cell'>" + data.id + "</td>" +
        "<td class='product_id_cell'>" + data.product.id + "</td>" +
        "<td class='product_name_cell'>" + data.product.name + "</td>" +
        "<td class='product_author_cell'>" + data.product.author + "</td>" +
        "<td class='available_quantity_cell'>" + data.available_quantity + "</td>" +
        "<td class='booked_quantity_cell'>" + data.booked_quantity + "</td>" +
        "<td class='sold_quantity_cell'>" + data.sold_quantity + "</td>" +
        "</tr>");
    $("#create_store_item").modal("hide");
};


function update_record_in_table(data) {
    $("#store_items_table td.id_cell:contains(" + data["id"] + ")").parent().replaceWith(
        "<tr>" +
        "<td class='id_cell'>" + data.id + "</td>" +
        "<td class='product_id_cell'>" + data.product.id + "</td>" +
        "<td class='product_name_cell'>" + data.product.name + "</td>" +
        "<td class='product_author_cell'>" + data.product.author + "</td>" +
        "<td class='available_quantity_cell'>" + data.available_quantity + "</td>" +
        "<td class='booked_quantity_cell'>" + data.booked_quantity + "</td>" +
        "<td class='sold_quantity_cell'>" + data.sold_quantity + "</td>" +
        "</tr>");
    $("#update_store_item").modal("hide");
};


function delete_record_from_table(id) {
    $("#store_items_table td.id_cell:contains(" + id + ")").parent().remove();
    $("#update_store_item").modal("hide");
};


function display_error(modal_id, response) {
    $("#" + modal_id + "_error-message-banner").removeClass("visually-hidden").addClass("opacity-85");
    $("#" + modal_id + "_error-message").html(jQuery.parseJSON(response.responseText).detail);
};


$(document).ready(function() {
    $(document).on("click", "#store_items_table tbody tr", function() {
        $(this).addClass("bg-light-subtle").siblings().removeClass("bg-light-subtle");
    });

    $("#create_store_item_form").on("submit", function(event) {
        event.preventDefault();

        var product_id = $(this).find("#create_store_item_product_id").val();
        var available_quantity = $(this).find("#create_store_item_available_quantity").val();
        var booked_quantity = $(this).find("#create_store_item_booked_quantity").val();
        var sold_quantity = $(this).find("#create_store_item_sold_quantity").val();

        var request_data = {
            "product_id": product_id != "" ? parseInt(product_id) : product_id,
            "available_quantity": available_quantity != "" ? parseInt(available_quantity) : available_quantity,
            "booked_quantity": booked_quantity != "" ? parseInt(booked_quantity) : booked_quantity,
            "sold_quantity": sold_quantity != "" ? parseInt(sold_quantity) : sold_quantity
        };
        var filtered_data = Object.fromEntries(Object.entries(request_data).filter(([_, v]) => v != ""));

        $.ajax("/api/store-item", {
            data: JSON.stringify(filtered_data),
            contentType: "application/json",
            type: "POST",
            beforeSend: function(xhr) {
                xhr.setRequestHeader("Authorization", `Bearer ${window.localStorage.getItem("AuthToken")}`);
            },
            success: function(data) {
                add_record_to_table(data);
                $("#create_store_item").modal("hide");
            },
            error: function(request, status, error) {
                display_error("create_store_item", request);
            }
        });
    });

    $("#update_store_item_form").on("submit", function(event) {
        event.preventDefault();

        var id = $(this).find("#update_store_item_id").val();
        var product_id = $(this).find("#update_store_item_product_id").val();
        var available_quantity = $(this).find("#update_store_item_available_quantity").val();
        var booked_quantity = $(this).find("#update_store_item_booked_quantity").val();
        var sold_quantity = $(this).find("#update_store_item_sold_quantity").val();

        var request_data = {
            "product_id": product_id != "" ? parseInt(product_id) : product_id,
            "available_quantity": available_quantity != "" ? parseInt(available_quantity) : available_quantity,
            "booked_quantity": booked_quantity != "" ? parseInt(booked_quantity) : booked_quantity,
            "sold_quantity": sold_quantity != "" ? parseInt(sold_quantity) : sold_quantity
        };
        var filtered_data = Object.fromEntries(Object.entries(request_data).filter(([_, v]) => v != ""));

        $.ajax("/api/store-item/" + id, {
            data: JSON.stringify(filtered_data),
            contentType: "application/json",
            type: "PUT",
            beforeSend: function(xhr) {
                xhr.setRequestHeader("Authorization", `Bearer ${window.localStorage.getItem("AuthToken")}`);
            },
            success: function(data) {
                update_record_in_table(data);
                $("#update_store_item").modal("hide");
            },
            error: function(request, status, error) {
                display_error("update_store_item", request);
            }
        });
    });

    $("#delete_store_item_form").on("submit", function(event) {
        event.preventDefault();
        var id = $(this).find("#delete_store_item_id").val();
        $.ajax("/api/store-item/" + id, {
            contentType: "application/json",
            type: "DELETE",
            beforeSend: function(xhr) {
                xhr.setRequestHeader("Authorization", `Bearer ${window.localStorage.getItem("AuthToken")}`);
            },
            success: function(data) {
                delete_record_from_table(id);
                $("#delete_store_item").modal("hide");
            },
            error: function(request, status, error) {
                display_error("delete_store_item", request);
            }
        });
    });

    $("#delete_store_item").on("shown.bs.modal", function(event) {
        var id = $("tr.bg-light-subtle td:eq(0)").text();
        $(this).find("#delete_store_item_id").val(id);
    });

    $("#update_store_item").on("shown.bs.modal", function(event) {
        var id = $("tr.bg-light-subtle td:eq(0)").text();
        var product_id = $("tr.bg-light-subtle td:eq(1)").text();
        var available_quantity = $("tr.bg-light-subtle td:eq(4)").text();
        var booked_quantity = $("tr.bg-light-subtle td:eq(5)").text();
        var sold_quantity = $("tr.bg-light-subtle td:eq(6)").text();

        $(this).find("#update_store_item_id").val(id);
        $(this).find("#update_store_item_product_id").val(product_id);
        $(this).find("#update_store_item_available_quantity").val(available_quantity);
        $(this).find("#update_store_item_booked_quantity").val(booked_quantity);
        $(this).find("#update_store_item_sold_quantity").val(sold_quantity);
    });
});
