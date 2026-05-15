from tools.kb_search import (
    split_sections,
    keyword_score,
    build_kb_result,
    tokenize,
)


def test_split_sections():

    content = """
# 标题1

内容1

## 标题2

内容2
"""

    sections = split_sections(content)

    assert len(sections) >= 2

    assert sections[0]["title"] == "标题1"
    assert sections[1]["title"] == "标题2"


def test_keyword_score():

    score = keyword_score(
        "年假怎么算",
        "年假：入职满1年5天",
    )

    assert score > 0


def test_build_kb_result():

    text = build_kb_result({
        "file": "hr_policies.md",
        "title": "请假类型",
        "content": "年假：入职满1年5天",
    })

    assert "hr_policies.md" in text
    assert "年假" in text


def test_no_result():

    result = build_kb_result({
        "file": "faq.md",
        "title": "ROOT",
        "content": "测试内容",
    })

    assert "来源：" in result


def test_tokenize():
    tokens = tokenize("年假怎么算 How to calculate")
    assert "年假" in tokens
    assert "年假" in tokens
    assert "how" in tokens
    assert "calculate" in tokens


def test_tokenize_chinese_bigrams():
    tokens = tokenize("年假")
    assert "年假" in tokens


def test_split_sections_empty():
    sections = split_sections("")
    assert len(sections) == 0


def test_split_sections_no_heading():
    content = "这是普通段落\n没有标题"
    sections = split_sections(content)
    assert len(sections) >= 1
    assert sections[0]["title"] == "ROOT"


def test_build_kb_result_long_content():
    long_content = "a" * 600
    result = build_kb_result({
        "file": "test.md",
        "title": "Test",
        "content": long_content,
    })
    assert len(result) < len(long_content) + 100
    assert "..." in result


def test_build_kb_result_exact_500_chars():
    content = "a" * 500
    result = build_kb_result({
        "file": "test.md",
        "title": "Test",
        "content": content,
    })
    assert "..." not in result


def test_search_kb_no_result(monkeypatch, tmp_path):
    import tools.kb_search as kb

    kb.KB_ROOT = tmp_path

    (tmp_path / "test.md").write_text("# 无相关内容", encoding="utf-8")

    result = kb.search_kb("完全不匹配的查询字符串xyzabc")
    assert "未找到相关知识库内容" in result


def test_search_kb_with_result(monkeypatch, tmp_path):
    import tools.kb_search as kb

    kb.KB_ROOT = tmp_path

    (tmp_path / "policy.md").write_text("# 年假\n年假：入职满1年5天", encoding="utf-8")

    result = kb.search_kb("年假怎么算")
    assert "policy.md" in result
    assert "年假" in result
    assert "来源：" in result


def test_search_kb_recent_events(monkeypatch, tmp_path):
    import tools.kb_search as kb

    kb.KB_ROOT = tmp_path

    (tmp_path / "faq.md").write_text("# FAQ\n## Q: 工资什么时候发？\nA: 每月10日发放", encoding="utf-8")
    (tmp_path / "meeting_notes").mkdir()
    (tmp_path / "meeting_notes" / "2026-03-15-tech-sync.md").write_text(
        "# 2026年3月15日技术同步会\n\n演讲人：张三\n\n## 决议\n下周启动代码重构", encoding="utf-8"
    )

    result = kb.search_kb("最近有什么事")

    assert "2026年3月15日" in result or "技术同步会" in result
    assert "faq.md" not in result or "工资" not in result
