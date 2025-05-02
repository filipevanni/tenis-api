from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel
from PIL import Image
import os
import json

app = FastAPI()

class Escolhas(BaseModel):
    cliente_id: str
    escolhas: dict

@app.post("/gerar-tenis")
async def gerar_tenis(data: Escolhas):
    # Abrir mockup base
    base_image = Image.open("mockup_tifi.png").convert("RGBA")
    texture_dir = "textures"
    mask_dir = "masks"

    # Carregar cores sólidas
    with open("colors.json", "r") as f:
        cores = json.load(f)

    # Processar partes
    for parte, escolha in data.escolhas.items():
        mask_path = os.path.join(mask_dir, f"{parte}.png")
        if not os.path.exists(mask_path):
            continue

        mask = Image.open(mask_path).convert("L")
        if escolha in cores:
            cor_rgba = tuple(cores[escolha])
            color_image = Image.new("RGBA", base_image.size, cor_rgba)
            recorte = Image.composite(color_image, Image.new("RGBA", base_image.size), mask)
        else:
            textura_path = os.path.join(texture_dir, f"{escolha}.png")
            if not os.path.exists(textura_path):
                continue
            textura = Image.open(textura_path).convert("RGBA").resize(base_image.size)
            recorte = Image.composite(textura, Image.new("RGBA", base_image.size), mask)

        base_image = Image.alpha_composite(base_image, recorte)

    # Salvar imagem final
    output_path = f"tenis_{data.cliente_id}.png"
    base_image.convert("RGB").save(output_path, "PNG")
    return FileResponse(output_path, media_type="image/png")
