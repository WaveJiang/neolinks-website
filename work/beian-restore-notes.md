# 备案期间「关闭访问」改动与恢复清单

本地备忘（`work/` 已在 `.gitignore` 中，不会提交到仓库）
日期：2026-09-17　域名：neolinks.top / www.neolinks.top

## 一、已完成的仓库改动（GitHub: WaveJiang/neolinks-website, main）

| 提交 | 内容 |
|---|---|
| `8c30840` | 撤下 `index.html`、`privacy.html`，新增空白 `404.html` |
| `eaa175a` | 新增 `.nojekyll`，关掉 Jekyll（否则它用 README 生成首页并返回 HTTP 200） |
| `72e7c01` | 撤下 `README.md`、`robots.txt`、`sitemap.xml`、`version.json`、`assets/`、`styles/`、`scripts/` |

当前 `main` 上只保留 `.gitignore`、`.nojekyll`、`404.html`、`CNAME`。

实测结果：`neolinks.top` 下任意路径（首页、隐私政策、version.json、README、静态资源、随机路径、/admin/）
全部返回 **HTTP 404 + 空白页**（267 字节），符合管局「关闭访问」的要求。

## 二、解析记录（DNSPod）—— 已删除 ✅（2026-09-17 17:15）

三条记录已在 DNSPod 控制台（域名所有者的账号）逐条删除，控制台提示「删除成功」，记录数由 3 条 → 0 条：

- `@`   A     `185.199.108.153` ✅
- `@`   A     `185.199.109.153` ✅
- `www` CNAME `wavejiang.github.io.` ✅

复核：doh.pub、dns.google、Cloudflare、AliDNS 四家公共 DNS 对 `neolinks.top` 均返回 NOERROR 且**无答案**，对 `www.neolinks.top` 返回 **NXDOMAIN**，域名已不解析。

> 执行方式：浏览器自动化直接操作已登录的 DNSPod 控制台（途中会话过期，点了腾讯云的「立即登录」续期）。备用的 API 方案（`work\dnspod-records.py` + `work\dnspod-token.txt`）最终未使用。
> 该脚本只处理 `@` 的 A 记录与 `www` 的 CNAME 记录，不碰 NS、MX、TXT 及其他子域名。

### 备用：以后若要改用 API 操作

```
python work\dnspod-records.py                    # 干跑：只列记录 + 显示计划
python work\dnspod-records.py --apply --delete   # 删除 @ A / www CNAME
```

### 被删除的 3 条记录（恢复时按此重建，TTL 600）

| 主机 | 类型 | 值 |
|---|---|---|
| `@` | A | `185.199.108.153` |
| `@` | A | `185.199.109.153` |
| `www` | CNAME | `wavejiang.github.io` |

（这 4 个 GitHub Pages 的 A 记录为 `185.199.108/109/110/111.153`，原配置只用了前两个。）

### 关于 DNSPod API 的注意事项

- 国内站 `dnsapi.cn` 从本机出口 IP 被 EdgeOne 拦成 **HTTP 401**（官方文档的原样 curl 也一样），脚本因此优先走国际站 `api.dnspod.com`（实测可用）。
- 若 URL 报 `10002 Incorrect token ID`，说明 Token 与域名不在同一账号体系，改用腾讯云 API 3.0（`dnspod.tencentcloudapi.com`，实测可达）的签名方式。
- 用完 Token 请立即在 DNSPod 密钥管理中删除。

## 三、验收

```powershell
powershell -ExecutionPolicy Bypass -File .\work\beian-check.ps1
```

判定标准：解析那一节出现 4 个「无解析结果」，访问那一节全部为 404 / 无法连接。

> 该脚本含中文，必须保存为**带 BOM 的 UTF-8**；PowerShell 5.1 会把无 BOM 的 `.ps1` 当 ANSI 读取，导致乱码和语法错误。用编辑器改过之后记得补回 BOM。

## 四、备案通过后恢复

```powershell
cd E:\Github\neolinks-website
git revert --no-edit 72e7c01 8c30840
git push origin main
```

只想恢复页面、暂不恢复 README 等文件时，只 revert `8c30840` 即可。

- 保留 `eaa175a` 的 `.nojekyll`（不要 revert）：这个站没用任何 Jekyll 特性，关掉它可避免「README 变首页 200」和中文乱码。
- 在 DNSPod 按上表**重建**这 3 条解析记录（记录是删除的，不能用开关恢复；TTL 填 600 即可）。
- 恢复后按 README 的搜索优化步骤重新提交 `sitemap.xml`：404 期间搜索引擎会把已收录页面清掉。
- 抽查首页、隐私政策、二维码图片（`assets/qr-code/neolinks-download-qr.png`）和蓝奏云下载链接。
