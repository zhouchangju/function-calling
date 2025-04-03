def get_current_weather(location, unit="摄氏度"):
    """
    模拟获取指定地点的天气情况
    
    Args:
        location: 地点名称，如北京
        unit: 温度单位，默认为摄氏度
    
    Returns:
        包含天气信息的字典
    """
    # 这里应该是实际调用天气API的代码
    # 为了演示，返回模拟数据
    weather_data = {
        "location": location,
        "temperature": "23" if unit == "摄氏度" else "73.4",
        "unit": unit,
        "forecast": ["晴朗", "多云"],
        "humidity": "60%"
    }
    return weather_data

def get_weather_tool_definition():
    """返回天气工具的定义"""
    return {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "获取给定地点的天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "地点的位置信息，比如北京"
                    },
                    "unit": {
                        "type": "string",
                        "enum": [
                            "摄氏度",
                            "华氏度"
                        ]
                    }
                },
                "required": [
                    "location"
                ]
            }
        }
    } 