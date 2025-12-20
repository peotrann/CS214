import pandas as pd
from pathlib import Path
import re
import importlib.util
from datetime import datetime

# Load inference engine
ENGINE_DIR = Path(__file__).resolve().parent.parent / "Engine"
spec = importlib.util.spec_from_file_location(
    "engine_module",
    ENGINE_DIR / "05_inference_engine.py"
)
engine_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine_module)

# Load alias resolver
spec = importlib.util.spec_from_file_location(
    "alias_module",
    ENGINE_DIR / "06_alias_resolver.py"
)
alias_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(alias_module)

# Load data
DATA_DIR = Path(__file__).resolve().parent.parent / "Data"
df_pt = pd.read_excel(DATA_DIR / "phuong_tien.xlsx")
df_hv = pd.read_excel(DATA_DIR / "hanh_vi.xlsx")
df_dk = pd.read_excel(DATA_DIR / "dieu_kien.xlsx")
df_vb = pd.read_excel(DATA_DIR / "van_ban_phap_luat.xlsx")

pt_id2name = dict(zip(df_pt.id_phuong_tien, df_pt.ten_phuong_tien))
hv_id2name = dict(zip(df_hv.id_hanh_vi, df_hv.ten_hanh_vi))
dk_id2name = dict(zip(df_dk.id_dieu_kien, df_dk.ten_dieu_kien))
vb_id2info = df_vb.set_index("id_van_ban").to_dict("index")

# Format money in VND with ".000"
def format_money(value):
    if value is None:
        return ""
    try:
        return f"{int(value*1000):,}".replace(",", ".")
    except:
        return str(value)

# Parse year from text
def find_year(text):
    m = re.search(r"\b(19\d{2}|20\d{2})\b", text)
    return int(m.group(0)) if m else None

# Format legal document validity
def format_validity(vb_info):
    from_date = vb_info.get("hieu_luc_tu")
    to_date = vb_info.get("hieu_luc_den")
    if from_date is None:
        from_date = ""
    if to_date is None or pd.isna(to_date):
        to_date = "nay"
    return f"{from_date} -> {to_date}"

# API for web display
def filter_laws_for_web(query_text):
    vehicle_id = alias_module.resolve_vehicle(query_text)
    action_id = alias_module.resolve_action(query_text)
    condition_id = alias_module.resolve_condition(query_text)
    year = find_year(query_text)

    laws = engine_module.infer_penalties(
        vehicle_id=vehicle_id,
        action_id=action_id,
        condition_id=condition_id
    )

    results = []

    for law in laws:
        vb_ids = law.get("van_ban", [])
        vb_info = vb_id2info.get(vb_ids[0] if vb_ids else None, {})

        if year and vb_info.get("nam") != year:
            continue

        results.append({
            "id_luat": law.get("id_luat"),
            "phuong_tien": [pt_id2name.get(p, p) for p in law.get("phuong_tien", [])],
            "hanh_vi": [hv_id2name.get(h, h) for h in law.get("hanh_vi", [])],
            "dieu_kien": [dk_id2name.get(d, d) for d in law.get("dieu_kien", [])],
            "muc_phat_min": format_money(law.get("muc_phat_min")),
            "muc_phat_max": format_money(law.get("muc_phat_max")),
            "hinh_thuc_bo_sung": law.get("hinh_thuc_bo_sung"),
            "dieu": law.get("dieu"),
            "khoan": law.get("khoan"),
            "ghi_chu": law.get("ghi_chu"),
            "doi_tuong_ap_dung": law.get("doi_tuong_ap_dung"), 
            "van_ban": vb_info.get("ten_van_ban"),
            "so_hieu": vb_info.get("so_hieu"),
            "loai": vb_info.get("loai"),
            "nam": vb_info.get("nam"),
            "hieu_luc": format_validity(vb_info),
            "tinh_trang": vb_info.get("tinh_trang")
        })

    return results
