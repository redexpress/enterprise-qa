# -*- coding: utf-8 -*-

import subprocess
import sys


def run_tool(script: str, *args):

    cmd = [
        sys.executable,
        script,
        *args,
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    return result.stdout.strip()


def route(question: str):

    if "晋升" in question:
        return run_tool(
            ".claude/skills/enterprise-qa/tools/promotion_check.py",
            question,
        )

    if "迟到" in question:
        return run_tool(
            ".claude/skills/enterprise-qa/tools/attendance_query.py",
            "张三",
            "2026-02",
        )

    if "项目" in question:
        return run_tool(
            ".claude/skills/enterprise-qa/tools/project_query.py",
            "张三",
        )

    if (
        "部门" in question
        or "邮箱" in question
        or "员工" in question
    ):
        return run_tool(
            ".claude/skills/enterprise-qa/tools/query_employee.py",
            "张三",
        )

    return run_tool(
        ".claude/skills/enterprise-qa/tools/kb_search.py",
        question,
    )


def main():

    if len(sys.argv) < 2:
        print("请输入问题")
        sys.exit(1)

    question = sys.argv[1]

    print(route(question))


if __name__ == "__main__":
    main()
