
# Hướng dẫn chạy hệ thống (Python Backend)

Để trang web React này hoạt động, bạn cần một API server chạy ở `http://localhost:8000`. Hãy tạo file `server.py` tại `D:\CS214\WebApp\server.py` với nội dung sau:

```python
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import importlib.util
import uvicorn

app = FastAPI()

# Cho phép React WebApp truy cập
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đường dẫn tới Engine của bạn
ENGINE_DIR = Path("D:/CS214/Engine")
spec = importlib.util.spec_from_file_location(
    "web_api_module", 
    ENGINE_DIR / "07_web_api.py" # Hoặc file chứa filter_laws_for_web
)
web_api = importlib.util.module_from_spec(spec)
spec.loader.exec_module(web_api)

@app.post("/query")
async def handle_query(request: Request):
    data = await request.json()
    query_text = data.get("query", "")
    results = web_api.filter_laws_for_web(query_text)
    return {"status": "success", "results": results}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Sau đó chạy lệnh: `pip install fastapi uvicorn` và `python server.py`.
Trang web sẽ tự động kết nối và hiển thị kết quả.
