# -*- coding: utf-8 -*-
"""
wechat-article · MIT License · Author: Darrius · https://github.com/DarriusHQ/wechat-article-skill

公众号文章抓取脚本：输入文章链接，提取标题/公众号/发布时间/正文，存为 txt。
纯 Python 标准库，Windows / macOS / Linux 通用。

用法：
  python3 fetch_wx_articles.py <链接1> <链接2> ...        # 直接给链接
  python3 fetch_wx_articles.py -f links.txt -o ./抓取结果  # 从文件读链接（每行一条）

说明：
  - 链接为 mp.weixin.qq.com/s/... 全文链接（永久有效）
  - 抓取结果用于「账号建档 / 增量更新档案」（见 SKILL.md 阶段 0）
  - 个别文章若开启了防爬验证会抓不到，脚本会明确报错并列出失败清单
"""

import argparse
import json
import pathlib
import re
import sys
import time
import urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")


def http_get(url: str, retries: int = 2, timeout: int = 20) -> str:
    last_err = None
    for i in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8", errors="ignore")
        except Exception as e:  # noqa: BLE001
            last_err = e
            if i < retries:
                time.sleep(2 * (i + 1))
    raise RuntimeError(f"请求失败: {last_err}")


def strip_tags(fragment: str) -> str:
    text = re.sub(r"<[^>]+>", "\n", fragment)
    text = (text.replace("&nbsp;", " ").replace("&amp;", "&")
                .replace("&lt;", "<").replace("&gt;", ">")
                .replace("&quot;", '"').replace("&#39;", "'"))
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n\s*\n+", "\n", text)
    return text.strip()


def extract(html: str) -> dict:
    m = (re.search(r'<h1[^>]*class="rich_media_title"[^>]*>(.*?)</h1>', html, re.S)
         or re.search(r'<meta property="og:title" content="([^"]*)"', html))
    title = m.group(1).strip() if m else ""
    if "<" in title:
        title = strip_tags(title)

    m = (re.search(r'<strong class="profile_nickname"[^>]*>(.*?)</strong>', html, re.S)
         or re.search(r'var nickname = htmlDecode\("([^"]*)"\)', html))
    account = m.group(1).strip() if m else ""

    m = (re.search(r"var createTime = '([^']*)'", html)
         or re.search(r'<em id="publish_time"[^>]*>(.*?)</em>', html, re.S))
    pub = m.group(1).strip() if m else ""

    mc = (re.search(r'<div[^>]*id="js_content"[^>]*>(.*?)</div>\s*<script', html, re.S)
          or re.search(r'<div[^>]*id="js_content"[^>]*>(.*)', html, re.S))
    body = mc.group(1) if mc else ""
    body = re.sub(r"<script.*?</script>", "", body, flags=re.S)
    body = re.sub(r"<style.*?</style>", "", body, flags=re.S)
    img_count = len(re.findall(r'data-src="[^"]*mmbiz[^"]*"', body))
    text = strip_tags(body)

    return {
        "title": title or "(未解析到标题，可能触发了验证，请换网络重试)",
        "account": account,
        "publish_time": pub,
        "image_count": img_count,
        "content": text,
        "ok": bool(text),
    }


def safe_name(s: str) -> str:
    return re.sub(r'[\\/:*?"<>|\s]+', "_", s)[:50]


def main() -> int:
    ap = argparse.ArgumentParser(description="公众号文章抓取（建档/增量更新用）")
    ap.add_argument("urls", nargs="*", help="文章链接（空格分隔多条）")
    ap.add_argument("-f", "--file", help="从文本文件读取链接（每行一条）")
    ap.add_argument("-o", "--out", default="./抓取结果", help="输出目录（默认 ./抓取结果）")
    ap.add_argument("--json", action="store_true", help="额外输出汇总 JSON")
    args = ap.parse_args()

    urls = list(args.urls)
    if args.file:
        lines = pathlib.Path(args.file).read_text(encoding="utf-8").splitlines()
        urls += [ln.strip() for ln in lines if ln.strip() and not ln.startswith("#")]
    urls = [u for u in urls if u.startswith("http")]
    if not urls:
        ap.print_help()
        print("\n错误：未提供任何链接。")
        return 2

    out_dir = pathlib.Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    ok_list, fail_list = [], []
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] 抓取中：{url}")
        try:
            item = extract(http_get(url))
        except RuntimeError as e:
            print(f"  ✗ {e}")
            fail_list.append(url)
            continue
        if not item["ok"]:
            print("  ✗ 未取到正文（可能触发防爬验证），请换网络或稍后重试")
            fail_list.append(url)
            continue
        name = f"{i:02d}_{safe_name(item['title'])}.txt"
        header = (f"标题: {item['title']}\n公众号: {item['account']}\n"
                  f"时间: {item['publish_time']}\n图片数: {item['image_count']}\n链接: {url}\n--- 正文 ---\n")
        (out_dir / name).write_text(header + item["content"], encoding="utf-8")
        print(f"  ✓ {item['title']}（{len(item['content'])} 字）")
        ok_list.append(item)

    if args.json:
        (out_dir / "汇总.json").write_text(
            json.dumps(ok_list, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n完成：成功 {len(ok_list)} 篇，失败 {len(fail_list)} 篇，输出目录：{out_dir.resolve()}")
    if fail_list:
        print("失败链接（请换网络重试或手动复制正文）：")
        for u in fail_list:
            print("  " + u)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
