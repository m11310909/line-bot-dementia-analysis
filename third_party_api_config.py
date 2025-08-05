#!/usr/bin/env python3
"""
Third-Party API Configuration
Different API configurations for testing
"""

# OpenAI API Configuration
OPENAI_CONFIG = {
    'url': 'https://api.openai.com/v1/chat/completions',
    'headers': {
        'Authorization': 'Bearer {api_key}',
        'Content-Type': 'application/json'
    },
    'data_template': {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {
                'role': 'system',
                'content': 'You are a helpful assistant. Answer in Traditional Chinese.'
            },
            {
                'role': 'user',
                'content': '{user_message}'
            }
        ],
        'max_tokens': 500,
        'temperature': 0.7
    }
}

# Google Gemini API Configuration
GEMINI_CONFIG = {
    'url': 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent',
    'headers': {
        'Content-Type': 'application/json'
    },
    'data_template': {
        'contents': [
            {
                'parts': [
                    {
                        'text': 'You are a helpful assistant. Answer in Traditional Chinese. User question: {user_message}'
                    }
                ]
            }
        ],
        'generationConfig': {
            'temperature': 0.7,
            'maxOutputTokens': 500
        }
    }
}

# Custom API Configuration (for your specific API)
CUSTOM_API_CONFIG = {
    'url': 'https://your-api-endpoint.com/chat',
    'headers': {
        'Authorization': 'Bearer {api_key}',
        'Content-Type': 'application/json'
    },
    'data_template': {
        'message': '{user_message}',
        'language': 'zh-TW',
        'max_length': 500
    }
}

# Response parsing functions for different APIs
def parse_openai_response(response_data):
    """Parse OpenAI API response"""
    try:
        return response_data['choices'][0]['message']['content']
    except (KeyError, IndexError) as e:
        raise Exception(f"Invalid OpenAI response format: {e}")

def parse_gemini_response(response_data):
    """Parse Google Gemini API response"""
    try:
        return response_data['candidates'][0]['content']['parts'][0]['text']
    except (KeyError, IndexError) as e:
        raise Exception(f"Invalid Gemini response format: {e}")

def parse_custom_response(response_data):
    """Parse custom API response"""
    try:
        return response_data.get('response', response_data.get('message', str(response_data)))
    except Exception as e:
        raise Exception(f"Invalid custom API response format: {e}")

# API configurations mapping
API_CONFIGS = {
    'openai': {
        'config': OPENAI_CONFIG,
        'parser': parse_openai_response
    },
    'gemini': {
        'config': GEMINI_CONFIG,
        'parser': parse_gemini_response
    },
    'custom': {
        'config': CUSTOM_API_CONFIG,
        'parser': parse_custom_response
    }
} 