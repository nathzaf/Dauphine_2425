from typing import List, Optional
from domain.model.document import Document, DocumentStatus, DocumentType
from domain.model.document_chunk import DocumentChunk
from domain.port.document_repository_port import DocumentRepositoryPort
from domain.port.document_chunk_repository_port import DocumentChunkRepositoryPort
from domain.port.document_processor_port import DocumentProcessorPort
from domain.port.embedding_service_port import EmbeddingServicePort


class DocumentService:
    def __init__(
        self,
        document_repository: DocumentRepositoryPort,
        chunk_repository: DocumentChunkRepositoryPort,
        document_processor: DocumentProcessorPort,
        embedding_service: EmbeddingServicePort
    ):
        self.document_repository = document_repository
        self.chunk_repository = chunk_repository
        self.document_processor = document_processor
        self.embedding_service = embedding_service

    def upload_document(
        self,
        document_id: str,
        filename: str,
        file_path: str,
        document_type: DocumentType,
        chat_id: str
    ) -> Document:
        """Upload and save a new document"""
        document = Document(
            document_id=document_id,
            filename=filename,
            document_type=document_type,
            file_path=file_path,
            chat_id=chat_id,
            status=DocumentStatus.PENDING
        )
        return self.document_repository.save_document(document)

    def process_document(self, document_id: str) -> bool:
        """Process a document: extract text, create chunks, and generate embeddings"""
        document = self.document_repository.get_document_by_id(document_id)
        if not document:
            return False

        try:
            # Mark as processing
            document.mark_as_processing()
            self.document_repository.save_document(document)

            # Process the document to get chunks
            chunks = self.document_processor.process_document(document)

            # Generate embeddings for each chunk
            texts = [chunk.content for chunk in chunks]
            embeddings = self.embedding_service.generate_embeddings_batch(texts)

            # Add embeddings to chunks
            for chunk, embedding in zip(chunks, embeddings):
                chunk.embedding = embedding

            # Save chunks
            self.chunk_repository.save_chunks(chunks)

            # Mark as processed
            document.mark_as_processed()
            self.document_repository.save_document(document)

            return True

        except Exception as e:
            # Mark as failed
            document.mark_as_failed()
            self.document_repository.save_document(document)
            raise e

    def get_documents_for_chat(self, chat_id: str) -> List[Document]:
        """Get all documents for a specific chat"""
        return self.document_repository.get_documents_by_chat_id(chat_id)

    def get_processed_documents_for_chat(self, chat_id: str) -> List[Document]:
        """Get only processed documents for a specific chat"""
        documents = self.get_documents_for_chat(chat_id)
        return [doc for doc in documents if doc.is_processed()]

    def delete_document(self, document_id: str) -> bool:
        """Delete a document and its chunks"""
        # Delete chunks first
        self.chunk_repository.delete_chunks_by_document_id(document_id)
        # Then delete the document
        return self.document_repository.delete_document(document_id)

    def get_pending_documents(self) -> List[Document]:
        """Get all documents that need processing"""
        return self.document_repository.get_documents_by_status(DocumentStatus.PENDING) 