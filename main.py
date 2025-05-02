from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
from typing import List, Dict
import base64
from io import BytesIO
from PIL import Image
import os

app = FastAPI()

# CORS liberado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class GerarTenisRequest(BaseModel):
    cliente_id: str
    masks: List[str]
    escolhas: Dict[str, str]
    textures: Dict[str, str]

@app.post("/gerar-tenis")
def gerar_tenis(request: GerarTenisRequest):
    # Carrega o mockup base
    base_path = os.path.join(os.path.dirname(__file__), "mockup_tifi.png")
    imagem_base = Image.open(base_path).convert("RGBA")

    for letra in request.masks:
        textura_nome = request.escolhas[letra]
        textura_base64 = request.textures[letra]

        # Decodifica a imagem da textura em base64
        textura_bytes = base64.b64decode(textura_base64.split(",")[1])
        textura_img = Image.open(BytesIO(textura_bytes)).convert("RGBA")

        # Carrega a máscara
        mask_path = os.path.join(os.path.dirname(__file__), f"masks/{letra}.png")
        mascara = Image.open(mask_path).convert("L")

        # Redimensiona textura para o tamanho da máscara
        textura_redimensionada = textura_img.resize(imagem_base.size)

        # Aplica a máscara
        imagem_base.paste(textura_redimensionada, (0, 0), mascara)

    # Salva resultado em buffer e envia
    buffer = BytesIO()
    imagem_base.save(buffer, format="PNG")
    buffer.seek(0)

    return Response(content=buffer.getvalue(), media_type="image/png")
