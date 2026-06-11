(function () {
  "use strict";

  var sidebar = document.getElementById("sidebar");
  var overlay = document.getElementById("overlay");
  var menuToggle = document.getElementById("menuToggle");
  var closeSidebar = document.getElementById("closeSidebar");
  var themeToggle = document.getElementById("themeToggle");

  function openSidebar() {
    if (sidebar) sidebar.classList.add("sidebar-open");
    if (overlay) overlay.classList.add("active");
  }

  function closeSidebarFn() {
    if (sidebar) sidebar.classList.remove("sidebar-open");
    if (overlay) overlay.classList.remove("active");
  }

  if (menuToggle) menuToggle.addEventListener("click", openSidebar);
  if (closeSidebar) closeSidebar.addEventListener("click", closeSidebarFn);
  if (overlay) overlay.addEventListener("click", closeSidebarFn);

  if (themeToggle) {
    if (localStorage.getItem("dashboard-theme") === "dark") {
      document.body.classList.add("dark-mode");
    }
    themeToggle.addEventListener("click", function () {
      document.body.classList.toggle("dark-mode");
      localStorage.setItem(
        "dashboard-theme",
        document.body.classList.contains("dark-mode") ? "dark" : "light"
      );
    });
  }

  if (window.dashboardChart && window.Chart) {
    var canvas = document.getElementById("contentChart");
    if (canvas) {
      new Chart(canvas, {
        type: "bar",
        data: {
          labels: window.dashboardChart.labels,
          datasets: [{
            label: "Entries",
            data: window.dashboardChart.values,
            backgroundColor: "rgba(8, 102, 255, 0.7)",
            borderRadius: 6,
          }],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            y: { beginAtZero: true, ticks: { stepSize: 1 } },
          },
        },
      });
    }
  }
})();
