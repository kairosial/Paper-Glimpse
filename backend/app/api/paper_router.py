from fastapi import APIRouter, HTTPException
from app.domains.paper import PaperSearchRequest, PaperSearchResponse
from app.services.paper_service import PaperService
from app.core.exceptions import ArxivAPIException, ValidationException

router = APIRouter(prefix="/api/v1/papers", tags=["papers"])
paper_service = PaperService()


@router.post("/search", response_model=PaperSearchResponse, status_code=200)
async def search_papers(request: PaperSearchRequest) -> PaperSearchResponse:
    """
    Search papers using arXiv API.
    
    Args:
        request: Search request containing query
        
    Returns:
        PaperSearchResponse with search results
        
    Raises:
        HTTPException: If search fails
    """
    try:
        result = await paper_service.search_papers(request.query)
        return result
        
    except ValidationException as e:
        raise e
    except ArxivAPIException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )