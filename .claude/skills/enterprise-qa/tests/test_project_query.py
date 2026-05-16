from unittest.mock import patch, MagicMock

from tools.project_query import (
    get_employee_id,
    query_projects,
    format_projects,
    main,
)


def test_get_employee_id():
    employee_id = get_employee_id("张三")
    assert employee_id == "EMP-001"


def test_query_projects():
    projects = query_projects("EMP-001")
    assert len(projects) == 4


def test_project_contains_reme():
    projects = query_projects("EMP-001")
    names = [p["name"] for p in projects]
    assert "ReMe 记忆框架" in names


def test_project_contains_role():
    projects = query_projects("EMP-001")
    roles = [p["role"] for p in projects]
    assert "lead" in roles


def test_format_projects():
    text = format_projects(
        "张三",
        [
            {
                "project_id": "PRJ-001",
                "name": "ReMe 记忆框架",
                "status": "active",
                "role": "lead",
            }
        ],
    )
    assert "张三" in text
    assert "ReMe 记忆框架" in text
    assert "负责人" in text


@patch("sys.argv", ["project_query.py", "张三"])
@patch("tools.project_query.print")
def test_main_success(mock_print):
    """测试 main 函数正常执行"""
    main()
    assert mock_print.called


@patch("sys.argv", ["project_query.py"])
def test_main_no_args():
    """测试 main 函数无参数退出"""
    import pytest
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 1


@patch("sys.argv", ["project_query.py", "不存在的员工"])
@patch("tools.project_query.print")
def test_main_employee_not_found(mock_print):
    """测试 main 函数员工不存在"""
    import sys
    with patch.object(sys, "exit") as mock_exit:
        main()
        mock_exit.assert_called_once()