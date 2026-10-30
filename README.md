# wechat-article · 微信公众号软文生成 Agent Skill

> 生成可直接发布的微信公众号软文的一个可复用 [Agent Skill](https://agentskills.io)。
> 覆盖**账号建档 → 选题对齐 → 素材分级 → 场景化写作 → 严谨性审查 → 去 AI 文风 → 配图 → 标题打磨**的完整七阶段流程，产出可直接排版发布的 `.md` 与配图。

源自林草行业 B 端公众号的实战复盘，方法论对政企向行业账号通用。

## 为什么需要它

让 AI 写公众号文章不难，难的是写出**能直接发**的文章。直接让 AI 动笔，通常会踩三类坑：

| 坑 | 表现 | 本 Skill 的对策 |
|---|---|---|
| **数字翻车** | 把内部访谈口径、征求意见稿的数字当公开事实写进正文 | 素材三级分级（A 可引用 / B 只用结构 / C 数值禁用），写作前定级 |
| **AI 味扑鼻** | 破折号堆砌、"不仅…更是…"、三段式滥用、口语化到看不懂 | 内置去 AI 文风检查单 + 可选接入 [humanizer-zh](https://github.com/op7418/humanizer-zh) 复检，评分门禁 |
| **场景写错** | 对产品主线理解偏差，成稿方向错误 | 选题与案例定位双重用户确认门禁，未确认不动笔 |

## 七阶段流水线

```text
阶段0 账号档案 → 阶段1 选题方案【门禁A:用户确认】→ 阶段2 素材盘点分级
→ 阶段3 场景化写作 → 阶段4 严谨性审查【门禁B:清单全过】
→ 阶段5 文风检查【门禁C:≥40/50】→ 阶段6 配图【门禁D:图文对齐】
→ 阶段7 标题打磨与交付
```

- **账号档案**（`accounts/<账号名>.yaml`）：定位、受众、语境属性、品牌口号库、标题骨架、文章索引（选题查重）、高频引用规范、语境红线
- **中间产物留痕**：选题方案、素材分级、严谨审查记录、文风检查记录落盘存档，团队协作可追溯
- **配图规范**：头图 AI 生图 Prompt 模板 + 真实系统截图流程（含内部术语裁剪规则），图文互检

## 快速开始

```bash
# 1. 克隆到 Agent 技能目录（二选一）
git clone https://github.com/DarriusHQ/wechat-article-skill.git ~/.agents/skills/wechat-article
# 或项目级：<项目>/.agents/skills/wechat-article

# 2. 重启 agent 会话，即可被识别

# 3. 新账号先建档：提供 5~10 篇近期文章链接
#    > "帮我给「某某公众号」建账号档案，链接：..."
# 4. 之后随时：
#    > "写本月公众号推文" / "写一篇 XX 主题的软文"
```

依赖与可选能力见 [`references/install.md`](references/install.md)。**降级策略**：可选依赖缺失时流程不中断（无 Pillow 交原图、无 playwright 走 AI 生图、无 humanizer-zh 用内置检查单）。

## 目录结构

```text
wechat-article/
├── SKILL.md                        # 主流程：三条铁律 + 七阶段流水线
├── accounts/
│   └── example.yaml                # 账号档案示例（虚构数据，照此格式建档）
├── references/
│   ├── style-guide.md              # 文风规范：结构模板、术语翻译、政企语境
│   ├── rigor-checklist.md          # 严谨清单：素材三级分级、数字审查
│   ├── humanize-checklist.md       # 去 AI 文风检查单（离线可用）
│   ├── image-guide.md              # 配图规范：Prompt 模板、截图流程
│   └── install.md                  # 安装说明（Windows / macOS 通用）
└── scripts/
    ├── fetch_wx_articles.py        # 公众号文章抓取（纯标准库）
    └── crop_image.py               # 截图裁剪（需 Pillow）
```

## 隐私约定

`accounts/` 下除 `example.yaml`（虚构示例）外的真实账号档案**不入库**（见 `.gitignore`），属各团队私有资产。请勿将客户业务档案提交到公开仓库。

## License

[MIT](LICENSE) © Darrius
