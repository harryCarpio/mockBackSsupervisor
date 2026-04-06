from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from typing import List, Optional
import jwt

# ==========================================
# Configuración y Variables
# ==========================================
SECRET_KEY = "mock_secret_key"
ALGORITHM = "HS256"

app = FastAPI(
    title="Mock Backend API",
    description="Mock Server para backend. El endpoint de login genera JWT reales para testear autorización.",
    version="1.0.0",
)

security = HTTPBearer()


# ==========================================
# Autenticación y JWT
# ==========================================
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(
            credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM]
        )
        return payload
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ==========================================
# Modelos Pydantic (Request y Response)
# ==========================================


class LoginRequest(BaseModel):
    username: str = "admin"
    password: str = "123456"


class UserProfile(BaseModel):
    user_id: str
    full_name: str
    roles: List[str]


class SecurityMetadata(BaseModel):
    last_login_at: datetime
    is_new_device: bool


class LoginData(BaseModel):
    session_id: str
    access_token: str
    refresh_token: str
    expires_in: int
    user_profile: UserProfile
    security_metadata: SecurityMetadata


class LoginResponse(BaseModel):
    status: str
    message: str
    data: LoginData


class MetaResponse(BaseModel):
    timestamp: datetime
    error_code: str
    status: int
    message: str


class TicketCalculateResponse(BaseModel):
    ticket_id: str
    placa: str
    hora_ingreso: datetime
    tiempo_minutos: int
    valor_total: float
    estado_actual: str
    meta: MetaResponse


class PaymentCashRequest(BaseModel):
    ticket_id: str = "TKT-998273"
    monto_entregado: float = 10.00


class PaymentCashResponse(BaseModel):
    ticket_id: str
    estado_actual: str
    vuelto: float
    fecha_pago: datetime
    meta: MetaResponse


class PaymentVerifyResponse(BaseModel):
    is_paid: bool
    metodo_pago: str
    minutos_gracia: int


class IncidentRequest(BaseModel):
    placa: str = "ABC-1234"
    tipo: str = "MAL_ESTACIONAMIENTO"
    descripcion: str = "Auto bloqueando la salida de emergencia en el nivel 2."
    evidencia: List[str]


class IncidentResponse(BaseModel):
    incidencia_id: str
    estado: str
    meta: MetaResponse


# ==========================================
# Endpoints
# ==========================================


@app.post("/api/v1/auth/login", response_model=LoginResponse, tags=["Auth"])
async def login(request: LoginRequest):
    """
    1. Endpoint: Iniciar sesión.
    (Endpoint real que genera un JWT access_token y refresh_token).
    """
    # Genera los tokens en la vida real
    access_token = create_access_token({"sub": request.username}, timedelta(minutes=60))
    refresh_token = create_access_token(
        {"sub": request.username, "type": "refresh"}, timedelta(days=7)
    )

    return {
        "status": "success",
        "message": "Authentication successful",
        "data": {
            "session_id": "sess_987654321_abc123xyz",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": 604800,  # 7 días en segundos
            "user_profile": {
                "user_id": "user_550e8400_e29b",
                "full_name": "Juan Pérez",
                "roles": ["admin", "editor"],
            },
            "security_metadata": {
                "last_login_at": "2026-03-25T14:05:01Z",
                "is_new_device": False,
            },
        },
    }


