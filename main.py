from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Api.Router.router import api_router 

app = FastAPI(
    title='apiLlama',
    version= '1.0',
    docs_url= '/docs',
    openapi_url='/openapi.json'

)

origins = [
    "http://localhost:4200", 
    "http://127.0.0.1:4200",   
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # Permite las solicitudes de estos orígenes
    allow_credentials=True,         # Permite credenciales (cookies, encabezados de autorización)
    allow_methods=["*"],            # Permite todos los métodos HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],            # Permite todos los encabezados HTTP
)

app.include_router(
    api_router
)