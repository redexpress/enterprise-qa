
threshold=80
pytest .claude/skills/enterprise-qa/tests -v \
    --cov=.claude/skills/enterprise-qa/tools \
    --cov-report=term \
    --cov-report=html \
    --cov-fail-under=$threshold
