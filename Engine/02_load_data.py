# 02_load_data.py
import pandas as pd
from pathlib import Path

ENGINE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = ENGINE_DIR.parent
DATA_DIR = PROJECT_ROOT / "Data"

def load_excel(name):
    path = DATA_DIR / f"{name}.xlsx"
    if not path.exists():
        print(f"[02_load_data.py] ERROR: Missing file {path}")
        raise FileNotFoundError(f"Missing file: {path}")
    print(f"[02_load_data.py] Loading {path}")
    return pd.read_excel(path)

def load_all_data():
    data = {
        "phuong_tien": load_excel("phuong_tien"),
        "hanh_vi": load_excel("hanh_vi"),
        "dieu_kien": load_excel("dieu_kien"),
        "van_ban": load_excel("van_ban_phap_luat"),
        "luat": load_excel("luat_xu_phat"),
    }
    print("[02_load_data.py] All Excel files loaded successfully")
    return data
