$(document).ready(function () {
   $("form").on("submit", function (event) {
      var form_name = $(this).attr('id');
      if (form_name.indexOf("change_booking_status_form") > -1) {
         event.preventDefault();
         var id = form_name.split(/[\s_]+/).pop();
         var data = {
            "status_id": Number($(this).find("#status_id_" + id).val())
         };
         $.ajax("/api/booking/" + id, {
            data: JSON.stringify(data),
            contentType: "application/json",
            type: "PUT",
            beforeSend: function (xhr) {
               xhr.setRequestHeader("Authorization", `Bearer ${window.localStorage.getItem("AuthToken")}`);
            },
            success: function (data, textStatus) {
               history.go(0);
            }
         });
      }
   });
});
