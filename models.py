# ==========================================
# Pydantic Models (Request and Response)
# ==========================================

from pydantic import BaseModel
from typing import List
from datetime import datetime


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


class ATMCheckoutResponse(BaseModel):
    tx: str
    amount: int
    stayMinutes: int


class ATMGracePeriodResponse(BaseModel):
    hasGracePeriod: bool
    minutesRemaining: int


class ATMChargeResponse(BaseModel):
    tx: str
    status: str
    mode: str
    lines: List[int]


class ATMChargeRequest(BaseModel):
    tx: str
    status: str
    mode: str
    lines: List[int]
