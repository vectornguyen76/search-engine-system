from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from feature_extractor import FeatureExtractor
from faiss_search.searcher import FaissSearch
from qdrant_search.searcher import QdrantSearch
from qdrant_client.http.exceptions import UnexpectedResponse
from datetime import datetime
from config import settings
from schemas import Product
from log_config import configure_logging

logger = configure_logging(__name__)

# Initialize the feature extractor and FaissSearch instances
feature_extractor = FeatureExtractor()
faiss_search = FaissSearch()
qdrant_search = QdrantSearch()

# Create a FastAPI app instance with the specified title from settings
app = FastAPI(title=settings.APP_NAME)

# Config CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/search-image", response_model=list[Product])
async def search_image_qdrant(file: UploadFile = File(...)):
    """
    Endpoint to upload an image, extract features, and perform a search.

    Args:
        file (UploadFile): The image file to be uploaded.

    Returns:
        dict: A dictionary containing search results, including item information.
    """
    try:
        # Prepend the current datetime to the filename
        file.filename = datetime.now().strftime("%Y%m%d-%H%M%S-") + file.filename
        
        # Construct the full image path based on the settings
        image_path = settings.IMAGEDIR + file.filename
        
        # Read the contents of the uploaded file asynchronously
        contents = await file.read()
    
        # Write the uploaded contents to the specified image path
        with open(image_path, "wb") as f:
            f.write(contents)
            
        # Extract features from the uploaded image using the feature extractor
        feature = feature_extractor.extract_feature(image_path=image_path)
        
        # Perform a search using the extracted feature vector
        search_results = await qdrant_search.search(query_vector=feature, top_k=20)
        
        result = [
            Product.from_point(point)
            for point in search_results.result
        ]
        
        logger.info(f"Search image successfully, file name: {file.filename}")
        
        return result
    
    except UnexpectedResponse as e:
        # Handle the case when Qdrant returns an error and convert it to an exception
        # that FastAPI will understand and return to the client
        logger.error("Could not perform search: %s", e)
        raise HTTPException(status_code=500, detail=e.reason_phrase)

@app.post("/search-image-faiss", response_model=list[Product])
async def upload_image(file: UploadFile = File(...)):
    """
    Endpoint to upload an image, extract features, and perform a search.

    Args:
        file (UploadFile): The image file to be uploaded.

    Returns:
        dict: A dictionary containing search results, including item information.
    """
    try:
        # Prepend the current datetime to the filename
        file.filename = datetime.now().strftime("%Y%m%d-%H%M%S-") + file.filename
        
        # Construct the full image path based on the settings
        image_path = settings.IMAGEDIR + file.filename
        
        # Read the contents of the uploaded file asynchronously
        contents = await file.read()
    
        # Write the uploaded contents to the specified image path
        with open(image_path, "wb") as f:
            f.write(contents)
            
        # Extract features from the uploaded image using the feature extractor
        feature = feature_extractor.extract_feature(image_path=image_path)
        
        # Perform a search using the extracted feature vector
        search_results = faiss_search.search(query_vector=feature, top_k=20)
        
        logger.info(f"Search image use faiss successfully, file name: {file.filename}")
        
        return search_results
    
    except Exception as e:
        logger.error("Could not perform search: %s", e)
        raise HTTPException(status_code=500, detail=e)

