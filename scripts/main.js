const appConfig = {
  minAndroidVersion: "Android 8.0 及以上",
  downloadUrl: "https://wwbah.lanzoul.com/b01eunew0b",
  downloadPageUrl: "#download",
  downloadPassword: "24fr"
};

function applyConfig() {
  document.querySelectorAll("[data-config]").forEach((element) => {
    const key = element.dataset.config;

    if (Object.prototype.hasOwnProperty.call(appConfig, key)) {
      element.textContent = appConfig[key];
    }
  });

  document.querySelectorAll(".download-link, .releases-link").forEach((link) => {
    link.href = appConfig.downloadPageUrl;
    link.removeAttribute("target");
    link.setAttribute("aria-label", "查看 NeoLinks 下载方式、提取密码和二维码");
  });

  document.querySelectorAll(".download-external-link").forEach((link) => {
    link.href = appConfig.downloadUrl;
    link.target = "_blank";
    link.setAttribute("aria-label", "前往蓝奏云下载 NeoLinks");
  });

}

function setupMobileMenu() {
  const toggle = document.querySelector(".menu-toggle");
  const menu = document.querySelector(".nav-menu");

  if (!toggle || !menu) return;

  const closeMenu = () => {
    toggle.setAttribute("aria-expanded", "false");
    menu.classList.remove("is-open");
  };

  toggle.addEventListener("click", () => {
    const willOpen = toggle.getAttribute("aria-expanded") !== "true";

    toggle.setAttribute("aria-expanded", String(willOpen));
    menu.classList.toggle("is-open", willOpen);
  });

  menu.querySelectorAll("a").forEach((link) => link.addEventListener("click", closeMenu));

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeMenu();
      toggle.focus();
    }
  });

  document.addEventListener("click", (event) => {
    if (!menu.contains(event.target) && !toggle.contains(event.target)) {
      closeMenu();
    }
  });
}

function setupRevealAnimation() {
  const items = document.querySelectorAll(".reveal");

  if (!items.length) return;

  if (
    window.matchMedia("(prefers-reduced-motion: reduce)").matches ||
    !("IntersectionObserver" in window)
  ) {
    items.forEach((item) => item.classList.add("is-visible"));
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12 }
  );

  items.forEach((item) => observer.observe(item));
}

function setCurrentYear() {
  const year = document.querySelector("#current-year");

  if (year) year.textContent = new Date().getFullYear();
}

applyConfig();

setupMobileMenu();
setupRevealAnimation();
setCurrentYear();
