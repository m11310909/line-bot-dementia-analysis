import gc
from typing import Iterator, Dict, Any
from dataclasses import dataclass, asdict
import weakref

@dataclass
class Explanation:
    chunk_id: str
    reasoning_chain: list
    confidence_breakdown: dict
    evidence_sources: list
    related_concepts: list

class ExplanationEngine:
    def __init__(self, max_cache_size: int = 50):
        self._concept_cache = {}
        self._max_cache_size = max_cache_size

    def generate_explanations(self, chunks, user_context) -> Iterator[Dict[str, Any]]:
        """Memory-efficient streaming explanation generator"""
        for chunk in chunks:
            # Process one chunk at a time to minimize memory usage
            explanation = self._process_chunk(chunk, user_context)

            # Yield as dict to avoid keeping objects in memory
            yield asdict(explanation)

            # Force garbage collection after each chunk
            del explanation
            gc.collect()

    def _process_chunk(self, chunk: Dict, user_context: Dict) -> Explanation:
        """Process single chunk with minimal memory allocation"""
        return Explanation(
            chunk_id=chunk['chunk_id'],
            reasoning_chain=self._build_reasoning_chain_lean(chunk),
            confidence_breakdown=self._analyze_confidence_lean(chunk),
            evidence_sources=self._trace_sources_lean(chunk),
            related_concepts=self._find_related_concepts_cached(chunk)
        )

    def _build_reasoning_chain_lean(self, chunk: Dict) -> list:
        """Build reasoning chain with minimal intermediate objects"""
        steps = []
        content = chunk.get('content', '')

        # Direct processing without storing intermediate results
        if len(content) > 100:
            steps.append(f"Analysis of {len(content)} character content")
        if 'keywords' in chunk:
            steps.append(f"Key concepts: {', '.join(chunk['keywords'][:3])}")

        return steps

    def _analyze_confidence_lean(self, chunk: Dict) -> dict:
        """Lightweight confidence analysis"""
        score = chunk.get('relevance_score', 0.5)
        return {
            'overall': round(score, 2),
            'factors': ['content_length', 'keyword_match'] if score > 0.7 else ['partial_match']
        }

    def _trace_sources_lean(self, chunk: Dict) -> list:
        """Minimal source tracing"""
        return [chunk.get('source', 'unknown')]

    def _find_related_concepts_cached(self, chunk: Dict) -> list:
        """Use weak references and LRU-style cache for concepts"""
        chunk_id = chunk['chunk_id']

        # Check cache first
        if chunk_id in self._concept_cache:
            return self._concept_cache[chunk_id]

        # Clean cache if too large
        if len(self._concept_cache) >= self._max_cache_size:
            # Remove oldest half of entries
            items = list(self._concept_cache.items())
            self._concept_cache = dict(items[len(items)//2:])

        # Generate concepts
        concepts = self._extract_concepts_minimal(chunk)
        self._concept_cache[chunk_id] = concepts

        return concepts

    def _extract_concepts_minimal(self, chunk: Dict) -> list:
        """Extract concepts without heavy NLP processing"""
        content = chunk.get('content', '').lower()
        keywords = chunk.get('keywords', [])

        # Simple concept extraction
        concepts = []
        if keywords:
            concepts.extend(keywords[:5])  # Limit to 5 concepts max

        return list(set(concepts))  # Remove duplicates

    def clear_cache(self):
        """Manual cache clearing for memory management"""
        self._concept_cache.clear()
        gc.collect()

# Usage optimized for Replit shell execution
if __name__ == "__main__":
    # Example usage with memory monitoring
    import sys

    engine = ExplanationEngine(max_cache_size=30)  # Smaller cache for Replit

    # Mock data for testing
    test_chunks = [
        {
            'chunk_id': f'chunk_{i}',
            'content': f'Sample content {i} with relevant information',
            'keywords': [f'keyword_{i}', f'concept_{i}'],
            'relevance_score': 0.8,
            'source': f'source_{i}'
        }
        for i in range(5)
    ]

    user_context = {'user_level': 'intermediate'}

    print("Processing explanations...")
    for explanation in engine.generate_explanations(test_chunks, user_context):
        print(f"Chunk: {explanation['chunk_id']}")
        print(f"Confidence: {explanation['confidence_breakdown']['overall']}")
        print("---")

        # Optional: Monitor memory usage in shell
        # print(f"Memory usage: {sys.getsizeof(explanation)} bytes")

    engine.clear_cache()
    print("Processing complete, cache cleared.")