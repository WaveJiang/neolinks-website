# 备案验收脚本（本地文件，work/ 已被 .gitignore 忽略，不会提交）
# 用法： powershell -ExecutionPolicy Bypass -File .\work\beian-check.ps1
param([string]$Domain = 'neolinks.top')

$ErrorActionPreference = 'Continue'

function Get-Doh([string]$Url) {
  $raw = curl.exe -sS --ssl-no-revoke --max-time 20 -H "accept: application/dns-json" $Url 2>$null
  if (-not $raw) { return $null }
  try { return ($raw | ConvertFrom-Json) } catch { return $null }
}

Write-Host "===== 1. 解析状态（备案期间应为 NXDOMAIN = 已暂停解析）=====" -ForegroundColor Cyan
$targets = @(
  @{ Name = 'DNSPod  doh.pub';        Url = "https://doh.pub/dns-query?name=$Domain&type=A" },
  @{ Name = 'Google dns.google';      Url = "https://dns.google/resolve?name=$Domain&type=A" },
  @{ Name = 'Cloudflare';             Url = "https://cloudflare-dns.com/dns-query?name=$Domain&type=A" },
  @{ Name = 'AliDNS';                 Url = "https://dns.alidns.com/resolve?name=$Domain&type=A" }
)
$suspended = 0
foreach ($t in $targets) {
  $j = Get-Doh $t.Url
  if (-not $j) { Write-Host ("{0,-20} 查询失败（网络/代理问题）" -f $t.Name); continue }
  $answers = @($j.Answer | Where-Object { $_ -and $_.data })
  if ($answers.Count -eq 0) {
    $word = switch ($j.Status) { 3 { 'NXDOMAIN' } 0 { 'NOERROR 但无答案' } default { "Status=$($j.Status)" } }
    Write-Host ("{0,-20} 无解析结果  ({1})" -f $t.Name, $word) -ForegroundColor Green
    $suspended++
  } else {
    $ips = ($answers | ForEach-Object { $_.data }) -join ', '
    Write-Host ("{0,-20} 仍在解析: {1}" -f $t.Name, $ips) -ForegroundColor Yellow
  }
}

Write-Host ""
Write-Host "===== 2. 网站访问状态（备案期间应为 404 或无法连接）=====" -ForegroundColor Cyan
$closed = 0
$paths = @('/', '/index.html', '/privacy.html', '/version.json', '/README.md', '/assets/logo/neolinks-icon.png')
foreach ($p in $paths) {
  $b = [DateTime]::UtcNow.Ticks
  $code = curl.exe -sS -o NUL -w "%{http_code}" --ssl-no-revoke --max-time 20 "https://$Domain$p`?v=$b" 2>$null
  $note = switch ("$code") { '404' { '已关闭' } '000' { '无法连接（解析已暂停）' } '200' { '仍可访问！' } default { "状态码 $code" } }
  Write-Host ("{0,-34} {1,-5} {2}" -f $p, $code, $note)
  if ("$code" -eq '404' -or "$code" -eq '000') { $closed++ }
}

Write-Host ""
Write-Host "===== 结论 =====" -ForegroundColor Cyan
Write-Host ("解析: {0}/{1} 个公共 DNS 已无解析结果" -f $suspended, $targets.Count)
Write-Host ("访问: {0}/{1} 个路径已不可访问" -f $closed, $paths.Count)
if ($suspended -eq $targets.Count -and $closed -eq $paths.Count) {
  Write-Host "备案期间要求已满足：解析已暂停且网站无法访问。" -ForegroundColor Green
} else {
  Write-Host "尚未完全满足：解析仍需在 DNSPod 暂停（或在 TTL 600 秒内等待生效）。" -ForegroundColor Yellow
}
