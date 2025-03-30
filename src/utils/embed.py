
import os
from typing import List
import cohere
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("COHERE_API_KEY")

co = cohere.ClientV2(
    api_key=API_KEY
)

def embed(texts: List[str]) -> List[List[float]]:
  """
  Embeds a list of texts into a list of vectors.
  """
  response = co.embed(
      texts=texts,
      model="embed-english-v3.0",
      input_type="search_document",
      embedding_types=["float"],
  )
  return response.embeddings.float_
