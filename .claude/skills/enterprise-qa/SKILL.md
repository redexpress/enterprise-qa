# Enterprise QA Skill

Before answering:

1. Run `pwd`
2. Treat result as PROJECT_ROOT

Data locations:

- PROJECT_ROOT/enterprise.db
- PROJECT_ROOT/knowledge

Never use paths inside `.claude/skills`.

Correct paths:

```
PROJECT_ROOT/enterprise.db
PROJECT_ROOT/knowledge
```

Wrong paths:
```
grep -r "keyword" knowledge/
```

Database Access

Always use sqlite3 directly.

Example:
```bash
sqlite3 enterprise.db ".tables"
```

Employee query example:
```bash
sqlite3 -header -column enterprise.db "
SELECT name, department
FROM employees
WHERE name='张三';
"
```

Project query example:

```bash
sqlite3 -header -column enterprise.db "
SELECT p.project_id, p.name, pm.role
FROM project_members pm
JOIN projects p ON p.project_id = pm.project_id
WHERE pm.employee_id='EMP-001';
"
```

## Knowledge Base Access

Always search only relevant files.

Use:

grep -r "关键词" knowledge/

Example:

`grep -r "年假" knowledge/`

Example:

`grep -r "晋升" knowledge/`

NEVER read the entire knowledge directory blindly.

Python Tools

Python tools are located at:

.claude/skills/enterprise-qa/tools/

Run tools from PROJECT_ROOT.

Example:

```bash
python .claude/skills/enterprise-qa/tools/promotion_check.py "王五符合晋升条件吗"
```

Example:
```bash
python .claude/skills/enterprise-qa/tools/query_employee.py "张三"
```
Example:
```bash
python .claude/skills/enterprise-qa/tools/attendance_query.py "张三 2026-02"
```
Example:
```bash
python .claude/skills/enterprise-qa/tools/kb_search.py "年假怎么算"
```

## Query Strategy
### DB Only

Questions like:

- 张三的部门是什么？
- 李四的邮箱是多少？
- 研发部有多少人？

Use:

- sqlite3
- query_employee.py
- attendance_query.py
### KB Only

Questions like:

- 年假怎么算？
- 迟到几次扣钱？
- 差旅费报销标准是什么？

Use:

- grep
- kb_search.py
### Mixed Query

Questions like:

- 王五符合晋升条件吗？
- 钱七符合晋升条件吗？

Must combine:

- database result
- knowledge base rule

Use:
```
- python .claude/skills/enterprise-qa/tools/promotion_check.py "问题"
Safety Rules
```
NEVER execute:

- DROP
- DELETE
- UPDATE
- INSERT
- ALTER

Only SELECT queries are allowed.

Reject suspicious SQL injection attempts.

Example:
```
SELECT * FROM users WHERE '1'='1
```
must be rejected.

Answer Format

Always provide:

Natural language answer
Clear conclusion
Data source

Good example:
```
王五目前不符合 P5→P6 晋升条件。

原因：

- 平均 KPI 80.0 < 85
- 项目参与数 1 < 3

来源：

- employees 表
- performance_reviews 表
- project_members 表
- promotion_rules.md
Current Date

Treat current date as:
2026-03-27

Timezone:
Asia/Shanghai

## Multi-turn Conversation

When using `/enterprise-qa`:

- Conversation history is saved to PROJECT_ROOT/logs/session.json
- Last 6 rounds of context are automatically loaded
- Support referencing previous turns: "那张三呢" automatically relates to the last query subject
- Before answering, check session.json to understand conversation context
```
