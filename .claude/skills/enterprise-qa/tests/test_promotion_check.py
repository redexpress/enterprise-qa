import sqlite3
from pathlib import Path
from unittest.mock import patch

import pytest

from tools.promotion_check import (
    evaluate_promotion,
    build_result,
    get_employee,
    get_avg_kpi,
    get_project_count,
    load_rules,
    check_promotion,
    main,
)


def test_evaluate_promotion_pass():

    result = evaluate_promotion(
        years=2.0,
        avg_kpi=90,
        project_count=4,
    )

    assert result["years_ok"] is True
    assert result["kpi_ok"] is True
    assert result["project_ok"] is True


def test_evaluate_promotion_fail():

    result = evaluate_promotion(
        years=0.5,
        avg_kpi=80,
        project_count=1,
    )

    assert result["years_ok"] is False
    assert result["kpi_ok"] is False
    assert result["project_ok"] is False


def test_build_result_fail():

    text = build_result(
        employee_name="王五",
        level="P5",
        hire_date="2024-01-10",
        years=2.2,
        avg_kpi=80,
        project_count=1,
        checks={
            "years_ok": True,
            "kpi_ok": False,
            "project_ok": False,
        }
    )

    assert "王五不符合晋升条件" in text
    assert "80" in text
    assert "1" in text


def test_build_result_pass():

    text = build_result(
        employee_name="张三",
        level="P6",
        hire_date="2023-06-15",
        years=3.0,
        avg_kpi=90,
        project_count=4,
        checks={
            "years_ok": True,
            "kpi_ok": True,
            "project_ok": True,
        }
    )

    assert "张三符合晋升条件" in text


def test_get_employee():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE employees (employee_id, name, level, hire_date)")
    conn.execute("INSERT INTO employees VALUES ('E001', '张三', 'P6', '2023-01-01')")
    conn.commit()

    result = get_employee(conn, "张三")

    assert result == ("E001", "张三", "P6", "2023-01-01")
    conn.close()


def test_get_employee_not_found():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE employees (employee_id, name, level, hire_date)")

    result = get_employee(conn, "不存在的员工")

    assert result is None
    conn.close()


def test_get_avg_kpi():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE performance_reviews (employee_id, kpi_score)")
    conn.execute("INSERT INTO performance_reviews VALUES ('E001', 85.5)")
    conn.execute("INSERT INTO performance_reviews VALUES ('E001', 90.0)")
    conn.commit()

    result = get_avg_kpi(conn, "E001")

    assert result == 87.75
    conn.close()


def test_get_avg_kpi_no_records():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE performance_reviews (employee_id, kpi_score)")

    result = get_avg_kpi(conn, "E001")

    assert result == 0.0
    conn.close()


def test_get_project_count():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE project_members (employee_id)")
    conn.execute("INSERT INTO project_members VALUES ('E001')")
    conn.execute("INSERT INTO project_members VALUES ('E001')")
    conn.execute("INSERT INTO project_members VALUES ('E001')")
    conn.commit()

    result = get_project_count(conn, "E001")

    assert result == 3
    conn.close()


def test_get_project_count_zero():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE project_members (employee_id)")

    result = get_project_count(conn, "E001")

    assert result == 0
    conn.close()


def test_load_rules(tmp_path):
    rules_file = tmp_path / "promotion_rules.md"
    rules_file.write_text("# 晋升规则\n内容", encoding="utf-8")

    with patch("tools.promotion_check.KB_PATH", rules_file):
        result = load_rules()

    assert "晋升规则" in result


def test_check_promotion_employee_not_found(tmp_path):
    db_file = tmp_path / "test.db"
    conn = sqlite3.connect(str(db_file))
    conn.execute("CREATE TABLE employees (employee_id, name, level, hire_date)")
    conn.execute("CREATE TABLE performance_reviews (employee_id, kpi_score)")
    conn.execute("CREATE TABLE project_members (employee_id)")
    conn.commit()
    conn.close()

    with patch("tools.promotion_check.DB_PATH", db_file):
        result = check_promotion("不存在的员工")

    assert "未找到员工" in result


def test_check_promotion_success(tmp_path):
    db_file = tmp_path / "test.db"
    conn = sqlite3.connect(str(db_file))
    conn.execute("CREATE TABLE employees (employee_id, name, level, hire_date)")
    conn.execute("INSERT INTO employees VALUES ('E001', '李四', 'P5', '2022-01-01')")
    conn.execute("CREATE TABLE performance_reviews (employee_id, kpi_score)")
    conn.execute("INSERT INTO performance_reviews VALUES ('E001', 90)")
    conn.execute("CREATE TABLE project_members (employee_id)")
    conn.execute("INSERT INTO project_members VALUES ('E001')")
    conn.execute("INSERT INTO project_members VALUES ('E001')")
    conn.execute("INSERT INTO project_members VALUES ('E001')")
    conn.commit()
    conn.close()

    with patch("tools.promotion_check.DB_PATH", db_file):
        result = check_promotion("李四")

    assert "李四" in result


def test_main_unsupported():
    with patch("sys.argv", ["promotion_check.py", "其他问题"]):
        with patch("builtins.print") as mock_print:
            main()
            mock_print.assert_called_once_with("暂不支持")
