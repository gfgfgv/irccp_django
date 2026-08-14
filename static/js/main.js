document.addEventListener("DOMContentLoaded", function () {
  var toggle = document.getElementById("menuToggle");
  var menu = document.getElementById("mobileMenu");
  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      menu.classList.toggle("open");
    });
  }

  // Live avatar preview on the registration form
  var photoInput = document.getElementById("id_photo");
  var photoPreview = document.getElementById("photoPreview");
  if (photoInput && photoPreview) {
    photoInput.addEventListener("change", function (e) {
      var file = e.target.files && e.target.files[0];
      if (!file) return;
      var reader = new FileReader();
      reader.onload = function (ev) {
        photoPreview.innerHTML = '<img src="' + ev.target.result + '" alt="Preview">';
      };
      reader.readAsDataURL(file);
    });
  }
});
