from typing import Any

from pydantic import BaseModel, Field
from qdrant_client.http.models import ExtendedPointId


class QdrantSearchResult(BaseModel):
    id: "ExtendedPointId" = Field(..., description="The unique point ID in qdrant")
    score: float = Field(..., description="Cosine similarity score")
    payload: dict[str, Any] = Field(..., description="The raw JSON payload attached to the vector")
