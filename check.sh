#!/bin/bash
set -e

pycodestyle --max-line-length=100 .claude/skills/enterprise-qa/tools/*.py
pycodestyle --max-line-length=100 .claude/skills/enterprise-qa/tests/*.py