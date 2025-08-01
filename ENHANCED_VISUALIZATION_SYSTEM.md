# 🎨 Enhanced M1-M4 Visualization System

## 📋 Overview

This document describes the redesigned M1-M4 visualization system that perfectly adapts to LINE Flex Message and LIFF requirements. The system implements a sophisticated design system with senior-friendly typography, progressive information disclosure, and seamless Flex → LIFF transitions.

## 🎯 Design System

### Color System
```scss
// Primary Actions
$primary-blue: #2196F3;
$primary-green: #4CAF50;
$primary-orange: #FF9800;
$primary-red: #F44336;

// Confidence Levels
$confidence-high: #4CAF50;
$confidence-medium: #2196F3;
$confidence-low: #FF9800;

// Background Colors
$bg-card: #FFFFFF;
$bg-subtle: #F8F9FA;
$bg-section: #F5F5F5;
```

### Typography (Optimized for Seniors)
```scss
// Size Scale
$text-xs: 13px;   // Minimum readable
$text-sm: 15px;   // Secondary info
$text-base: 17px; // Body text
$text-lg: 19px;   // Subheadings
$text-xl: 21px;   // Headings
```

## 📱 Module Designs

### M1: 十大警訊比對卡 (Warning Signs Comparison)

**Key Features:**
- AI confidence indicator with visual progress bar
- Side-by-side comparison cards (正常老化 vs 失智警訊)
- Color-coded confidence levels
- Timestamp and analysis metadata

**Design Elements:**
- Header with AI analysis branding
- Confidence progress bar (85% high confidence)
- Comparison cards with icons and descriptions
- Footer with LIFF integration button

**Sample Output:**
```json
{
  "type": "bubble",
  "size": "mega",
  "header": {
    "type": "box",
    "layout": "vertical",
    "backgroundColor": "#F8F9FA",
    "paddingAll": "16px",
    "contents": [
      {
        "type": "text",
        "text": "AI 智慧分析",
        "size": "sm",
        "color": "#666666"
      },
      {
        "type": "text",
        "text": "記憶力評估分析",
        "size": "xl",
        "weight": "bold",
        "color": "#212121"
      }
    ]
  }
}
```

### M2: 病程階段對照 (Progression Matrix)

**Key Features:**
- Visual stage progress indicator
- Color-coded stage information
- Stage-specific descriptions and recommendations
- Progress percentage display

**Design Elements:**
- Stage dots with connecting lines
- Stage-specific color coding
- Detailed stage descriptions
- Care recommendation buttons

**Stage Information:**
- **Early Stage**: Green theme, mild symptoms
- **Middle Stage**: Orange theme, moderate symptoms
- **Late Stage**: Red theme, severe symptoms

### M3: BPSD 症狀分類 (BPSD Classification)

**Key Features:**
- Symptom categorization grid
- Confidence badges for each symptom
- Color-coded symptom categories
- Category-based organization

**Symptom Categories:**
- **躁動不安** (Agitation): Red theme
- **憂鬱情緒** (Depression): Blue theme
- **幻覺症狀** (Hallucination): Purple theme
- **妄想症狀** (Delusion): Orange theme

**Design Elements:**
- Grid layout with category cards
- Confidence percentage badges
- Category-specific color coding
- Symptom descriptions

### M4: 任務導航儀表板 (Care Navigation Dashboard)

**Key Features:**
- Priority-based task organization
- Task icons and descriptions
- Priority color coding
- Action buttons for each task

**Priority Levels:**
- **High Priority**: Red theme, immediate attention needed
- **Medium Priority**: Orange theme, moderate urgency
- **Low Priority**: Green theme, routine tasks

**Design Elements:**
- Task cards with icons
- Priority-based color coding
- Task descriptions and categories
- Action buttons for LIFF integration

## 🔧 Implementation

### Core Components

