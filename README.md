# Enterprise QA System

<p align="center">
  <a href="README.md">English</a> |
  <a href="README.zh.md">简体中文</a>
</p>

## Documentation

- [Requirements Specification](./srs.md) - Software requirements specification
- [Design Document](./design.md) - System design document
- [Development Standards](./convince.md) - Development standards
- [Exam Instructions](./enterprise-qa-exam.md) - Detailed exam requirements
- [Unit Test Report](htmlcov/index.html) - Generated after running build.sh
- Using MiniMax M2.7 with Claude Code - [Test Results](./test.md)

## Usage

### System Requirements

- Python 3.8+
- sqlite3 command (Windows users need to install separately, Linux/Mac usually include it)

### Trigger Command

Use `/enterprise-qa` to trigger the Skill:

```
/enterprise-qa "What is Zhang San's department?"
/enterprise-qa "How is annual leave calculated?"
/enterprise-qa "Does Wang Wu qualify for promotion?"
```

### Installation

1. Copy the `.claude/skills/enterprise-qa/` directory into your Claude Code project
2. Install dependencies using a virtual environment:
```
# Create virtual environment
python -m venv .venv
# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate
# Install dependencies
pip install -r requirements.txt
```
3. Configure database path (optional):
   - Environment variable:
     ```bash
     export ENTERPRISE_QA_DB_PATH="./enterprise.db"
     export ENTERPRISE_QA_KB_PATH="./knowledge"
     ```
   - Or copy config file:
     ```bash
     cp config.yaml.example config.yaml
     ```

### Run Tests

Install virtual environment and run `pip install -r requirements-dev.txt` to install dependencies.

> requirements-dev.txt references requirements.txt and includes unit testing and code inspection tools.

```bash
chmod +x *.sh

# Style check
./check.sh

# Unit tests
./build.sh
```

## Release

Run `./release.sh` to build distributable packages:

```bash
./release.sh
```

Output:
- `dist/enterprise-qa-skill-{version}.zip`
- `dist/enterprise-qa-skill-{version}.tar.gz`

Extract the zip to install the Skill.

- Using MiniMax M2.7 with Claude Code - [Test Results](./test.md)
## Project Structure

```
enterprise-qa/
├── .claude/
│   └── skills/
│       └── enterprise-qa/
│           ├── SKILL.md         # Skill definition
│           ├── tools/          # Tool implementation
│           └── tests/          # Unit tests
├── knowledge/                   # Knowledge base documents
├── enterprise.db               # SQLite database
├── config.yaml.example         # Configuration file example
├── requirements.txt            # Dependencies
├── requirements-dev.txt        # Dependencies including testing and code inspection tools
```

### Directory Structure

```
.venv/                      # Python virtual environment (auto-created)
htmlcov/                    # Test coverage report (generated after tests)
logs/                       # Log files (auto-created at runtime)
session.json               # Conversation history (auto-created for multi-turn)
enterprise.db              # SQLite database
config.yaml                # Configuration file (optional, copied from config.yaml.example)
```

## Deliverables

| Item | Location/Status |
|------|----------------|
| Skill executable in Claude Code | `.claude/skills/enterprise-qa/SKILL.md` |
| Test database enterprise.db | Project root |
| Knowledge base knowledge/ | Project root |
| Skill usage instructions | This file |
| Test case execution | This file |
| Dependencies requirements.txt | Project root |
| Configuration file example | `config.yaml.example` |