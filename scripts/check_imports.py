import sys
from importlib import import_module
sys.path.insert(0, r"f:\\student portal\\grievance_portal")
modules = [
    "app",
    "app.db",
    "app.db.base",
    "app.models",
    "app.models.grievance",
    "app.models.department",
    "app.models.audit",
]

for m in modules:
    try:
        mod = import_module(m)
        print(f"OK: {m} -> {getattr(mod, '__file__', None)}")
    except Exception as e:
        print(f"ERROR: {m} -> {type(e).__name__}: {e}")
