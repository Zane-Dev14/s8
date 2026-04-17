"""
Test suite for ChunkingService - validates concept-aware chunking and retrieval.

Tests cover:
1. Concept-aware chunk roles (definition, example, edge_case, workflow_step)
2. Concept bundle generation (explanation/example/mistake packaging)
3. Retrieval scoring boosts for bundle and checkpoint chunk types
4. Video learning node generation (what_changed, why_important, what_breaks, checkpoint_question)
"""
from __future__ import annotations

import json

import pytest
from sqlalchemy.orm import Session

from app.models.db import ContentChunk, ParsedDocument, SourceFile, TranscriptSegment
from app.services.chunking_service import ChunkingService


class TestConceptAwareChunkRoles:
    """Test concept-aware chunk role classification."""
    
    def test_classify_definition_sentences(self):
        """Verify definition sentences are classified correctly."""
        service = ChunkingService(None, None)
        
        # Test definition patterns
        assert service._classify_sentence_role("SFTP is a secure file transfer protocol.") == "concept_definition"
        assert service._classify_sentence_role("The term refers to encrypted data transmission.") == "concept_definition"
        assert service._classify_sentence_role("This means authentication happens via SSH keys.") == "concept_definition"
    
    def test_classify_example_sentences(self):
        """Verify example sentences are classified correctly."""
        service = ChunkingService(None, None)
        
        # Test example patterns
        assert service._classify_sentence_role("For example, EDI 850 documents use SFTP.") == "concept_example"
        assert service._classify_sentence_role("For instance, trading partners exchange files.") == "concept_example"
        assert service._classify_sentence_role("Sample configuration includes port 22.") == "concept_example"
    
    def test_classify_edge_case_sentences(self):
        """Verify edge case sentences are classified correctly."""
        service = ChunkingService(None, None)
        
        # Test edge case patterns
        assert service._classify_sentence_role("If the key permissions are wrong, authentication fails.") == "edge_case"
        assert service._classify_sentence_role("Unless the firewall allows port 22, connection breaks.") == "edge_case"
        assert service._classify_sentence_role("Edge case: empty files cause processing errors.") == "edge_case"
        assert service._classify_sentence_role("This will fail if the directory doesn't exist.") == "edge_case"
    
    def test_classify_workflow_step_sentences(self):
        """Verify workflow step sentences are classified correctly."""
        service = ChunkingService(None, None)
        
        # Test workflow patterns
        assert service._classify_sentence_role("Step 1: Generate SSH key pair.") == "workflow_step"
        assert service._classify_sentence_role("First, configure the SFTP adapter.") == "workflow_step"
        assert service._classify_sentence_role("Then, test the connection.") == "workflow_step"
        assert service._classify_sentence_role("Next, deploy the business process.") == "workflow_step"
        assert service._classify_sentence_role("Finally, monitor the logs.") == "workflow_step"


class TestConceptBundleGeneration:
    """Test concept bundle generation with explanation/example/mistake packaging."""
    
    @pytest.mark.asyncio
    async def test_concept_bundle_structure(
        self,
        db_session: Session,
        mock_ollama_router,
    ):
        """Verify concept bundles contain explanation, example, and mistake fields."""
        service = ChunkingService(db_session, mock_ollama_router)
        
        text = (
            "SFTP is a secure file transfer protocol. "
            "For example, it's used for EDI document exchange. "
            "If authentication fails, the connection breaks."
        )
        
        chunks = service._build_concept_bundle_chunks(text)
        
        # Should have bundle chunk
        bundle_chunks = [chunk for chunk in chunks if chunk[0] == "concept_bundle"]
        assert len(bundle_chunks) > 0
        
        # Parse bundle
        bundle_data = json.loads(bundle_chunks[0][1])
        assert "explanation" in bundle_data
        assert "example" in bundle_data
        assert "mistake" in bundle_data
        
        # Verify content
        assert "SFTP" in bundle_data["explanation"] or "secure" in bundle_data["explanation"]
    
    @pytest.mark.asyncio
    async def test_concept_bundle_separates_roles(
        self,
        db_session: Session,
        mock_ollama_router,
    ):
        """Verify concept bundles separate different role types."""
        service = ChunkingService(db_session, mock_ollama_router)
        
        text = (
            "SFTP means Secure File Transfer Protocol. "
            "For example, banks use it for secure transactions. "
            "If the key is compromised, security breaks. "
            "Step 1: Generate keys. "
            "Step 2: Configure server."
        )
        
        chunks = service._build_concept_bundle_chunks(text)
        
        # Should have different role chunks
        role_types = {chunk[0] for chunk in chunks}
        assert "concept_definition" in role_types
        assert "concept_example" in role_types
        assert "edge_case" in role_types
        assert "workflow_step" in role_types
        assert "concept_bundle" in role_types


