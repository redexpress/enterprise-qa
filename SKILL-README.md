# Enterprise QA Skill

This project is an internal enterprise question-answering system.

It supports querying:
- Employee information (SQLite database)
- Attendance records
- Project data
- Promotion evaluation info
- Internal knowledge base documents

## Features

- Structured data query via SQLite (enterprise.db)
- Unstructured knowledge search via local files (knowledge/)
- Automatic query routing via Python tools
- Lightweight, no external dependencies required

## How It Works

1. User asks a question
2. Skill routes query to appropriate module:
   - Employee → query_employee.py
   - Attendance → attendance_query.py
   - Promotion → promotion_check.py
   - Project → project_query.py
   - Knowledge → kb_search.py
3. Data is retrieved from:
   - SQLite database
   - Local knowledge files

## Dependencies

Install Python dependencies:

```shell
pip install -r requirements.txt
```

## Notes

* No external API calls
* No internet access required
* All data is local
