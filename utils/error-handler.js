class ErrorHandler {
  static handleAITimeout(userInput) {
    return {
      type: 'bubble',
      body: {
        type: 'box',
        layout: 'vertical',
        contents: [
          {
            type: 'text',
            text: '⏰ 分析處理中...',
            weight: 'bold',
            color: '#FF6B35'
          },
          {
            type: 'text',
            text: '正在為您提供基礎建議',
            size: 'sm',
            wrap: true
          }
        ]
      },
      footer: {
        type: 'box',
        layout: 'vertical',
        contents: [
          {
            type: 'button',
            action: {
              type: 'postback',
              label: '查看常見症狀',
              data: 'action=common_symptoms'
            }
          }
        ]
      }
    };
  }

  static handleJSONParseError(templateId, error) {
    console.error(`JSON Template Error [${templateId}]:`, error);
    return {
      type: 'bubble',
      body: {
        type: 'box',
        layout: 'vertical',
        contents: [
          {
            type: 'text',
            text: '系統暫時忙碌中',
            weight: 'bold'
          },
          {
            type: 'text',
            text: '請稍後再試或聯繫客服',
            size: 'sm'
          }
        ]
      }
    };
  }
}