---
description: Enterprise QA system
---

用户问题：

$ARGUMENTS

你必须：

1. 优先查询真实数据
2. 禁止编造
3. 不允许基于记忆回答
4. 如果信息不存在，明确说不存在

必须执行：

```bash
sqlite3 enterprise.db ".tables"
```