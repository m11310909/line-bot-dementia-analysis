# Design System Component Guide

## 📋 Component Naming System

### Format: `Category_SubCategory_Property_State`

## 🎨 Component Categories

### Text Components
- **Title Components**: Page and section headings
  - `Title_LG_Bold` - Main page title (20px, bold)
  - `Title_MD_Bold` - Section title (18px, bold)  
  - `Title_SM_Regular` - Subsection title (16px, regular)

- **Body Components**: Content text
  - `Body_LG_Regular` - Large content (18px)
  - `Body_MD_Regular` - Standard content (18px)
  - `Body_SM_Light` - Small content (16px, light)

- **Caption Components**: Secondary text
  - `Caption_XS_Gray` - General captions (#6C757D)
  - `Caption_XS_Blue` - Info captions (#007BFF)
  - `Caption_XS_Red` - Alert captions (#DC3545)

### Icon Components
- **Alert Icons**: Warning and error states
  - `Alert_Icon_Red` - Error/danger (20×20px)
  - `Alert_Icon_Yellow` - Warning/caution (20×20px)

- **Stage Icons**: Process and status
  - `Stage_Icon_Blue` - Current stage (#007BFF)
  - `Stage_Icon_Green` - Completed stage (#28A745)

- **Support Icons**: Help and resources
  - `Support_Icon_Green` - Positive support (#28A745)
  - `Support_Icon_Purple` - Resource/info (#6F42C1)

### Container Components
- **Bubble Containers**: MESSAGE-style containers
  - `Bubble_Container_Basic` - Standard message bubble
  - `Bubble_Container_Hero` - Featured content bubble
  - `Bubble_Container_Footer` - Bottom action bubble

- **Card Containers**: Content cards
  - `Card_Container_Default` - Standard state
  - `Card_Container_Hover` - Interactive state
  - `Card_Container_Selected` - Active state

- **List Components**: Structured content
  - `List_Item_Row_Basic` - Simple list item
  - `List_Item_Row_Icon` - List item with icon
  - `List_Item_Row_Action` - List item with action

### Interactive Components
- **Button Components**: User actions
  - `Button_LG_Primary` - Main action (56px min-height)
  - `Button_MD_Secondary` - Secondary action (48px min-height)
  - `Button_SM_Text` - Tertiary/text action

- **Quick Reply**: Rapid responses
  - `Quick_Reply_Text` - Text-based quick reply
  - `Quick_Reply_Icon` - Icon-based quick reply

## 🎯 Usage Guidelines

### 1. Typography Hierarchy
```
H1: Title_LG_Bold (Page main title only)
H2: Title_MD_Bold (Module titles)
H3: Title_SM_Regular (Subsections)
Body: Body_MD_Regular (General content)
Caption: Caption_XS_Gray (Supplementary info)
```

### 2. Color Semantics
- 🔴 **Red**: Alerts, errors, immediate attention
- 🟢 **Green**: Success, recommendations, positive actions
- 🔵 **Blue**: Information, links, neutral prompts
- 🟡 **Yellow**: Caution, transitional states

### 3. Accessibility Standards
- **Font Size**: Minimum 16px for 60+ users
- **Line Height**: 1.6 for readability
- **Color Contrast**: WCAG AA (4.5:1 minimum)
- **Touch Targets**: 48px minimum for interactive elements

### 4. Responsive Breakpoints
```css
/* Small screens */
@media (max-width: 374px) { font-size: 16px; }

/* Standard mobile */
@media (min-width: 375px) { font-size: 18px; }

/* Large mobile/tablet */
@media (min-width: 768px) { font-size: 20px; }
```

## 🔄 Module Mapping

### M1: Alert Cards
- Components: `Alert_Icon_Red` + `Title_MD_Bold`
- Container: `Card_Container_Default`

### M2: Matrix Tables  
- Components: `Card_Container_Default` + `Body_SM_Regular`
- Icons: `Stage_Icon_Blue` for status

### M3: Category Cards
- Components: `Bubble_Container_Basic` + `List_Item_Row_Icon`
- Actions: `Quick_Reply_Text`

### M4: Task Navigation
- Components: `Stage_Icon_Blue` + `Button_MD_Primary`
- Container: `List_Item_Row_Action`

## 📱 LINE Platform Considerations

### Flex Message Constraints
- **Bubble Max Width**: 400px
- **Icon Standard Size**: 20×20px
- **JSON Structure**: Supports nested components
- **Color Limitations**: Hex codes only

### LIFF Integration
- **Responsive Design**: Mobile-first approach
- **Touch Optimization**: 48px minimum targets
- **Performance**: Lightweight CSS classes
- **Accessibility**: Screen reader compatible

## 🔧 Implementation

### CSS Class Usage
```html
<!-- Title -->
<h1 class="title--lg-bold">Main Title</h1>

<!-- Alert Card -->
<div class="card-container--default">
  <span class="alert-icon--red">⚠️</span>
  <h2 class="title--md-bold">Alert Title</h2>
  <p class="body--md-regular">Alert content</p>
</div>

<!-- Quick Reply -->
<button class="quick-reply--text">Quick Action</button>
```

### JSON Flex Message
```json
{
  "type": "bubble",
  "styles": {
    "body": {
      "backgroundColor": "#F8F9FA"
    }
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "Title",
        "size": "lg",
        "weight": "bold",
        "color": "#212529"
      }
    ]
  }
}
```
