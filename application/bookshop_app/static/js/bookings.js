$(document).ready(function(){
    $("form").on("click", function (e) {
        e.preventDefault();
        var id = $(this).find('#booking_id').val()
        var data = {};
        data['status_id'] = Number($(this).find('#status_id').val())
        $.ajax('/api/booking/' + id, {
            data: JSON.stringify(data),
            contentType: 'application/json',
            type: 'PUT',
            error: function(request, status, error) {
                alert(request.responseText);
            }
        });
    });
});
