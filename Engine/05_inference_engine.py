from owlready2 import *
from pathlib import Path

# Đường dẫn ontology
ENGINE_DIR = Path(__file__).resolve().parent
ONTO_FILE = ENGINE_DIR / "traffic_ontology.owl"

# Load ontology
onto = get_ontology(str(ONTO_FILE)).load()
print("[05_inference_engine.py] Ontology loaded")

def infer_penalties(vehicle_id=None, action_id=None, condition_id=None):
    results = []
    
    for law in onto.LuatXuPhat.instances():
        # Kiểm tra phương tiện (nếu có filter)
        if vehicle_id and law.ap_dung_cho_phuong_tien and law.ap_dung_cho_phuong_tien[0].name != vehicle_id:
            continue
        # Kiểm tra hành vi (nếu có filter)
        if action_id and law.ap_dung_hanh_vi and law.ap_dung_hanh_vi[0].name != action_id:
            continue
        # Kiểm tra điều kiện (nếu luật có)
        if law.co_dieu_kien_ap_dung:
            if condition_id and law.co_dieu_kien_ap_dung[0].name != condition_id:
                continue

        # Lấy thông tin đầy đủ từ luật
        law_dict = {
            "id_luat": law.name,
            "phuong_tien": law.ap_dung_cho_phuong_tien[0].name if law.ap_dung_cho_phuong_tien else None,
            "hanh_vi": law.ap_dung_hanh_vi[0].name if law.ap_dung_hanh_vi else None,
            "dieu_kien": law.co_dieu_kien_ap_dung[0].name if law.co_dieu_kien_ap_dung else None,
            "van_ban": law.can_cu_van_ban[0].name if law.can_cu_van_ban else None,
            "muc_phat_min": getattr(law, "muc_phat_min", None),
            "muc_phat_max": getattr(law, "muc_phat_max", None),
            "hinh_thuc_bo_sung": getattr(law, "hinh_thuc_bo_sung", None),
            "dieu": getattr(law, "dieu", None),
            "khoan": getattr(law, "khoan", None),
            "doi_tuong_ap_dung": getattr(law, "doi_tuong_ap_dung", None),
            "ghi_chu": getattr(law, "ghi_chu", None)
        }

        results.append(law_dict)
        
    return results