@app.get(
    "/api/v1/tickets/calculate",
    response_model=TicketCalculateResponse,
    tags=["Tickets"],
)
async def calculate_ticket(
    placa: str = Query(..., description="Placa del vehículo"),
    token: dict = Depends(verify_token),
):
    """
    2. Endpoint: Consulta valor a cobrar.
    Requiere token Bearer.
    """
    print(f"Calculando ticket para placa: {placa} con token: {token}")
    if placa == "ABC-1234":
        return {
            "ticket_id": "TKT-998273",
            "placa": "ABC-1234",
            "hora_ingreso": "2026-03-24T14:30:00Z",
            "tiempo_minutos": 125,
            "valor_total": 4.50,
            "estado_actual": "NO-PAGADO",
            "meta": {
                "timestamp": "2026-03-31T16:15:00Z",
                "error_code": "",
                "status": 200,
                "message": "Cálculo exitoso",
            },
        }
    elif placa == "XYZ-5678":
        return {
            "ticket_id": "TKT-998213",
            "placa": "XYZ-5678",
            "hora_ingreso": "2026-03-24T14:30:00Z",
            "tiempo_minutos": 80,
            "valor_total": 0,
            "estado_actual": "PAGADO",
            "meta": {
                "timestamp": "2026-03-31T16:15:00Z",
                "error_code": "ERR-TKT-422",
                "status": 422,
                "message": "El vehículo no registra valores pendientes de cobro.",
            },
        }
    elif placa == "DEF-0000":
        return {
            "ticket_id": "",
            "placa": "DEF-0000",
            "hora_ingreso": datetime.min.isoformat() + "Z",
            "tiempo_minutos": 0,
            "valor_total": 0,
            "estado_actual": "",
            "meta": {
                "timestamp": "2026-03-31T16:15:00Z",
                "error_code": "ERR-TKT-404",
                "status": 404,
                "message": "No se encontró un ticket de ingreso activo para la placa proporcionada.",
            },
        }
    else:
        return {
            "ticket_id": "",
            "placa": "DEF-0001",
            "hora_ingreso": datetime.min.isoformat() + "Z",
            "tiempo_minutos": 0,
            "valor_total": 0,
            "estado_actual": "",
            "meta": {
                "timestamp": "2026-03-31T16:15:00Z",
                "error_code": "ERR-TKT-400",
                "status": 400,
                "message": "Bad request",
            },
        }


@app.post(
    "/api/v1/payments/cash", response_model=PaymentCashResponse, tags=["Payments"]
)
async def payment_cash(
    request: PaymentCashRequest, token: dict = Depends(verify_token)
):
    """
    3. Endpoint: Registro de Pago en Efectivo.
    Requiere token Bearer.
    """
    return {
        "ticket_id": "TKT-998273",
        "estado_actual": "COMPLETED",
        "vuelto": 5.50,
        "fecha_pago": "2026-03-24T16:35:12Z",
        "meta": {
            "timestamp": "2026-03-31T16:15:00Z",
            "error_code": "",
            "status": 200,
            "message": "Cálculo exitoso",
        },
    }


@app.get(
    "/api/v1/payments/verify", response_model=PaymentVerifyResponse, tags=["Payments"]
)
async def verify_payment(
    code: str = Query(..., description="Código de barras o placa"),
    type: str = Query(..., description="'barcode' o 'placa'"),
    token: dict = Depends(verify_token),
):
    """
    4. Endpoint: Pantalla de Escáner y Validación.
    Requiere token Bearer.
    Nota: Se definen variables individuales `code` y `type` como parámetros de querystring
    estándares en URLs (?code=ABC&type=placa).
    """
    return {"is_paid": True, "metodo_pago": "APP_MOVIL", "minutos_gracia": 12}


@app.post("/api/v1/incidents", response_model=IncidentResponse, tags=["Incidents"])
async def create_incident(
    request: IncidentRequest, token: dict = Depends(verify_token)
):
    """
    5. Endpoint: Pantalla de Nueva Incidencia.
    Requiere token Bearer.
    """
    return {
        "incidencia_id": "INC-00452",
        "estado": "REGISTRADO",
        "meta": {
            "timestamp": "2026-03-31T16:15:00Z",
            "error_code": "",
            "status": 200,
            "message": "Cálculo exitoso",
        },
    }


if __name__ == "__main__":
    import uvicorn

    # Ejecuta el servidor en 0.0.0.0 para permitir conexiones desde la red local
    uvicorn.run(app, host="0.0.0.0", port=8000)
