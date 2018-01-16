var imageData;
var didRotate = false;

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
    post_rotate_img({ auto_crop: $("#autoCrop").is(":checked") });
  });

  $("#noRotation").click(function () {
    post_rotate_img({
      auto_crop: $("#autoCrop").is(":checked"),
      threshold: 50,
    });
  });

  $("#incorrectRotation").click(function () {
    post_rotate_img({
      auto_crop: $("#autoCrop").is(":checked"),
      threshold: 200,
    });
  });
});

var post_rotate_img = function (data) {
  data.image_data = imageData.substring(imageData.indexOf(",") + 1);

  $.ajax({
    url: "/rotate",
    type: "POST",
    data: JSON.stringify(data),
  }).done(function (result) {
    var data = JSON.parse(result);
    if (data.success) {
      $("#outputImage").attr("src", "data:image/png;base64," + data.imageData.trim());
      $(".retryButton").show();
    } else {
      console.log("Error", data.error);
    }
  }).fail(function (xhr, ajaxOptions, thrownError) {
    console.log("Error", thrownError);
  });
}
