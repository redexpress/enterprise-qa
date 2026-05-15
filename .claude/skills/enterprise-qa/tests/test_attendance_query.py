import sqlite3

from tools.attendance_query import (
    parse_month,
    parse_employee,
    build_attendance_result,
    get_employee_id,
    get_late_count,
    attendance_query,
    DB_PATH,
)


def test_parse_month():

    month = parse_month(
        "张三2月迟到几次"
    )

    assert month == "2026-02"


def test_parse_employee():

    name = parse_employee(
        "张三2月迟到几次"
    )

    assert name == "张三"


def test_build_attendance_result_no_penalty():

    text = build_attendance_result(
        employee_name="张三",
        month="2026-02",
        late_count=2,
    )

    assert "2 次" in text
    assert "无需扣款" in text


def test_build_attendance_result_penalty():

    text = build_attendance_result(
        employee_name="王五",
        month="2026-02",
        late_count=5,
    )

    assert "5 次" in text
    assert "250 元" in text


def test_build_attendance_result_absent():

    text = build_attendance_result(
        employee_name="测试员工",
        month="2026-02",
        late_count=8,
    )

    assert "旷工" in text


def test_parse_month_march():
    month = parse_month("张三3月迟到几次")
    assert month == "2026-03"


def test_parse_month_default():
    month = parse_month("张三5月迟到几次")
    assert month == "2026-02"


def test_parse_employee_not_found():
    name = parse_employee("未知人员5月迟到几次")
    assert name is None


def test_build_attendance_result_boundary_3():
    text = build_attendance_result(
        employee_name="张三",
        month="2026-02",
        late_count=3,
    )
    assert "3 次" in text
    assert "无需扣款" in text


def test_build_attendance_result_boundary_4():
    text = build_attendance_result(
        employee_name="张三",
        month="2026-02",
        late_count=4,
    )
    assert "4 次" in text
    assert "200 元" in text


def test_build_attendance_result_boundary_6():
    text = build_attendance_result(
        employee_name="张三",
        month="2026-02",
        late_count=6,
    )
    assert "6 次" in text
    assert "300 元" in text


def test_get_employee_id_found():
    conn = sqlite3.connect(DB_PATH)
    emp_id = get_employee_id(conn, "张三")
    conn.close()
    assert emp_id is not None


def test_get_employee_id_not_found():
    conn = sqlite3.connect(DB_PATH)
    emp_id = get_employee_id(conn, "不存在的员工")
    conn.close()
    assert emp_id is None


def test_get_late_count():
    conn = sqlite3.connect(DB_PATH)
    emp_id = get_employee_id(conn, "张三")
    count = get_late_count(conn, emp_id, "2026-02")
    conn.close()
    assert isinstance(count, int)


def test_attendance_query_employee_not_found():
    result = attendance_query("未知人员2月迟到几次")
    assert "无法识别员工" in result


def test_attendance_query_not_in_db():
    result = attendance_query("不存在的员工2月迟到几次")
    assert "无法识别员工" in result


def test_attendance_query_success():
    result = attendance_query("张三2月迟到几次")
    assert "张三" in result
    assert "2026-02" in result
