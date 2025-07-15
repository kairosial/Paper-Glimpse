from fastapi import HTTPException


class ArxivAPIException(HTTPException):
    """Exception for arXiv API related errors."""
    
    def __init__(self, detail: str):
        super().__init__(status_code=503, detail=f"arXiv API error: {detail}")


class ValidationException(HTTPException):
    """Exception for input validation errors."""
    
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=f"Validation error: {detail}")