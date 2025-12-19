from owlready2 import *
from pathlib import Path

ENGINE_DIR = Path(__file__).resolve().parent
ONTO_FILE = ENGINE_DIR / "traffic_ontology.owl"

# Load ontology
onto = get_ontology(str(ONTO_FILE)).load()
print("[05_inference_engine.py] Ontology loaded")

def safe_getattr(obj, attr):
    """Lấy thuộc tính nếu tồn tại, nếu None trả về None"""
    return getattr(obj, attr) if hasattr(obj, attr) and getattr(obj, attr) is not None else None

def infer_penalties(vehicle_id=None, action_id=None, condition_id=None):
    """
    Động cơ suy diễn (forward chaining):
    - Áp dụng nhiều luật liên quan
    - Trả về danh sách luật áp dụng + trường suy diễn
    """
    inferred_results = []

    for law in onto.LuatXuPhat.instances():
        # Kiểm tra điều kiện phương tiện
        if vehicle_id:
            vehicle_names = [pt.name for pt in law.ap_dung_cho_phuong_tien] if law.ap_dung_cho_phuong_tien else []
            if vehicle_id not in vehicle_names:
                continue

        # Kiểm tra hành vi
        if action_id:
            action_names = [hv.name for hv in law.ap_dung_hanh_vi] if law.ap_dung_hanh_vi else []
            if action_id not in action_names:
                continue

        # Kiểm tra điều kiện áp dụng
        if law.co_dieu_kien_ap_dung:
            condition_names = [dk.name for dk in law.co_dieu_kien_ap_dung]
            if condition_id and condition_id not in condition_names:
                continue

        # Tạo dict luật
        law_dict = {
            "id_luat": law.name,
            "phuong_tien": [pt.name for pt in law.ap_dung_cho_phuong_tien] if law.ap_dung_cho_phuong_tien else [],
            "hanh_vi": [hv.name for hv in law.ap_dung_hanh_vi] if law.ap_dung_hanh_vi else [],
            "dieu_kien": [dk.name for dk in law.co_dieu_kien_ap_dung] if law.co_dieu_kien_ap_dung else [],
            "van_ban": [vb.name for vb in law.can_cu_van_ban] if law.can_cu_van_ban else [],
            "muc_phat_min": safe_getattr(law, "muc_phat_min"),
            "muc_phat_max": safe_getattr(law, "muc_phat_max"),
            "hinh_thuc_bo_sung": safe_getattr(law, "hinh_thuc_bo_sung"),
            "dieu": safe_getattr(law, "dieu"),
            "khoan": safe_getattr(law, "khoan"),
            "doi_tuong_ap_dung": safe_getattr(law, "doi_tuong_ap_dung"),
            "ghi_chu": safe_getattr(law, "ghi_chu")
        }

        min_penalty = safe_getattr(law, "muc_phat_min")
        max_penalty = safe_getattr(law, "muc_phat_max")
        hinh_thuc = safe_getattr(law, "hinh_thuc_bo_sung")

        suy_ra_list = []
        if min_penalty or max_penalty:
            suy_ra_list.append(f"Mức phạt từ {min_penalty or 0} đến {max_penalty or 0}")
        if hinh_thuc:
            suy_ra_list.append(f"Hình thức bổ sung: {hinh_thuc}")

        law_dict["suy_ra"] = "; ".join(suy_ra_list) if suy_ra_list else "Không có thông tin suy diễn"

        inferred_results.append(law_dict)

    return inferred_results