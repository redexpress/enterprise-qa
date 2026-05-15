from unittest.mock import patch, MagicMock
from tools.router import route, run_tool


@patch("tools.router.subprocess.run")
def test_route_promotion(mock_run):
    mock_run.return_value = MagicMock(stdout="晋升结果")

    result = route("如何申请晋升")

    assert "promotion_check.py" in str(mock_run.call_args)
    assert "如何申请晋升" in str(mock_run.call_args)


@patch("tools.router.subprocess.run")
def test_route_attendance(mock_run):
    mock_run.return_value = MagicMock(stdout="迟到记录")

    result = route("本月迟到情况")

    assert "attendance_query.py" in str(mock_run.call_args)
    assert "张三" in str(mock_run.call_args)
    assert "2026-02" in str(mock_run.call_args)


@patch("tools.router.subprocess.run")
def test_route_project(mock_run):
    mock_run.return_value = MagicMock(stdout="项目列表")

    result = route("张三的项目有哪些")

    assert "project_query.py" in str(mock_run.call_args)
    assert "张三" in str(mock_run.call_args)


@patch("tools.router.subprocess.run")
def test_route_employee_dept(mock_run):
    mock_run.return_value = MagicMock(stdout="部门信息")

    result = route("张三的部门")

    assert "query_employee.py" in str(mock_run.call_args)


@patch("tools.router.subprocess.run")
def test_route_employee_email(mock_run):
    mock_run.return_value = MagicMock(stdout="邮箱信息")

    result = route("李四的邮箱")

    assert "query_employee.py" in str(mock_run.call_args)


@patch("tools.router.subprocess.run")
def test_route_employee_staff(mock_run):
    mock_run.return_value = MagicMock(stdout="员工信息")

    result = route("员工王五的信息")

    assert "query_employee.py" in str(mock_run.call_args)


@patch("tools.router.subprocess.run")
def test_route_default(mock_run):
    mock_run.return_value = MagicMock(stdout="知识库结果")

    result = route("不知道是什么的问题")

    assert "kb_search.py" in str(mock_run.call_args)


@patch("tools.router.subprocess.run")
def test_run_tool(mock_run):
    mock_run.return_value = MagicMock(stdout="输出内容")

    result = run_tool("script.py", "arg1", "arg2")

    assert mock_run.called
    assert result == "输出内容"
    args = mock_run.call_args[0][0]
    assert "script.py" in args
    assert "arg1" in args
    assert "arg2" in args


@patch("tools.router.sys.exit")
def test_main_no_args(mock_exit):
    import tools.router as router

    with patch.object(router, "__name__", "__main__"):
        pass
