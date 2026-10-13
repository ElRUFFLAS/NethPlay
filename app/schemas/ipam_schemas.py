from pydantic import BaseModel, Field, IPvAnyAddress
from typing import Optional
import uuid

# Esquemas para Subredes
class SubredCreate(BaseModel):
    etiqueta_vlan: int = Field(..., description="Número de VLAN")
    nombre_segmento: str = Field(..., max_length=100)
    descripcion: Optional[str] = None

class SubredResponse(SubredCreate):
    id_subred: uuid.UUID

    class Config:
        from_attributes = True

# Esquemas para Direcciones IP
class DireccionIPCreate(BaseModel):
    id_subred: uuid.UUID
    direccion: str = Field(..., description="Dirección IP válida dentro del segmento")
    estado_asignacion: str = Field(default="libre", description="libre, ocupada, reservada")
    proposito: Optional[str] = None

class DireccionIPResponse(DireccionIPCreate):
    id_ip: uuid.UUID

    class Config:
        from_attributes = True

# Esquemas para Dispositivos
class DispositivoCreate(BaseModel):
    nombre_host: str = Field(..., max_length=100)
    fqdn: Optional[str] = None
    ip_gestion: str
    numero_serie: Optional[str] = None
    estado_operativo: str = Field(default="activo")

class DispositivoResponse(DispositivoCreate):
    id_dispositivo: uuid.UUID

    class Config:
        from_attributes = True