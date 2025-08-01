"""
線程安全的枚舉處理工具
解決間歇性枚舉值訪問錯誤
"""
import threading
from enum import Enum
from typing import Any, Union, Optional
import logging

class SafeEnumHandler:
    """線程安全的枚舉處理器"""
    
    def __init__(self):
        self._lock = threading.RLock()
        self.logger = logging.getLogger(__name__)
    
    def safe_get_enum_value(self, enum_obj: Any, default: str = "unknown") -> str:
        """
        線程安全地獲取枚舉值
        
        Args:
            enum_obj: 可能是枚舉對象或字符串
            default: 默認返回值
        
        Returns:
            枚舉的值或默認值
        """
        with self._lock:
            try:
                # 檢查是否為枚舉對象
                if isinstance(enum_obj, Enum):
                    return str(enum_obj.value)
                
                # 檢查是否有 value 屬性
                elif hasattr(enum_obj, 'value'):
                    return str(enum_obj.value)
                
                # 如果是字符串，直接返回
                elif isinstance(enum_obj, str):
                    return enum_obj
                
                # 其他情況轉換為字符串
                else:
                    return str(enum_obj) if enum_obj is not None else default
                    
            except Exception as e:
                self.logger.warning(f"枚舉值獲取失敗: {e}, 使用默認值: {default}")
                return default
    
    def validate_enum_type(self, enum_obj: Any, expected_enum_class: type) -> bool:
        """
        驗證枚舉類型
        
        Args:
            enum_obj: 待驗證的對象
            expected_enum_class: 期望的枚舉類
        
        Returns:
            是否為期望的枚舉類型
        """
        with self._lock:
            try:
                return isinstance(enum_obj, expected_enum_class)
            except Exception:
                return False
    
    def convert_to_enum(self, value: Any, enum_class: type, default: Optional[Enum] = None) -> Optional[Enum]:
        """
        安全地將值轉換為枚舉
        
        Args:
            value: 待轉換的值
            enum_class: 目標枚舉類
            default: 默認枚舉值
        
        Returns:
            枚舉對象或None
        """
        with self._lock:
            try:
                # 如果已經是正確的枚舉類型
                if isinstance(value, enum_class):
                    return value
                
                # 嘗試通過值查找枚舉
                if hasattr(enum_class, '_value2member_map_'):
                    return enum_class._value2member_map_.get(value, default)
                
                # 嘗試通過名稱查找枚舉
                if isinstance(value, str):
                    try:
                        return enum_class[value]
                    except KeyError:
                        pass
                
                return default
                
            except Exception as e:
                self.logger.warning(f"枚舉轉換失敗: {e}")
                return default

# 全局安全枚舉處理器實例
safe_enum_handler = SafeEnumHandler()

# 便捷函數
def safe_enum_value(enum_obj: Any, default: str = "unknown") -> str:
    """獲取枚舉值的便捷函數"""
    return safe_enum_handler.safe_get_enum_value(enum_obj, default)

def safe_enum_convert(value: Any, enum_class: type, default: Optional[Enum] = None) -> Optional[Enum]:
    """轉換為枚舉的便捷函數"""
    return safe_enum_handler.convert_to_enum(value, enum_class, default)

# 裝飾器：自動處理枚舉參數
def handle_enum_params(*enum_params):
    """
    裝飾器：自動處理函數中的枚舉參數
    
    Args:
        enum_params: 需要處理的枚舉參數名稱
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # 處理 kwargs 中的枚舉參數
            for param_name in enum_params:
                if param_name in kwargs:
                    original_value = kwargs[param_name]
                    kwargs[param_name] = safe_enum_value(original_value)
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

# 使用示例
if __name__ == "__main__":
    from enum import Enum
    
    class WarningLevel(Enum):
        LOW = "low"
        MEDIUM = "medium"
        HIGH = "high"
    
    # 測試安全枚舉處理
    test_values = [
        WarningLevel.HIGH,
        "medium",
        None,
        42,
        WarningLevel.LOW
    ]
    
    for value in test_values:
        safe_value = safe_enum_value(value)
        converted_enum = safe_enum_convert(value, WarningLevel, WarningLevel.LOW)
        print(f"原值: {value} -> 安全值: {safe_value} -> 枚舉: {converted_enum}") 