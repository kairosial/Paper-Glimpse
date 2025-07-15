from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, validator


class PaperSearchRequest(BaseModel):
    """Request model for paper search."""
    
    query: str
    
    @validator('query')
    def validate_query(cls, v):
        if not v or not v.strip():
            raise ValueError('Query cannot be empty')
        if len(v.strip()) < 2:
            raise ValueError('Query must be at least 2 characters long')
        return v.strip()


class PaperResponse(BaseModel):
    """Response model for individual paper."""
    
    id: str
    title: str
    authors: List[str]
    abstract: str
    published_date: str
    journal: str
    url: str


class PaperSearchResponse(BaseModel):
    """Response model for paper search results."""
    
    papers: List[PaperResponse]
    total_results: int
    query: str