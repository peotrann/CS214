import pandas as pd
from pathlib import Path
import re
import importlib.util
from datetime import datetime

# Load modules: inference + alias
ENGINE_DIR = Path(__file__).resolve().parent.parent / "Engine"

# Inference engine
spec = importlib.util.spec_from_file_location(
    "engine_module",
    ENGINE_DIR / "05_inference_engine.py"
)
engine_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine_module)

# Alias resolver
spec = importlib.util.spec_from_file_location(
    "alias_module",
    ENGINE_DIR / "06_alias_resolver.py"
)
alias_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(alias_module)

# Load reference data
DATA_DIR = Path(__file__).resolve().parent.parent / "Data"
df_pt = pd.read_excel(DATA_DIR / "phuong_tien.xlsx")
df_hv = pd.read_excel(DATA_DIR / "hanh_vi.xlsx")
df_dk = pd.read_excel(DATA_DIR / "dieu_kien.xlsx")
df_vb = pd.read_excel(DATA_DIR / "van_ban_phap_luat.xlsx")

pt_id2name = dict(zip(df_pt.id_phuong_tien, df_pt.ten_phuong_tien))
hv_id2name = dict(zip(df_hv.id_hanh_vi, df_hv.ten_hanh_vi))
dk_id2name = dict(zip(df_dk.id_dieu_kien, df_dk.ten_dieu_kien))
vb_id2info = df_vb.set_index("id_van_ban").to_dict("index")

# Helpers
def format_money(value):
    """Định dạng tiền: 1000 -> 1.000.000 VND"""
    if value is None:
        return ""
    try:
        return f"{int(value*1000):,}".replace(",", ".")
    except:
        return str(value)

def format_date(value):
    """Định dạng ngày dd/mm/yyyy"""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    if isinstance(value, pd.Timestamp):
        return value.strftime("%d/%m/%Y")
    return str(value)

def format_validity(vb_info):
    """Hiệu lực văn bản"""
    from_date = format_date(vb_info.get("hieu_luc_tu"))
    to_date = format_date(vb_info.get("hieu_luc_den")) or "nay"
    return f"{from_date} -> {to_date}"

def find_year(text):
    """Tìm năm trong query"""
    m = re.search(r"\b(19\d{2}|20\d{2})\b", text)
    return int(m.group(0)) if m else None

# Main API: filter laws
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

        # lọc theo năm nếu có
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
            "doi_tuong_ap_dung": law.get("doi_tuong_ap_dung"),  # thêm trường này
            "van_ban": vb_info.get("ten_van_ban"),
            "so_hieu": vb_info.get("so_hieu"),
            "loai": vb_info.get("loai"),
            "nam": vb_info.get("nam"),
            "ngay_ban_hanh": format_validity(vb_info),
            "hieu_luc": format_validity(vb_info),
            "tinh_trang": vb_info.get("tinh_trang")
        })

    return results

# CLI test mode
if __name__ == "__main__":
    print("Nhập câu hỏi vi phạm giao thông (gõ exit để thoát)\n")

    while True:
        query = input("Câu hỏi: ").strip()
        if query.lower() == "exit":
            break

        results = filter_laws_for_web(query)

        if not results:
            print("Không tìm thấy luật phù hợp\n")
            continue

        for r in results:
            print("=" * 60)
            print(f"Luật: {r['id_luat']}")
            print(f"Hành vi: {', '.join(r['hanh_vi'])}")
            print(f"Phương tiện: {', '.join(r['phuong_tien'])}")
            print(f"Mức phạt: {r['muc_phat_min']} - {r['muc_phat_max']}")
            print(f"Văn bản: {r['van_ban']}")
            print(f"Số hiệu: {r['so_hieu']}")
            print(f"Hiệu lực: {r['hieu_luc']}")
            print(f"Tình trạng: {r['tinh_trang']}")
            print(f"Điều/Khoản: {r['dieu']} / {r['khoan']}")
            print(f"Đối tượng áp dụng: {r['doi_tuong_ap_dung']}")
            if r["ghi_chu"]:
                print(f"Ghi chú: {r['ghi_chu']}")
            print("=" * 60)
            print()
