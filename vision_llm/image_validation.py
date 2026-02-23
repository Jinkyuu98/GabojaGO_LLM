# 경로: GabojaGO_backend/library/
import base64

ALLOWED_MIME = {"image/jpeg", "image/png", "image/webp"}
MAX_BYTES = 10 * 1024 * 1024  # 10MB

class ImageValidationError(ValueError):
    pass

def validate_image(content_type: str, size: int) -> None:
    if content_type not in ALLOWED_MIME:
        raise ImageValidationError("지원하지 않는 이미지 형식입니다. (jpeg/png/webp만 가능)")
    if size > MAX_BYTES:
        raise ImageValidationError("이미지 파일 크기가 너무 큽니다. (최대 10MB)")

def image_uri_prefix(content_type: str) -> str:
    return f"data:{content_type};base64,"

def to_data_uri(image_bytes: bytes, content_type: str) -> str:
    validate_image(content_type, len(image_bytes))
    b64 = base64.b64encode(image_bytes).decode("utf-8")
    return image_uri_prefix(content_type) + b64