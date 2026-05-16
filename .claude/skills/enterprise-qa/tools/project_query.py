# -*- coding: utf-8 -*-

import logging
import sqlite3
import sys
from pathlib import Path

from tools.config import DB_PATH, setup_logging

logger = setup_logging()
ROOT_DIR = Path(__file__).resolve().parents[4]

DB_PATH = str(ROOT_DIR / "enterprise.db")


ROLE_MAP = {
    "lead": "负责人",
    "core": "核心成员",
    "contributor": "参与成员",
}


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_employee_id(name: str) -> str | None:

    conn = get_conn()
    try:
        row = conn.execute(
            """
            SELECT employee_id
            FROM employees
            WHERE name = ?
            """,
            (name,),
        ).fetchone()

        if not row:
            return None
        return row["employee_id"]

    finally:
        conn.close()


def query_projects(employee_id: str) -> list[dict]:
    conn = get_conn()
    try:

        rows = conn.execute(
            """
            SELECT
                p.project_id,
                p.name,
                p.status,
                pm.role
            FROM project_members pm
            JOIN projects p
              ON pm.project_id = p.project_id
            WHERE pm.employee_id = ?
            ORDER BY p.project_id
            """,
            (employee_id,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def format_projects(employee_name: str, projects: list[dict]) -> str:

    if not projects:
        return f"{employee_name} 没有参与项目。"
    lines = []
    lines.append(f"{employee_name} 参与的项目：")
    lines.append("")
    for p in projects:
        role_cn = ROLE_MAP.get(p["role"], p["role"])
        lines.append(
            f"- {p['project_id']} | {p['name']} "
            f"| {p['status']} | {role_cn}"
        )

    lines.append("")
    lines.append("数据来源：")
    lines.append("- projects 表")
    lines.append("- project_members 表")
    return "\n".join(lines)


def main():
    logger.info("Project query module initialized")

    if len(sys.argv) < 2:
        print("Usage:")
        print("python project_query.py 张三")
        sys.exit(1)

    name = sys.argv[1]
    logger.info(f"Querying projects: {name}")
    employee_id = get_employee_id(name)
    if not employee_id:
        print(f"未找到员工：{name}")
        sys.exit(1)
    projects = query_projects(employee_id)
    print(format_projects(name, projects))


if __name__ == "__main__":
    main()
