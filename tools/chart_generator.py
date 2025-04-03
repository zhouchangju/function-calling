#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
from utils.model_utils import call_model, extract_json_from_response

def read_prompt_file():
    """读取chart_with_insight.md文件内容"""
    # 尝试多种可能的路径
    possible_paths = [
        # 相对于当前文件的路径
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompts", "chart_with_insight.md"),
    ]
    
    for path in possible_paths:
        try:
            print(f"尝试读取文件: {path}")
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    print(f"成功读取文件: {path}")
                    return content
        except Exception as e:
            print(f"尝试路径 {path} 出错: {str(e)}")
    
    # 如果所有路径都失败，则抛出异常
    raise FileNotFoundError("无法找到chart_with_insight.md文件，请确保文件存在并检查路径")

def generate_chart_with_insight(table_data, user_query, change_vis_num=1):
    """
    分析表格数据并根据用户查询生成可视化建议和洞察
    
    Args:
        table_data: 包含表格数据的对象数组
        user_query: 用户的问题或陈述，表明可视化意图（趋势、比较、分布等）
        change_vis_num: 生成的图表建议数量，默认为1
    
    Returns:
        包含推荐图表参数和基于数据分析的洞察的JSON对象
    """
    # 读取提示文件内容
    prompt_content = read_prompt_file()
    
    # 组合提示模板和输入参数
    # 替换模板中的变量
    prompt_content = prompt_content.replace("${data}", json.dumps(table_data, ensure_ascii=False))
    prompt_content = prompt_content.replace("${query}", user_query)
    prompt_content = prompt_content.replace("${change_vis_num}", str(change_vis_num))
    combined_prompt = f"""
{prompt_content}
"""
    print("combined_prompt", combined_prompt)

    try:
        # 使用公共函数调用模型
        completion = call_model(prompt=combined_prompt)
        response = completion.choices[0].message.content
        
        # 使用公共函数解析JSON响应
        result = extract_json_from_response(response)
        if result:
            return result
        else:
            return {
                "parameter": [],
                "insight": [],
                "error": "无法解析模型响应"
            }
            
    except Exception as e:
        print(f"调用模型时出错: {str(e)}")
        return {
            "parameter": [],
            "insight": [],
            "error": str(e)
        }

def get_chart_generator_tool_definition():
    """返回图表生成工具的定义"""
    return {
        "type": "function",
        "function": {
            "name": "generate_chart_with_insight",
            "description": "分析表格数据并生成可视化建议和洞察。该工具充当财务分析师，专业地生成和解释财务数据可视化。",
            "parameters": {
                "type": "object",
                "properties": {
                    "table_data": {
                        "type": "array",
                        "description": "包含要分析的表格数据的对象数组。"
                    },
                    "user_query": {
                        "type": "string",
                        "description": "用户的问题或陈述，表明可视化意图（趋势、比较、分布等）。"
                    },
                    "change_vis_num": {
                        "type": "integer",
                        "description": "生成的图表建议数量。",
                        "default": 1
                    }
                },
                "required": ["table_data", "user_query"]
            }
        }
    } 