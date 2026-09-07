# NeoLinks 官网

纯 HTML、CSS、原生 JavaScript 网站，可直接部署至 GitHub Pages。正式域名为 https://neolinks.top/，由根目录 CNAME 配置。

## 本地预览

在仓库根目录运行任意静态 HTTP 服务器，例如 `python -m http.server 8000`，然后打开 http://localhost:8000/。

## 内容维护

- `index.html`：首页文案、截图、FAQ、下载链接、提取码和搜索元数据。核心信息直接写在 HTML 中，关闭 JavaScript 也能阅读、展开 FAQ 和下载。
- `styles/main.css`：首页和隐私政策页的响应式样式，包含手机布局、键盘焦点与减少动画适配。
- `scripts/main.js`：提取码复制和版权年份。剪贴板不可用时显示手动复制提示。
- `privacy.html`：现有隐私政策；政策内容应与 App 的实际数据处理一致。
- `assets/screenshots/`：现有应用界面图片。替换时核对图片宽高与 alt 描述。
- `assets/qr-code/neolinks-download-qr.png`：蓝奏云下载二维码。

下载地址为 https://wwbah.lanzoul.com/b01eunew0b，提取码为 `24fr`。更换地址时同步更新首页下载链接、JSON-LD 中的 downloadUrl、二维码。更换密码时同步更新下载区可见文字、按钮 data-copy 和安装 FAQ。

## 搜索优化

首页已包含描述性标题、description、canonical、Open Graph、Twitter 卡片、WebSite / SoftwareApplication 结构化数据、图片替代文字、语义化标题、可抓取的原生链接与常见问题。没有添加未经证实的评分、价格、版本号或兼容性承诺。截图按需延迟加载，首屏图片优先加载，无外部字体或前端框架依赖。

`robots.txt` 允许抓取，`sitemap.xml` 使用正式域名。只有页面实际变化时才更新对应 lastmod。

发布后仍需由站点所有者完成：

1. 在 Google Search Console 和 Bing Webmaster Tools 验证 `https://neolinks.top/`；如面向百度搜索，也在百度搜索资源平台按当前开放能力验证站点。
2. 提交 `https://neolinks.top/sitemap.xml`，检查首页是否可以抓取，使用平台提供的 URL 检查或收录提交功能。
3. 在 App 的关于页、蓝奏云说明、真实的社区介绍中统一使用 NeoLinks 名称，并链接回正式域名。
4. 持续根据搜索词补充真实、有帮助的使用说明，并观察收录和自然搜索点击。技术优化和站点地图不保证收录或排名。

参考：Google SEO 入门指南 https://developers.google.com/search/docs/fundamentals/seo-starter-guide

## 发布

推送到 GitHub Pages 配置的发布分支后生效。正式发布后检查 HTTPS、主页、隐私政策、二维码和下载地址，再提交站点地图。

## 冻结文件：version.json

自 2026-09-06 起，App 更新已经切换到 CloudBase 分发中心。`version.json` 保持 1.0.2 / 102 / forceUpdate:true，继续引导 0.4.x 及更早版本用户升级。不要修改本文件的任何字段，也不要随网站更新调整它。

本仓库仅放官网资源，不要提交 Android 源代码、APK、KeyStore、密钥或其他敏感文件。
