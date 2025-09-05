from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import algorithms
from app.core.registry import algorithm_registry

app = FastAPI(
    title="Algorithm Visualization API",
    description="可扩展的算法可视化平台后端",
    version="1.0.0"
)

# CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Vue开发服务器
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册API路由
app.include_router(algorithms.router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    """启动时自动发现并注册算法"""
    algorithm_registry.discover_algorithms()

@app.get("/")
async def root():
    return {"message": "Algorithm Visualization Platform", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)