#### 1. EnhancedFlexMessageGenerator
```python
class EnhancedFlexMessageGenerator:
    def __init__(self):
        self.design = DesignSystem()
    
    def create_m1_warning_signs_card(self, result: AnalysisResult) -> Dict:
        """M1: 十大警訊比對卡 (重新設計)"""
    
    def create_m2_progression_matrix(self, result: AnalysisResult) -> Dict:
        """M2: 病程階段對照"""
    
    def create_m3_bpsd_classification(self, result: AnalysisResult) -> Dict:
        """M3: BPSD 症狀分類"""
    
    def create_m4_care_navigation(self, result: AnalysisResult) -> Dict:
        """M4: 任務導航儀表板"""
```

#### 2. AnalysisResult Data Structure
```python
@dataclass
class AnalysisResult:
    module: str
    confidence: float
    matched_items: List[Dict]
    summary: str
    timestamp: datetime
    user_input: str
```

#### 3. Design System Constants
```python
class DesignSystem:
    # Color System
    PRIMARY_BLUE = "#2196F3"
    PRIMARY_GREEN = "#4CAF50"
    PRIMARY_ORANGE = "#FF9800"
    PRIMARY_RED = "#F44336"
    
    # Confidence Colors
    CONFIDENCE_HIGH = "#4CAF50"
    CONFIDENCE_MEDIUM = "#2196F3"
    CONFIDENCE_LOW = "#FF9800"
```

### API Integration

#### Enhanced API Endpoints
```python
@app.post("/analyze/{module_name}")
async def analyze_single_module(module_name: str, request: UserInput):
    """Single module analysis endpoint"""

@app.post("/flex/{module_name}")
async def get_flex_message(module_name: str, request: UserInput):
    """Get enhanced flex message for specific module"""

@app.get("/design-system")
async def get_design_system():
    """Get design system information"""
```

## 📊 Test Results

### Performance Metrics
- **M1 Flex Message**: 2,684 bytes
- **M2 Flex Message**: 2,652 bytes
- **M3 Flex Message**: 3,032 bytes
- **M4 Flex Message**: 4,393 bytes

### Confidence Levels
- **High Confidence** (≥75%): Green theme, reliable analysis
- **Medium Confidence** (50-74%): Blue theme, moderate reliability
- **Low Confidence** (<50%): Orange theme, requires human review

### Sample Data Results
```
✅ M1: 85% confidence, 2 matched items
✅ M2: 78% confidence, middle stage (65% progress)
✅ M3: 82% confidence, 3 symptoms across 3 categories
✅ M4: 75% confidence, 4 tasks (2 high, 2 medium priority)
```

## 🚀 Usage Examples

### 1. Generate M1 Flex Message
```python
from enhanced_flex_message_generator import create_enhanced_flex_message, AnalysisResult

# Create analysis result
result = AnalysisResult(
    module="M1",
    confidence=0.85,
    matched_items=[...],
    summary="檢測到記憶力減退症狀",
    timestamp=datetime.now(),
    user_input="我媽媽最近常常忘記事情"
)

# Generate flex message
flex_message = create_enhanced_flex_message("M1", result)
```

### 2. API Integration
```python
import requests

# Test flex message generation
response = requests.post(
    "http://localhost:8006/flex/M1",
    json={"text": "我媽媽最近記憶力變差"}
)

flex_message = response.json()
```

### 3. Comprehensive Analysis
```python
# Analyze with all modules
response = requests.post(
    "http://localhost:8006/analyze",
    json={
        "user_input": "我媽媽最近記憶力變差，情緒不穩定",
        "modules": ["M1", "M2", "M3", "M4"]
    }
)
```

## 🎨 Design Patterns

### 1. Confidence Indicator Pattern
```javascript
const confidenceDisplay = {
  high: {
    color: '#4CAF50',
    label: '高信心度',
    minValue: 75
  },
  medium: {
    color: '#2196F3',
    label: '中信心度',
    minValue: 50
  },
  low: {
    color: '#FF9800',
    label: '需人工確認',
    minValue: 0
  }
};
```

