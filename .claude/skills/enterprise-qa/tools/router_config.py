# Router configuration
# Tool registry and route definitions

TOOL_REGISTRY = {
    "晋升": ".claude/skills/enterprise-qa/tools/promotion_check.py",
    "迟到": ".claude/skills/enterprise-qa/tools/attendance_query.py",
    "部门": ".claude/skills/enterprise-qa/tools/query_employee.py",
    "邮箱": ".claude/skills/enterprise-qa/tools/query_employee.py",
    "员工": ".claude/skills/enterprise-qa/tools/query_employee.py",
    "项目": ".claude/skills/enterprise-qa/tools/project_query.py",
}

DEFAULT_TOOL = ".claude/skills/enterprise-qa/tools/kb_search.py"

ROUTES = [
    (["晋升"], "promotion_check.py"),
    (["迟到"], "attendance_query.py"),
    (["部门", "邮箱", "员工"], "query_employee.py"),
    (["项目"], "project_query.py"),
]

# Name extraction
NAMES = ["张三", "李四", "王五", "赵六", "钱七", "孙八", "周九", "吴十"]

# Department list
DEPARTMENTS = ["研发部", "产品部", "市场部", "管理层"]
