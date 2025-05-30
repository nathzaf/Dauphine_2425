from abc import ABC, abstractmethod
from typing import List, Dict, Any

class DocumentIngestionPort(ABC):
    
    @abstractmethod
    def ingest_from_external_source(self, source_id: str, source_config: Dict[str, Any]) -> List[str]:
        pass
    
    @abstractmethod
    def ingest_user_specific_documents(self, user_id: str, user_info: Dict[str, Any]) -> List[str]:
        pass 