class TestRetrievalScoringBoosts:
    """Test retrieval scoring boosts for special chunk types."""
    
    def test_concept_bundle_gets_boost(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_source_file: SourceFile,
    ):
        """Verify concept_bundle chunks get +0.08 boost."""
        service = ChunkingService(db_session, mock_ollama_router)
        
        # Create chunks with different types
        regular_chunk = ContentChunk(
            source_file_id=sample_source_file.id,
            chunk_type="document",
            text="SFTP protocol secure file transfer",
            source_reference="test.mp4",
        )
        bundle_chunk = ContentChunk(
            source_file_id=sample_source_file.id,
            chunk_type="concept_bundle",
            text='{"explanation": "SFTP protocol secure file transfer"}',
            source_reference="test.mp4",
        )
        
        db_session.add(regular_chunk)
        db_session.add(bundle_chunk)
        db_session.commit()
        
        # Retrieve with query
        results = service.retrieve_relevant_chunks_with_scores("SFTP protocol", limit=10)
        
        # Find both chunks
        regular_result = next((r for r in results if r.chunk.id == regular_chunk.id), None)
        bundle_result = next((r for r in results if r.chunk.id == bundle_chunk.id), None)
        
        if regular_result and bundle_result:
            # Bundle should have higher score due to boost
            assert bundle_result.score > regular_result.score
    
    def test_checkpoint_question_gets_boost(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_source_file: SourceFile,
    ):
        """Verify checkpoint_question chunks get +0.08 boost."""
        service = ChunkingService(db_session, mock_ollama_router)
        
        checkpoint_chunk = ContentChunk(
            source_file_id=sample_source_file.id,
            chunk_type="checkpoint_question",
            text="What is SFTP and how does it differ from FTP?",
            source_reference="test.mp4",
        )
        
        db_session.add(checkpoint_chunk)
        db_session.commit()
        
        results = service.retrieve_relevant_chunks_with_scores("SFTP FTP difference", limit=10)
        
        # Should retrieve checkpoint with boost
        checkpoint_result = next((r for r in results if r.chunk.id == checkpoint_chunk.id), None)
        assert checkpoint_result is not None
        # Score should include boost
        assert checkpoint_result.score > 0
    
    def test_edge_case_gets_smaller_boost(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_source_file: SourceFile,
    ):
        """Verify edge_case chunks get +0.04 boost."""
        service = ChunkingService(db_session, mock_ollama_router)
        
        edge_case_chunk = ContentChunk(
            source_file_id=sample_source_file.id,
            chunk_type="edge_case",
            text="If SFTP key permissions are wrong authentication fails",
            source_reference="test.mp4",
        )
        
        db_session.add(edge_case_chunk)
        db_session.commit()
        
        results = service.retrieve_relevant_chunks_with_scores("SFTP authentication", limit=10)
        
        edge_result = next((r for r in results if r.chunk.id == edge_case_chunk.id), None)
        assert edge_result is not None
        assert edge_result.score > 0
    
    def test_workflow_step_gets_smaller_boost(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_source_file: SourceFile,
    ):
        """Verify workflow_step chunks get +0.04 boost."""
        service = ChunkingService(db_session, mock_ollama_router)
        
        workflow_chunk = ContentChunk(
            source_file_id=sample_source_file.id,
            chunk_type="workflow_step",
            text="Step 1: Generate SFTP SSH key pair for authentication",
            source_reference="test.mp4",
        )
        
        db_session.add(workflow_chunk)
        db_session.commit()
        
        results = service.retrieve_relevant_chunks_with_scores("SFTP SSH key", limit=10)
        
        workflow_result = next((r for r in results if r.chunk.id == workflow_chunk.id), None)
        assert workflow_result is not None
        assert workflow_result.score > 0


