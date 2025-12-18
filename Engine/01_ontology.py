# 01_ontology.py
from owlready2 import *
from datetime import date
from pathlib import Path

ENGINE_DIR = Path(__file__).resolve().parent
ONTO_FILE = ENGINE_DIR / "traffic_ontology.owl"
ONTO_IRI = "http://cs214.org/traffic_ontology.owl"

onto = get_ontology(ONTO_IRI)

with onto:
    # Classes
    class PhuongTien(Thing): pass
    class HanhVi(Thing): pass
    class DieuKien(Thing): pass
    class VanBanPhapLuat(Thing): pass
    class LuatXuPhat(Thing): pass

    # Object Properties
    class ap_dung_cho_phuong_tien(ObjectProperty): domain=[LuatXuPhat]; range=[PhuongTien]
    class ap_dung_hanh_vi(ObjectProperty): domain=[LuatXuPhat]; range=[HanhVi]
    class co_dieu_kien_ap_dung(ObjectProperty): domain=[LuatXuPhat]; range=[DieuKien]
    class can_cu_van_ban(ObjectProperty): domain=[LuatXuPhat]; range=[VanBanPhapLuat]

    # Data Properties (Functional)
    class ten_phuong_tien(DataProperty, FunctionalProperty): domain=[PhuongTien]; range=[str]
    class ten_hanh_vi(DataProperty, FunctionalProperty): domain=[HanhVi]; range=[str]
    class loai_hanh_vi(DataProperty, FunctionalProperty): domain=[HanhVi]; range=[str]
    class mo_ta_hanh_vi(DataProperty, FunctionalProperty): domain=[HanhVi]; range=[str]
    class mo_ta_dieu_kien(DataProperty, FunctionalProperty): domain=[DieuKien]; range=[str]
    class ten_van_ban(DataProperty, FunctionalProperty): domain=[VanBanPhapLuat]; range=[str]
    class so_hieu(DataProperty, FunctionalProperty): domain=[VanBanPhapLuat]; range=[str]
    class loai_van_ban(DataProperty, FunctionalProperty): domain=[VanBanPhapLuat]; range=[str]
    class nam_ban_hanh(DataProperty, FunctionalProperty): domain=[VanBanPhapLuat]; range=[int]
    class hieu_luc_tu(DataProperty, FunctionalProperty): domain=[VanBanPhapLuat]; range=[date]
    class hieu_luc_den(DataProperty, FunctionalProperty): domain=[VanBanPhapLuat]; range=[date]
    class tinh_trang(DataProperty, FunctionalProperty): domain=[VanBanPhapLuat]; range=[str]
    class muc_phat_min(DataProperty, FunctionalProperty): domain=[LuatXuPhat]; range=[float]
    class muc_phat_max(DataProperty, FunctionalProperty): domain=[LuatXuPhat]; range=[float]
    class hinh_thuc_bo_sung(DataProperty, FunctionalProperty): domain=[LuatXuPhat]; range=[str]
    class dieu(DataProperty, FunctionalProperty): domain=[LuatXuPhat]; range=[str]
    class khoan(DataProperty, FunctionalProperty): domain=[LuatXuPhat]; range=[str]
    class doi_tuong_ap_dung(DataProperty, FunctionalProperty): domain=[LuatXuPhat]; range=[str]
    class ghi_chu(DataProperty, FunctionalProperty): domain=[LuatXuPhat]; range=[str]

onto.save(file=str(ONTO_FILE), format="rdfxml")
print(f"[01_ontology.py] Ontology saved at: {ONTO_FILE}")
