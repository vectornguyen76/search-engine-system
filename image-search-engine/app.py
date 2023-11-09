import time

from config import settings
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from qdrant_client.http.exceptions import UnexpectedResponse
from src.faiss_search.searcher import FaissSearch
from src.feature_extraction.extractor import FeatureExtractor
from src.qdrant_search.searcher import QdrantSearch
from src.schemas import ImageBase64Request, Product
from src.utils import LOGGER, save_image_file

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


@app.get("/")
def healthcheck() -> bool:
    """Check the server's status."""
    return True


@app.post("/search-image-faiss", response_model=list[Product])
async def search_image_faiss(file: UploadFile = File(...)):
    start_time = time.time()
    try:
        image_path = await save_image_file(file=file)

        # Extract features from the uploaded image using the feature extractor
        feature = feature_extractor.extract_feature(image_path=image_path)

        # Perform a search using the extracted feature vector
        search_results = faiss_search.search(query_vector=feature, top_k=20)

        LOGGER.info(f"Faiss search executed in {time.time() - start_time:.4f} seconds.")
        return search_results

    except Exception as e:
        LOGGER.error("Could not perform search: %s", e)
        raise HTTPException(status_code=500, detail=e)


@app.post("/search-image-qdrant", response_model=list[Product])
async def search_image_qdrant(file: UploadFile = File(...)):
    start_time = time.time()
    try:
        image_path = await save_image_file(file=file)

        # Extract features from the uploaded image using the feature extractor
        feature = feature_extractor.extract_feature(image_path=image_path)

        # Perform a search using the extracted feature vector
        search_results = await qdrant_search.search(query_vector=feature, top_k=20)

        result = [Product.from_point(point) for point in search_results.result]

        LOGGER.info(
            f"Qdrant search executed in {time.time() - start_time:.4f} seconds."
        )
        return result

    except UnexpectedResponse as e:
        # Handle the case when Qdrant returns an error and convert it to an exception
        # that FastAPI will understand and return to the client
        LOGGER.error("Could not perform search: %s", e)
        raise HTTPException(status_code=500, detail=e.reason_phrase)


@app.post("/search-image", response_model=list[Product])
async def search_image_qdrant_triton(file: UploadFile = File(...)):
    """
    Endpoint to upload an image, extract features, and perform a search.

    Args:
        file (UploadFile): The image file to be uploaded.

    Returns:
        dict: A dictionary containing search results, including item information.
    """
    image_path = await save_image_file(file=file)

    # Extract features from the uploaded image using the feature extractor
    feature = await feature_extractor.triton_extract_feature(
        image_path=image_path, model_name=settings.PYTORCH_MODEL_NAME
    )

    # Perform a search using the extracted feature vector
    search_results = await qdrant_search.search(query_vector=feature, top_k=20)

    result = [Product.from_point(point) for point in search_results.result]

    return result


@app.post("/search-image-base64", response_model=list[Product])
async def search_image_base64(data: ImageBase64Request):
    # Extract features from the uploaded image using the feature extractor
    feature = await feature_extractor.triton_extract_base64(
        image=data.image, model_name=settings.PYTORCH_MODEL_NAME
    )

    # Perform a search using the extracted feature vector
    search_results = await qdrant_search.search(query_vector=feature, top_k=20)

    result = [Product.from_point(point) for point in search_results.result]

    return result
