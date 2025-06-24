import unittest
from unittest.mock import MagicMock, patch
from typing import List

from domain.model.document import Document, DocumentStatus, DocumentType
from domain.model.document_chunk import DocumentChunk
from domain.port.document_repository_port import DocumentRepositoryPort
from domain.port.document_chunk_repository_port import DocumentChunkRepositoryPort
from domain.port.document_processor_port import DocumentProcessorPort
from domain.port.embedding_service_port import EmbeddingServicePort
from domain.service.document_service import DocumentService


class TestDocumentService(unittest.TestCase):
    def setUp(self):
        # Create mocks for all dependencies
        self.document_repository_mock = MagicMock(spec=DocumentRepositoryPort)
        self.chunk_repository_mock = MagicMock(spec=DocumentChunkRepositoryPort)
        self.document_processor_mock = MagicMock(spec=DocumentProcessorPort)
        self.embedding_service_mock = MagicMock(spec=EmbeddingServicePort)
        
        # Create the service with mocked dependencies
        self.document_service = DocumentService(
            document_repository=self.document_repository_mock,
            chunk_repository=self.chunk_repository_mock,
            document_processor=self.document_processor_mock,
            embedding_service=self.embedding_service_mock
        )

    def test_upload_document_creates_and_saves_document(self):
        # Given: document details
        document_id = "doc-123"
        filename = "test.pdf"
        file_path = "/path/to/test.pdf"
        document_type = DocumentType.PDF
        chat_id = "chat-456"
        
        expected_document = Document(
            document_id=document_id,
            filename=filename,
            document_type=document_type,
            file_path=file_path,
            chat_id=chat_id,
            status=DocumentStatus.PENDING
        )
        
        self.document_repository_mock.save_document.return_value = expected_document

        # When: uploading a document
        result = self.document_service.upload_document(
            document_id=document_id,
            filename=filename,
            file_path=file_path,
            document_type=document_type,
            chat_id=chat_id
        )

        # Then: document is created with correct properties and saved
        self.document_repository_mock.save_document.assert_called_once()
        saved_document = self.document_repository_mock.save_document.call_args[0][0]
        
        self.assertEqual(saved_document.document_id, document_id)
        self.assertEqual(saved_document.filename, filename)
        self.assertEqual(saved_document.document_type, document_type)
        self.assertEqual(saved_document.file_path, file_path)
        self.assertEqual(saved_document.chat_id, chat_id)
        self.assertEqual(saved_document.status, DocumentStatus.PENDING)
        self.assertEqual(result, expected_document)

    def test_process_document_success(self):
        # Given: a document exists and processing succeeds
        document_id = "doc-123"
        document = Document(
            document_id=document_id,
            filename="test.pdf",
            document_type=DocumentType.PDF,
            file_path="/path/to/test.pdf",
            chat_id="chat-456",
            status=DocumentStatus.PENDING
        )
        
        # Mock chunks returned by processor
        chunks = [
            DocumentChunk("chunk-1", document_id, "First chunk content", 0),
            DocumentChunk("chunk-2", document_id, "Second chunk content", 1)
        ]
        
        # Mock embeddings
        embeddings = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
        
        self.document_repository_mock.get_document_by_id.return_value = document
        self.document_processor_mock.process_document.return_value = chunks
        self.embedding_service_mock.generate_embeddings_batch.return_value = embeddings

        # When: processing the document
        result = self.document_service.process_document(document_id)

        # Then: document is processed successfully
        self.assertTrue(result)
        
        # Verify the flow
        self.document_repository_mock.get_document_by_id.assert_called_once_with(document_id)
        self.document_processor_mock.process_document.assert_called_once_with(document)
        self.embedding_service_mock.generate_embeddings_batch.assert_called_once_with(
            ["First chunk content", "Second chunk content"]
        )
        
        # Verify chunks have embeddings
        saved_chunks = self.chunk_repository_mock.save_chunks.call_args[0][0]
        self.assertEqual(len(saved_chunks), 2)
        self.assertEqual(saved_chunks[0].embedding, [0.1, 0.2, 0.3])
        self.assertEqual(saved_chunks[1].embedding, [0.4, 0.5, 0.6])
        
        # Verify document status updates
        self.assertEqual(self.document_repository_mock.save_document.call_count, 2)  # processing + processed

    def test_process_document_not_found(self):
        # Given: document doesn't exist
        document_id = "non-existent"
        self.document_repository_mock.get_document_by_id.return_value = None

        # When: trying to process non-existent document
        result = self.document_service.process_document(document_id)

        # Then: returns False
        self.assertFalse(result)
        self.document_repository_mock.get_document_by_id.assert_called_once_with(document_id)

    def test_process_document_failure_marks_as_failed(self):
        # Given: a document exists but processing fails
        document_id = "doc-123"
        document = Document(
            document_id=document_id,
            filename="test.pdf",
            document_type=DocumentType.PDF,
            file_path="/path/to/test.pdf",
            chat_id="chat-456",
            status=DocumentStatus.PENDING
        )
        
        self.document_repository_mock.get_document_by_id.return_value = document
        self.document_processor_mock.process_document.side_effect = Exception("Processing failed")

        # When: processing fails
        with self.assertRaises(Exception):
            self.document_service.process_document(document_id)

        # Then: document is marked as failed
        self.assertEqual(document.status, DocumentStatus.FAILED)

    def test_get_documents_for_chat(self):
        # Given: documents exist for a chat
        chat_id = "chat-123"
        expected_documents = [
            Document("doc-1", "file1.pdf", DocumentType.PDF, "/path1", chat_id),
            Document("doc-2", "file2.jpg", DocumentType.IMAGE, "/path2", chat_id)
        ]
        
        self.document_repository_mock.get_documents_by_chat_id.return_value = expected_documents

        # When: getting documents for chat
        result = self.document_service.get_documents_for_chat(chat_id)

        # Then: returns expected documents
        self.assertEqual(result, expected_documents)
        self.document_repository_mock.get_documents_by_chat_id.assert_called_once_with(chat_id)

    def test_get_processed_documents_for_chat(self):
        # Given: mix of processed and unprocessed documents
        chat_id = "chat-123"
        doc1 = Document("doc-1", "file1.pdf", DocumentType.PDF, "/path1", chat_id, DocumentStatus.PROCESSED)
        doc2 = Document("doc-2", "file2.jpg", DocumentType.IMAGE, "/path2", chat_id, DocumentStatus.PENDING)
        doc3 = Document("doc-3", "file3.pdf", DocumentType.PDF, "/path3", chat_id, DocumentStatus.PROCESSED)
        
        all_documents = [doc1, doc2, doc3]
        self.document_repository_mock.get_documents_by_chat_id.return_value = all_documents

        # When: getting processed documents
        result = self.document_service.get_processed_documents_for_chat(chat_id)

        # Then: returns only processed documents
        self.assertEqual(len(result), 2)
        self.assertIn(doc1, result)
        self.assertIn(doc3, result)
        self.assertNotIn(doc2, result)

    def test_delete_document(self):
        # Given: a document ID
        document_id = "doc-123"
        
        self.chunk_repository_mock.delete_chunks_by_document_id.return_value = True
        self.document_repository_mock.delete_document.return_value = True

        # When: deleting the document
        result = self.document_service.delete_document(document_id)

        # Then: chunks are deleted first, then document
        self.assertTrue(result)
        self.chunk_repository_mock.delete_chunks_by_document_id.assert_called_once_with(document_id)
        self.document_repository_mock.delete_document.assert_called_once_with(document_id)

    def test_get_pending_documents(self):
        # Given: pending documents exist
        pending_documents = [
            Document("doc-1", "file1.pdf", DocumentType.PDF, "/path1", "chat-1", DocumentStatus.PENDING),
            Document("doc-2", "file2.jpg", DocumentType.IMAGE, "/path2", "chat-2", DocumentStatus.PENDING)
        ]
        
        self.document_repository_mock.get_documents_by_status.return_value = pending_documents

        # When: getting pending documents
        result = self.document_service.get_pending_documents()

        # Then: returns pending documents
        self.assertEqual(result, pending_documents)
        self.document_repository_mock.get_documents_by_status.assert_called_once_with(DocumentStatus.PENDING)


if __name__ == '__main__':
    unittest.main() 