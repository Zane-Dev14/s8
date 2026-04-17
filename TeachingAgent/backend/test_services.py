"""
Quick test script to verify core services work
"""
import asyncio
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.settings import settings, ensure_data_dirs
from app.services.streaming_service import StreamingService
from app.services.concept_extraction_service import ConceptExtractionService


async def test_streaming():
    """Test streaming service"""
    print("\n=== Testing Streaming Service ===")
    streaming = StreamingService()
    
    print("Testing stream_chat...")
    token_count = 0
    async for chunk in streaming.stream_chat(
        model=settings.model_fast,
        system_prompt="You are a helpful assistant.",
        user_prompt="Say 'Hello, world!' in one sentence.",
        temperature=0.7,
        max_tokens=50,
    ):
        token_count += 1
        if token_count <= 5:  # Print first 5 tokens
            print(f"  Token {token_count}: {chunk[:50]}")
    
    print(f"✓ Received {token_count} token chunks")
    return True


async def test_concept_extraction():
    """Test concept extraction"""
    print("\n=== Testing Concept Extraction ===")
    extractor = ConceptExtractionService()
    
    sample_content = [
        "Neural networks are computational models inspired by biological neurons.",
        "A neural network consists of layers: input layer, hidden layers, and output layer.",
        "Backpropagation is the algorithm used to train neural networks by adjusting weights.",
        "Common mistake: Not normalizing input data leads to poor training performance.",
    ]
    
    print("Extracting concepts from sample content...")
    concepts = await extractor.extract_concepts(
        subject_name="Machine Learning",
        content_chunks=sample_content,
        max_concepts=3,
    )
    
    print(f"✓ Extracted {len(concepts)} concepts:")
    for concept in concepts:
        print(f"  - {concept.get('name')} ({concept.get('difficulty')})")
    
    return len(concepts) > 0


async def main():
    """Run all tests"""
    print("=" * 60)
    print("Teaching Agent - Service Tests")
    print("=" * 60)
    
    # Ensure directories exist
    ensure_data_dirs()
    print(f"✓ Data directories created at: {settings.data_root}")
    
    # Test services
    tests = [
        ("Streaming", test_streaming),
        ("Concept Extraction", test_concept_extraction),
    ]
    
    results = {}
    for name, test_func in tests:
        try:
            result = await test_func()
            results[name] = "✓ PASS" if result else "✗ FAIL"
        except Exception as e:
            results[name] = f"✗ ERROR: {str(e)[:50]}"
            print(f"  Error: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary:")
    print("=" * 60)
    for name, result in results.items():
        print(f"{name:.<40} {result}")
    
    all_passed = all("PASS" in r for r in results.values())
    print("\n" + ("✓ All tests passed!" if all_passed else "✗ Some tests failed"))
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

# Made with Bob
