def calculate(operation, x, y):
    """
    执行基本的数学运算
    
    Args:
        operation: 运算类型，可选值为 "加"、"减"、"乘"、"除"
        x: 第一个数值
        y: 第二个数值
    
    Returns:
        计算结果
    """
    x, y = float(x), float(y)
    if operation == "加":
        result = x + y
    elif operation == "减":
        result = x - y
    elif operation == "乘":
        result = x * y
    elif operation == "除":
        if y == 0:
            return {"error": "除数不能为零"}
        result = x / y
    else:
        return {"error": f"不支持的运算: {operation}"}
    
    return {
        "operation": operation,
        "x": x,
        "y": y,
        "result": result
    }

def get_calculator_tool_definition():
    """返回计算器工具的定义"""
    return {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "执行基本的数学运算，如加、减、乘、除",
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": ["加", "减", "乘", "除"],
                        "description": "要执行的数学运算"
                    },
                    "x": {
                        "type": "number",
                        "description": "第一个数值"
                    },
                    "y": {
                        "type": "number",
                        "description": "第二个数值"
                    }
                },
                "required": ["operation", "x", "y"]
            }
        }
    } 