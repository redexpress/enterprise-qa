# 设计文档

## 项目结构

Router 基于关键词匹配将请求分发到对应工具：
- "晋升" → promotion_check.py
- "迟到/考勤" → attendance_query.py
- "项目" → project_query.py
- "部门/员工/邮箱" → query_employee.py
- 默认 → kb_search.py

```
enterprise-qa-skill/
├── .claude/
│   ├── commands/         # 命令定义
│   └── skills/
│       └── enterprise-qa/
│           ├── tools/     # 工具实现
│           └── tests/     # 单元测试
├── knowledge/             # 知识库文档
├── enterprise.db          # SQLite 数据库
└── *.sh                   # 构建脚本
```

## 数据流

用户问题 → Router（关键词匹配）→ Tool（数据库查询/知识库搜索）→ 格式化结果

## 数据库表

- employees: 员工信息
- projects: 项目信息
- project_members: 项目成员关系
- attendance: 考勤记录
- performance_reviews: 绩效评估

## 配置优先级

环境变量 > config.yaml > 代码默认值

## 安全

- 参数化 SQL 查询（`?` 占位符）
- 输入验证防 SQL 注入
- 只读操作

## 测试覆盖率

不低于80%，采用TDD工作模式，发现bug先增加单元测试，修复bug后进行单元测试。

## 设计要点

- 关键词路由：简单快速
- 中文分词：二元语法 + 英文单词
- 会议笔记优先："最近/会议/全员" 触发 meeting_notes
- 在职员工过滤：部门统计排除离职员工

## 缓存策略

- 层级：Router 层缓存，避免重复查询工具
- 存储：内存 dict，Key 为问题文本
- TTL：员工/项目数据 30 分钟，知识库 1 小时
- 适用场景：重复问题、短时间内多次查询
