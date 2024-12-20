from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

@dataclass
class Document:
    title: str
    content: str
    amount: float
    department: str
    
class ApprovalHandler(ABC):
    def __init__(self) -> None:
        self._next_handler: Optional[ApprovalHandler] = None
    
    def set_next(self, handler: 'ApprovalHandler') -> 'ApprovalHandler':
        self._next_handler = handler
        return handler
    
    @abstractmethod
    def handle(self, document: Document) -> str:
        if self._next_handler:
            return self._next_handler.handle(document)
        return "End of chain"

class DepartmentManagerHandler(ApprovalHandler):
    """Can approve documents up to $1000"""
    
    def handle(self, document: Document) -> str:
        if document.amount <= 1000:
            return f"Department Manager approved document: {document.title}"
        
        print(f"Amount ${document.amount} exceeds Department Manager's limit. Passing to next handler...")
        return super().handle(document)

class DirectorHandler(ApprovalHandler):
    """Can approve documents up to $10000"""
    
    def handle(self, document: Document) -> str:
        if document.amount <= 10000:
            return f"Director approved document: {document.title}"
            
        print(f"Amount ${document.amount} exceeds Director's limit. Passing to next handler...")
        return super().handle(document)

class VPHandler(ApprovalHandler):
    """Can approve documents up to $50000"""
    
    def handle(self, document: Document) -> str:
        if document.amount <= 50000:
            return f"VP approved document: {document.title}"
            
        print(f"Amount ${document.amount} exceeds VP's limit. Passing to next handler...")
        return super().handle(document)

class CEOHandler(ApprovalHandler):
    """Can approve any document"""
    
    def handle(self, document: Document) -> str:
        return f"CEO approved document: {document.title}"

# Example usage
def setup_approval_chain() -> ApprovalHandler:
    # Create handlers
    department_manager = DepartmentManagerHandler()
    director = DirectorHandler()
    vp = VPHandler()
    ceo = CEOHandler()
    
    # Set up the chain
    department_manager.set_next(director).set_next(vp).set_next(ceo)
    
    return department_manager

def process_document(document: Document, chain: ApprovalHandler) -> None:
    print(f"\nProcessing document: {document.title}")
    print(f"Amount: ${document.amount}")
    result = chain.handle(document)
    print(f"Result: {result}\n")

# Test the chain with different documents
if __name__ == "__main__":
    approval_chain = setup_approval_chain()
    
    # Test different scenarios
    documents = [
        Document("Office Supplies", "Monthly supplies order", 800, "IT"),
        Document("Software Licenses", "Annual software renewal", 8000, "IT"),
        Document("Server Infrastructure", "New server cluster", 45000, "IT"),
        Document("Company Acquisition", "Acquiring startup", 1000000, "Executive")
    ]
    
    for doc in documents:
        process_document(doc, approval_chain)

