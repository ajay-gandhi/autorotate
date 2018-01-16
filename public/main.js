var imageData;
var fr = new FileReader();
fr.onload = function (e) {
  $("#previewUpload").attr("src", e.target.result);
  imageData = e.target.result;
};

$(document).ready(function () {
  $("#selectImage").change(function () {
    fr.readAsDataURL($(this).prop("files")[0]);
  });

  $("#submitImage").click(function () {
    var base64ImageData = imageData.substring(imageData.indexOf(",") + 1);
    var data = JSON.stringify({
      image_data: base64ImageData,
      auto_crop: $("#autoCrop").is(":checked"),
    });

    $.ajax({
      url: "/rotate",
      type: "POST",
      data: data,
    }).done(function (result) {
      var data = JSON.parse(result);
      if (data.success) {
        $("#outputImage").attr("src", "data:image/png;base64," + data.imageData.trim());
      } else {
        console.log("Error", result.error);
      }
    }).fail(function (xhr, ajaxOptions, thrownError) {
      console.log("Error", thrownError);
    });
  });
});
