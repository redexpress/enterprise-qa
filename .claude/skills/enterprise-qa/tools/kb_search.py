from pathlib import Path
import re
import sys

from tools.config import KB_PATH

KB_ROOT = Path(KB_PATH)


def load_markdown_files():

    docs = []

    for path in KB_ROOT.rglob("*.md"):

        content = path.read_text(
            encoding="utf-8"
        )

        docs.append({
            "file": path.name,
            "path": path,
            "content": content,
        })

    return docs


def split_sections(content: str):

    sections = []

    current_title = "ROOT"
    current_lines = []

    for line in content.splitlines():

        heading = re.match(
            r"^(#{1,6})\s+(.+)",
            line
        )

        if heading:

            if current_lines and any(line.strip() for line in current_lines):
                sections.append({
                    "title": current_title,
                    "content": "\n".join(current_lines).strip(),
                })

            current_title = heading.group(2)
            current_lines = []

        else:
            current_lines.append(line)

    if current_lines:
        sections.append({
            "title": current_title,
            "content": "\n".join(current_lines).strip(),
        })

    return sections


def tokenize(text: str):
    tokens = []
    chinese = re.findall(
        r"[\u4e00-\u9fff]",
        text,
    )
    for i in range(len(chinese) - 1):
        tokens.append(
            chinese[i] + chinese[i + 1]
        )
    english = re.findall(
        r"[a-zA-Z]+",
        text.lower(),
    )
    tokens.extend(english)
    return tokens


def keyword_score(query: str, text: str,):
    score = 0
    query_tokens = tokenize(query)
    text_tokens = tokenize(text)
    text_set = set(text_tokens)
    for token in query_tokens:
        if token in text_set:
            score += 1
    return score


def search_kb(question: str):

    docs = load_markdown_files()

    if "最近" in question or "会议" in question or "全员" in question:
        meeting_notes_dir = KB_ROOT / "meeting_notes"
        if meeting_notes_dir.exists():
            md_files = list(meeting_notes_dir.glob("*.md"))
            if md_files:
                md_files.sort(key=lambda p: p.name, reverse=True)
                latest_meeting = md_files[0]
                content = latest_meeting.read_text(encoding="utf-8")
                sections = split_sections(content)
                if sections:
                    first_section = sections[0]
                    first_section["file"] = str(latest_meeting.relative_to(KB_ROOT))
                    first_section["score"] = 999
                    return build_kb_result(first_section)

    best = None
    best_score = 0

    for doc in docs:

        sections = split_sections(
            doc["content"]
        )

        for section in sections:

            score = keyword_score(
                question,
                section["content"] + section["title"],
            )

            if score > best_score:

                best_score = score

                best = {
                    "file": doc["file"],
                    "title": section["title"],
                    "content": section["content"],
                    "score": score,
                }

    if not best or best_score == 0:
        return (
            "未找到相关知识库内容\n\n"
            "来源：knowledge/"
        )

    return build_kb_result(best)


def build_kb_result(result):

    lines = []

    lines.append(
        f"根据 {result['file']}："
    )

    lines.append("")

    content = result["content"].strip()

    if len(content) > 500:
        content = content[:500] + "..."

    lines.append(content)

    lines.append("")
    lines.append(
        f"来源：{result['file']} §{result['title']}"
    )

    return "\n".join(lines)


def main():

    if len(sys.argv) < 2:
        print("usage: kb_search.py <question>")
        return

    question = sys.argv[1]

    print(search_kb(question))


if __name__ == "__main__":
    main()
