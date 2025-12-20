
export interface LawResult {
  id_luat: string;
  phuong_tien: string[];
  hanh_vi: string[];
  dieu_kien: string[];
  muc_phat_min: string;
  muc_phat_max: string;
  hinh_thuc_bo_sung: string | null;
  dieu: string | null;
  khoan: string | null;
  ghi_chu: string | null;
  doi_tuong_ap_dung: string | null;
  van_ban: string;
  so_hieu: string;
  loai: string;
  nam: number;
  hieu_luc: string;
  tinh_trang: string;
  suy_ra?: string;
}

export interface ApiResponse {
  status: 'success' | 'error';
  data: LawResult[];
  message?: string;
}
