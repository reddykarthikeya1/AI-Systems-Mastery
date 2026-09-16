import re
from pathlib import Path

mods = sorted(p for p in Path('.').glob('Module_*') if p.is_dir())
def has(d, pat): return any(d.rglob(pat))

cell_pat = re.compile(r'"cell_type"')
def count_cells(d):
    total = 0
    for f in d.glob('*.ipynb'):
        txt = f.read_text(encoding='utf-8', errors='ignore')
        total += len(cell_pat.findall(txt))
    return total

tier_pat = re.compile(r'Tier \d')
def count_tiers(d):
    p = d / 'PROJECT_GUIDE.md'
    if not p.exists():
        return 0
    return len(tier_pat.findall(p.read_text(encoding='utf-8', errors='ignore')))

n_live = sum(has(d, '*_live.py') for d in mods)
n_notebooks = sum(count_cells(d) >= 12 for d in mods)
n_quizzes = sum((d / 'SELF_ASSESSMENT_AND_CHALLENGES.md').exists() for d in mods)
n_trouble = sum((d / 'TROUBLESHOOTING_AND_EDGE_CASES.md').exists() for d in mods)
n_projects = sum(count_tiers(d) >= 3 for d in mods)
n_readmes = sum(len((d / 'README.md').read_text(encoding='utf-8', errors='ignore').splitlines()) >= 150 for d in mods)
n_starters = sum(has(d, '*.py') and (d / 'starter').exists() for d in mods)
n_debug = sum((d / 'debug_lab').exists() for d in mods)
n_checkpoints = len(list(Path('Phase_Checkpoints').glob('PHASE_*_CHECKPOINT.md')))

# Count real drivers imported across the repo
driver_files = []
drivers = ["import psycopg2", "import pymongo", "import redis", "from neo4j", "from cassandra", "import duckdb", "import oracledb", "from elasticsearch", "from qdrant_client", "import boto3"]
for f in Path('.').rglob('*.py'):
    if "site-packages" in str(f) or ".pytest_cache" in str(f) or "tools" in str(f):
        continue
    try:
        txt = f.read_text(encoding='utf-8', errors='ignore')
        if any(d in txt for d in drivers):
            driver_files.append(f)
    except Exception:
        pass

print("==================================================================")
print("             CURRICULUM AUDIT: 10/10 TARGET METRICS               ")
print("==================================================================")
print(f"live/real-engine files: {n_live} / 22 (M20 & M03 exempt)")
print(f"notebooks >=12 cells  : {n_notebooks} / 24")
print(f"quizzes               : {n_quizzes} / 24")
print(f"troubleshooting       : {n_trouble} / 24")
print(f"3-tier project guides : {n_projects} / 24")
print(f"READMEs >=150 lines   : {n_readmes} / 24")
print(f"starters              : {n_starters} / 24")
print(f"debug labs            : {n_debug} / 24")
print(f"phase checkpoints     : {n_checkpoints} / 8")
print(f"real driver files     : {len(set(driver_files))} (target >= 20)")
print("==================================================================")
