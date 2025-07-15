from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration."""
    
    app_name: str = "Paper Glimpse API"
    debug: bool = True
    version: str = "1.0.0"
    
    # arXiv API settings
    arxiv_base_url: str = "https://export.arxiv.org/api/query"
    arxiv_max_results: int = 20
    arxiv_timeout: int = 30
    
    class Config:
        env_file = ".env"


settings = Settings()