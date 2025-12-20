
import React, { useState, useCallback } from 'react';
import { LawResult } from './types';
import { queryTrafficLaw } from './services/api';
import LawCard from './components/LawCard';

const CATEGORIES = [
  { label: 'Say xỉn quên lối về', icon: '🍷' },
  { label: 'Quá nhanh quá nguy hiểm!', icon: '⚡' },
  { label: 'Vượt đèn đỏ', icon: '🚥' },
];

const App: React.FC = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<LawResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = useCallback(async (e?: React.FormEvent, customQuery?: string) => {
    if (e) e.preventDefault();
    const finalQuery = customQuery || query;
    if (!finalQuery.trim()) return;

    setLoading(true);
    setError(null);
    setHasSearched(true);

    try {
      const data = await queryTrafficLaw(finalQuery);
      setResults(data);
    } catch (err) {
      setError('Hệ thống Engine không phản hồi. Vui lòng kiểm tra API tại localhost:8000.');
    } finally {
      setLoading(false);
    }
  }, [query]);

  return (
    <div className="max-w-6xl mx-auto px-6 py-12 md:py-24 relative">
      {/* Abstract Radar Background */}
      <div className="fixed top-0 right-0 p-24 opacity-20 pointer-events-none">
         <div className="radar-sweep"></div>
      </div>

      <header className="relative mb-24 text-center">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 mb-8 rounded-full bg-sky-500/10 border border-sky-500/20 backdrop-blur-md">
           <span className="w-1.5 h-1.5 rounded-full bg-sky-400 animate-ping"></span>
           <span className="text-[10px] font-black tracking-[0.3em] text-sky-400 uppercase">Siêu lẹ v3.0</span>
        </div>
        
        <div className="relative inline-block mb-10">
          {/* Animated Header Graphic */}
          <div className="absolute -inset-10 bg-sky-500/20 blur-[80px] rounded-full pointer-events-none opacity-50"></div>
          <h1 className="relative text-6xl md:text-8xl font-black text-white tracking-tighter leading-[0.9]">
            AI <span className="text-transparent bg-clip-text bg-gradient-to-b from-sky-400 to-blue-600">LEGAL</span><br />
            ASSISTANT
          </h1>
        </div>
        
        <p className="text-xl text-slate-400 max-w-2xl mx-auto font-medium leading-relaxed mb-12">
          Truy xuất chính xác các quy định xử phạt dựa trên hệ thống thực thể số (Ontology) từ Engine CS214.
        </p>

        <div className="flex flex-wrap justify-center gap-3">
          {CATEGORIES.map((cat) => (
            <button
              key={cat.label}
              onClick={() => { setQuery(cat.label); handleSearch(undefined, cat.label); }}
              className="bg-white/5 border border-white/10 hover:border-sky-500/50 hover:bg-sky-500/5 px-6 py-3 rounded-2xl text-xs font-bold text-slate-400 hover:text-white transition-all flex items-center gap-2 group"
            >
              <span className="text-lg group-hover:scale-125 transition-transform">{cat.icon}</span>
              {cat.label}
            </button>
          ))}
        </div>
      </header>

      <section className="mb-24 sticky top-12 z-50">
        <form onSubmit={handleSearch} className="relative max-w-4xl mx-auto group">
          <div className="absolute -inset-1 bg-gradient-to-r from-sky-500 to-blue-600 rounded-[2.5rem] blur opacity-25 group-focus-within:opacity-50 transition duration-1000"></div>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-10 flex items-center pointer-events-none">
              <svg className="w-6 h-6 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
            </div>
            <input
              type="text"
              className="w-full bg-black/80 backdrop-blur-3xl border border-white/10 rounded-[2.5rem] py-8 pl-20 pr-48 text-white text-xl placeholder-slate-600 transition-all outline-none focus:bg-black"
              placeholder="Bạn muốn tra cứu hành vi vi phạm nào?"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
            <button
              type="submit"
              disabled={loading}
              className="absolute right-4 top-4 bottom-4 bg-sky-600 hover:bg-sky-500 disabled:bg-slate-800 text-white px-12 rounded-[1.8rem] font-black text-xs uppercase tracking-[0.2em] transition-all flex items-center gap-3"
            >
              {loading ? <span className="w-5 h-5 border-2 border-white/20 border-t-white rounded-full animate-spin"></span> : 'QUÉT DỮ LIỆU'}
            </button>
          </div>
          {loading && <div className="absolute bottom-0 left-10 right-10 scanning-line rounded-full opacity-50"></div>}
        </form>
      </section>

      <main>
        {error && (
          <div className="glass-panel border-red-500/20 rounded-[2.5rem] p-12 text-center max-w-2xl mx-auto animate-in zoom-in duration-500">
             <div className="w-20 h-20 bg-red-500/10 rounded-3xl flex items-center justify-center mx-auto mb-8 text-red-500">
                <svg className="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
             </div>
             <h2 className="text-2xl font-black text-white mb-4">Mất kết nối với Engine</h2>
             <p className="text-slate-400 mb-8 leading-relaxed">Không thể kết nối với máy chủ xử lý logic tại localhost:8000. Hãy đảm bảo bạn đã chạy server.py.</p>
             <button onClick={() => window.location.reload()} className="px-8 py-3 bg-white/5 border border-white/10 rounded-2xl text-xs font-black uppercase tracking-widest text-white hover:bg-white/10 transition-all">Thử lại</button>
          </div>
        )}

        {!loading && hasSearched && results.length === 0 && !error && (
          <div className="text-center py-40 animate-in fade-in zoom-in duration-1000">
             <div className="mb-10 text-6xl">🔍</div>
             <h3 className="text-3xl font-black text-white mb-4 tracking-tight">Cơ sở dữ liệu chưa ghi nhận</h3>
             <p className="text-slate-500 font-medium text-lg">Hành vi này chưa tồn tại trong Ontology hoặc Alias Resolver.</p>
          </div>
        )}

        <div className="grid grid-cols-1 gap-4">
          {results.map((law, idx) => (
            <div 
              key={idx} 
              className="animate-in fade-in slide-in-from-bottom-12 duration-700" 
              style={{ animationDelay: `${idx * 150}ms`, animationFillMode: 'both' }}
            >
              <LawCard law={law} />
            </div>
          ))}
        </div>
      </main>

      <footer className="mt-40 pb-20 text-center border-t border-white/5 pt-20">
        <div className="flex flex-col md:flex-row justify-between items-center gap-8 px-10">
          <div className="text-left">
            <h4 className="text-xs font-black text-slate-600 uppercase tracking-widest mb-4">CS214 Traffic Engine</h4>
            <div className="flex gap-4">
               <div className="bg-white/5 p-4 rounded-2xl border border-white/5">
                 <p className="text-[10px] text-slate-500 font-bold mb-1">DATA REPO</p>
                 <p className="mono text-xs text-sky-500 font-bold">CS214\Engine</p>
               </div>
               <div className="bg-white/5 p-4 rounded-2xl border border-white/5">
                 <p className="text-[10px] text-slate-500 font-bold mb-1">INTERFACE</p>
                 <p className="mono text-xs text-sky-500 font-bold">CS214\WebApp</p>
               </div>
            </div>
          </div>
          <p className="text-[10px] font-black text-slate-700 uppercase tracking-[0.4em] max-w-xs text-right hidden md:block">
            Designed for high-performance regulatory intelligence lookup and traffic law education.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default App;
