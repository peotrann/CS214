from owlready2 import *
from pathlib import Path
import importlib.util

ENGINE_DIR = Path(__file__).resolve().parent
ONTO_FILE = ENGINE_DIR / "traffic_ontology.owl"

onto = get_ontology(str(ONTO_FILE)).load()
print("[05_inference_engine.py] Ontology loaded")

spec = importlib.util.spec_from_file_location(
    "alias_module",
    ENGINE_DIR / "06_alias_resolver.py"
)
alias_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(alias_module)

def safe_getattr(obj, attr):
    return getattr(obj, attr) if hasattr(obj, attr) and getattr(obj, attr) is not None else None

def infer_penalties(vehicle_id=None, action_id=None, condition_id=None):
    inferred_results = []

    for law in onto.LuatXuPhat.instances():
        if not law.name:
            continue

        vehicle_names = []
        vehicle_aliases = []
        if law.ap_dung_cho_phuong_tien:
            for pt in law.ap_dung_cho_phuong_tien:
                vehicle_names.append(pt.name)
                alias = alias_module.resolve_vehicle(pt.name)
                if alias:
                    vehicle_aliases.append(alias)
        if vehicle_id and (vehicle_id not in vehicle_names and vehicle_id not in vehicle_aliases):
            continue

        action_names = []
        action_aliases = []
        if law.ap_dung_hanh_vi:
            for hv in law.ap_dung_hanh_vi:
                action_names.append(hv.name)
                alias = alias_module.resolve_action(hv.name)
                if alias:
                    action_aliases.append(alias)
        if action_id and (action_id not in action_names and action_id not in action_aliases):
            continue

        law_condition_names = []
        law_condition_aliases = []
        if law.co_dieu_kien_ap_dung:
            for dk in law.co_dieu_kien_ap_dung:
                law_condition_names.append(dk.name)
                alias = alias_module.resolve_condition(dk.name)
                if alias:
                    law_condition_aliases.append(alias)
        if condition_id:
            if not law_condition_names and not law_condition_aliases:
                continue
            if condition_id not in law_condition_names and condition_id not in law_condition_aliases:
                continue

        law_dict = {
            "id_luat": law.name,
            "phuong_tien": vehicle_names if vehicle_names else [],
            "hanh_vi": action_names if action_names else [],
            "dieu_kien": law_condition_names if law_condition_names else [],
            "van_ban": [vb.name for vb in law.can_cu_van_ban] if law.can_cu_van_ban else [],
            "muc_phat_min": safe_getattr(law, "muc_phat_min"),
            "muc_phat_max": safe_getattr(law, "muc_phat_max"),
            "hinh_thuc_bo_sung": safe_getattr(law, "hinh_thuc_bo_sung"),
            "dieu": safe_getattr(law, "dieu"),
            "khoan": safe_getattr(law, "khoan"),
            "doi_tuong_ap_dung": safe_getattr(law, "doi_tuong_ap_dung"),
            "ghi_chu": safe_getattr(law, "ghi_chu")
        }

        suy_ra_list = []
        min_penalty = law_dict["muc_phat_min"]
        max_penalty = law_dict["muc_phat_max"]
        hinh_thuc = law_dict["hinh_thuc_bo_sung"]
        if min_penalty or max_penalty:
            suy_ra_list.append(f"Mức phạt từ {min_penalty or 0} đến {max_penalty or 0}")
        if hinh_thuc:
            suy_ra_list.append(f"Hình thức bổ sung: {hinh_thuc}")
        law_dict["suy_ra"] = "; ".join(suy_ra_list) if suy_ra_list else "Không có thông tin suy diễn"

        inferred_results.append(law_dict)

    return inferred_results