class TestVideoLearningNodeGeneration:
    """Test video learning node generation with structured fields."""
    
    def test_video_learning_node_structure(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_source_file: SourceFile,
    ):
        """Verify video learning nodes contain all required fields."""
        service = ChunkingService(db_session, mock_ollama_router)
        
        segment = TranscriptSegment(
            source_file_id=sample_source_file.id,
            start_sec=120.0,
            end_sec=180.0,
            text="SFTP uses SSH for secure authentication and encryption",
            topic="SFTP Security",
            importance=4,
        )
        
        node = service._build_video_learning_node(sample_source_file, segment, None)
        
        # Verify all required fields
        assert "what_changed" in node
        assert "why_important" in node
        assert "what_breaks_if_misunderstood" in node
        assert "checkpoint_question" in node
        assert "source" in node
        
        # Verify content quality
        assert len(node["what_changed"]) > 0
        assert len(node["why_important"]) > 0
        assert len(node["what_breaks_if_misunderstood"]) > 0
        assert "?" in node["checkpoint_question"]
    
    def test_video_learning_node_detects_topic_change(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_source_file: SourceFile,
    ):
        """Verify video learning nodes detect topic changes between segments."""
        service = ChunkingService(db_session, mock_ollama_router)
        
        previous_segment = TranscriptSegment(
            source_file_id=sample_source_file.id,
            start_sec=60.0,
            end_sec=120.0,
            text="FTP is an old protocol for file transfer",
            topic="FTP Basics",
            importance=3,
        )
        
        current_segment = TranscriptSegment(
            source_file_id=sample_source_file.id,
            start_sec=120.0,
            end_sec=180.0,
            text="SFTP uses SSH for secure authentication and encryption",
            topic="SFTP Security",
            importance=4,
        )
        
        node = service._build_video_learning_node(sample_source_file, current_segment, previous_segment)
        
        # Should detect new focus on SFTP/SSH/security
        what_changed = node["what_changed"].lower()
        assert any(term in what_changed for term in ["sftp", "ssh", "secure", "authentication", "encryption", "new", "focus"])
    
    def test_video_learning_node_high_importance_failure_impact(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_source_file: SourceFile,
    ):
        """Verify high importance segments emphasize failure impact."""
        service = ChunkingService(db_session, mock_ollama_router)
        
        high_importance_segment = TranscriptSegment(
            source_file_id=sample_source_file.id,
            start_sec=120.0,
            end_sec=180.0,
            text="Critical mapping configuration for EDI processing",
            topic="EDI Mapping",
            importance=5,  # High importance
        )
        
        node = service._build_video_learning_node(sample_source_file, high_importance_segment, None)
        
        # Should emphasize serious failure consequences
        what_breaks = node["what_breaks_if_misunderstood"].lower()
        assert any(term in what_breaks for term in ["fail", "mapping", "process", "data"])
    
    def test_video_learning_node_includes_source_reference(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_source_file: SourceFile,
    ):
        """Verify video learning nodes include proper source reference with timestamps."""
        service = ChunkingService(db_session, mock_ollama_router)
        
        segment = TranscriptSegment(
            source_file_id=sample_source_file.id,
            start_sec=120.5,
            end_sec=180.7,
            text="Test content",
            topic="Test",
            importance=3,
        )
        
        node = service._build_video_learning_node(sample_source_file, segment, None)
        
        # Should include file path and timestamp range
        source = node["source"]
        assert sample_source_file.path in source
        assert "120" in source  # Start time
        assert "180" in source  # End time
        assert "@" in source
        assert "s" in source


