import logging
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def str_to_bool(value: str) -> bool:
    """Converte string 'true'/'false' para booleano."""
    return value.lower() == "true"

@app.post("/iniciar")
async def iniciar(
    image: UploadFile = File(),
    upscale: str = Form(),
    selectedFunction: str = Form(),
    solidTiles: str = Form(),
    generateMosaic: str = Form(),
):
    # Convertendo strings em booleanos
    upscale_bool = str_to_bool(upscale)
    solidTiles_bool = str_to_bool(solidTiles)
    generateMosaic_bool = str_to_bool(generateMosaic)

    logger.info(f"Recebendo requisição: upscale={upscale_bool}, selectedFunction={selectedFunction}, solidTiles={solidTiles_bool}, generateMosaic={generateMosaic_bool}")
    logger.info(f"Nome do arquivo recebido: {image.filename}")

    return JSONResponse(content={"message": "Processo iniciado com sucesso!", "processedImage": "http://example.com/processed_image.png"})

@app.post("/nova_pastilha")
async def nova_pastilha(
    image: UploadFile = File(),
    upscale: str = Form(),
    selectedFunction: str = Form(),
    solidTiles: str = Form(),
    generateMosaic: str = Form(),
):
    # Convertendo strings em booleanos
    upscale_bool = str_to_bool(upscale)
    solidTiles_bool = str_to_bool(solidTiles)
    generateMosaic_bool = str_to_bool(generateMosaic)

    logger.info(f"Recebendo requisição: upscale={upscale_bool}, selectedFunction={selectedFunction}, solidTiles={solidTiles_bool}, generateMosaic={generateMosaic_bool}")
    logger.info(f"Nome do arquivo recebido: {image.filename}")

    return JSONResponse(content={"message": "Processo iniciado com sucesso!", "processedImage": "http://example.com/processed_image.png"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
