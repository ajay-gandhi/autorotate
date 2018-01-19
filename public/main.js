var imageData;
var didRotate = false;

var fr = new FileReader();
fr.onload = function (e) {
  $(".ImageSelect__preview").attr("src", e.target.result);

  // Only need to do this once
  if (!imageData) {
    $(".Options__rotateButton").removeProp("disabled");
    $(".ImageSelect__preview").show();
    $(".ImageSelect__prompt").hide().text("Choose new file").addClass("ImageSelect__prompt--reselect");

    $(".Input__ImageSelect").hover(function () {
      $(".ImageSelect__prompt").stop().fadeIn();
    }, function () {
      $(".ImageSelect__prompt").stop().fadeOut();
    });
  }

  imageData = e.target.result;
};

$(document).ready(function () {
  $(".AutoRotator__Carousel").slick({
    centerMode: true,
    slidesToShow: 1,
    variableWidth: true,
    slide: ".Carousel__pane",

    // Disable manual navigation
    accessibility: false,
    arrows: false,
    infinite: false,
    swipeToSlide: false,
    draggable: false,
  });

  $(".ImageSelect__prompt").click(function () {
    $(".ImageSelect__input").click();
  });

  $(".ImageSelect__input").change(function () {
    fr.readAsDataURL($(this).prop("files")[0]);
  });

  $(".Options__rotateButton").click(function () {
    post_rotate_img({ auto_crop: $(".Options__autoCropContainer__checkbox").is(":checked") });
  });

  $(".Actions__newButton").click(function () {
    $(".AutoRotator__Carousel").slick("slickPrev");
  });

  // $(".Options__retryButton--none").click(function () {
    // post_rotate_img({
      // auto_crop: $(".Options__autoCrop").is(":checked"),
      // threshold: 50,
    // });
  // });

  // $(".Options__retryButton--incorrect").click(function () {
    // post_rotate_img({
      // auto_crop: $(".Options__autoCrop").is(":checked"),
      // threshold: 200,
    // });
  // });
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
      $(".ImageOutput__image").attr("src", "data:image/png;base64," + data.imageData.trim());
      $(".AutoRotator__Carousel").slick("slickGoTo", 2);
    } else {
      console.log("Error", data.error);
    }
  }).fail(function (xhr, ajaxOptions, thrownError) {
    console.log("Error", thrownError);
  });
}