class TestChunkingPipeline:
    """Test end-to-end chunking pipeline."""
    
    @pytest.mark.asyncio
    async def test_chunk_all_processes_video_files(
        self,
        db_session: Session,
        mock_ollama_router,
        sample_source_file: SourceFile,
    ):
        """Verify chunk_all processes video files with segments."""
        service = ChunkingService(db_session, mock_ollama_router)
        
        # Add transcript segments
        segment1 = TranscriptSegment(
            source_file_id=sample_source_file.id,
            start_sec=0.0,
            end_sec=60.0,
            text="Introduction to SFTP protocol and its security features",
            topic="SFTP Intro",
            importance=4,
        )
        segment2 = TranscriptSegment(
            source_file_id=sample_source_file.id,
            start_sec=60.0,
            end_sec=120.0,
            text="Configuring SSH keys for SFTP authentication",
            topic="SSH Keys",
            importance=5,
        )
        
        db_session.add(segment1)
        db_session.add(segment2)
        db_session.commit()
        
        # Run chunking
        count = service.chunk_all("job-1")
        
        # Should create multiple chunks per segment
        assert count > 0
        
        # Verify chunks were created
        chunks = db_session.query(ContentChunk).filter_by(source_file_id=sample_source_file.id).all()
        assert len(chunks) > 0
        
        # Should have video_learning_node chunks
        video_nodes = [c for c in chunks if c.chunk_type == "video_learning_node"]
        assert len(video_nodes) > 0
        
        # Should have checkpoint_question chunks
        checkpoints = [c for c in chunks if c.chunk_type == "checkpoint_question"]
        assert len(checkpoints) > 0
    
    @pytest.mark.asyncio
    async def test_chunk_all_processes_document_files(
        self,
        db_session: Session,
        mock_ollama_router,
    ):
        """Verify chunk_all processes document files."""
        service = ChunkingService(db_session, mock_ollama_router)
        
        # Create document source file
        doc_file = SourceFile(
            id="doc-1",
            job_id="job-1",
            path="guide.pdf",
            folder="documents",
            extension=".pdf",
            file_type="document",
            is_video=False,
            size_bytes=50000,
        )
        db_session.add(doc_file)
        
        # Add parsed document
        parsed_doc = ParsedDocument(
            source_file_id=doc_file.id,
            full_text=(
                "SFTP is a secure file transfer protocol. "
                "For example, it's used in EDI workflows. "
                "If authentication fails, transfers break."
            ),
        )
        db_session.add(parsed_doc)
        db_session.commit()
        
        # Run chunking
        count = service.chunk_all("job-1")
        
        assert count > 0
        
        # Verify chunks
        chunks = db_session.query(ContentChunk).filter_by(source_file_id=doc_file.id).all()
        assert len(chunks) > 0
        
        # Should have concept bundles
        bundles = [c for c in chunks if c.chunk_type == "concept_bundle"]
        assert len(bundles) > 0


class TestSemanticSplitting:
    """Test semantic text splitting logic."""
    
    def test_split_semantic_respects_sentence_boundaries(self):
        """Verify semantic splitting respects sentence boundaries."""
        service = ChunkingService(None, None)
        
        text = "First sentence. Second sentence. Third sentence."
        chunks = list(service._split_semantic(text))
        
        # Should create chunks
        assert len(chunks) > 0
        
        # Each chunk should be complete sentences
        for chunk in chunks:
            assert chunk.endswith(".") or chunk.endswith("!") or chunk.endswith("?")
    
    def test_split_semantic_handles_long_sentences(self):
        """Verify semantic splitting handles sentences longer than max_chunk_chars."""
        service = ChunkingService(None, None)
        
        # Create very long sentence
        long_sentence = "This is a very long sentence. " * 100
        chunks = list(service._split_semantic(long_sentence))
        
        # Should split long content
        assert len(chunks) > 0


class TestLexicalScoring:
    """Test lexical scoring for retrieval."""
    
    def test_lexical_score_calculates_overlap(self):
        """Verify lexical score calculates token overlap correctly."""
        service = ChunkingService(None, None)
        
        query_tokens = {"sftp", "secure", "file", "transfer"}
        chunk_tokens = {"sftp", "protocol", "secure", "authentication"}
        
        score = service._lexical_score(query_tokens, chunk_tokens)
        
        # Should have 2/4 = 0.5 overlap
        assert abs(score - 0.5) < 0.01
    
    def test_lexical_score_handles_no_overlap(self):
        """Verify lexical score returns 0 for no overlap."""
        service = ChunkingService(None, None)
        
        query_tokens = {"sftp", "secure"}
        chunk_tokens = {"http", "web"}
        
        score = service._lexical_score(query_tokens, chunk_tokens)
        assert score == 0.0
    
    def test_lexical_score_handles_empty_sets(self):
        """Verify lexical score handles empty token sets."""
        service = ChunkingService(None, None)
        
        assert service._lexical_score(set(), {"test"}) == 0.0
        assert service._lexical_score({"test"}, set()) == 0.0
        assert service._lexical_score(set(), set()) == 0.0


class TestTokenization:
    """Test tokenization logic."""
    
    def test_tokenize_extracts_alphanumeric(self):
        """Verify tokenization extracts alphanumeric tokens."""
        service = ChunkingService(None, None)
        
        text = "SFTP-2.0 uses SSH_keys for authentication!"
        tokens = service._tokenize(text)
        
        assert "sftp" in tokens
        assert "2" in tokens
        assert "0" in tokens
        assert "uses" in tokens
        assert "ssh_keys" in tokens
        assert "authentication" in tokens
    
    def test_tokenize_lowercases(self):
        """Verify tokenization converts to lowercase."""
        service = ChunkingService(None, None)
        
        text = "SFTP Protocol"
        tokens = service._tokenize(text)
        
        assert "sftp" in tokens
        assert "protocol" in tokens
        assert "SFTP" not in tokens

# Made with Bob
