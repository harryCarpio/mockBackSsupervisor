from fastapi import FastAPI
import uvicorn
from routes import router, atm_router

# ==========================================
# FastAPI App Configuration
# ==========================================

app = FastAPI(
    title="Mock Backend API",
    description="Mock Server para backend. El endpoint de login genera JWT reales para testear autorización.",
    version="1.0.0",
)

# Include routers
app.include_router(router)
app.include_router(atm_router)


if __name__ == "__main__":
    # Ejecuta el servidor en 0.0.0.0 para permitir conexiones desde la red local
    uvicorn.run(app, host="0.0.0.0", port=8000)
