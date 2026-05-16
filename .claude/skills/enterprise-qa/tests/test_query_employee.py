from pathlib import Path
import sqlite3
import sys
from unittest.mock import patch

from tools.query_employee import (
    get_employee_by_name,
    get_manager,
    build_employee_result,
    build_manager_result,
    query_employee,
    count_by_department,
    main,
)


def test_build_employee_result():

    row = (
        "EMP-001",
        "ZhangSan",
        "Engineering",
        "P6",
        "zhangsan@company.com",
        "EMP-000",
        "active",
    )

    text = build_employee_result(row)

    assert "ZhangSan" in text
    assert "Engineering" in text
    assert "P6" in text
    assert "zhangsan@company.com" in text


def test_build_manager_result():

    text = build_manager_result(
        employee_name="LiSi",
        manager_name="CEO",
    )

    assert "LiSi" in text
    assert "CEO" in text
    assert "来源" in text


def test_get_employee_by_name():
    conn = sqlite3.connect(":memory:")
    conn.execute("""
        CREATE TABLE employees (
            employee_id, name, department, level,
            email, manager_id, status
        )
    """)
    conn.execute("""
        INSERT INTO employees VALUES
        ('E001', 'ZhangSan', 'Engineering', 'P6', 'zhangsan@company.com',
                 'E000', 'active')
    """)
    conn.commit()

    result = get_employee_by_name(conn, "ZhangSan")

    assert result == ("E001", "ZhangSan", "Engineering", "P6",
                      "zhangsan@company.com", "E000", "active")
    conn.close()


def test_get_employee_by_name_not_found():
    conn = sqlite3.connect(":memory:")
    conn.execute("""
        CREATE TABLE employees (
            employee_id, name, department, level,
            email, manager_id, status
        )
    """)
    conn.commit()

    result = get_employee_by_name(conn, "NotExist")

    assert result is None
    conn.close()


def test_get_manager():
    conn = sqlite3.connect(":memory:")
    conn.execute("""
        CREATE TABLE employees (employee_id, name, department,
                 level, email, manager_id, status)
    """)
    conn.execute("""
        INSERT INTO employees VALUES ('E000', 'CEO', 'Management',
                  'P9', 'ceo@company.com', NULL, 'active')
    """)
    conn.commit()

    result = get_manager(conn, "E000")

    assert result == ("CEO",)
    conn.close()


def test_get_manager_not_found():
    conn = sqlite3.connect(":memory:")
    conn.execute("""
        CREATE TABLE employees (employee_id, name, department,
                 level, email, manager_id, status)
    """)

    result = get_manager(conn, "E999")

    assert result is None
    conn.close()


def test_query_employee_unsupported():
    with patch("tools.query_employee.DB_PATH", ":memory:"):
        result = query_employee("ZhaoLiu info")

    assert "暂不支持" in result


def test_query_employee_not_found(tmp_path):
    db_file = tmp_path / "test.db"
    conn = sqlite3.connect(str(db_file))
    conn.execute("""
        CREATE TABLE employees (
            employee_id, name, department, level,
            email, manager_id, status
        )
    """)
    conn.commit()
    conn.close()

    with patch("tools.query_employee.DB_PATH", db_file):
        result = query_employee("张三")

    assert "未找到员工" in result


def test_query_employee_with_manager(tmp_path):
    db_file = tmp_path / "test.db"
    conn = sqlite3.connect(str(db_file))
    conn.execute("""
        CREATE TABLE employees (
            employee_id, name, department, level,
            email, manager_id, status
        )
    """)
    conn.execute(
        "INSERT INTO employees VALUES "
        "('E001', '李四', 'Engineering', 'P6', 'lisi@company.com', 'E000', 'active')"
    )
    conn.execute("""
        INSERT INTO employees VALUES ('E000', 'CEO', 'Management',
                 'P9', 'ceo@company.com', NULL, 'active')
    """)
    conn.commit()
    conn.close()

    with patch("tools.query_employee.DB_PATH", db_file):
        result = query_employee("李四的上级")

    assert "CEO" in result


def test_query_employee_no_manager(tmp_path):
    db_file = tmp_path / "test.db"
    conn = sqlite3.connect(str(db_file))
    conn.execute("""
        CREATE TABLE employees (
            employee_id, name, department, level,
            email, manager_id, status
        )
    """)
    conn.execute("""
        INSERT INTO employees VALUES ('E001', '王五', 'Product', 'P5',
                 'wangwu@company.com', NULL, 'active')
    """)
    conn.commit()
    conn.close()

    with patch("tools.query_employee.DB_PATH", db_file):
        result = query_employee("王五的上级")

    assert "没有上级" in result


