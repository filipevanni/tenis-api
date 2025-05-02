# Passo a passo para aplicar texturas nas máscaras do tênis usando Python e PIL

from PIL import Image
import base64
from io import BytesIO
import os

# 1. Função para aplicar uma textura base64 em uma máscara
def aplicar_textura(mask_path, textura_base64, imagem_base):
    # Abrir a imagem da máscara e converter para modo de transparência (L)
    mascara = Image.open(mask_path).convert("L")

    # Remover o prefixo do base64 (data:image/png;base64,)
    textura_data = base64.b64decode(textura_base64.split(',')[1])

    # Abrir a imagem da textura a partir do base64
    textura = Image.open(BytesIO(textura_data)).convert("RGBA")

    # Redimensionar a textura para o tamanho da máscara
    textura = textura.resize(mascara.size)

    # Aplicar a máscara sobre a textura (fundo transparente onde não for branco)
    textura_mascarada = Image.composite(textura, imagem_base, mascara)
    return textura_mascarada

# 2. Criar imagem base transparente do tamanho do mockup do tênis (ajuste conforme o seu mockup)
imagem_base = Image.new("RGBA", (1024, 768), (255, 255, 255, 0))

# 3. Lista de máscaras que deseja aplicar
mascaras = ['A', 'B', 'C']

# 4. Texturas em base64 recebidas da API ou input do cliente
texturas_base64 = {
    'A': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...',  # couro_bovino
    'B': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...',  # pirarucu
    'C': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...',  # pirarucu
}

# 5. Aplicar cada textura na sua máscara correspondente
for letra in mascaras:
    caminho_mascara = os.path.join('masks', f'{letra}.png')
    imagem_base = aplicar_textura(caminho_mascara, texturas_base64[letra], imagem_base)

# 6. Salvar imagem final do tênis personalizado
imagem_base.save('tenis_personalizado.png')
