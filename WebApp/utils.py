import pandas as pd
from pathlib import Path
import re
import importlib.util

# Import engine
ENGINE_DIR = Path(__file__).resolve().parent.parent / "Engine"
spec = importlib.util.spec_from_file_location("engine_module", ENGINE_DIR / "05_inference_engine.py")
engine_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine_module)

# Load dữ liệu Excel
DATA_DIR = Path(__file__).resolve().parent.parent / "Data"
df_pt = pd.read_excel(DATA_DIR / "phuong_tien.xlsx")
df_hv = pd.read_excel(DATA_DIR / "hanh_vi.xlsx")
df_dk = pd.read_excel(DATA_DIR / "dieu_kien.xlsx")
df_vb = pd.read_excel(DATA_DIR / "van_ban_phap_luat.xlsx")

# Build dictionaries id <-> tên
def build_dict(df, id_col, name_col):
    id2name = dict(zip(df[id_col], df[name_col]))
    name2id = dict(zip(df[name_col].str.lower(), df[id_col]))
    return id2name, name2id

pt_id2name, pt_name2id = build_dict(df_pt, "id_phuong_tien", "ten_phuong_tien")
hv_id2name, hv_name2id = build_dict(df_hv, "id_hanh_vi", "ten_hanh_vi")
dk_id2name, dk_name2id = build_dict(df_dk, "id_dieu_kien", "mo_ta")
vb_id2info = df_vb.set_index("id_van_ban").to_dict("index")

# Tìm từ khóa trong câu (không phân biệt hoa thường)
def find_keyword(input_text, kw_dict):
    input_lower = input_text.lower()
    matched = [kw for kw in kw_dict if kw in input_lower]
    return max(matched, key=len) if matched else None

# Tìm năm trong câu nhập
def find_year(input_text):
    m = re.search(r"\b(20\d{2}|19\d{2})\b", input_text)
    return int(m.group(0)) if m else None

# Phân tích câu hỏi
def parse_query(query):
    vehicle_kw = find_keyword(query, pt_name2id)
    action_kw = find_keyword(query, hv_name2id)
    condition_kw = find_keyword(query, dk_name2id)
    year = find_year(query)
    return vehicle_kw, action_kw, condition_kw, year

# Lọc luật và format chuẩn cho web
def filter_laws_for_web(vehicle_kw=None, action_kw=None, condition_kw=None, year=None):
    vid = pt_name2id.get(vehicle_kw.lower()) if vehicle_kw else None
    aid = hv_name2id.get(action_kw.lower()) if action_kw else None
    did = dk_name2id.get(condition_kw.lower()) if condition_kw else None

    laws = engine_module.infer_penalties(vehicle_id=vid, action_id=aid, condition_id=did)
    results = []

    for law in laws:
        # Lấy thông tin văn bản
        vb_id = law.get("van_ban", [])
        vb_info = vb_id2info.get(vb_id[0] if vb_id else None, {})

        # Kiểm tra năm nếu có
        if year and vb_info.get("nam") != year:
            continue

        # Thời gian hiệu lực
        hieu_luc_tu = vb_info.get("hieu_luc_tu")
        hieu_luc_den = vb_info.get("hieu_luc_den")
        hieu_luc_tu_fmt = pd.to_datetime(hieu_luc_tu).strftime("%d/%m/%Y") if pd.notna(hieu_luc_tu) else "Không có"
        hieu_luc_den_fmt = pd.to_datetime(hieu_luc_den).strftime("%d/%m/%Y") if pd.notna(hieu_luc_den) else "hiện nay"

        results.append({
            "luat": law.get("id_luat"),
            "phuong_tien": [pt_id2name.get(pt, pt) for pt in law.get("phuong_tien", [])],
            "hanh_vi": [hv_id2name.get(hv, hv) for hv in law.get("hanh_vi", [])],
            "dieu_kien": [dk_id2name.get(dk, dk) for dk in law.get("dieu_kien", [])] or ["Không có"],
            "muc_phat_min": "{:,}".format(law.get("muc_phat_min")) if law.get("muc_phat_min") else "Không xác định",
            "muc_phat_max": "{:,}".format(law.get("muc_phat_max")) if law.get("muc_phat_max") else "Không xác định",
            "hinh_thuc_bo_sung": law.get("hinh_thuc_bo_sung") or "Không có",
            "dieu": law.get("dieu") or "Không có",
            "khoan": law.get("khoan") or "Không có",
            "doi_tuong_ap_dung": law.get("doi_tuong_ap_dung") or "Không có",
            "ghi_chu": law.get("ghi_chu") or "Không có",
            "van_ban": vb_info.get("ten_van_ban") or "Không có",
            "so_hieu": vb_info.get("so_hieu") or "Không có",
            "loai": vb_info.get("loai") or "Không có",
            "nam": vb_info.get("nam") or "Không có",
            "hieu_luc": f"{hieu_luc_tu_fmt} -> {hieu_luc_den_fmt}",
            "tinh_trang": vb_info.get("tinh_trang") or "Không có"
        })

    return results
