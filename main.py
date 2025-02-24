from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from pdf2image import convert_from_bytes
from fastapi.responses import JSONResponse
from io import BytesIO
import base64
from extractor import Insighter, Extractor

app = FastAPI()
insighter = Insighter()
extractor = Extractor()

@app.get("/extract")
async def extract(doc_type: str = Query(..., description="Type of document"), file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()

        pages = convert_from_bytes(file_bytes, dpi=275)

        page_images = []
        for page in pages:
            buffered = BytesIO()
            page.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            page_images.append(img_str)

        page_level_content = insighter.extract(page_images, doc_type)

        extracted_json = extractor.extract(page_level_content)

        return JSONResponse(content={"page_content": page_level_content, "extracted_json": extracted_json})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/v2/extract")
async def extract(doc_type: str = Query(..., description="Type of document"), file: UploadFile = File(...), dynamic_keys: str = Query(..., description="Keys to extract")):
    try:
        file_bytes = await file.read()

        pages = convert_from_bytes(file_bytes, dpi=275)

        page_images = []
        for page in pages:
            buffered = BytesIO()
            page.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            page_images.append(img_str)

        page_level_content = insighter.extract(page_images, doc_type)
        extracted_json = extractor.extract(page_level_content, doc_type,dynamic_keys)

        return JSONResponse(content={"page_content": page_level_content, "extracted_json": extracted_json})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))