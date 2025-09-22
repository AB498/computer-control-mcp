import cv2
from rapidocr import RapidOCR
from rapidocr_onnxruntime import VisRes

image_path = r"C:\Users\Admin\AppData\Local\Temp\tmpdw2d8r14\screenshot_20250815_033153_f99a8396.png"
img = cv2.imread(image_path)
if img is None:
    print(f"Failed to load img: {image_path}")
else:
    print(f"Loaded img: {image_path}, shape: {img.shape}")
    engine = RapidOCR()
    vis = VisRes()
    output = engine(img)

    # Separate into boxes, texts, and scores
    boxes  = output.boxes
    txts   = output.txts
    scores = output.scores
    zipped_results = list(zip(boxes, txts, scores))
    print(f"Found {len(zipped_results)} text items in OCR result.")
    print(f"First 10 items: {str(zipped_results).encode("utf-8", errors="ignore")}")
