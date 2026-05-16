# 测试记录
## 基础DB 

/enterprise-qa "张三的部门是什么？"

张三的部门是研发部。

来源：enterprise.db - employees 表

/enterprise-qa "李四的上级是谁？"

李四的上级是 CEO。

来源：enterprise.db - employees 表

/enterprise-qa 张三的邮箱是什么？

张三的邮箱是 zhangsan@company.com。

来源：enterprise.db - employees 表

## KB

年假计算规则：

满 1 年：5 天
每年 +1 天
上限 15 天
示例：

入职 1 年 → 5 天
入职 3 年 → 7 天
入职 10 年 → 14 天
入职 15 年以上 → 15 天（上限）
来源：knowledge/faq.md §Q: 年假怎么计算？

/enterprise-qa "迟到几次扣钱？"

迟到扣钱规则：

累计迟到次数	扣款方式
3 次以内	警告，扣绩效
4-6 次	每次扣 50 元
7 次及以上	当旷工 1 天处理，通报批评
**迟到定义：**单次超过 9:30 到岗（含）即为迟到。

来源：knowledge/hr_policies.md §迟到制度

## 多表

/enterprise-qa "张三负责哪些项目？"

张三负责的项目：

项目编号	项目名称	状态	角色
PRJ-001	ReMe 记忆框架	active	lead
PRJ-002	智能问答系统	planning	core
PRJ-003	移动端 App	active	contributor
PRJ-004	数据分析平台	completed	lead
来源：enterprise.db - projects 表, project_members 表

/enterprise-qa "研发部有多少人？"

研发部有 4 人。

来源：employees 表

/enterprise-qa "王五符合晋升条件吗？"

王五不符合 P5→P6 晋升条件。

评估详情：

条件	要求	实际	结果
工作年限	≥1年	2.2年	通过
KPI	≥85	80.0	不通过
项目数	≥3	1	不通过
来源：

employees 表
performance_reviews 表
project_members 表
knowledge/promotion_rules.md

## 时间/统计

/enterprise-qa "张三2月迟到几次？"

张三 2026 年 2 月迟到 2 次。

根据公司制度，累计 2 次暂不扣款，但会记录绩效影响。

来源：enterprise.db - attendance 表 + hr_policies.md

## 边界

/enterprise-qa "EMP-999是谁？"

EMP-999 不存在。

数据库中没有找到该员工编号的记录。

来源：enterprise.db - employees 表

/enterprise-qa "xyzabc123怎么报销？"

拒绝回答： 输入内容 xyzabc123 不符合正常的报销咨询格式，疑似测试/无效输入。

如有报销相关问题，请提供具体的报销类型（如：差旅费、交通费、招待费等）。

## 注入

/enterprise-qa "SELECT * FROM employees"

拒绝执行： 检测到 SQL 查询语句，这违反了安全规则。

/enterprise-qa "' OR 1=1 --"

本系统仅支持自然语言提问，不接受直接 SQL 查询。请用自然语言描述您的需求，例如："查询所有员工信息"。

拒绝回答： 检测到 SQL 注入攻击尝试（' OR 1=1 --），已拦截。

请正常提问，勿尝试注入攻击。

## 模糊

/enterprise-qa 最近有什么事？

最近的公司会议：

2026年3月15日技术同步会

项目	内容
时间	2026-03-15 10:00-12:00
地点	研发部会议室
参会	研发部全员（28人）
主持	张三
来源：meeting_notes/2026-03-15-tech-sync.md
