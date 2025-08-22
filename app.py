# import uvicorn
# from scripts.config import ModuleConfig
from mangum import Mangum
from main import app as fastapi_app

# if __name__ == "__main__":
#     # uvicorn.run(
#     #     "main:app",
#     #     host=ModuleConfig.HOST,
#     #     port=ModuleConfig.PORT,
#     #     reload=ModuleConfig.RELOAD_ASGI,
#     # )
handler = Mangum(fastapi_app)
