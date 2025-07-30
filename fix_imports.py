with open('enhanced_m1_m2_m3_integrated_api.py', 'r') as f:
    content = f.read()

# 修復 import
content = content.replace(
    "from linebot.v3.messaging.models import FlexMessage, BubbleContainer, BoxComponent, TextComponent, ButtonComponent, MessageAction",
    """from linebot.models import (
    FlexSendMessage,
    BubbleContainer,
    BoxComponent,
    TextComponent,
    ButtonComponent,
    MessageAction,
    SeparatorComponent,
    SpacerComponent
)"""
)

# 修復 FlexMessage
content = content.replace('FlexMessage(', 'FlexSendMessage(')

with open('enhanced_m1_m2_m3_integrated_api.py', 'w') as f:
    f.write(content)

print("✅ 修復完成！")
