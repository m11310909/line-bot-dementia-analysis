from typing import Dict, Any, List

class FlexBuilder:
    def __init__(self):
        self.message = {
            "type": "flex",
            "altText": "",
            "contents": {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": []
                }
            }
        }
    
    def set_alt_text(self, text: str):
        self.message["altText"] = text
        return self
    
    def add_header(self, title: str, subtitle: str = None):
        header = {
            "type": "text",
            "text": title,
            "weight": "bold",
            "size": "xl",
            "color": "#1DB446"
        }
        self.message["contents"]["body"]["contents"].append(header)
        
        if subtitle:
            subtitle_element = {
                "type": "text", 
                "text": subtitle,
                "size": "sm",
                "color": "#666666",
                "margin": "md"
            }
            self.message["contents"]["body"]["contents"].append(subtitle_element)
        
        # 分隔線
        separator = {
            "type": "separator",
            "margin": "xl"
        }
        self.message["contents"]["body"]["contents"].append(separator)
        return self
    
    def add_text_section(self, title: str, content: str, color: str = "#333333"):
        section = {
            "type": "box",
            "layout": "vertical", 
            "margin": "lg",
            "contents": [
                {
                    "type": "text",
                    "text": title,
                    "weight": "bold",
                    "color": "#1DB446",
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": content,
                    "wrap": True,
                    "color": color,
                    "size": "sm",
                    "margin": "sm"
                }
            ]
        }
        self.message["contents"]["body"]["contents"].append(section)
        return self
    
    def add_recommendations(self, recommendations: List[str]):
        if not recommendations:
            return self
            
        rec_contents = []
        for i, rec in enumerate(recommendations[:3]):  # 限制3個建議
            rec_contents.append({
                "type": "text",
                "text": f"{i+1}. {rec}",
                "wrap": True,
                "size": "sm",
                "color": "#333333",
                "margin": "sm"
            })
        
        section = {
            "type": "box",
            "layout": "vertical",
            "margin": "lg", 
            "contents": [
                {
                    "type": "text",
                    "text": "💡 建議事項",
                    "weight": "bold",
                    "color": "#1DB446",
                    "margin": "md"
                }
            ] + rec_contents
        }
        self.message["contents"]["body"]["contents"].append(section)
        return self
    
    def add_footer(self):
        footer = {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "contents": [
                {
                    "type": "separator",
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": "⚠️ 此分析僅供參考，如有疑慮請諮詢專業醫師",
                    "wrap": True,
                    "color": "#888888",
                    "size": "xs",
                    "margin": "md"
                }
            ]
        }
        self.message["contents"]["body"]["contents"].append(footer)
        return self
    
    def build(self) -> Dict[str, Any]:
        return self.message
