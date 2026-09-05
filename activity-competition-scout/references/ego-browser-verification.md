# ego-browser 真实浏览器官方核查实战指南

本指南提供了使用 `ego-browser`（基于真实 Chromium 的隔离环境）对国际高中生学术科创与商业设计竞赛进行 100% 官方溯源核查的完整实操流程与脚本范式。

---

## 为什么必须使用 ego-browser 而非单纯 Web Fetch / 搜索 API？

1. **规避反爬虫与 JS 动态渲染**：绝大多数全球知名科创与商业竞赛官网（如 `conradchallenge.org`, `technovationgirls.org`, `chinathinksbig.com`）重度依赖前端 React/Vue/Webflow 动态渲染，静态 HTML 抓取工具往往只能拿到空白骨架或 403 阻拦页面。
2. **直击官方 Handbook 与 Rules PDF**：许多赛事的关键国籍条款、组队细则和评分量表（Rubrics）隐藏在嵌套的 Tab、折叠面板或内嵌 PDF 预览中，必须通过真浏览器的 DOM 交互、滚动与点击才能获取。
3. **真实表单与报名入口验证**：通过真浏览器可以探测当季报名系统是否已开启注册、是否有针对大陆手机号/学校邮箱的特定限制。

---

## 标准核验操作模板（Node.js Heredoc）

### 模板 1：排查全球官网参赛资格（Eligibility & Citizenship）

```bash
ego-browser nodejs <<'EOF'
// 1. 初始化或复用任务空间
const task = await useOrCreateTaskSpace('competition-eligibility-audit');
cliLog('Task Space ID: ' + task.id);

// 2. 打开竞赛官方规则页面
await openOrReuseTab('https://www.conradchallenge.org/the-challenge', { wait: true, timeout: 30 });
await wait(3000);

// 3. 截取首屏正文
let text = await snapshotText();
cliLog('--- Page Title & Initial Text ---');
cliLog(text.slice(0, 1500));

// 4. 滚动页面寻找 Eligibility / Rules 区域
await scrollBy(0, 1500);
await wait(2000);
text = await snapshotText();

// 5. 关键词检索与提取
const keywords = ['citizen', 'resident', 'eligible', 'grade', 'age', 'international', 'team', 'fee'];
for (const kw of keywords) {
  if (text.toLowerCase().includes(kw)) {
    cliLog(`Found keyword [${kw}] in current view.`);
  }
}
EOF
```

---

### 模板 2：深挖当季时间节点与截止日期（Timeline & Deadlines）

```bash
ego-browser nodejs <<'EOF'
const task = await useOrCreateTaskSpace('competition-dates-audit');

// 访问滑铁卢大学 CEMC 欧几里得竞赛官方页面
await openOrReuseTab('https://www.cemc.uwaterloo.ca/contests/euclid.html', { wait: true, timeout: 30 });
await wait(3000);

const pageContent = await snapshotText();

// 提取关键日期
const dateMatches = pageContent.match(/(deadline|date|contest date|outside north america).*?(\d{4}|\d{1,2}\s+[a-zA-Z]+)/gi);
if (dateMatches) {
  cliLog('=== EXTRACTED OFFICIAL DATES ===');
  dateMatches.forEach(m => cliLog(m));
} else {
  cliLog('Full Page Snapshot for Date Inspection:');
  cliLog(pageContent);
}
EOF
```

---

### 模板 3：处理弹窗、Cookie 遮罩与点击导航（Interactions）

```bash
ego-browser nodejs <<'EOF'
const task = await useOrCreateTaskSpace('competition-interactive-audit');
await openOrReuseTab('https://www.technovation.org/', { wait: true, timeout: 30 });
await wait(3000);

// 检查是否存在对话框或阻挡元素
const info = await pageInfo();
if (info.dialog) {
  await cdp('Page.handleJavaScriptDialog', { accept: true });
}

// 模拟滚动浏览完整规则
await scrollToBottomUntil(5000);
cliLog(await snapshotText());
EOF
```

---

### 模板 4：清理并释放任务空间（Task Cleanup）

> **【操作规范】**
> 在所有事实核查完成并获得确切结论后，必须在最后一个 heredoc 中执行彻底清理，避免残留后台孤儿标签页：

```bash
ego-browser nodejs <<'EOF'
await completeTaskSpace('competition-eligibility-audit', { keep: false });
cliLog('Task space cleaned up successfully.');
EOF
```

---

## 常见核验排查要点速查表

| 目标赛事 | 官方主站 URL | 核心必查页面/关键词 | 常见陷阱与注意事项 |
| :--- | :--- | :--- | :--- |
| **Conrad Challenge** | `conradchallenge.org` | `/the-challenge` / `Student Guide` / `Lean Canvas` | 检查 Phase 2 提交截止日（通常在11月初）；视频严卡 3 分钟以内；必须有成人 Coach。 |
| **Technovation Girls** | `technovation.org`<br>`technovationgirls.org` | `/curriculum` / `Rules` / `Senior Division` | 检查是否仅限女生；100% 免费；Senior 组年龄为 16-18 岁；提交物包括 5-10 页商业计划书与 2 部视频。 |
| **China Thinks Big (CTB)** | `chinathinksbig.com` | `参赛手册` / `创新行动类` / `重要日期` | **绝非阿思丹承办**，必须在独立官网注册；常规报名截止为 11 月 30 日；成果提交 1 月 20 日；全国站展演 2 月底。 |
| **CEMC Euclid** | `cemc.uwaterloo.ca` | `/contests/euclid.html` | 注意区分北美（North America）考试日与**北美以外（Outside North America - 中国考区）考试日**！前 25% 获 Distinction。 |
| **Imagine Cup Jr** | `imaginecup.microsoft.com/junior` | `Rules` / `AI for Good` / `PowerPoint Template` | 确认是否为官方 PPT 模板提交；由成年指导老师统一上传；不可超时 2 分钟视频。 |
| **Diamond Challenge** | `diamondchallenge.org` | `/rules` / `Social Innovation` | 100% 免费；方案提交截止为 1 月中旬；3-5 页商业计划书。 |
