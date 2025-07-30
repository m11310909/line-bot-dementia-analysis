import json
from typing import List, Dict, Any
from datetime import datetime

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
                for source in sources[:2]:  # Limit to 2 sources for memory
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

    def to_json(self, response: Dict[str, Any]) -> str:
        """Convert response to JSON for API usage"""
        return json.dumps(response, indent=2, ensure_ascii=False)

    def to_plain_text(self, response: Dict[str, Any]) -> str:
        """Convert response to plain text"""
        content = response.get('content', '')
        metadata = response.get('metadata', {})

        footer = f"\n\nSummary: {metadata.get('processing_summary', 'No summary')}"
        if metadata.get('average_confidence'):
            footer += f" | Avg Confidence: {metadata['average_confidence']}"

        return content + footer

# Usage optimized for Replit shell execution
if __name__ == "__main__":
    # Test with mock explanations
    generator = ResponseGenerator(max_explanations=3)

    mock_explanations = [
        {
            'chunk_id': 'chunk_001',
            'reasoning_chain': ['Content analyzed', 'Keywords extracted', 'Relevance scored'],
            'confidence_breakdown': {'overall_confidence': 0.85, 'factors': ['high_relevance']},
            'evidence_sources': [{'reference': 'source_1.pdf', 'confidence': 0.9}],
            'related_concepts': ['AI', 'machine learning', 'NLP']
        },
        {
            'chunk_id': 'chunk_002',
            'reasoning_chain': ['Brief content processed', 'Partial match found'],
            'confidence_breakdown': {'overall_confidence': 0.65, 'factors': ['partial_match']},
            'evidence_sources': [{'reference': 'source_2.txt', 'confidence': 0.7}],
            'related_concepts': ['data analysis']
        }
    ]

    # Test different formats
    formats = ['detailed', 'concise', 'technical']

    for format_type in formats:
        print(f"\n{'='*50}")
        print(f"FORMAT: {format_type.upper()}")
        print('='*50)

        response = generator.format_response(mock_explanations, format_type=format_type)
        print(generator.to_plain_text(response))

        # Show metadata
        print(f"\nMetadata: {response['metadata']}")

    print("\n" + "="*50)
    print("ResponseGenerator testing complete!")