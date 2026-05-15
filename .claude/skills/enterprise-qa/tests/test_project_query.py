
from tools.project_query import (
    get_employee_id,
    query_projects,
    format_projects,
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
