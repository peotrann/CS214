from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import importlib.util
import uvicorn

app = FastAPI()

# Cho phép Giao diện Web truy cập vào API này
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đường dẫn tới thư mục Engine chứa các file .py gốc của bạn
ENGINE_DIR = Path("D:/CS214/Engine")

# Load file 07_web_api.py của bạn
spec = importlib.util.spec_from_file_location(
    "web_api_module", 
    ENGINE_DIR / "07_query_example.py"
)
web_api = importlib.util.module_from_spec(spec)
spec.loader.exec_module(web_api)

@app.post("/query")
async def handle_query(request: Request):
    data = await request.json()
    query_text = data.get("query", "")
    
    # Gọi hàm xử lý logic từ file 07_web_api.py của bạn
    results = web_api.filter_laws_for_web(query_text)
    
    return {"status": "success", "results": results}

if __name__ == "__main__":
    # Chạy server tại cổng 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)