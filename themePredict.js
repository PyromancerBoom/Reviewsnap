const toggleThemeButton = document.getElementById("toggle-theme-button");
const body = document.body;

toggleThemeButton.addEventListener("click", function () {
  body.classList.toggle("dark-mode");
});
