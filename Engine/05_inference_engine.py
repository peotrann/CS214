from owlready2 import *
from pathlib import Path

# Đường dẫn ontology
ENGINE_DIR = Path(__file__).resolve().parent
ONTO_FILE = ENGINE_DIR / "traffic_ontology.owl"

# Load ontology
onto = get_ontology(str(ONTO_FILE)).load()
print("[05_inference_engine.py] Ontology loaded")

def infer_penalties(vehicle_id, action_id, condition_id=None):
    """
    Hàm suy diễn luật: trả về danh sách luật áp dụng cho phương tiện, hành vi, điều kiện.
    """
    results = []
    for law in onto.LuatXuPhat.instances():
        # Kiểm tra phương tiện
        if law.ap_dung_cho_phuong_tien[0].name != vehicle_id:
            continue
        # Kiểm tra hành vi
        if law.ap_dung_hanh_vi[0].name != action_id:
            continue
        # Kiểm tra điều kiện (nếu luật có)
        if law.co_dieu_kien_ap_dung:
            if condition_id is None or law.co_dieu_kien_ap_dung[0].name != condition_id:
                continue
        results.append({
            "id_luat": law.name,
            "phuong_tien": law.ap_dung_cho_phuong_tien[0].name,
            "hanh_vi": law.ap_dung_hanh_vi[0].name,
            "dieu_kien": law.co_dieu_kien_ap_dung[0].name if law.co_dieu_kien_ap_dung else None,
            "van_ban": law.can_cu_van_ban[0].name,
            "muc_phat_min": law.muc_phat_min,
            "muc_phat_max": law.muc_phat_max
        })
    return results
