from fastapi import FastAPI
from fastapi.routing import APIRoute

from api.routes import mcp_router

app = FastAPI()

app.include_router(mcp_router, prefix="/mcp")


@app.get("/routes")
def list_routes():
    return [
        {"path": route.path, "methods": sorted(route.methods), "name": route.name}
        for route in app.routes
        if isinstance(route, APIRoute)
    ]
