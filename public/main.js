var imageData;
var didRotate = false;

var fr = new FileReader();
fr.onload = function (e) {
  $(".ImageSelect__imageWrapper__preview").attr("src", e.target.result);
  $(".Options__rotateButton").removeProp("disabled");
  $(".ImageSelect__imageWrapper").show();
  $(".ImageSelect__imageWrapper__RemoveWrapper").hide();

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

  // Image select actions
  $(".ImageSelect__prompt").click(function () {
    $(".ImageSelect__input").click();
  });

  $(".ImageSelect__imageWrapper__RemoveWrapper").click(function () {
    $(".ImageSelect__input").val("");
    $(".Options__rotateButton").prop("disabled", "true");
    $(".ImageSelect__imageWrapper").fadeOut(100);
  });

  $(".ImageSelect__input").change(function () {
    fr.readAsDataURL($(this).prop("files")[0]);
  });

  attach_image_hover();

  // Buttons
  $(".Options__rotateButton").click(function () {
    post_rotate_img();
  });

  $("#newRotateButton").click(function () {
    attach_image_hover();
    $(".AutoRotator__Carousel").slick("slickPrev");
  });

  $("#downloadButton").click(function () {
    $("#downloadButton a")[0].click();
  });

  $("#retryNoRotate").click(function () {
    post_rotate_img({ threshold: 50 });
  });

  $("#retryIncorrectRotate").click(function () {
    post_rotate_img({ threshold: 200 });
  });
});

var post_rotate_img = function (arg) {
  var data = arg || {};
  data.auto_crop = $(".Options__autoCropContainer__checkbox").is(":checked");
  data.image_data = imageData.substring(imageData.indexOf(",") + 1);

  $(".ImageOutput__image").attr("src", "loading.gif");
  $(".Input__ImageSelect").off("hover");
  $(".AutoRotator__Carousel").slick("slickGoTo", 2);

  $.ajax({
    url: "/rotate",
    type: "POST",
    data: JSON.stringify(data),
  }).done(function (result) {
    var data = JSON.parse(result);
    if (data.success) {
      var imageOutput = "data:image/png;base64," + data.imageData.trim();
      $(".ImageOutput__image").attr("src", imageOutput);
      $("a").attr("href", imageOutput);
    } else {
      $(".ImageOutput__image").attr("src", imageData);
      console.log("Error", data.error);
    }
  }).fail(function (xhr, ajaxOptions, thrownError) {
    console.log("Error", thrownError);
  });
}

var attach_image_hover = function () {
  $(".Input__ImageSelect").hover(function () {
    $(".ImageSelect__imageWrapper__RemoveWrapper").stop().fadeIn(200);
  }, function () {
    $(".ImageSelect__imageWrapper__RemoveWrapper").stop().fadeOut(200);
  });
}
