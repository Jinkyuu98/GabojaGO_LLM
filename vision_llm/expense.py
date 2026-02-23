# 경로: GabojaGO_backend/routes/
# pip install python-multipart
from fastapi import APIRouter, UploadFile, File, HTTPException
from langchain_core.exceptions import OutputParserException

from .LLM import ExpenseGPT
from .image_validation import to_data_uri, ImageValidationError

router = APIRouter()
OCR_model = ExpenseGPT()

@router.post("/parse")
async def parse_expense(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        content_type = file.content_type

        # 1) validation + data uri 변환
        data_uri = to_data_uri(image_bytes, content_type)
        # 2) LLM 호출
        result = OCR_model.chain.invoke({"image_data": data_uri})
        # 3) JSON 반환
        return result.model_dump()

    except ImageValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except OutputParserException:
        raise HTTPException(status_code=422, detail="LLM output parsing failed")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {e}")