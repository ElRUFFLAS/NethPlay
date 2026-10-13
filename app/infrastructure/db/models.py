from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, INET
from sqlalchemy.orm import declarative_base
import uuid

Base = declarative_base()

class SubredModel(Base):
    __tablename__ = "subredes"
    id_subred = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    etiqueta_vlan = Column(Integer, nullable=False)
    nombre_segmento = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)

class DireccionIPModel(Base):
    __tablename__ = "direcciones_ip"
    id_ip = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_subred = Column(UUID(as_uuid=True), ForeignKey("subredes.id_subred"), nullable=False)
    direccion = Column(INET, nullable=False, unique=True)
    estado_asignacion = Column(String(20), nullable=False, default="libre")
    proposito = Column(String(100), nullable=True)

class DispositivoModel(Base):
    __tablename__ = "dispositivos"
    id_dispositivo = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre_host = Column(String(100), nullable=False, unique=True)
    fqdn = Column(String(150), nullable=True)
    ip_gestion = Column(INET, nullable=False, unique=True)
    numero_serie = Column(String(100), nullable=True)
    estado_operativo = Column(String(50), nullable=False, default="activo")