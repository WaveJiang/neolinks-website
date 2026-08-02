const appConfig = {
  minAndroidVersion: "Android 8.0 及以上",
  downloadUrl: "https://wwbah.lanzoul.com/b01eunew0b",
  downloadPageUrl: "#download",
  downloadPassword: "24fr",
  feedbackUrl: "https://wj.qq.com/s2/27422059/gvdu/",
  userGuideUrl: "USER_GUIDE_URL"
};

const placeholderTokens = [
  "FEISHU_FORM_URL",
  "USER_GUIDE_URL"
];

function isPlaceholderUrl(url) {
  return !url || placeholderTokens.some((token) => url.includes(token));
}

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

  document.querySelectorAll(".feedback-link").forEach((link) => {
    link.href = appConfig.feedbackUrl;
  });
}

function setupPlaceholderLinks() {
  document.addEventListener("click", (event) => {
    const link = event.target.closest("a");

    if (!link || !isPlaceholderUrl(link.href)) return;

    event.preventDefault();
    window.alert("此链接仍是占位配置，请先在 scripts/main.js 中替换对应地址。");
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
setupPlaceholderLinks();
setupMobileMenu();
setupRevealAnimation();
setCurrentYear();
