import pandas as pd
from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec

# Đường dẫn module engine
ENGINE_DIR = Path(__file__).resolve().parent
spec = spec_from_file_location("engine_module", ENGINE_DIR / "05_inference_engine.py")
engine_module = module_from_spec(spec)
spec.loader.exec_module(engine_module)

# Đường dẫn dữ liệu Excel
DATA_DIR = ENGINE_DIR.parent / "Data"

# Load Excel để map từ khóa -> id
df_pt = pd.read_excel(DATA_DIR / "phuong_tien.xlsx")
df_hv = pd.read_excel(DATA_DIR / "hanh_vi.xlsx")
df_dk = pd.read_excel(DATA_DIR / "dieu_kien.xlsx")

# Hàm tạo dictionary từ tên -> id
def build_dict(df):
    cols = df.columns
    # Giả sử 2 cột đầu: id, tên
    return dict(zip(df[cols[1]], df[cols[0]]))

pt_dict = build_dict(df_pt)
hv_dict = build_dict(df_hv)
dk_dict = build_dict(df_dk)

# Chuyển từ khóa sang id
def keyword_to_id(vehicle_kw, action_kw, condition_kw=None):
    vehicle_id = pt_dict.get(vehicle_kw)
    action_id = hv_dict.get(action_kw)
    condition_id = dk_dict.get(condition_kw) if condition_kw else None
    if vehicle_id is None or action_id is None:
        raise ValueError(f"Không tìm thấy id cho từ khóa: {vehicle_kw}, {action_kw}")
    return vehicle_id, action_id, condition_id

# Danh sách câu hỏi (nhiều case)

"""
questions = [
    {"vehicle": "Xe máy", "action": "Không đội mũ bảo hiểm", "condition": None},
    {"vehicle": "Xe tải", "action": "Vượt đèn đỏ", "condition": "Ban ngày"},
    {"vehicle": "Xe máy", "action": "Chạy quá tốc độ", "condition": None},
    {"vehicle": "Ô tô con", "action": "Chạy quá tốc độ", "condition": "Gây tai nạn giao thông"},
]


# Thực hiện hỏi đáp
if __name__ == "__main__":
    print("[06_query_example.py] Demo inference with keywords:")

    for i, q in enumerate(questions, 1):
        try:
            vid, aid, did = keyword_to_id(q["vehicle"], q["action"], q["condition"])
            results = engine_module.infer_penalties(vehicle_id=vid, action_id=aid, condition_id=did)
            print(f"\nCase {i}: {q['vehicle']} vi phạm {q['action']}" +
                  (f" với điều kiện {q['condition']}" if q['condition'] else ""))
            for r in results:
                print(r)
        except ValueError as e:
            print(f"\nCase {i}: Lỗi - {e}")

"""