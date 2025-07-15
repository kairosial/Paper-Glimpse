from typing import List
from app.domains.paper import PaperResponse, PaperSearchResponse
from app.infrastructure.arxiv_client import ArxivClient
from app.core.exceptions import ValidationException


class PaperService:
    """Service for paper-related operations."""
    
    def __init__(self):
        self.arxiv_client = ArxivClient()
    
    async def search_papers(self, query: str) -> PaperSearchResponse:
        """
        Search papers using arXiv API.
        
        Args:
            query: Search query string
            
        Returns:
            PaperSearchResponse with search results
            
        Raises:
            ValidationException: If query is invalid
        """
        # Validate query
        if not query or not query.strip():
            raise ValidationException("Query cannot be empty")
        
        # Search papers using arXiv client
        paper_data = await self.arxiv_client.search_papers(query.strip())
        
        # Convert to response models
        papers = []
        for data in paper_data:
            if data:  # Skip None entries from parsing errors
                paper = PaperResponse(
                    id=data['id'],
                    title=data['title'],
                    authors=data['authors'],
                    abstract=data['abstract'],
                    published_date=data['published_date'],
                    journal=data['journal'],
                    url=data['url']
                )
                papers.append(paper)
        
        return PaperSearchResponse(
            papers=papers,
            total_results=len(papers),
            query=query.strip()
        )