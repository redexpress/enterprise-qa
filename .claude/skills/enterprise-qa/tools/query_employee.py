import logging
import sqlite3
import sys
from pathlib import Path

from tools.config import DB_PATH, setup_logging
from tools.router_config import NAMES, DEPARTMENTS

logger = setup_logging()


def get_employee_by_name(conn: sqlite3.Connection, name: str) -> sqlite3.Row | None:

    cursor = conn.execute(
        """
        SELECT
            employee_id,
            name,
            department,
            level,
            email,
            manager_id,
            status
        FROM employees
        WHERE name = ?
        """,
        (name,)
    )

    return cursor.fetchone()


def get_manager(conn: sqlite3.Connection, manager_id: str) -> sqlite3.Row | None:

    cursor = conn.execute(
        """
        SELECT name
        FROM employees
        WHERE employee_id = ?
        """,
        (manager_id,)
    )

    return cursor.fetchone()


def count_by_department(conn: sqlite3.Connection, department: str) -> int:
    cursor = conn.execute(
        "SELECT COUNT(*) FROM employees WHERE department = ? AND status = 'active'",
        (department,)
    )
    return cursor.fetchone()[0]


def build_employee_result(row: sqlite3.Row) -> str:

    (
        employee_id,
        name,
        department,
        level,
        email,
        manager_id,
        status,
    ) = row

    lines = []

    lines.append(f"员工信息：{name}")
    lines.append("")
    lines.append(f"- 工号: {employee_id}")
    lines.append(f"- 部门: {department}")
    lines.append(f"- 职级: {level}")
    lines.append(f"- 邮箱: {email}")
    lines.append(f"- 状态: {status}")

    return "\n".join(lines)


def build_manager_result(employee_name: str, manager_name: str) -> str:

    return (
        f"{employee_name} 的上级是：{manager_name}\n\n"
        f"来源：employees 表"
    )


def query_employee(question: str) -> str:
    logger.info(f"Querying employee: {question}")

    # Check DB path existence (skip for in-memory databases)
    if DB_PATH != ":memory:" and not Path(DB_PATH).exists():
        logger.error(f"Database file not found: {DB_PATH}")
        return "Database file not found. Please contact administrator."

    try:
        conn = sqlite3.connect(DB_PATH)
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return "Database connection failed. Please try again later."

    try:

        if "有多少人" in question or "多少人" in question:
            for dept in DEPARTMENTS:
                if dept in question:
                    count = count_by_department(conn, dept)
                    return f"{dept}有 {count} 人。\n\n来源：employees 表"

        name = None
        for emp_name in NAMES:
            if emp_name in question:
                name = emp_name
                break

        if not name:
            return "暂不支持该员工"

        employee = get_employee_by_name(conn, name)

        if not employee:
            return f"未找到员工：{name}"

        if "上级" in question or "经理" in question:

            manager_id = employee[5]

            if not manager_id:
                return f"{name} 没有上级"

            manager = get_manager(conn, manager_id)

            if not manager:
                return "未找到上级"

            return build_manager_result(
                employee_name=name,
                manager_name=manager[0],
            )

        return build_employee_result(employee)

    finally:
        conn.close()


def main():
    logger.info("Employee query module initialized")

    if len(sys.argv) < 2:
        print("usage: query_employee.py <question>")
        return

    question = sys.argv[1]

    print(query_employee(question))


if __name__ == "__main__":
    main()
