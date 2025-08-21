// Apply saved theme on page load
(function () {
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "dark") {
        document.body.classList.add("dark-mode");
        document.body.classList.remove("light-mode");
        const toggleBtn = document.getElementById("themeToggle");
        if (toggleBtn) toggleBtn.innerHTML = '<i class="fa-solid fa-sun"></i>';
    } else {
        document.body.classList.add("light-mode");
        document.body.classList.remove("dark-mode");
        const toggleBtn = document.getElementById("themeToggle");
        if (toggleBtn) toggleBtn.innerHTML = '<i class="fa-solid fa-moon"></i>';
    }
})();

document.getElementById("themeToggle").addEventListener("click", function () {
    const isDark = document.body.classList.toggle("dark-mode");
    document.body.classList.toggle("light-mode", !isDark);
    localStorage.setItem("theme", isDark ? "dark" : "light");
    this.innerHTML = isDark
        ? '<i class="fa-solid fa-sun"></i>'
        : '<i class="fa-solid fa-moon"></i>';
});
