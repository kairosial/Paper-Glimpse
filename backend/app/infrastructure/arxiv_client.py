import xml.etree.ElementTree as ET
from typing import List, Dict, Any
import requests
from datetime import datetime
import re

from app.core.config import settings
from app.core.exceptions import ArxivAPIException


class ArxivClient:
    """Client for interacting with arXiv API."""
    
    def __init__(self):
        self.base_url = settings.arxiv_base_url
        self.timeout = settings.arxiv_timeout
        
    async def search_papers(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Search papers on arXiv using keyword.
        
        Args:
            keyword: Search keyword or field name
            
        Returns:
            List of paper dictionaries
            
        Raises:
            ArxivAPIException: If API request fails
        """
        try:
            url = self._build_query_url(keyword)
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            papers = self._parse_response(response.text)
            return papers
            
        except requests.exceptions.RequestException as e:
            raise ArxivAPIException(f"Failed to fetch papers: {str(e)}")
        except Exception as e:
            raise ArxivAPIException(f"Unexpected error: {str(e)}")
    
    def _build_query_url(self, keyword: str) -> str:
        """Build arXiv API query URL."""
        # Encode keyword for URL
        encoded_keyword = keyword.replace(' ', '+')
        
        params = {
            'search_query': f'all:{encoded_keyword}',
            'sortBy': 'submittedDate',
            'sortOrder': 'descending',
            'max_results': settings.arxiv_max_results
        }
        
        param_string = '&'.join([f'{k}={v}' for k, v in params.items()])
        return f"{self.base_url}?{param_string}"
    
    def _parse_response(self, xml_content: str) -> List[Dict[str, Any]]:
        """Parse arXiv API XML response."""
        try:
            root = ET.fromstring(xml_content)
            
            # Define namespaces
            namespaces = {
                'atom': 'http://www.w3.org/2005/Atom',
                'arxiv': 'http://arxiv.org/schemas/atom'
            }
            
            papers = []
            entries = root.findall('.//atom:entry', namespaces)
            
            for entry in entries:
                paper = self._parse_entry(entry, namespaces)
                if paper:
                    papers.append(paper)
            
            return papers
            
        except ET.ParseError as e:
            raise ArxivAPIException(f"Failed to parse XML response: {str(e)}")
    
    def _parse_entry(self, entry: ET.Element, namespaces: dict) -> Dict[str, Any]:
        """Parse individual paper entry from XML."""
        try:
            # Extract ID from arXiv URL
            id_elem = entry.find('atom:id', namespaces)
            arxiv_id = id_elem.text.split('/')[-1] if id_elem is not None else ""
            
            # Extract title
            title_elem = entry.find('atom:title', namespaces)
            title = title_elem.text.strip() if title_elem is not None else ""
            
            # Extract authors
            authors = []
            author_elems = entry.findall('atom:author', namespaces)
            for author_elem in author_elems:
                name_elem = author_elem.find('atom:name', namespaces)
                if name_elem is not None:
                    authors.append(name_elem.text.strip())
            
            # Extract abstract
            summary_elem = entry.find('atom:summary', namespaces)
            abstract = summary_elem.text.strip() if summary_elem is not None else ""
            
            # Extract published date
            published_elem = entry.find('atom:published', namespaces)
            published_date = published_elem.text if published_elem is not None else ""
            
            # Extract journal/category
            category_elem = entry.find('arxiv:primary_category', namespaces)
            journal = category_elem.get('term', 'arXiv') if category_elem is not None else 'arXiv'
            
            # Build paper URL
            url = f"https://arxiv.org/abs/{arxiv_id}"
            
            return {
                'id': arxiv_id,
                'title': self._clean_text(title),
                'authors': authors,
                'abstract': self._clean_text(abstract),
                'published_date': published_date,
                'journal': journal,
                'url': url
            }
            
        except Exception as e:
            # Log error but don't fail entire request
            return None
    
    def _clean_text(self, text: str) -> str:
        """Clean text by removing extra whitespace and newlines."""
        if not text:
            return ""
        
        # Remove extra whitespace and newlines
        cleaned = re.sub(r'\s+', ' ', text).strip()
        return cleaned