from db.reserva_db import ReservaInDB
from db.reserva_db import update_reserva, get_reserva, database_reservas
from models.reserva_models import ReservaIn, ReservaOut
from datetime import datetime, date
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from db import reserva_db

api = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://frontend-proyhotel.herokuapp.com"
    
]

api.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)
consecutivo=5
reserva_in_db:ReservaInDB

@api.get("/reserva/vista/{num_reserva}")
async def listar_reserva(num_reserva: str):

    reserva_in_db = get_reserva(num_reserva)

    if reserva_in_db == None:
        
        raise HTTPException(status_code=404, detail="La reserva no existe")

    
    reserva_out = ReservaOut(**reserva_in_db.dict())

    return  reserva_out


@api.post("/reserva/crear")
async def crear_reserva(reserva:ReservaIn):
    global consecutivo
 
        
    try:
        fechai = datetime.strptime(reserva.fecha_inicial, '%Y-%m-%d')
        fechaf = datetime.strptime(reserva.fecha_final, '%Y-%m-%d')
        
    except:
        raise HTTPException(status_code=422, detail="Formato de fecha inválido. debe ser aaaa-mm-dd")
    

        
    fecha=datetime.now()
    
       
    dias= (fechaf-fechai).days
    if(reserva.tipo_hab == "Sencilla"):
        valor=100000*dias
    elif(reserva.tipo_hab == "Doble"):
        valor=150000*dias
    else:
        valor=200000*dias 
    consecutivo+=1
    pre ="rsrv_"
    idreserva=pre+str(consecutivo)
    reserva_in_db=ReservaInDB(**{"nombre":reserva.nombre,
                            "identificacion":reserva.identificacion,
                            "fecha":fecha.strftime('%Y-%m-%d %H:%M:%S'),
                            "fecha_inicial":reserva.fecha_inicial,
                            "fecha_final":reserva.fecha_final,
                            "tipo_hab":reserva.tipo_hab,
                            "valor":valor,
                            "num_reserva": idreserva})
           
    database_reservas[reserva_in_db.num_reserva]=reserva_in_db

    return {"mensaje":"Se ha creado la reserva "+idreserva}

@api.get("/reserva/listar")
async def obtener_reservas():
    reservas = reserva_db.obtener_reservas()
    return reservas