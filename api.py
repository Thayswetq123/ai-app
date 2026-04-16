from fastapi import FastAPI, UploadFile, File, Depends
from sqlalchemy.orm import Session
from ultralytics import YOLO
import numpy as np
import cv2

from database import SessionLocal, Base, engine
from models import Detection
from auth import router as auth_router

app = FastAPI()
app.include_router(auth_router)

Base.metadata.create_all(bind=engine)

model = YOLO("model/yoloe-11s-seg.pt")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/detect/")
async def detect(user_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    results = model(img)

    boxes = results[0].boxes
    output = []

    if boxes is not None:
        cls = boxes.cls.cpu().numpy().astype(int)
        confs = boxes.conf.cpu().numpy()

        for i, c in enumerate(cls):
            det = Detection(
                user_id=user_id,
                object_class=model.names[c],
                confidence=float(confs[i])
            )
            db.add(det)

            output.append({
                "class": model.names[c],
                "confidence": float(confs[i])
            })

    db.commit()
    return {"detections": output}
