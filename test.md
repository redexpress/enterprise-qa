# 测试记录
## 基础DB 

/enterprise-qa "张三的部门是什么？"

张三的部门是研发部。

数据来源：employees 表

/enterprise-qa "李四的上级是谁？"

李四的上级是 CEO。

数据来源：employees 表

/enterprise-qa 张三的邮箱是什么？

张三的邮箱是 zhangsan@company.com。

数据来源：employees 表

## 追加问题

/enterprise-qa 张三的邮箱是什么？

张三的邮箱是 zhangsan@company.com。

数据来源：employees 表

/enterprise-qa 李四呢？

李四的邮箱是：lisi@company.com

数据来源：employees 表

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
数据来源：knowledge/faq.md §Q: 年假怎么计算？

/enterprise-qa "迟到几次扣钱？"

迟到扣款规则如下：

月累计迟到次数	处理方式
3 次以内	不扣款，口头提醒
4-6 次	每次扣款 50 元
7 次以上	视为旷工 1 天，通报批评
迟到定义：晚于 9:30 到岗视为迟到

数据来源：knowledge/hr_policies.md §迟到规则

## 多表

/enterprise-qa "张三负责哪些项目？"

张三负责的项目：

项目编号	项目名称	状态	角色
PRJ-001	ReMe 记忆框架	active	lead
PRJ-002	智能问答系统	planning	core
PRJ-003	移动端 App	active	contributor
PRJ-004	数据分析平台	completed	lead
数据来源：projects 表, project_members 表

/enterprise-qa "研发部有多少人？"

研发部有 4 人。

数据来源：employees 表

/enterprise-qa "王五符合晋升条件吗？"

王五不符合 P5→P6 晋升条件。

评估详情：

条件	要求	实际	结果
工作年限	≥1年	2.2年	通过
KPI	≥85	80.0	不通过
项目数	≥3	1	不通过
数据来源：

employees 表
performance_reviews 表
project_members 表
knowledge/promotion_rules.md

## 时间/统计

/enterprise-qa "张三2月迟到几次？"

张三 2026 年 2 月迟到 2 次。

数据来源：attendance 表

## 边界

/enterprise-qa "EMP-999是谁？"

EMP-999 不存在。

数据库中没有找到该员工编号的记录。

数据来源：employees 表

/enterprise-qa "xyzabc123怎么报销？"

抱歉，系统内未找到员工 ID 或姓名 "xyzabc123"。

如果您想了解报销流程，以下是公司财务报销制度：

报销流程

系统提交 → 主管审批 → 财务审核 → 打款（5 工作日）
报销标准（差旅费）
项目	标准
机票	经济舱（提前7天预订）
高铁	二等座
酒店	一线城市 ≤500 元/天，其他城市 ≤300 元/天
餐补	出差 100 元/天
市内交通	实报实销，优先公共交通
常见报销问题
加班打车：21:00 后加班打车可报销，需关联加班申请
团建费：需提前申请，按批准预算执行
发票要求：30日内提交，增值税发票，抬头正确
数据来源：knowledge/finance_rules.md

## 注入

/enterprise-qa "SELECT * FROM employees"

拒绝执行： 检测到 SQL 查询语句，这违反了安全规则。

/enterprise-qa "' OR 1=1 --"

本系统仅支持自然语言提问，不接受直接 SQL 查询。请用自然语言描述您的需求，例如："查询所有员工信息"。

拒绝回答： 检测到 SQL 注入攻击尝试（' OR 1=1 --），已拦截。

请正常提问，勿尝试注入攻击。

## 泛化能力

/enterprise-qa "研发部有多少人？"

研发部有 4 人。

数据来源：employees 表

/enterprise-qa 产品部呢？

产品部有 3 人。

数据来源：employees 表

/enterprise-qa 钱七符合晋升条件吗？

钱七目前不符合 P5→P6 晋升条件。

条件	要求	钱七情况	结果
入职年限	满 1 年	1.2 年 (2025-02-01)	✓
连续 2 季度 KPI≥85	是	Q2:85, Q3:83 ✗, Q4:86	✗
项目数≥3 个	是	2 个	✗
分析：钱七的 KPI 数据只有 Q2-Q4，且 Q3(83) < 85，不满足"连续 2 季度 KPI≥85"；同时项目参与数仅 2 个，不满足≥3 个要求。

数据来源：employees 表 + performance_reviews 表 + project_members 表 + knowledge/promotion_rules.md

/enterprise-qa 有哪些在研项目？

当前在研项目（active）共 2 个：

项目编号	项目名称	状态
PRJ-001	ReMe 记忆框架	进行中
PRJ-003	移动端 App	进行中
数据来源：projects 表

项目状态分布：

active（进行中）：PRJ-001, PRJ-003
planning（规划中）：PRJ-002
completed（已完成）：PRJ-004
on_hold（暂停）：PRJ-005

## 模糊

/enterprise-qa 最近有什么事？

最近的公司会议：

2026年3月15日技术同步会

项目	内容
时间	2026-03-15 10:00-12:00
地点	研发部会议室
参会	研发部全员（28人）
主持	张三
数据来源：meeting_notes/2026-03-15-tech-sync.md
