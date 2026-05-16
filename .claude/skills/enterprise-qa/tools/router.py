# -*- coding: utf-8 -*-

import json
import time
import logging
import subprocess
import sys
from pathlib import Path

from tools.config import DB_PATH, KB_PATH, setup_logging
from tools.router_config import TOOL_REGISTRY, DEFAULT_TOOL, NAMES

logger = setup_logging()

# Cache: DB queries 30 min, KB 1 hour
_DB_TTL = 30 * 60
_KB_TTL = 60 * 60

cache: dict[str, tuple[str, float]] = {}  # key -> (result, timestamp)

# Session config
SESSION_FILE = "./logs/session.json"
MAX_HISTORY = 6


def load_session() -> list[dict]:
    """Load last 6 rounds of conversation"""
    if Path(SESSION_FILE).exists():
        try:
            with open(SESSION_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            return []
    return []


def save_session(question: str, answer: str):
    """Save Q&A to session"""
    session = load_session()
    session.append({"q": question, "a": answer})
    session = session[-MAX_HISTORY:]
    Path(SESSION_FILE).parent.mkdir(parents=True, exist_ok=True)
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump(session, f, ensure_ascii=False)


def extract_name(question: str) -> str | None:
    """Extract name from question (方案C)"""
    for name in NAMES:
        if name in question:
            return name
    return None


def match_tool(question: str) -> str:
    """Match tool by keywords from registry"""
    for keyword, script in TOOL_REGISTRY.items():
        if keyword in question:
            return script
    return DEFAULT_TOOL


def get_tool_type(question: str) -> str:
    """Determine tool type for TTL"""
    if any(k in question for k in TOOL_REGISTRY.keys()):
        return "db"
    return "kb"


def is_cache_hit(question: str) -> bool:
    """Check if cache hit and not expired"""
    if question not in cache:
        return False

    result, timestamp = cache[question]
    tool_type = get_tool_type(question)
    ttl = _DB_TTL if tool_type == "db" else _KB_TTL

    if time.time() - timestamp > ttl:
        del cache[question]
        return False

    return True


def set_cache(question: str, result: str) -> None:
    """Write to cache"""
    cache[question] = (result, time.time())


def run_tool(script: str, *args) -> str:
    """Execute tool script"""
    cmd = [
        sys.executable,
        script,
        *args,
    ]

    logger.info(f"Executing tool: {script}, args: {args}")

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    if result.returncode != 0:
        logger.error(f"Tool execution failed: {result.stderr}")
    else:
        logger.debug(f"Tool execution succeeded")

    return result.stdout.strip()


def route(question: str) -> str:
    logger.info(f"Received question: {question}")

    # Cache check
    if is_cache_hit(question):
        cached_result, _ = cache[question]
        logger.info(f"Cache hit, returning directly")
        return cached_result

    # Match tool from registry
    tool_script = match_tool(question)
    name = extract_name(question)

    # Execute tool with extracted name
    if name:
        result = run_tool(tool_script, name)
    else:
        result = run_tool(tool_script, question)

    # Write to cache
    set_cache(question, result)
    # Save conversation history
    save_session(question, result)
    logger.info(f"Returning result")
    return result


def main():

    if len(sys.argv) < 2:
        print("Please enter a question")
        sys.exit(1)

    question = sys.argv[1]

    print(route(question))


if __name__ == "__main__":
    main()