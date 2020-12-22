from pydantic import BaseModel

class ReservaIn(BaseModel):
    nombre: str
    identificacion: str
    fecha_inicial: str
    fecha_final: str
    tipo_hab: str
    

class ReservaOut(BaseModel):
    num_reserva: str
    nombre: str
    identificacion: str
    fecha: str
    fecha_inicial: str
    fecha_final: str
    tipo_hab: str
    valor: int
