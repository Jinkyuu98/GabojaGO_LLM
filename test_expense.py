import base64
import random
from pathlib import Path

from IMAGE_VALIDATION import validate_image, image_uri_prefix
from LLM import ExpenseGPT

ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".webp"}

def guess_content_type(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in [".jpg", ".jpeg"]:
        return "image/jpeg"
    if ext == ".png":
        return "image/png"
    if ext == ".webp":
        return "image/webp"
    raise ValueError(f"지원하지 않는 확장자: {ext}")

def pick_random_receipt(folder: Path) -> Path:
    files = [p for p in folder.rglob("*") if p.is_file() and p.suffix.lower() in ALLOWED_EXT]
    if not files:
        raise FileNotFoundError(f"{folder} 안에 jpg/jpeg/png/webp 파일이 없음")
    return random.choice(files)

def main():
    BASE_DIR = Path(__file__).parent
    receipts_dir = BASE_DIR / "dataset"

    files = [p for p in receipts_dir.iterdir() if p.suffix.lower() in [".jpg",".jpeg",".png",".webp"]]

    TEST_COUNT = 5

    llm = ExpenseGPT()

    for i in range(TEST_COUNT):
        img_path = random.choice(files)  # 랜덤 1개 선택

        print(f"\n[TEST {i+1}] {img_path.name}")

        image_bytes = img_path.read_bytes()
        content_type = guess_content_type(img_path)
        validate_image(content_type, len(image_bytes))

        b64 = base64.b64encode(image_bytes).decode("utf-8")
        data_uri = image_uri_prefix(content_type) + b64

        result = llm.chain.invoke({"image_data": data_uri})

        if hasattr(result, "model_dump"):
            print(result.model_dump())
        else:
            print(result)

if __name__ == "__main__":
    main()