def test_query_employee_manager_not_found(tmp_path):
    db_file = tmp_path / "test.db"
    conn = sqlite3.connect(str(db_file))
    conn.execute("""
        CREATE TABLE employees (
            employee_id, name, department, level,
            email, manager_id, status
        )
    """)
    conn.execute(
        """INSERT INTO employees VALUES ('E001', '张三', 'Engineering',
            'P6', 'zhangsan@company.com', 'E999', 'active')"""
    )
    conn.commit()
    conn.close()

    with patch("tools.query_employee.DB_PATH", db_file):
        result = query_employee("张三的上级")

    assert "未找到上级" in result


def test_main():
    with patch("sys.argv", ["query_employee.py", "张三"]):
        with patch("builtins.print"):
            main()


def test_count_by_department():
    conn = sqlite3.connect(":memory:")
    conn.execute("""
        CREATE TABLE employees (
            employee_id, name, department, level,
            email, manager_id, status
        )
    """)
    conn.execute(
        "INSERT INTO employees VALUES "
        "('E001', '张三', '研发部', 'P6', 'zhangsan@company.com', 'E000', 'active')"
    )
    conn.execute(
        "INSERT INTO employees VALUES "
        "('E002', '李四', '研发部', 'P7', 'lisi@company.com', 'E000', 'active')"
    )
    conn.execute(
        "INSERT INTO employees VALUES "
        "('E003', '离职人', '研发部', 'P5', 'left@company.com', 'E000', 'resigned')"
    )
    conn.commit()

    count = count_by_department(conn, "研发部")

    assert count == 2
    conn.close()


def test_count_by_department_excludes_inactive():
    conn = sqlite3.connect(":memory:")
    conn.execute("""
        CREATE TABLE employees (
            employee_id, name, department, level,
            email, manager_id, status
        )
    """)
    conn.execute(
        "INSERT INTO employees VALUES "
        "('E001', '张三', '产品部', 'P6', 'zhangsan@company.com', 'E000', 'active')"
    )
    conn.execute(
        "INSERT INTO employees VALUES "
        "('E002', '王五', '产品部', 'P5', 'wangwu@company.com', 'E000', 'resigned')"
    )
    conn.execute(
        "INSERT INTO employees VALUES "
        "('E003', '赵六', '产品部', 'P6', 'zhaoliu@company.com', 'E000', 'active')"
    )
    conn.commit()

    count = count_by_department(conn, "产品部")

    assert count == 2
    conn.close()


def test_query_employee_department_count(tmp_path):
    db_file = tmp_path / "test.db"
    conn = sqlite3.connect(str(db_file))
    conn.execute("""
        CREATE TABLE employees (
            employee_id, name, department, level,
            email, manager_id, status
        )
    """)
    conn.execute(
        "INSERT INTO employees VALUES "
        "('E001', '张三', '研发部', 'P6', 'zhangsan@company.com', 'E000', 'active')"
    )
    conn.execute(
        "INSERT INTO employees VALUES "
        "('E002', '李四', '研发部', 'P7', 'lisi@company.com', 'E000', 'active')"
    )
    conn.execute(
        "INSERT INTO employees VALUES "
        "('E003', '周九', '研发部', 'P7', 'zhoujiu@company.com', 'E000', 'active')"
    )
    conn.execute(
        "INSERT INTO employees VALUES "
        "('E004', '钱七', '研发部', 'P5', 'qianqi@company.com', 'E000', 'active')"
    )
    conn.commit()
    conn.close()

    with patch("tools.query_employee.DB_PATH", db_file):
        result = query_employee("研发部有多少人")

    assert "研发部有 4 人" in result
    assert "来源" in result


def test_query_employee_db_path_not_found(tmp_path):
    non_existent_db = tmp_path / "non_existent.db"

    with patch("tools.query_employee.DB_PATH", str(non_existent_db)):
        result = query_employee("张三的部门")

    assert "Database file not found" in result


def test_query_employee_connection_failure():
    original_exists = Path.exists

    def mock_exists(self):
        if str(self).endswith(".db"):
            return True  # pretend DB exists
        return original_exists(self)

    with patch.object(Path, "exists", mock_exists):
        with patch("sqlite3.connect", side_effect=sqlite3.Error("Connection failed")):
            result = query_employee("张三的部门")

    assert "Database connection failed" in result
