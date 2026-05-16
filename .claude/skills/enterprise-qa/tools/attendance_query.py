import logging
import sqlite3
import sys

from tools.config import DB_PATH, setup_logging
from tools.router_config import NAMES

logger = setup_logging()


def parse_month(question: str) -> str:

    if "2月" in question:
        return "2026-02"

    if "3月" in question:
        return "2026-03"

    return "2026-02"


def parse_employee(question: str) -> str | None:

    employees = NAMES

    for name in employees:
        if name in question:
            return name

    return None


def get_employee_id(conn: sqlite3.Connection, name: str) -> str | None:

    cursor = conn.execute(
        """
        SELECT employee_id
        FROM employees
        WHERE name = ?
        """,
        (name,)
    )

    row = cursor.fetchone()

    if not row:
        return None

    return row[0]


def get_late_count(
    conn: sqlite3.Connection,
    employee_id: str,
    month: str,
) -> int:

    cursor = conn.execute(
        """
        SELECT COUNT(*)
        FROM attendance
        WHERE employee_id = ?
        AND status = 'late'
        AND date LIKE ?
        """,
        (
            employee_id,
            f"{month}%",
        )
    )

    row = cursor.fetchone()

    return row[0]


def build_attendance_result(
    employee_name: str,
    month: str,
    late_count: int,
) -> str:

    lines = []

    lines.append(
        f"{employee_name} 在 {month} 的迟到次数：{late_count} 次"
    )

    lines.append("")

    if late_count <= 3:
        lines.append("根据公司制度：无需扣款")

    elif 4 <= late_count <= 6:
        penalty = late_count * 50

        lines.append(
            f"根据公司制度：需扣款 {penalty} 元"
        )

    else:
        lines.append(
            "根据公司制度：视为旷工 1 天"
        )

    lines.append("")
    lines.append("来源：attendance 表 + hr_policies.md")

    return "\n".join(lines)


def attendance_query(question: str) -> str:
    logger.info(f"Querying attendance: {question}")

    employee_name = parse_employee(question)

    if not employee_name:
        return "无法识别员工"

    month = parse_month(question)

    conn = sqlite3.connect(DB_PATH)

    try:

        employee_id = get_employee_id(
            conn,
            employee_name,
        )

        if not employee_id:
            return f"未找到员工：{employee_name}"

        late_count = get_late_count(
            conn,
            employee_id,
            month,
        )

        return build_attendance_result(
            employee_name,
            month,
            late_count,
        )

    finally:
        conn.close()


def main():
    logger.info("Attendance query module initialized")

    if len(sys.argv) < 2:
        print("usage: attendance_query.py <question>")
        return

    question = sys.argv[1]

    print(attendance_query(question))


if __name__ == "__main__":
    main()
