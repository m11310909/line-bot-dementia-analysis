import gc
from typing import Iterator, Dict, Any, List
from dataclasses import dataclass, asdict
import json
from datetime import datetime

# ExplanationEngine (optimized version)
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

    def generate_explanations(self, chunks, user_context):
        """Generate explanations for chunks with memory optimization"""
        explanations = []
        for chunk in chunks:
            explanation = {
                'chunk_id': chunk['chunk_id'],
                'reasoning_chain': self.build_reasoning_chain(chunk),
                'confidence_breakdown': self.analyze_confidence(chunk),
                'evidence_sources': self.trace_sources(chunk),
                'related_concepts': self.find_related_concepts(chunk)
            }
            explanations.append(explanation)

            # Clean up after every 10 chunks to manage memory
            if len(explanations) % 10 == 0:
                gc.collect()

        return explanations

    def build_reasoning_chain(self, chunk):
        """Build logical reasoning chain for chunk analysis"""
        chain = []
        content = chunk.get('content', '')

        # Step 1: Content analysis
        if len(content) > 200:
            chain.append("Comprehensive content detected - full analysis applied")
        elif len(content) > 50:
            chain.append("Moderate content length - targeted analysis")
        else:
            chain.append("Brief content - focused extraction")

        # Step 2: Keyword relevance
        if 'keywords' in chunk and chunk['keywords']:
            chain.append(f"Key concepts identified: {', '.join(chunk['keywords'][:3])}")

        # Step 3: Context matching
        if chunk.get('relevance_score', 0) > 0.7:
            chain.append("High relevance to query - priority processing")
        elif chunk.get('relevance_score', 0) > 0.4:
            chain.append("Moderate relevance - supplementary information")

        return chain

    def analyze_confidence(self, chunk):
        """Analyze confidence levels with breakdown"""
        score = chunk.get('relevance_score', 0.5)
        word_count = len(chunk.get('content', '').split())

        factors = []
        if score > 0.8:
            factors.append("high_relevance")
        if word_count > 100:
            factors.append("comprehensive_content")
        if chunk.get('keywords'):
            factors.append("keyword_match")

        return {
            'overall_confidence': round(score, 2),
            'contributing_factors': factors,
            'content_quality': 'high' if word_count > 50 else 'medium',
            'reliability_score': min(score + (word_count / 1000), 1.0)
        }

    def trace_sources(self, chunk):
        """Trace and validate evidence sources"""
        sources = []

        # Primary source
        if 'source' in chunk:
            sources.append({
                'type': 'primary',
                'reference': chunk['source'],
                'confidence': chunk.get('source_confidence', 0.8)
            })

        return sources

    def find_related_concepts(self, chunk):
        """Find related concepts with caching"""
        chunk_id = chunk['chunk_id']

        # Check cache first
        if chunk_id in self._concept_cache:
            return self._concept_cache[chunk_id]

        # Clean cache if too large
        if len(self._concept_cache) >= self._max_cache_size:
            items = list(self._concept_cache.items())
            self._concept_cache = dict(items[len(items)//2:])

        # Generate concepts
        concepts = self._extract_concepts_minimal(chunk)
        self._concept_cache[chunk_id] = concepts

        return concepts

    def _extract_concepts_minimal(self, chunk):
        """Extract concepts without heavy processing"""
        keywords = chunk.get('keywords', [])
        content = chunk.get('content', '').lower()

        concepts = []
        if keywords:
            concepts.extend(keywords[:5])

        # Simple keyword extraction from content
        important_words = ['analysis', 'data', 'research', 'study', 'result']
        for word in important_words:
            if word in content:
                concepts.append(word)

        return list(set(concepts))

# ResponseGenerator
class ResponseGenerator:
    def __init__(self, max_explanations: int = 5):
        self.max_explanations = max_explanations
        self.response_templates = {
            'detailed': self._detailed_template,
            'concise': self._concise_template,
            'technical': self._technical_template
        }

    def format_response(self, explanations: List[Dict], user_context: Dict = None, 
                       format_type: str = 'detailed') -> Dict[str, Any]:
        """Main method to format explanations into user-friendly response"""

        # Limit explanations for memory efficiency
        limited_explanations = explanations[:self.max_explanations]

        # Get formatting template
        template_func = self.response_templates.get(format_type, self._detailed_template)

        response = {
            'timestamp': datetime.now().isoformat(),
            'total_explanations': len(limited_explanations),
            'format_type': format_type,
            'content': template_func(limited_explanations, user_context or {}),
            'metadata': self._generate_metadata(limited_explanations)
        }

        return response

    def _detailed_template(self, explanations: List[Dict], user_context: Dict) -> str:
        """Detailed explanation format with reasoning chains"""
        output = []

        for i, exp in enumerate(explanations, 1):
            section = [
                f"## Explanation {i} (ID: {exp['chunk_id']})",
                "",
                "**Reasoning Process:**"
            ]

            # Add reasoning chain
            for step in exp.get('reasoning_chain', []):
                section.append(f"• {step}")

            section.extend([
                "",
                f"**Confidence Level:** {exp.get('confidence_breakdown', {}).get('overall_confidence', 'N/A')}",
                ""
            ])

            # Add evidence if available
            sources = exp.get('evidence_sources', [])
            if sources:
                section.append("**Evidence Sources:**")
                for source in sources[:2]:
                    section.append(f"• {source.get('reference', 'Unknown source')}")
                section.append("")

            # Add related concepts
            concepts = exp.get('related_concepts', [])
            if concepts:
                section.append(f"**Related Concepts:** {', '.join(concepts[:3])}")
                section.append("")

            output.extend(section)
            output.append("---")

        return "\n".join(output)

    def _concise_template(self, explanations: List[Dict], user_context: Dict) -> str:
        """Concise format for quick overview"""
        output = ["# Quick Explanations Summary", ""]

        for i, exp in enumerate(explanations, 1):
            confidence = exp.get('confidence_breakdown', {}).get('overall_confidence', 'N/A')
            concepts = exp.get('related_concepts', [])

            line = f"{i}. **{exp['chunk_id']}** (Confidence: {confidence})"
            if concepts:
                line += f" - Key concepts: {', '.join(concepts[:2])}"

            output.append(line)

        return "\n".join(output)

    def _technical_template(self, explanations: List[Dict], user_context: Dict) -> str:
        """Technical format with detailed breakdowns"""
        output = ["# Technical Analysis Report", ""]

        for exp in explanations:
            output.extend([
                f"### Chunk Analysis: {exp['chunk_id']}",
                "",
                "**Confidence Breakdown:**"
            ])

            confidence_data = exp.get('confidence_breakdown', {})
            for key, value in confidence_data.items():
                output.append(f"• {key}: {value}")

            output.extend(["", "**Processing Chain:**"])
            for step in exp.get('reasoning_chain', []):
                output.append(f"1. {step}")

            output.extend(["", "---", ""])

        return "\n".join(output)

    def _generate_metadata(self, explanations: List[Dict]) -> Dict[str, Any]:
        """Generate response metadata for tracking"""
        if not explanations:
            return {}

        # Calculate average confidence
        confidences = []
        for exp in explanations:
            conf = exp.get('confidence_breakdown', {}).get('overall_confidence', 0)
            if isinstance(conf, (int, float)):
                confidences.append(conf)

        avg_confidence = sum(confidences) / len(confidences) if confidences else 0

        return {
            'average_confidence': round(avg_confidence, 2),
            'high_confidence_count': sum(1 for c in confidences if c > 0.7),
            'total_sources': sum(len(exp.get('evidence_sources', [])) for exp in explanations),
            'processing_summary': f"Processed {len(explanations)} explanations"
        }

    def to_plain_text(self, response: Dict[str, Any]) -> str:
        """Convert response to plain text"""
        content = response.get('content', '')
        metadata = response.get('metadata', {})

        footer = f"\n\nSummary: {metadata.get('processing_summary', 'No summary')}"
        if metadata.get('average_confidence'):
            footer += f" | Avg Confidence: {metadata['average_confidence']}"

        return content + footer

# Complete Integration System
class IntegratedSystem:
    def __init__(self):
        self.engine = ExplanationEngine(max_cache_size=30)  # Smaller for Replit
        self.generator = ResponseGenerator(max_explanations=3)

    def process_query(self, chunks, user_context, format_type='detailed'):
        """Complete processing pipeline"""
        print("🔄 Processing chunks through ExplanationEngine...")
        explanations = self.engine.generate_explanations(chunks, user_context)

        print("🔄 Formatting response through ResponseGenerator...")
        response = self.generator.format_response(explanations, user_context, format_type)

        print("✅ Processing complete!\n")
        return response

    def clear_cache(self):
        """Clear all caches for memory management"""
        self.engine._concept_cache.clear()
        gc.collect()

# Sample Data and Usage
def create_sample_data():
    """Create sample chunks and user context for testing"""
    chunks = [
        {
            'chunk_id': 'doc1_chunk_001',
            'content': 'Machine learning algorithms have revolutionized data analysis by enabling computers to learn patterns from large datasets without explicit programming. These systems use statistical techniques to improve performance on specific tasks through experience.',
            'keywords': ['machine learning', 'algorithms', 'data analysis', 'patterns'],
            'relevance_score': 0.92,
            'source': 'ML_Fundamentals_2024.pdf',
            'source_confidence': 0.95
        },
        {
            'chunk_id': 'doc2_chunk_015',
            'content': 'Neural networks are computing systems inspired by biological neural networks. They consist of interconnected nodes that process information.',
            'keywords': ['neural networks', 'computing', 'nodes'],
            'relevance_score': 0.78,
            'source': 'Neural_Networks_Guide.pdf',
            'source_confidence': 0.88
        },
        {
            'chunk_id': 'doc3_chunk_007',
            'content': 'AI research continues to advance rapidly.',
            'keywords': ['AI', 'research'],
            'relevance_score': 0.45,
            'source': 'AI_News_2024.txt',
            'source_confidence': 0.60
        }
    ]

    user_context = {
        'user_level': 'intermediate',
        'preferred_format': 'detailed',
        'focus_areas': ['machine learning', 'practical applications']
    }

    return chunks, user_context

# Main execution for Replit shell
if __name__ == "__main__":
    print("🚀 Starting Integrated Explanation System")
    print("=" * 60)

    # Create system instance
    system = IntegratedSystem()

    # Get sample data
    chunks, user_context = create_sample_data()

    print(f"📊 Input: {len(chunks)} chunks loaded")
    print(f"👤 User context: {user_context['user_level']} level")
    print("-" * 60)

    # Test all three formats
    formats = ['detailed', 'concise', 'technical']

    for format_type in formats:
        print(f"\n🎯 FORMAT: {format_type.upper()}")
        print("=" * 60)

        # Process through complete pipeline
        response = system.process_query(chunks, user_context, format_type)

        # Display result
        output = system.generator.to_plain_text(response)
        print(output)

        print(f"\n📈 Metadata: {response['metadata']}")
        print("-" * 60)

    # Clean up
    system.clear_cache()
    print("\n✅ System test complete! Memory cleared.")

    print("\n💡 Usage in your code:")
    print("system = IntegratedSystem()")
    print("response = system.process_query(your_chunks, your_context, 'detailed')")
    print("print(system.generator.to_plain_text(response))")