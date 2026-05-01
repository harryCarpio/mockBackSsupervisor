# ==========================================
# API Endpoints
# ==========================================

from fastapi import APIRouter, Depends, Query
from datetime import datetime, timedelta
from uuid import uuid4
from models import (
    LoginRequest,
    LoginResponse,
    TicketCalculateResponse,
    PaymentCashRequest,
    PaymentCashResponse,
    PaymentVerifyResponse,
    IncidentRequest,
    IncidentResponse,
    ATMCheckoutResponse,
)
from auth import create_access_token, verify_token
from config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS

router = APIRouter(prefix="/api/v1")


@router.post("/auth/login", response_model=LoginResponse, tags=["Auth"])
async def login(request: LoginRequest):
    """
    1. Endpoint: Iniciar sesión.
    (Endpoint real que genera un JWT access_token y refresh_token).
    """
    # Genera los tokens en la vida real
    access_token = create_access_token(
        {"sub": request.username}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_access_token(
        {"sub": request.username, "type": "refresh"},
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
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


@router.get(
    "/tickets/calculate",
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


@router.post("/payments/cash", response_model=PaymentCashResponse, tags=["Payments"])
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


@router.get("/payments/verify", response_model=PaymentVerifyResponse, tags=["Payments"])
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


@router.post("/incidents", response_model=IncidentResponse, tags=["Incidents"])
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


# ==========================================
# ATM Endpoints (without v1 prefix)
# ==========================================

atm_router = APIRouter(prefix="/api/atm")


@atm_router.get("/checkout", response_model=ATMCheckoutResponse, tags=["ATM"])
async def atm_checkout(
    plate: str = Query(..., description="Placa del vehículo"),
    cajeroKey: str = Query(..., description="UUID de la caja"),
):
    """
    ATM Checkout Endpoint.
    Consulta de saldo y detalles de pago en el ATM.
    """
    return {
        "tx": str(uuid4()),
        "amount": 3500,
        "stayMinutes": 120,
    }
