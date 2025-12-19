from owlready2 import *
from pathlib import Path

# Đường dẫn ontology
ENGINE_DIR = Path(__file__).resolve().parent
ONTO_FILE = ENGINE_DIR / "traffic_ontology.owl"

# Load ontology
onto = get_ontology(str(ONTO_FILE)).load()
print("[05_inference_engine.py] Ontology loaded")

def infer_penalties(vehicle_id=None, action_id=None, condition_id=None):
    """
    vehicle_id: mã phương tiện (ví dụ 'PT01')
    action_id: mã hành vi (ví dụ 'HV02')
    condition_id: mã điều kiện (ví dụ 'DK01')
    Trả về danh sách luật áp dụng
    """
    results = []
    
    for law in onto.LuatXuPhat.instances():
        # Kiểm tra phương tiện
        if vehicle_id:
            vehicle_names = [pt.name for pt in law.ap_dung_cho_phuong_tien] if law.ap_dung_cho_phuong_tien else []
            if vehicle_id not in vehicle_names:
                continue

        # Kiểm tra hành vi
        if action_id:
            action_names = [hv.name for hv in law.ap_dung_hanh_vi] if law.ap_dung_hanh_vi else []
            if action_id not in action_names:
                continue

        # Kiểm tra điều kiện
        if law.co_dieu_kien_ap_dung:
            condition_names = [dk.name for dk in law.co_dieu_kien_ap_dung]
            if condition_id and condition_id not in condition_names:
                continue

        # Lấy thông tin đầy đủ từ luật
        law_dict = {
            "id_luat": law.name,
            "phuong_tien": [pt.name for pt in law.ap_dung_cho_phuong_tien] if law.ap_dung_cho_phuong_tien else [],
            "hanh_vi": [hv.name for hv in law.ap_dung_hanh_vi] if law.ap_dung_hanh_vi else [],
            "dieu_kien": [dk.name for dk in law.co_dieu_kien_ap_dung] if law.co_dieu_kien_ap_dung else [],
            "van_ban": [vb.name for vb in law.can_cu_van_ban] if law.can_cu_van_ban else [],
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
