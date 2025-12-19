from owlready2 import *
from pathlib import Path

ENGINE_DIR = Path(__file__).resolve().parent
ONTO_FILE = ENGINE_DIR / "traffic_ontology.owl"

# Load ontology
onto = get_ontology(str(ONTO_FILE)).load()
print("[04_knowledge_ifthen.py] Ontology loaded from OWL file")

def safe_getattr(obj, attr):
    """Lấy thuộc tính nếu tồn tại, nếu None trả về None"""
    return getattr(obj, attr) if hasattr(obj, attr) and getattr(obj, attr) is not None else None

def build_rules():
    rules = []
    for l in onto.LuatXuPhat.instances():
        phuong_tien_list = [pt.name for pt in l.ap_dung_cho_phuong_tien] if l.ap_dung_cho_phuong_tien else []
        hanh_vi_list = [hv.name for hv in l.ap_dung_hanh_vi] if l.ap_dung_hanh_vi else []
        dieu_kien_list = [dk.name for dk in l.co_dieu_kien_ap_dung] if l.co_dieu_kien_ap_dung else []
        van_ban_list = [vb.name for vb in l.can_cu_van_ban] if l.can_cu_van_ban else []

        rule = {
            "id_luat": l.name,
            "phuong_tien": phuong_tien_list,
            "hanh_vi": hanh_vi_list,
            "dieu_kien": dieu_kien_list,
            "van_ban": van_ban_list,
            "muc_phat_min": safe_getattr(l, "muc_phat_min"),
            "muc_phat_max": safe_getattr(l, "muc_phat_max"),
            "hinh_thuc_bo_sung": safe_getattr(l, "hinh_thuc_bo_sung"),
            "dieu": safe_getattr(l, "dieu"),
            "khoan": safe_getattr(l, "khoan"),
            "doi_tuong_ap_dung": safe_getattr(l, "doi_tuong_ap_dung"),
            "ghi_chu": safe_getattr(l, "ghi_chu")
        }
        rules.append(rule)
    return rules

if __name__ == "__main__":
    rules = build_rules()
    print(f"[04_knowledge_ifthen.py] Tổng số luật IF–THEN: {len(rules)}")
    # Hiển thị 5 luật đầu tiên
    for r in rules[:5]:
        print(r)
