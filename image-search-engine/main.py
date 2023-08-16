from fastapi import FastAPI, File, UploadFile
from feature_extractor import FeatureExtractor
from faiss_search import FaissSearch
from datetime import datetime
from config import settings

app = FastAPI()
app = FastAPI(title=settings.APP_NAME)

feature_extractor = FeatureExtractor()
faiss_search = FaissSearch()

@app.post("/search-image")
async def upload_image(file: UploadFile = File(...)):
    file.filename = datetime.now().strftime("%Y%m%d-%H%M%S-") + file.filename
    
    image_path = settings.IMAGEDIR + file.filename
    
    contents = await file.read()
 
    with open(image_path, "wb") as f:
        f.write(contents)
        
    feature = feature_extractor.extract_feature(image_path=image_path)
    
    result = faiss_search.search(query_vector=feature, top_k=3)
    
    return {"filename": file.filename}

