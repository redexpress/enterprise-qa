import sqlite3
import sys

from tools.config import DB_PATH


def get_employee_by_name(conn, name: str):

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


def get_manager(conn, manager_id: str):

    cursor = conn.execute(
        """
        SELECT name
        FROM employees
        WHERE employee_id = ?
        """,
        (manager_id,)
    )

    return cursor.fetchone()


def count_by_department(conn, department: str):
    cursor = conn.execute(
        "SELECT COUNT(*) FROM employees WHERE department = ? AND status = 'active'",
        (department,)
    )
    return cursor.fetchone()[0]


def build_employee_result(row):

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


def build_manager_result(employee_name, manager_name):

    return (
        f"{employee_name} 的上级是：{manager_name}\n\n"
        f"来源：employees 表"
    )


def query_employee(question: str):

    conn = sqlite3.connect(DB_PATH)

    try:

        if "有多少人" in question or "多少人" in question:
            for dept in ["研发部", "产品部", "市场部", "管理层"]:
                if dept in question:
                    count = count_by_department(conn, dept)
                    return f"{dept}有 {count} 人。\n\n来源：employees 表"

        if "张三" in question:
            name = "张三"
        elif "李四" in question:
            name = "李四"
        elif "王五" in question:
            name = "王五"
        else:
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

    if len(sys.argv) < 2:
        print("usage: query_employee.py <question>")
        return

    question = sys.argv[1]

    print(query_employee(question))


if __name__ == "__main__":
    main()
