from unittest.mock import patch, MagicMock
from tools.router import route, run_tool, cache, set_cache, is_cache_hit
from tools.router import load_session, save_session, SESSION_FILE, MAX_HISTORY


def test_cache_hit():
    """测试缓存命中"""
    cache.clear()
    set_cache("测试问题", "缓存结果")
    assert is_cache_hit("测试问题") is True


def test_cache_miss():
    """测试缓存未命中"""
    cache.clear()
    assert is_cache_hit("不存在的问题") is False


def test_cache_with_ttl_expired():
    """测试 TTL 过期"""
    import time
    cache.clear()
    # "张三的部门" 含 DB 关键词，TTL=30分钟，用31分钟前的时间戳
    cache["张三的部门是什么"] = ("结果", time.time() - 31 * 60)
    assert is_cache_hit("张三的部门是什么") is False


@patch("tools.router.subprocess.run")
def test_route_uses_cache(mock_run):
    """测试 route 使用缓存"""
    cache.clear()
    mock_run.return_value = MagicMock(stdout="工具结果", returncode=0)

    # 第一次调用
    result1 = route("张三的部门是什么")
    assert mock_run.called  # 应该调用工具

    # 重置 mock
    mock_run.reset_mock()

    # 第二次相同问题
    result2 = route("张三的部门是什么")
    assert not mock_run.called  # 不应调用工具，直接返回缓存
    assert result1 == result2


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
    assert "本月迟到情况" in str(mock_run.call_args)


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


# Session 多轮对话测试
def test_load_session_empty():
    """测试空 session"""
    import os
    # 确保 session 文件不存在
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
    session = load_session()
    assert session == []


def test_save_and_load_session():
    """测试保存和加载 session"""
    import os
    import tempfile

    # 使用临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        temp_file = f.name

    try:
        # 临时修改 SESSION_FILE
        import tools.router as router
        original = router.SESSION_FILE
        router.SESSION_FILE = temp_file

        # 保存问答
        save_session("问题1", "答案1")
        session = load_session()
        assert len(session) == 1
        assert session[0]["q"] == "问题1"
        assert session[0]["a"] == "答案1"

        # 再保存一条
        save_session("问题2", "答案2")
        session = load_session()
        assert len(session) == 2

        # 恢复原值
        router.SESSION_FILE = original
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_session_max_history():
    """测试 session 保留最近6条"""
    import os
    import tempfile

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        temp_file = f.name

    try:
        import tools.router as router
        original = router.SESSION_FILE
        router.SESSION_FILE = temp_file

        # 保存7条，验证只保留6条
        for i in range(7):
            save_session(f"问题{i}", f"答案{i}")

        session = load_session()
        assert len(session) == MAX_HISTORY  # 6
        assert session[0]["q"] == "问题1"  # 第一条被删除

        router.SESSION_FILE = original
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


@patch("tools.router.subprocess.run")
def test_route_saves_session(mock_run):
    """测试 route 执行后保存 session"""
    import os
    import tempfile

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        temp_file = f.name

    try:
        import tools.router as router
        original = router.SESSION_FILE
        router.SESSION_FILE = temp_file

        cache.clear()
        mock_run.return_value = MagicMock(stdout="测试结果", returncode=0)

        route("测试问题")
        session = load_session()
        assert len(session) == 1
        assert session[0]["q"] == "测试问题"

        router.SESSION_FILE = original
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)