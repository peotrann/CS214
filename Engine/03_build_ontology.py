import importlib.util
from pathlib import Path
import datetime
import pandas as pd
from owlready2 import *

ENGINE_DIR = Path(__file__).resolve().parent

# Load ontology module
spec = importlib.util.spec_from_file_location(
    "ontology_module",
    ENGINE_DIR / "01_ontology.py"
)
ontology_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ontology_module)
onto = ontology_module.onto
print("[03_build_ontology.py] Ontology module loaded")

# Load data module
spec = importlib.util.spec_from_file_location(
    "load_data_module",
    ENGINE_DIR / "02_load_data.py"
)
load_data_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(load_data_module)
data = load_data_module.load_all_data()
print("[03_build_ontology.py] Data loaded successfully")

# Safe parsing helpers
def parse_float(x):
    try:
        if x is None or pd.isna(x):
            return None
        s = str(x).strip().lower()
        if s in ["", "none", "nan"]:
            return None
        return float(x)
    except:
        return None

def parse_int(x):
    try:
        if x is None or pd.isna(x):
            return None
        s = str(x).strip().lower()
        if s in ["", "none", "nan"]:
            return None
        return int(x)
    except:
        return None

def parse_date(x):
    try:
        if x is None or pd.isna(x):
            return None
        s = str(x).strip().lower()
        if s in ["", "none", "nan"]:
            return None
        s = str(x).split(" ")[0]
        return datetime.datetime.strptime(s, "%Y-%m-%d").date()
    except:
        return None

def parse_multi_ids(x):
    if x is None or pd.isna(x):
        return []
    return [i.strip() for i in str(x).split(",") if i.strip()]

# Build individuals
with onto:

    # PhuongTien
    phuong_tien_map = {}
    for _, r in data["phuong_tien"].iterrows():
        pid = str(r["id_phuong_tien"])
        pt = ontology_module.PhuongTien(pid)

        if pd.notna(r.get("ten_phuong_tien")):
            pt.ten_phuong_tien = str(r["ten_phuong_tien"])

        phuong_tien_map[pid] = pt

    # HanhVi
    hanh_vi_map = {}
    for _, r in data["hanh_vi"].iterrows():
        hid = str(r["id_hanh_vi"])
        hv = ontology_module.HanhVi(hid)

        if pd.notna(r.get("ten_hanh_vi")):
            hv.ten_hanh_vi = str(r["ten_hanh_vi"])

        if pd.notna(r.get("mo_ta")):
            hv.mo_ta_hanh_vi = str(r["mo_ta"])

        hanh_vi_map[hid] = hv

    # DieuKien
    dieu_kien_map = {}
    for _, r in data["dieu_kien"].iterrows():
        did = str(r["id_dieu_kien"])
        dk = ontology_module.DieuKien(did)

        if pd.notna(r.get("mo_ta")):
            dk.mo_ta_dieu_kien = str(r["mo_ta"])

        dieu_kien_map[did] = dk

    # VanBanPhapLuat
    van_ban_map = {}
    for _, r in data["van_ban"].iterrows():
        vid = str(r["id_van_ban"])
        vb = ontology_module.VanBanPhapLuat(vid)

        if pd.notna(r.get("ten_van_ban")):
            vb.ten_van_ban = str(r["ten_van_ban"])

        if pd.notna(r.get("so_hieu")):
            vb.so_hieu = str(r["so_hieu"])

        if pd.notna(r.get("loai")):
            vb.loai_van_ban = str(r["loai"])

        y = parse_int(r.get("nam"))
        if y is not None:
            vb.nam_ban_hanh = y

        d1 = parse_date(r.get("hieu_luc_tu"))
        if d1:
            vb.hieu_luc_tu = d1

        d2 = parse_date(r.get("hieu_luc_den"))
        if d2:
            vb.hieu_luc_den = d2

        if pd.notna(r.get("tinh_trang")):
            vb.tinh_trang = str(r["tinh_trang"])

        van_ban_map[vid] = vb

    # LuatXuPhat
    for _, r in data["luat"].iterrows():
        lid = str(r["id_luat"])
        l = ontology_module.LuatXuPhat(lid)

        v = parse_float(r.get("muc_phat_min"))
        if v is not None:
            l.muc_phat_min = v

        v = parse_float(r.get("muc_phat_max"))
        if v is not None:
            l.muc_phat_max = v

        if pd.notna(r.get("hinh_thuc_bo_sung")):
            l.hinh_thuc_bo_sung = str(r["hinh_thuc_bo_sung"])

        if pd.notna(r.get("dieu")):
            l.dieu = str(r["dieu"])

        if pd.notna(r.get("khoan")):
            l.khoan = str(r["khoan"])

        if pd.notna(r.get("doi_tuong_ap_dung")):
            l.doi_tuong_ap_dung = str(r["doi_tuong_ap_dung"])

        if pd.notna(r.get("ghi_chu")):
            l.ghi_chu = str(r["ghi_chu"])

        pts = []
        for pid in parse_multi_ids(r.get("id_phuong_tien")):
            if pid in phuong_tien_map:
                pts.append(phuong_tien_map[pid])
        if pts:
            l.ap_dung_cho_phuong_tien = pts

        hid = r.get("id_hanh_vi")
        if pd.notna(hid) and str(hid) in hanh_vi_map:
            l.ap_dung_hanh_vi = [hanh_vi_map[str(hid)]]

        vid = r.get("id_van_ban")
        if pd.notna(vid) and str(vid) in van_ban_map:
            l.can_cu_van_ban = [van_ban_map[str(vid)]]

        did = r.get("id_dieu_kien")
        if pd.notna(did) and str(did) in dieu_kien_map:
            l.co_dieu_kien_ap_dung = [dieu_kien_map[str(did)]]

# Save ontology
OUTPUT_FILE = ENGINE_DIR / "traffic_ontology.owl"
onto.save(file=str(OUTPUT_FILE), format="rdfxml")
print("[03_build_ontology.py] Ontology built successfully")
print("[03_build_ontology.py] Output:", OUTPUT_FILE)
