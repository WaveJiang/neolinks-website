#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""暂停 / 删除 neolinks.top 上对外提供网站的解析记录（DNSPod 传统 API）。

用法：
    python work\\dnspod-records.py                    # 干跑：列出记录 + 显示将要暂停哪些（不改动）
    python work\\dnspod-records.py --apply            # 真正暂停（Record.Status -> disable，可一键恢复）
    python work\\dnspod-records.py --apply --delete   # 删除记录（Record.Remove，不可一键恢复）

Token 来源（按顺序，脚本不会打印 Token 内容）：
    1) 环境变量 DNSPOD_TOKEN，格式 "ID,Token"
    2) 文件 work\\dnspod-token.txt，内容为一行 "ID,Token"

只处理这些"对外提供网站"的记录，其他记录（NS、MX、TXT 等）一律不碰：
    @    A
    www  CNAME
"""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

DOMAIN = "neolinks.top"
# 国内站 dnsapi.cn 在当前出口 IP 上被 EdgeOne 拦成 401，故先试国际站同款传统 API。
HOSTS = ["https://api.dnspod.com/", "https://dnsapi.cn/"]
TARGETS = [("@", "A"), ("www", "CNAME")]
UA = "neolinks-beian-check/1.0 (python)"


def get_token():
    token = (os.environ.get("DNSPOD_TOKEN") or "").strip()
    if not token:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dnspod-token.txt")
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8-sig") as handle:
                for line in handle:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        token = line
                        break
    if not token or "," not in token:
        print("找不到可用的 DNSPod Token。")
        print(r"请把一行 'ID,Token' 写入 work\dnspod-token.txt（该目录已在 .gitignore 中），")
        print("或设置环境变量 DNSPOD_TOKEN 后重跑。")
        sys.exit(2)
    return token


TOKEN = get_token()


def call(action, **params):
    """调用 DNSPod 传统 API：按「主机 × 直连/系统代理」依次尝试，返回首个可解析的 JSON。"""
    data = {"login_token": TOKEN, "format": "json", "lang": "cn", "error_on_empty": "no"}
    data.update(params)
    body = urllib.parse.urlencode(data).encode("utf-8")
    attempts = [
        ("直连", urllib.request.build_opener(urllib.request.ProxyHandler({}))),
        ("经系统代理", urllib.request.build_opener()),
    ]
    failures = []
    for host in HOSTS:
        for label, opener in attempts:
            request = urllib.request.Request(
                host + action, data=body, method="POST",
                headers={"User-Agent": UA, "Content-Type": "application/x-www-form-urlencoded"},
            )
            try:
                with opener.open(request, timeout=30) as response:
                    raw = response.read().decode("utf-8", "replace")
            except urllib.error.HTTPError as error:
                failures.append("%s %s -> HTTP %s" % (host, label, error.code))
                continue
            except Exception as error:  # noqa: BLE001
                failures.append("%s %s -> %s: %s" % (host, label, type(error).__name__, error))
                continue
            try:
                return json.loads(raw), "%s %s" % (host, label)
            except ValueError:
                return {"_raw": raw}, "%s %s" % (host, label)
    print("调用 %s 失败：" % action)
    for item in failures:
        print("  - " + item)
    sys.exit(3)


def status_of(record):
    value = str(record.get("status", "") or "").lower()
    if value in ("enable", "disable"):
        return value
    enabled = str(record.get("enabled", "") or "")
    return "enable" if enabled == "1" else "disable"


def fetch_records():
    payload, route = call("Record.List", domain=DOMAIN)
    status = payload.get("status") or {}
    code = str(status.get("code", ""))
    if code != "1":
        print("Record.List 返回错误（%s）：%s" % (route, payload))
        print("常见原因：Token 填错 / 已删除、Token 不是主账号、该账号下没有 %s。" % DOMAIN)
        if str(status.get("message", "")).lower().find("token") >= 0:
            print("若提示 Incorrect token ID 且走的是 api.dnspod.com：该 Token 属于国内站（dnspod.cn），")
            print("而国内站 dnsapi.cn 在当前出口 IP 上被拦（HTTP 401）。这种情况请改用腾讯云 API 密钥")
            print("（API 3.0，dnspod.tencentcloudapi.com），我可以换签名方式重做。")
        sys.exit(4)
    return payload.get("records") or []


def show(records):
    print("%-6s %-6s %-34s %-9s %s" % ("NAME", "TYPE", "VALUE", "STATUS", "ID"))
    print("-" * 76)
    for record in records:
        print("%-6s %-6s %-34s %-9s %s" % (
            record.get("name", ""), record.get("type", ""), record.get("value", ""),
            status_of(record), record.get("id", ""),
        ))


def main():
    apply_changes = "--apply" in sys.argv
    delete_mode = "--delete" in sys.argv

    records = fetch_records()
    print("域名 %s 当前解析记录：" % DOMAIN)
    show(records)
    print()

    targets = [r for r in records if (r.get("name", ""), (r.get("type") or "").upper()) in TARGETS]
    if not targets:
        print("没有找到 @ A / www CNAME 记录，可能记录名或类型与预期不符，脚本不做任何改动。")
        sys.exit(5)

    extras = [
        r for r in records
        if r.get("name", "") in ("@", "www")
        and (r.get("type") or "").upper() in ("A", "AAAA", "CNAME")
        and r not in targets
    ]
    if extras:
        print("注意：@ / www 下还有这些同类记录，脚本不会自动处理：")
        show(extras)
        print()

    action_word = "删除" if delete_mode else "暂停"
    print("将对以下 %d 条记录执行【%s】：" % (len(targets), action_word))
    for record in targets:
        print("  - %s %s -> %s  (当前 %s, id=%s)" % (
            record.get("name"), record.get("type"), record.get("value"),
            status_of(record), record.get("id"),
        ))
    print()

    if not apply_changes:
        print("这是干跑（未加 --apply），没有做任何改动。")
        return

    changed = 0
    for record in targets:
        if not delete_mode and status_of(record) == "disable":
            print("跳过（已是暂停状态）：%s %s" % (record.get("name"), record.get("type")))
            continue
        if delete_mode:
            payload, route = call("Record.Remove", domain=DOMAIN, record_id=record.get("id"))
        else:
            payload, route = call("Record.Status", domain=DOMAIN,
                                  record_id=record.get("id"), status="disable")
        status = payload.get("status") or {}
        ok = str(status.get("code", "")) == "1"
        print("%s %s %s (id=%s) -> %s  [%s]" % (
            "删除" if delete_mode else "暂停",
            record.get("name"), record.get("type"), record.get("id"),
            "成功" if ok else "失败", status.get("message", payload),
        ))
        if ok:
            changed += 1

    print("\n改动 %d 条；重新拉取记录确认：" % changed)
    show(fetch_records())


if __name__ == "__main__":
    main()
