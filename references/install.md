> 📌 wechat-article · MIT License · Author: Darrius · https://github.com/DarriusHQ/wechat-article-skill

# 团队安装说明（Windows / macOS 通用）

## 1. 放置 skill

把整个 `wechat-article/` 文件夹放入技能目录之一：

- 个人全局：`~/.agents/skills/wechat-article/`
- 某个项目内：`<项目>/.agents/skills/wechat-article/`

放置后重启 agent 会话即可被识别。

## 2. 依赖安装

### 必需

- **python3 ≥ 3.7**：Windows 从 python.org 安装，勾选 "Add to PATH"；macOS 自带
- 验证：`python3 --version`（Windows 可能是 `python --version`）

### 可选（按需，缺失不影响主流程）

| 能力 | 安装 | 用途 |
|---|---|---|
| 截图裁剪 | `pip install pillow` | 第 6 阶段截图裁剪 |
| Demo 真实截图 | 安装 Node.js LTS → `npm i -g playwright-cli` → `npx playwright install chromium` | 第 6 阶段产品截图 |
| 文风完整检查 | `npx skills add op7418/humanizer-zh` | 第 5 阶段 humanize 复检 |

三者都不装也能出稿：截图改 AI 生图 Prompt、文风用内置检查单。

## 3. 使用

对 agent 说：

- 「帮我写本月公众号推文」
- 「用 wechat-article 写一篇 XX 主题的软文」
- 「给新公众号建档，链接如下：……」

首次使用新公众号，先走建档（阶段 0），提供 5~10 篇近期文章链接。

## 4. 常见问题

- **抓文章失败**：确认链接是 `mp.weixin.qq.com/s/...` 全文链接；公司网络有限制时换手机热点重试
- **playwright 截图报错**：先 `npx playwright install chromium`；演示环境按剧本只用页面内按钮导航，不要刷新
- **中文字体报错**：裁剪脚本不涉及字体，如遇其他脚本报 UnicodeDecodeError，确认用 `python3` 而非 python2
