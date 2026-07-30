# NeoLinks 官方网站

NeoLinks 的纯静态官方网站，可直接部署到 GitHub Pages。项目只使用 HTML、CSS 和原生 JavaScript，不需要安装 Node.js，也不需要服务器、数据库或构建工具。

> 重要：本仓库只能存放官网文件。不要放入 NeoLinks Android 项目源代码、正式签名 APK、KeyStore、签名密码、API 密钥或其他敏感信息。当前官网主下载使用蓝奏云，GitHub Releases 可作为备份发布渠道。

## 项目结构

```text
.
├── index.html
├── privacy.html
├── styles/
│   └── main.css
├── scripts/
│   └── main.js
├── assets/
│   ├── logo/
│   │   ├── neolinks-icon.png
│   │   └── neolinks-wordmark.png
│   └── screenshots/
│       ├── screenshot-placeholder-1.svg
│       ├── screenshot-placeholder-2.svg
│       ├── screenshot-placeholder-3.svg
│       └── screenshot-placeholder-4.svg
├── .gitignore
└── README.md
```

所有站内资源均使用相对路径，因此兼容以下 GitHub Pages 项目仓库地址：

```text
https://你的用户名.github.io/neolinks-website/
```

## 发布前必须修改的配置

打开 `scripts/main.js`，修改文件顶部的 `appConfig`：

```javascript
const appConfig = {
  minAndroidVersion: "Android 8.0 及以上",
  downloadUrl: "https://wwbah.lanzoul.com/b01eunew0b",
  downloadPassword: "24fr",
  feedbackUrl: "https://wj.qq.com/s2/27422059/gvdu/",
  userGuideUrl: "USER_GUIDE_URL"
};
```

- 确认最低 Android 版本。
- `downloadUrl` 已设置为蓝奏云下载页面。
- `downloadPassword` 已设置为 `24fr`。
- `feedbackUrl` 已设置为腾讯问卷。
- `userGuideUrl` 当前未在页面展示，保留给以后增加使用说明入口。

官网不展示版本号、APK 大小、更新日期和更新日志，这些信息统一以蓝奏云页面为准，因此上传新 APK 时通常无需修改官网。系统要求、下载链接和提取密码从该配置统一读取。

## 本地预览

最简单的方法是直接双击 `index.html`。主要页面能够正常打开，但更推荐启动一个本地静态服务器，以便模拟 GitHub Pages：

### 使用 Python

1. 在项目文件夹的空白处按住 Shift 并点击鼠标右键。
2. 选择“在此处打开 PowerShell 窗口”或“在终端中打开”。
3. 输入：

```powershell
python -m http.server 8000
```

4. 用浏览器打开：

```text
http://localhost:8000/
```

5. 预览结束后回到终端，按 `Ctrl + C` 停止。

## 新手教程：部署到 GitHub Pages

### 1. 创建 GitHub 仓库

