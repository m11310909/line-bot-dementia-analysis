// tests/flex-message.test.js
const FlexMessageService = require('../utils/flex-generator');

describe('FlexMessageService', () => {
  let service;

  beforeEach(() => {
    service = new FlexMessageService();
  });

  test('should generate M2 message for early stage', () => {
    const result = service.generateM2Message({ stage: 'early' });
    expect(result.contents[0].header.contents[0].text).toBe('早期階段');
    expect(result.contents[0].header.backgroundColor).toBe('#F0F8F0');
  });

  test('should handle BPSD emotional symptoms', () => {
    const result = service.generateM3Message({ bpsdType: 'emotional' });
    expect(result.header.contents[1].text).toBe('情緒型症狀');
  });
});