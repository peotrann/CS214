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

# Safe parsing
def parse_float(x):
    try:
        if x is None or pd.isna(x) or str(x).strip().lower() in ["none", ""]:
            return None
        return float(x)
    except:
        return None

def parse_int(x):
    try:
        if x is None or pd.isna(x) or str(x).strip().lower() in ["none", ""]:
            return None
        return int(x)
    except:
        return None

def parse_date(x):
    try:
        if x is None or pd.isna(x) or str(x).strip().lower() in ["none", ""]:
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
    phuong_tien_map = {}
    for _, r in data["phuong_tien"].iterrows():
        pt = ontology_module.PhuongTien(r["id_phuong_tien"])
        if pd.notna(r.get("ten_phuong_tien")):
            pt.ten_phuong_tien = r["ten_phuong_tien"]
        phuong_tien_map[r["id_phuong_tien"]] = pt

    hanh_vi_map = {}
    for _, r in data["hanh_vi"].iterrows():
        hv = ontology_module.HanhVi(r["id_hanh_vi"])
        if pd.notna(r.get("ten_hanh_vi")):
            hv.ten_hanh_vi = r["ten_hanh_vi"]
        if pd.notna(r.get("loai_hanh_vi")):
            hv.loai_hanh_vi = r["loai_hanh_vi"]
        if pd.notna(r.get("mo_ta")):
            hv.mo_ta_hanh_vi = r["mo_ta"]
        hanh_vi_map[r["id_hanh_vi"]] = hv

    dieu_kien_map = {}
    for _, r in data["dieu_kien"].iterrows():
        dk = ontology_module.DieuKien(r["id_dieu_kien"])
        if pd.notna(r.get("mo_ta")):
            dk.mo_ta_dieu_kien = r["mo_ta"]
        dieu_kien_map[r["id_dieu_kien"]] = dk

    van_ban_map = {}
    for _, r in data["van_ban"].iterrows():
        vb = ontology_module.VanBanPhapLuat(r["id_van_ban"])
        if pd.notna(r.get("ten_van_ban")):
            vb.ten_van_ban = r["ten_van_ban"]
        if pd.notna(r.get("so_hieu")):
            vb.so_hieu = r["so_hieu"]
        if pd.notna(r.get("loai")):
            vb.loai_van_ban = r["loai"]

        tmp_int = parse_int(r.get("nam"))
        if tmp_int is not None:
            vb.nam_ban_hanh = tmp_int

        tmp_dt1 = parse_date(r.get("hieu_luc_tu"))
        tmp_dt2 = parse_date(r.get("hieu_luc_den"))
        if tmp_dt1:
            vb.hieu_luc_tu = tmp_dt1
        if tmp_dt2:
            vb.hieu_luc_den = tmp_dt2

        if pd.notna(r.get("tinh_trang")):
            vb.tinh_trang = r["tinh_trang"]

        van_ban_map[r["id_van_ban"]] = vb

    for _, r in data["luat"].iterrows():
        l = ontology_module.LuatXuPhat(r["id_luat"])

        tmp_min = parse_float(r.get("muc_phat_min"))
        tmp_max = parse_float(r.get("muc_phat_max"))
        if tmp_min is not None:
            l.muc_phat_min = tmp_min
        if tmp_max is not None:
            l.muc_phat_max = tmp_max

        if pd.notna(r.get("hinh_thuc_bo_sung")):
            l.hinh_thuc_bo_sung = r["hinh_thuc_bo_sung"]
        if pd.notna(r.get("dieu")):
            l.dieu = r["dieu"]
        if pd.notna(r.get("khoan")):
            l.khoan = r["khoan"]
        if pd.notna(r.get("doi_tuong_ap_dung")):
            l.doi_tuong_ap_dung = r["doi_tuong_ap_dung"]

        l.ghi_chu = r.get("ghi_chu", "")

        pt_list = []
        for pt_id in parse_multi_ids(r.get("id_phuong_tien")):
            if pt_id in phuong_tien_map:
                pt_list.append(phuong_tien_map[pt_id])
        if pt_list:
            l.ap_dung_cho_phuong_tien = pt_list

        if pd.notna(r.get("id_hanh_vi")) and r["id_hanh_vi"] in hanh_vi_map:
            l.ap_dung_hanh_vi = [hanh_vi_map[r["id_hanh_vi"]]]

        if pd.notna(r.get("id_van_ban")) and r["id_van_ban"] in van_ban_map:
            l.can_cu_van_ban = [van_ban_map[r["id_van_ban"]]]

        if pd.notna(r.get("id_dieu_kien")) and r["id_dieu_kien"] in dieu_kien_map:
            l.co_dieu_kien_ap_dung = [dieu_kien_map[r["id_dieu_kien"]]]

OUTPUT_FILE = ENGINE_DIR / "traffic_ontology.owl"
onto.save(file=str(OUTPUT_FILE), format="rdfxml")
print("[03_build_ontology.py] Ontology built successfully")
print("[03_build_ontology.py] Output:", OUTPUT_FILE)
