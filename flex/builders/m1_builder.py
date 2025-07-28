from flex.builders.base_builder import FlexBuilder
from api.modules.base_analyzer import AnalysisResult

class M1FlexBuilder(FlexBuilder):
    def build_analysis_result(self, result: AnalysisResult) -> dict:
        # 設定替代文字
        self.set_alt_text(f"失智症警訊分析：{result.category_name}")
        
        # 標題
        confidence_text = f"可信度: {result.confidence:.0%}"
        self.add_header("🧠 失智症警訊分析", confidence_text)
        
        # 用戶描述
        if result.user_description:
            self.add_text_section(
                "🔸 描述內容", 
                result.user_description
            )
        
        # 分析結果
        if result.category_name:
            severity_emoji = ["", "🟢", "🟡", "🟠", "🔴", "🔴"][min(result.severity, 5)]
            self.add_text_section(
                f"{severity_emoji} 警訊類別",
                f"{result.category_name}\n({', '.join(result.matched_categories)})"
            )
        
        # 正常老化對比
        if result.normal_aging:
            self.add_text_section(
                "✅ 正常老化", 
                result.normal_aging,
                "#2E7D32"
            )
        
        # 警訊說明
        if result.warning_sign:
            color = "#E65100" if result.require_medical_attention else "#F57C00"
            self.add_text_section(
                "⚠️ 警訊特徵",
                result.warning_sign,
                color
            )
        
        # 建議事項
        self.add_recommendations(result.recommendations)
        
        # 就醫提醒
        if result.require_medical_attention:
            self.add_text_section(
                "🏥 重要提醒",
                "建議盡快諮詢神經內科或精神科醫師進行詳細評估",
                "#D32F2F"
            )
        
        # 免責聲明
        self.add_footer()
        
        return self.build()
    
    def build_help_message(self) -> dict:
        self.set_alt_text("失智症分析系統使用說明")
        self.add_header("🤖 失智症分析助手", "使用說明")
        
        self.add_text_section(
            "📝 如何使用",
            "直接描述觀察到的行為或症狀，例如：\n• 媽媽最近常重複問同樣的問題\n• 爸爸忘記回家的路\n• 奶奶不會用原本熟悉的家電"
        )
        
        self.add_text_section(
            "🎯 分析範圍", 
            "本系統分析失智症十大警訊：\n• 記憶力問題\n• 計劃與解決問題困難\n• 熟悉事務執行困難\n• 時間地點混淆\n• 視覺空間問題等"
        )
        
        self.add_recommendations([
            "詳細描述具體行為更有助於分析",
            "持續記錄觀察到的變化", 
            "分析結果僅供參考，請諮詢專業醫師"
        ])
        
        self.add_footer()
        return self.build()
