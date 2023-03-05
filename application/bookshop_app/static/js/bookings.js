$(document).ready(function() {
    $("form").on("click", function(e) {
        e.preventDefault();
        var id = $(this).find("#booking_id").val()
        var data = {};
        data["status_id"] = Number($(this).find("#status_id").val())
        $.ajax("/api/booking/" + id, {
            data: JSON.stringify(data),
            contentType: "application/json",
            type: "PUT",
            beforeSend: function(xhr) {
                xhr.setRequestHeader("Authorization", `Bearer ${window.localStorage.getItem("AuthToken")}`);
            },
            success: function(data, textStatus) {
                history.go(0);
            },
            error: function(request, status, error) {
                alert(request.responseText);
            }
        });
    });
});
