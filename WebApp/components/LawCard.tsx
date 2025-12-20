import React from 'react';
import { LawResult } from '../types';

const VehicleIcon = ({ type }: { type: string }) => {
  const t = type.toLowerCase();
  if (t.includes('ô tô') || t.includes('xe hơi'))
    return (
      <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2"/>
        <circle cx="7" cy="17" r="2"/>
        <path d="M9 17h6"/>
        <circle cx="17" cy="17" r="2"/>
      </svg>
    );
  if (t.includes('máy') || t.includes('mô tô'))
    return (
      <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <circle cx="7" cy="15" r="3"/>
        <circle cx="18" cy="15" r="3"/>
        <path d="M18 15h-8l-4-4 4-4h4l4 4z"/>
      </svg>
    );
  if (t.includes('đạp'))
    return (
      <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <circle cx="5.5" cy="17.5" r="3.5"/>
        <circle cx="18.5" cy="17.5" r="3.5"/>
        <path d="M15 6a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm-3 11.5V14l-3-3 4-3 2 3h2"/>
      </svg>
    );
  return (
    <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>
      <circle cx="9" cy="7" r="4"/>
      <path d="M22 21v-2a4 4 0 0 0-3-3.87"/>
      <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
    </svg>
  );
};

const LawCard: React.FC<{ law: LawResult }> = ({ law }) => {
  const dieuDisplay = law.dieu !== undefined ? Math.floor(Number(law.dieu)) : '-';
  const khoanDisplay = law.khoan !== undefined ? Math.floor(Number(law.khoan)) : '-';

  return (
    <div className="glass-panel rounded-[2rem] p-8 transition-all duration-500 hover:border-sky-500/30 hover:shadow-[0_0_60px_-15px_rgba(14,165,233,0.3)] group mb-6 relative overflow-hidden">
      <div className="absolute top-0 right-0 w-32 h-32 bg-sky-500/5 rounded-full -mr-16 -mt-16 blur-3xl"></div>

      <div className="flex flex-col md:flex-row justify-between items-start gap-6 mb-8 relative z-10">
        <div className="flex-1 space-y-2">
          <div className="flex items-center gap-4">
            <div className="mono text-[10px] font-bold text-sky-400 border border-sky-400/30 px-3 py-1 rounded-full bg-sky-400/5">
              Ref: {law.id_luat}
            </div>
            {law.tinh_trang === 'Còn hiệu lực' && (
              <div className="flex items-center gap-1.5">
                <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 shadow-[0_0_8px_#10b981]"></div>
                <span className="text-[10px] font-extrabold text-emerald-500/80 uppercase tracking-widest">In Effect</span>
              </div>
            )}
          </div>
          <h3 className="text-2xl font-extrabold text-white leading-tight tracking-tight group-hover:text-sky-300 transition-colors">
            {law.hanh_vi[0]}
          </h3>
        </div>
        <div className="flex flex-wrap gap-2">
          {law.phuong_tien.map((pt, i) => (
            <div key={i} className="flex items-center gap-2 bg-white/5 px-3 py-1.5 rounded-xl border border-white/10 text-[11px] font-bold text-slate-300 whitespace-nowrap">
              <VehicleIcon type={pt} />
              {pt}
            </div>
          ))}
        </div>
      </div>

      <div className="flex items-center gap-6 mb-8 relative z-10">
        <div className="p-5 bg-gradient-to-br from-sky-500 to-blue-700 rounded-3xl shadow-[0_10px_30px_-10px_rgba(14,165,233,0.5)] text-white">
          <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>
        <div>
          <p className="text-[10px] font-black text-slate-500 uppercase tracking-[0.2em] mb-1">Mức phạt quy định</p>
          <div className="flex items-baseline gap-2">
            <span className="text-4xl font-black text-white tracking-tighter text-glow">
              {law.muc_phat_min}
            </span>
            <span className="text-slate-600 font-bold">—</span>
            <span className="text-4xl font-black text-white tracking-tighter text-glow">
              {law.muc_phat_max}
            </span>
            <span className="text-xs font-bold text-sky-500/60 ml-2">VND</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 relative z-10">
        <div className="lg:col-span-6 space-y-4">
          <div className="flex items-start gap-4 p-4 rounded-2xl bg-white/5 border border-white/5">
            <div className="text-sky-500 mt-1">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" strokeWidth="1.5"/>
              </svg>
            </div>
            <div>
              <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Căn cứ văn bản</p>
              <p className="text-xs text-slate-300 font-medium leading-relaxed mt-1">{law.van_ban}</p>
              <p className="text-[10px] text-sky-400/60 font-mono mt-1">SỐ HIỆU: {law.so_hieu}</p>
              <p className="text-[10px] text-slate-400/70 mt-1">Ngày ban hành: {law.ngay_ban_hanh || '-'}</p>
              <p className="text-[10px] text-emerald-400/60 font-mono mt-1">Tình trạng: {law.tinh_trang}</p>
            </div>
          </div>

          <div className="flex items-start gap-4 p-4 rounded-2xl bg-white/5 border border-white/5">
            <div className="text-sky-500 mt-1">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" strokeWidth="1.5"/>
                <path d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" strokeWidth="1.5"/>
              </svg>
            </div>
            <div>
              <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Đối tượng</p>
              <p className="text-xs text-slate-300 font-bold mt-1">{law.doi_tuong_ap_dung || 'Người điều khiển PT'}</p>
            </div>
          </div>
        </div>

        <div className="lg:col-span-6 space-y-4">
          <div className="p-6 rounded-3xl bg-black/40 border border-white/5 flex flex-col justify-center min-h-[160px]">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-8 h-8 rounded-lg bg-sky-500/10 flex items-center justify-center text-sky-400">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" strokeWidth="2"/>
                </svg>
              </div>
              <h4 className="text-[10px] font-black text-slate-500 uppercase tracking-[0.2em]">Tra cứu nhanh</h4>
            </div>
            <div className="space-y-3">
              <div className="flex justify-between items-center text-xs">
                <span className="text-slate-500">Điều khoản</span>
                <span className="mono text-white font-bold">{dieuDisplay} / {khoanDisplay}</span>
              </div>
              <div className="flex justify-between items-center text-xs">
                <span className="text-slate-500">Năm luật</span>
                <span className="mono text-white font-bold">{law.nam}</span>
              </div>
              <div className="pt-3 border-t border-white/5 flex gap-2">
                <button className="flex-1 bg-sky-500/10 hover:bg-sky-500/20 text-sky-400 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all">
                  Xem Chi Tiết
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {(law.hinh_thuc_bo_sung || law.ghi_chu) && (
        <div className="mt-8 pt-6 border-t border-white/5">
          <div className="flex flex-col sm:flex-row gap-4">
            {law.hinh_thuc_bo_sung && (
              <div className="flex-1 bg-amber-500/5 border border-amber-500/20 rounded-2xl p-4 flex gap-3">
                <svg className="w-4 h-4 text-amber-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" strokeWidth="2"/>
                </svg>
                <div>
                  <span className="text-[10px] font-black text-amber-500 uppercase tracking-widest block mb-1">Hình thức bổ sung</span>
                  <p className="text-[11px] text-amber-200/80 leading-relaxed italic">{law.hinh_thuc_bo_sung}</p>
                </div>
              </div>
            )}
            {law.ghi_chu && (
              <div className="flex-1 bg-sky-500/5 border border-sky-500/20 rounded-2xl p-4 flex gap-3">
                <svg className="w-4 h-4 text-sky-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" strokeWidth="2"/>
                </svg>
                <div>
                  <span className="text-[10px] font-black text-sky-500 uppercase tracking-widest block mb-1">Thông tin thêm</span>
                  <p className="text-[11px] text-sky-200/80 leading-relaxed italic">{law.ghi_chu}</p>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default LawCard;
