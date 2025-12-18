# 04_knowledge_ifthen.py
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
        phuong_tien = l.ap_dung_cho_phuong_tien[0].name if l.ap_dung_cho_phuong_tien else None
        hanh_vi = l.ap_dung_hanh_vi[0].name if l.ap_dung_hanh_vi else None
        dieu_kien = l.co_dieu_kien_ap_dung[0].name if l.co_dieu_kien_ap_dung else None
        van_ban = l.can_cu_van_ban[0].name if l.can_cu_van_ban else None
        muc_phat_min = safe_getattr(l, "muc_phat_min")
        muc_phat_max = safe_getattr(l, "muc_phat_max")

        rule = {
            "id_luat": l.name,
            "phuong_tien": phuong_tien,
            "hanh_vi": hanh_vi,
            "dieu_kien": dieu_kien,
            "van_ban": van_ban,
            "muc_phat_min": muc_phat_min,
            "muc_phat_max": muc_phat_max
        }
        rules.append(rule)
    return rules

if __name__ == "__main__":
    rules = build_rules()
    print(f"[04_knowledge_ifthen.py] Tổng số luật IF–THEN: {len(rules)}")
    for r in rules[:5]:
        print(r)
