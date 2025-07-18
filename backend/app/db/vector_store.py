import os
from pinecone import Pinecone, ServerlessSpec, CloudProvider, AwsRegion

# Load Pinecone credentials from environment variables
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY environment variable is required")
try:

    # Initialize Pinecone client
    pc = Pinecone(api_key=PINECONE_API_KEY)

except Exception as e:
    raise RuntimeError(f"Error occured while intialising pinecone client:{e}")

# Constants
INDEX_NAME = "perspective"
DIMENSIONS = 384
METRIC = "cosine"

# Create index if it doesn't exist
if not pc.has_index(INDEX_NAME):
    print(f"Creating index: {INDEX_NAME}")
    pc.create_index(
        name=INDEX_NAME,
        dimension=DIMENSIONS,
        metric=METRIC,
        spec=ServerlessSpec(
            cloud=CloudProvider.AWS,
            region=AwsRegion.US_EAST_1
        )
    )
else:
    print(f"Index '{INDEX_NAME}' already exists")

try:
    # Connect to the index
    index = pc.Index(INDEX_NAME)
except Exception as e:
    raise RuntimeError("Error occured while "
                       f"connecting to the index {INDEX_NAME}:{e}")
