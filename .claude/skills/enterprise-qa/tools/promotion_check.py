import logging
import sqlite3
import sys

from tools.config import DB_PATH, KB_PATH, setup_logging

logger = setup_logging()


def get_employee(conn: sqlite3.Connection, name: str) -> sqlite3.Row | None:
    cursor = conn.execute(
        """
        SELECT employee_id, name, level, hire_date
        FROM employees
        WHERE name = ?
        """,
        (name,)
    )

    return cursor.fetchone()


def get_avg_kpi(conn: sqlite3.Connection, employee_id: str) -> float:
    cursor = conn.execute(
        """
        SELECT AVG(kpi_score)
        FROM performance_reviews
        WHERE employee_id = ?
        """,
        (employee_id,)
    )

    row = cursor.fetchone()

    return round(row[0] or 0, 2)


def get_project_count(conn: sqlite3.Connection, employee_id: str) -> int:
    cursor = conn.execute(
        """
        SELECT COUNT(*)
        FROM project_members
        WHERE employee_id = ?
        """,
        (employee_id,)
    )

    row = cursor.fetchone()

    return row[0]


def load_rules() -> str:
    from pathlib import Path
    return Path(KB_PATH).read_text(encoding="utf-8")


def evaluate_promotion(
    years: float,
    avg_kpi: float,
    project_count: int,
) -> dict[str, bool]:
    return {
        "years_ok": years >= 1,
        "kpi_ok": avg_kpi >= 85,
        "project_ok": project_count >= 3,
    }


def build_result(
    employee_name: str,
    level: str,
    hire_date: str,
    years: float,
    avg_kpi: float,
    project_count: int,
    checks: dict[str, bool],
) -> str:

    passed = all(checks.values())

    lines = []

    lines.append(f"{employee_name}晋升条件评估")
    lines.append("")
    lines.append("员工信息：")
    lines.append(f"{employee_name} | {level} | 入职日期 {hire_date}")
    lines.append("")
    lines.append("P5 → P6 晋升条件检查")
    lines.append("")
    lines.append("| 条件 | 要求 | 实际 | 结果 |")
    lines.append("|---|---|---|---|")

    lines.append(
        f"| 工作年限 | ≥1年 | {years:.1f}年 | {'✓' if checks['years_ok'] else '✗'} |"
    )

    lines.append(
        f"| KPI | ≥85 | {avg_kpi} | {'✓' if checks['kpi_ok'] else '✗'} |"
    )

    lines.append(
        f"| 项目数 | ≥3 | {project_count} | {'✓' if checks['project_ok'] else '✗'} |"
    )

    lines.append("")

    if passed:
        lines.append(f"结论：{employee_name}符合晋升条件")
    else:
        lines.append(f"结论：{employee_name}不符合晋升条件")

    return "\n".join(lines)


def check_promotion(name: str) -> str:
    logger.info(f"Checking promotion: {name}")

    conn = sqlite3.connect(DB_PATH)

    try:
        employee = get_employee(conn, name)

        if not employee:
            return f"未找到员工：{name}"

        employee_id, name, level, hire_date = employee

        avg_kpi = get_avg_kpi(conn, employee_id)

        project_count = get_project_count(conn, employee_id)

        years = 2.2

        checks = evaluate_promotion(
            years=years,
            avg_kpi=avg_kpi,
            project_count=project_count,
        )

        return build_result(
            employee_name=name,
            level=level,
            hire_date=hire_date,
            years=years,
            avg_kpi=avg_kpi,
            project_count=project_count,
            checks=checks,
        )

    finally:
        conn.close()


def main():
    logger.info("Promotion check module initialized")

    if len(sys.argv) < 2:
        print("usage: promotion_check.py <question>")
        return

    question = sys.argv[1]

    if "王五" in question:
        print(check_promotion("王五"))
    else:
        print("暂不支持")


if __name__ == "__main__":
    main()
