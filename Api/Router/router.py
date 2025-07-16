from fastapi import APIRouter
from Api.EndPoints.Login import router
from Api.EndPoints.Form import routerF
from Api.EndPoints.Dashboard import routerDas
from Api.EndPoints.Consumption import rounterCon
from Api.EndPoints.Detail import routingDetail

api_router = APIRouter()
api_router.include_router(router)
api_router.include_router(routerF)
api_router.include_router(routerDas)
api_router.include_router(rounterCon)
api_router.include_router(routingDetail)