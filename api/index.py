from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image, ExifTags
import os
import shutil
from uuid import uuid4
# from mangum import Mangum





app = FastAPI()
# Adaptador para AWS Lambda/Vercel
# handler = Mangum(app)

# Pastas
UPLOAD_FOLDER = "/tmp/uploads"  # no Vercel só podemos escrever em /tmp
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.mount("/static", StaticFiles(directory="api/static"), name="static")
templates = Jinja2Templates(directory="api/templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

def corrigir_orientacao(img_path: str) -> str:
    try:
        imagem = Image.open(img_path)
        exif = imagem._getexif()
        if exif is not None:
            for tag, valor in ExifTags.TAGS.items():
                if valor == 'Orientation':
                    orientation_tag = tag
                    break

            orientacao = exif.get(orientation_tag, 1)
            if orientacao == 3:
                imagem = imagem.rotate(180, expand=True)
            elif orientacao == 6:
                imagem = imagem.rotate(270, expand=True)
            elif orientacao == 8:
                imagem = imagem.rotate(90, expand=True)

        nome_corrigido = f"{uuid4().hex}.jpg"
        caminho_corrigido = os.path.join(UPLOAD_FOLDER, nome_corrigido)
        imagem.save(caminho_corrigido)
        return nome_corrigido
    except Exception as e:
        print(f"Erro ao corrigir imagem: {e}")
        return None

@app.post("/upload")
async def upload_imagens(files: list[UploadFile] = File(...)):
    arquivos_corrigidos = []

    for file in files:
        original_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(original_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        nome_corrigido = corrigir_orientacao(original_path)
        if nome_corrigido:
            arquivos_corrigidos.append(nome_corrigido)

    return {"arquivos": arquivos_corrigidos}

@app.get("/download/{filename}")
async def download(filename: str):
    caminho = os.path.join(UPLOAD_FOLDER, filename)
    return FileResponse(caminho, media_type="image/jpeg", filename=filename)

# # Adaptador para AWS Lambda/Vercel
# handler = Mangum(app)
