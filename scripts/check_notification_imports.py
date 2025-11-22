import sys
sys.path.insert(0, r"f:\\student portal\\grievance_portal")
from importlib import import_module
modules = [
    "app.core.email",
    "app.core.notifications",
    "app.api.grievances",
    "app.main",
]
for m in modules:
    try:
        mod = import_module(m)
        print(f"OK: {m} -> {getattr(mod, '__file__', None)}")
    except Exception as e:
        print(f"ERROR: {m} -> {type(e).__name__}: {e}")