### 2. Progressive Disclosure Pattern
```javascript
const detailLevels = {
  summary: {
    // Flex Message View
    showConfidence: true,
    showComparison: true,
    showDetails: false
  },
  expanded: {
    // LIFF Initial View
    showConfidence: true,
    showComparison: true,
    showDetails: true,
    showReasoning: false
  },
  expert: {
    // LIFF Expert Mode
    showAll: true
  }
};
```

## 📱 LINE Integration

### Flex Message Constraints
- **Max bubble size**: 10KB
- **No JavaScript execution**: Static content only
- **Limited interactions**: URI actions only

### LIFF Optimizations
- **Lazy loading**: Detailed explanations loaded on demand
- **Skeleton screens**: Loading states during data fetch
- **Caching**: Frequently accessed data cached locally

### Accessibility Enhancements
- **Touch targets**: All interactive elements ≥ 44px
- **Color contrast**: Ratio ≥ 4.5:1 for readability
- **Focus indicators**: Clear visual feedback
- **Voice-over friendly**: Proper labels and descriptions

## 🔄 Migration Guide

### From Old System to Enhanced System

1. **Update Imports**
```python
# Old
from flex_message_generator import create_flex_message

# New
from enhanced_flex_message_generator import create_enhanced_flex_message
```

2. **Update Data Structure**
```python
# Old
result = {
    "confidence": 0.85,
    "matched_items": [...],
    "summary": "..."
}

# New
result = AnalysisResult(
    module="M1",
    confidence=0.85,
    matched_items=[...],
    summary="...",
    timestamp=datetime.now(),
    user_input="..."
)
```

3. **Update API Calls**
```python
# Old
response = requests.post("http://localhost:8000/analyze", json=data)

# New
response = requests.post("http://localhost:8006/analyze", json=data)
```

## 🧪 Testing

### Run Test Suite
```bash
python3 test_enhanced_visualization.py
```

### Expected Output
```
🎨 Enhanced M1-M4 Visualization System Test
============================================================
✅ All modules tested successfully
✅ Enhanced flex messages generated
✅ Sample files saved
```

### Generated Files
- `m1_warning_signs.json`: M1 flex message sample
- `m2_progression_matrix.json`: M2 flex message sample
- `m3_bpsd_classification.json`: M3 flex message sample
- `m4_care_navigation.json`: M4 flex message sample
- `enhanced_visualization_samples.json`: Combined samples

## 🚀 Deployment

### 1. Start Enhanced API
```bash
python3 enhanced_m1_m2_m3_m4_integrated_api.py
```

### 2. Update LINE Bot Webhook
```python
# Update webhook to use enhanced API
ENHANCED_API_URL = "http://localhost:8006"
```

### 3. Test Integration
```bash
curl -X POST http://localhost:8006/flex/M1 \
  -H "Content-Type: application/json" \
  -d '{"text": "我媽媽最近記憶力變差"}'
```

## 📈 Future Enhancements

### Planned Features
1. **Dynamic LIFF URLs**: Real-time LIFF URL generation
2. **Advanced Analytics**: Usage tracking and performance metrics
3. **Custom Themes**: User-configurable color schemes
4. **Multi-language Support**: Internationalization support
5. **Offline Mode**: Cached responses for offline use

### Performance Optimizations
1. **Message Caching**: Cache frequently requested flex messages
2. **Image Optimization**: Compress and optimize embedded images
3. **CDN Integration**: Distribute static assets globally
4. **Database Integration**: Store analysis results for history

## 📞 Support

### Documentation
- **API Reference**: `/docs` endpoint for interactive API documentation
- **Design System**: `/design-system` endpoint for design specifications
- **Health Check**: `/health` endpoint for system status

### Troubleshooting
1. **API Connection Issues**: Check if enhanced API is running on port 8006
2. **Flex Message Errors**: Verify JSON structure and size limits
3. **Module Errors**: Check individual module status via `/modules/{module}/status`
4. **Design Issues**: Validate against design system specifications

---

**Version**: 2.0.0  
**Last Updated**: 2025-08-01  
**Status**: ✅ Production Ready 