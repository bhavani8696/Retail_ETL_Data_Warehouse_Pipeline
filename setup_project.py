from pathlib import Path

PROJECT_NAME = "Retail_ETL_Data_Warehouse_Pipeline"

folders = [
    "assets/css",
    "assets/js",
    "assets/images",
    "assets/animations",

    "dashboard/components",
    "dashboard/pages",
    "dashboard/charts",

    "data/raw",
    "data/processed",
    "data/backup",
    "data/warehouse",

    "docs",
    "logs",
    "reports",

    "sql",

    "src/extract",
    "src/validate",
    "src/transform",
    "src/load",
    "src/warehouse",
    "src/analytics",
    "src/utils",
    "src/config",

    "tests"
]

files = [
    "README.md",
    "requirements.txt",
    ".gitignore",
    "main.py",

    "dashboard/app.py",

    "sql/create_tables.sql",

    "src/__init__.py",
    "src/extract/__init__.py",
    "src/validate/__init__.py",
    "src/transform/__init__.py",
    "src/load/__init__.py",
    "src/warehouse/__init__.py",
    "src/analytics/__init__.py",
    "src/utils/__init__.py",
    "src/config/__init__.py",
]

base = Path.cwd()

print("\nCreating folders...\n")

for folder in folders:
    path = base / folder
    path.mkdir(parents=True, exist_ok=True)
    print(f"Created: {folder}")

print("\nCreating files...\n")

for file in files:
    path = base / file
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.touch()
    print(f"Created: {file}")

print("\n===================================")
print("Project Structure Created Successfully!")
print("===================================")