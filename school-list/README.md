# school-list

给学生出大约 20 所学校的选校清单。任意 Agent 读本夹里的 `SKILL.md` 即可。

怎么找先读 [strategy.md](strategy.md)：学校第一；好看、好申、匹配；同校一高一低；别全搞难的。

浏览器强制：[browser.md](browser.md)。Mac 只用 **ego-lite**（`ego-browser`），Windows 只用 **Browser OS NEO**。本包不含这两份技能，也不准覆盖它们。

细则：`catalog.md`（查库）、`template.md`（填 Excel）、`examples.md`（怎么喊）。脚本在 `scripts/`。

库和模板的路径每次现找，不要写死盘符。

## 只装这一夹

不要把整个技能仓装进 skills 目录，那会铺一堆无关技能，看起来像把原来的技能冲掉。

```bash
npx skills add Shilaidong/essay-skills --skill school-list -g -y
```

只要这一夹时，也可以把 `school-list/` 整夹拷到目标 Agent 的 skills 目录，**不要覆盖同名以外的夹**。

## ego-lite 技能丢了（Mac）

`school-list` 的 `name` 是 `school-list`，不会写成 `ego-browser`，单独装这一夹不会覆盖 ego-lite。

若整仓安装或把仓直接铺到 skills 根目录，目录会被铺满，ego-lite 的夹可能被挤掉或不再出现在列表里。找回来：

1. 打开 **ego lite**，再走一遍引导（会重新挂上 `ego-browser` 命令，通常在 `~/.local/bin`）。
2. 把应用包里的 `ego-skills/ego-browser` 拷回**各 Agent 自己的 skills 目录**（应用一般在 `/Applications/ego lite.app`）。没有那条路径就在应用包里搜 `ego-browser/SKILL.md`。拷完新开一轮对话。