1. 打开 [GitHub](https://github.com/) 并登录。
2. 点击右上角 `+`，选择 `New repository`。
3. 在 `Repository name` 中填写仓库名，例如 `neolinks-website`。
4. 建议选择 `Public`。免费账户的 GitHub Pages 通常使用公开仓库最简单。
5. 不要勾选自动创建 README、`.gitignore` 或 License，因为本项目已经包含这些文件。
6. 点击 `Create repository`。

### 2. 上传官网文件

适合新手的网页上传方式：

1. 进入刚创建的仓库。
2. 点击 `uploading an existing file`；如果仓库已有文件，点击 `Add file` → `Upload files`。
3. 将本项目中的 `index.html`、`privacy.html`、`styles`、`scripts`、`assets`、`.gitignore` 和 `README.md` 一起拖入上传区域。
4. 确认文件夹结构没有被打散。
5. 在页面底部填写提交说明，例如 `Add NeoLinks website`。
6. 点击 `Commit changes`。

如果 `.gitignore` 在文件选择器中不可见，可先在 Windows 资源管理器中打开“显示隐藏的项目”，或稍后通过 Git 命令上传。

### 3. 进入仓库 Settings

1. 打开仓库首页。
2. 点击仓库顶部的 `Settings`。
3. 如果窗口较窄，`Settings` 可能藏在顶部的 `…` 菜单中。

### 4. 打开 Pages

1. 在 Settings 左侧菜单找到 `Code and automation`。
2. 点击 `Pages`。

### 5. 选择从 main 分支部署

1. 在 `Build and deployment` 区域，将 `Source` 选择为 `Deploy from a branch`。
2. 在 `Branch` 中选择 `main`。

### 6. 选择根目录

1. 在分支右侧的文件夹选项中选择 `/ (root)`。
2. 点击 `Save`。

这里的界面通常显示为 `/ (root)`，含义是从仓库根目录发布，不是创建名为 `root` 的文件夹。

### 7. 获得网站地址

1. 保存后等待约 1～5 分钟。
2. 刷新 Pages 设置页面。
3. 页面会显示已发布的网站地址，通常是：

```text
https://你的用户名.github.io/neolinks-website/
```

4. 点击 `Visit site` 打开官网。

如果页面暂时显示 404，请等待一两分钟后再次刷新，并确认仓库根目录存在 `index.html`。

### 8. 绑定自定义域名

准备好域名后：

1. 进入仓库 `Settings` → `Pages`。
2. 在 `Custom domain` 中填写域名，例如 `neolinks.example.com`。
3. 点击 `Save`。
4. 到域名服务商的 DNS 管理页面添加记录。
5. 使用子域名时，通常添加一条 `CNAME`，将 `neolinks` 指向 `你的用户名.github.io`。
6. 使用根域名时，需要按照 GitHub 当前页面给出的 A/AAAA 记录进行设置。
7. DNS 生效可能需要几分钟到 48 小时。

GitHub 保存自定义域名后可能会在仓库中自动创建 `CNAME` 文件，请保留它。

### 9. 启用 HTTPS

1. 自定义域名验证通过后，仍在 `Settings` → `Pages`。
2. 勾选 `Enforce HTTPS`。
3. 如果选项暂时不可用，等待 GitHub 签发证书后再试。
4. GitHub 默认的 `github.io` 地址会自动使用 HTTPS。

### 10. 修改网站内容

- 修改版本信息和链接：编辑 `scripts/main.js` 顶部的 `appConfig`。
- 修改页面功能介绍或其他固定文字：编辑 `index.html`。
- 修改视觉样式：编辑 `styles/main.css`。
- 替换截图：将真实截图放入 `assets/screenshots/`，并沿用现有文件名；如果使用 PNG/JPG，请同步修改 `index.html` 中相应后缀。
- 替换 Logo：覆盖 `assets/logo/neolinks-icon.png` 和 `assets/logo/neolinks-wordmark.png`。

每次修改后，在 GitHub 文件编辑页面点击 `Commit changes`。GitHub Pages 会自动重新发布，通常几分钟内生效。

## 当前主下载：蓝奏云

官网的“立即下载”、导航下载按钮、页脚下载入口和二维码均指向：

```text
https://wwbah.lanzoul.com/b01eunew0b
```

提取密码：

```text
24fr
```

更新 APK 后，请在蓝奏云中确认该分享链接仍可使用。如果更换了分享链接或密码，只需修改 `scripts/main.js` 中的 `downloadUrl` 和 `downloadPassword`，并重新生成二维码。

## 可选备份：发布 GitHub Release

APK 不应提交到官网文件列表中。除蓝奏云外，也可以使用 GitHub Releases 作为备用下载渠道。

1. 进入准备存放 APK 的 GitHub 仓库。
2. 在仓库首页右侧点击 `Releases`。如果没看到，点击顶部 `Code`，再在页面右侧寻找。
3. 点击 `Create a new release` 或 `Draft a new release`。
4. 点击 `Choose a tag`，输入版本标签，例如 `v0.3.1`，然后选择创建这个标签。
5. 填写 Release 标题，例如 `NeoLinks V0.3.1`。
6. 将已经正式签名的 APK 固定命名为：

```text
NeoLinks.apk
```

7. 把 `NeoLinks.apk` 拖入附件上传区域。
8. 在说明中填写本次更新内容。
9. 确认无误后点击 `Publish release`。

如果以后需要切回 GitHub Releases，可将 `downloadUrl` 改为：

```text
https://github.com/GITHUB_USERNAME/GITHUB_REPOSITORY/releases/latest/download/NeoLinks.apk
```

必须确保：

- APK 已使用正式发布签名。
- 不要上传 KeyStore、`.jks`、`.keystore` 或签名密码。
- 后续版本必须使用同一个签名，否则用户无法覆盖安装更新。
- 每个最新版 Release 的附件都必须准确命名为 `NeoLinks.apk`，包括大小写。
- 不要把 Android App 源代码放到官网仓库。
- 发布后亲自点击官网“立即下载”，确认得到的是正确版本。

## 替换截图和二维码

当前截图是明确标注的占位图：

- `screenshot-placeholder-1.svg`：图库首页
- `screenshot-placeholder-2.svg`：动态照片
- `screenshot-placeholder-3.svg`：影像信息
- `screenshot-placeholder-4.svg`：相册管理

推荐提供 1080 × 2340 或接近 9:19.5 比例的竖屏截图。页面使用 `object-fit: cover`，但设备框和占位图本身均按手机比例设计；如果不希望任何裁切，可将 CSS 中截图的 `object-fit` 改为 `contain`。

正式二维码位于 `assets/qr-code/neolinks-download-qr.png`，当前指向蓝奏云下载页面。更换下载链接后，请重新生成二维码并覆盖这个文件。

## 发布前检查清单

- [ ] Android 最低版本正确
- [ ] 官网下载按钮能打开正确的蓝奏云页面
- [ ] 蓝奏云提取密码 `24fr` 正确
- [ ] 腾讯问卷可以打开
- [ ] 已替换真实应用截图或接受占位图继续显示
- [ ] 下载二维码可以识别并打开正确链接
- [ ] 已核对并完善 `privacy.html` 中所有“待确认 / 待填写”
- [ ] 没有提交 APK、Android 源代码、KeyStore、密码、密钥或 `.env`
- [ ] 手机浏览器中导航、下载按钮和截图横向滑动正常
- [ ] 自定义域名（如使用）已启用 HTTPS
