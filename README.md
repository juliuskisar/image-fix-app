# 🖼️ Image Fix App

Uma aplicação web simples feita com **FastAPI** e **HTML/CSS/JavaScript puros** para **corrigir automaticamente a rotação de imagens** com base nos metadados EXIF. Ideal para fotos que aparecem "de lado" ao serem inseridas em documentos ou redes sociais.

## 🚀 Funcionalidades

- Upload de múltiplas imagens.
- Correção automática de rotação com base nos metadados EXIF.
- Download das imagens corrigidas.

## 🌐 Deploy na Vercel

Esta aplicação está pronta para ser implantada na [Vercel](https://vercel.com), utilizando uma função Serverless Python com FastAPI.

### 📦 Estrutura


## 🛠️ Requisitos Locais (opcional)

Para rodar localmente:

```bash
pip install -r requirements.txt
uvicorn api.index:app --reload
