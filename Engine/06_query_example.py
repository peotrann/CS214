import pandas as pd
from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec
import re

# Đường dẫn module engine
ENGINE_DIR = Path(__file__).resolve().parent
spec = spec_from_file_location("engine_module", ENGINE_DIR / "05_inference_engine.py")
engine_module = module_from_spec(spec)
spec.loader.exec_module(engine_module)

# Đường dẫn dữ liệu Excel
DATA_DIR = ENGINE_DIR.parent / "Data"

# Load dữ liệu từ Excel
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
vb_id2info = df_vb.set_index("id_van_ban").to_dict("index")  # id_van_ban -> dict thông tin

# Tìm từ khóa trong câu (không phân biệt hoa thường)
def find_keyword(input_text, kw_dict):
    input_lower = input_text.lower()
    matched = [kw for kw in kw_dict if kw in input_lower]
    if matched:
        return max(matched, key=len)  # chọn từ dài nhất nếu có nhiều match
    return None

# Tìm năm trong câu nhập
def find_year(input_text):
    m = re.search(r"\b(20\d{2}|19\d{2})\b", input_text)
    return int(m.group(0)) if m else None

# Lọc luật dựa trên từ khóa (None = tất cả)
def filter_laws(vehicle_kw=None, action_kw=None, condition_kw=None, year=None):
    vid = pt_name2id.get(vehicle_kw.lower()) if vehicle_kw else None
    aid = hv_name2id.get(action_kw.lower()) if action_kw else None
    did = dk_name2id.get(condition_kw.lower()) if condition_kw else None

    laws = engine_module.infer_penalties(vehicle_id=vid, action_id=aid, condition_id=did)

    results = []
    for law in laws:
        vb_info = vb_id2info.get(law.get("van_ban")[0] if law.get("van_ban") else None, {})
        if year and vb_info.get("nam") != year:
            continue
        results.append(law)
    return results

# Hiển thị luật dễ đọc, hỗ trợ nhiều phương tiện/hành vi/điều kiện
def display_law_readable(law):
    vb_info = vb_id2info.get(law.get("van_ban")[0] if law.get("van_ban") else None, {})

    min_fine = f"{int(law['muc_phat_min']):,} VND" if law.get('muc_phat_min') else "Không xác định"
    max_fine = f"{int(law['muc_phat_max']):,} VND" if law.get('muc_phat_max') else "Không xác định"

    start = vb_info.get("hieu_luc_tu")
    end = vb_info.get("hieu_luc_den")
    start_str = pd.to_datetime(start).strftime("%d/%m/%Y") if pd.notna(start) else "Không xác định"
    end_str = pd.to_datetime(end).strftime("%d/%m/%Y") if pd.notna(end) else "hiện nay"

    htbs_str = law.get("hinh_thuc_bo_sung") or "Không có"
    dieu = law.get('dieu', 'Không có')
    khoan = law.get('khoan', 'Không có')
    doi_tuong = law.get('doi_tuong_ap_dung', 'Không có')
    ghi_chu = law.get('ghi_chu', 'Không có')

    phuong_tien_names = [pt_id2name.get(pt, pt) for pt in law.get('phuong_tien', [])]
    hanh_vi_names = [hv_id2name.get(hv, hv) for hv in law.get('hanh_vi', [])]
    dieu_kien_names = [dk_id2name.get(dk, dk) for dk in law.get('dieu_kien', [])]

    print("===============================================")
    print(f"Luật áp dụng: {law['id_luat']}")
    print(f"Hành vi: {', '.join(hanh_vi_names)}")
    print(f"Phương tiện: {', '.join(phuong_tien_names)}")
    if dieu_kien_names:
        print(f"Điều kiện áp dụng: {', '.join(dieu_kien_names)}")
    print(f"Mức phạt tiền: {min_fine} – {max_fine}")
    print(f"Hình thức xử phạt bổ sung: {htbs_str}")
    print(f"Văn bản pháp luật: {vb_info.get('ten_van_ban', 'Không xác định')} "
          f"({vb_info.get('so_hieu', '')}, {vb_info.get('loai', '')}, Năm {vb_info.get('nam', '')})")
    print(f"Hiệu lực: {start_str} -> {end_str} | Tình trạng: {vb_info.get('tinh_trang', 'Không xác định')}")
    print(f"Điều/Khoản: {dieu} / {khoan}")
    print(f"Đối tượng áp dụng: {doi_tuong}")
    print(f"Ghi chú: {ghi_chu}")
    print("===============================================\n")

# Interactive
if __name__ == "__main__":
    print("[06_query_example.py] Nhập câu hỏi về vi phạm giao thông.")
    print("Có thể thiếu từ khóa hoặc nhập năm để lọc luật.")
    print("Ví dụ: Xe máy không đội mũ bảo hiểm, Xe tải vượt đèn đỏ 2024\n")

    while True:
        user_input = input("Câu hỏi (hoặc gõ 'exit' để thoát): ").strip()
        if user_input.lower() == "exit":
            break

        vehicle_kw = find_keyword(user_input, pt_name2id)
        action_kw = find_keyword(user_input, hv_name2id)
        condition_kw = find_keyword(user_input, dk_name2id)
        year = find_year(user_input)

        print(f"[DEBUG] Vehicle keyword: {vehicle_kw}, Action keyword: {action_kw}, "
              f"Condition keyword: {condition_kw}, Year: {year}")

        results = filter_laws(vehicle_kw, action_kw, condition_kw, year)
        if not results:
            print("Không tìm thấy luật phù hợp với điều kiện nhập vào. Hiển thị tất cả luật liên quan:")
            results = filter_laws()  # hiển thị tất cả luật

        for law in results:
            display_law_readable(law)
