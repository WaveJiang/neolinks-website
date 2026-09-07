"use strict";
const year = document.querySelector("#current-year");
if (year) year.textContent = new Date().getFullYear();
document.querySelectorAll("[data-copy]").forEach((button) => {
  button.addEventListener("click", async () => {
    const status = document.querySelector("#copy-status");
    try {
      await navigator.clipboard.writeText(button.dataset.copy);
      status.textContent = "提取码已复制，打开蓝奏云后粘贴即可。";
    } catch {
      status.textContent = "请手动复制提取码：" + button.dataset.copy;
    }
  });
});
