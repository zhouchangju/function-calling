#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import argparse

# 导入工具函数和工具定义
from tools import (
    get_current_weather,
    get_weather_tool_definition,
    calculate,
    get_calculator_tool_definition,
    generate_chart_with_insight,
    get_chart_generator_tool_definition
)

# 导入模型工具函数
from utils.model_utils import init_client, call_model

def process_query(query, data_file=None):
    """处理用户查询，自动选择合适的工具"""
    client = init_client()
    
    # 如果提供了数据文件，则加载数据
    table_data = []
    if data_file:
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                table_data = json.load(f)
            print(f"加载数据文件: {data_file}")
            print(f"数据示例: {json.dumps(table_data[:2], ensure_ascii=False)}... (共{len(table_data)}条)")
            
            # 如果提供了数据，将其添加到查询中
            query = f"{query}\n{json.dumps(table_data, ensure_ascii=False)}"
        except Exception as e:
            print(f"加载数据文件出错: {str(e)}")
    
    print(f"----- 用户查询: {query} -----")
    
    # 提供所有工具定义，让模型自行选择
    tools = [
        get_weather_tool_definition(),
        get_calculator_tool_definition(),
        get_chart_generator_tool_definition()
    ]
    
    # 使用公共函数调用模型
    completion = call_model(query, tools=tools)
    
    return handle_tool_calls(client, completion, query)

def handle_tool_calls(client, completion, query):
    """处理工具调用并返回结果"""
    response = completion.choices[0].message
    print("\n模型初始响应:")
    print(response.content if hasattr(response, 'content') and response.content else "无直接响应内容")
    
    if hasattr(response, 'tool_calls') and response.tool_calls:
        print("\n----- 处理工具调用 -----")
        for tool_call in response.tool_calls:
            tool_name = tool_call.function.name
            print(f"调用工具: {tool_name}")
            
            try:
                args = json.loads(tool_call.function.arguments)
                print(f"工具参数: {json.dumps(args, ensure_ascii=False, indent=2)}")
                
                # 根据工具类型调用相应函数
                if tool_name == "get_current_weather":
                    location = args.get("location")
                    unit = args.get("unit", "摄氏度")
                    result = get_current_weather(location, unit)
                    
                elif tool_name == "calculate":
                    operation = args.get("operation")
                    x = args.get("x")
                    y = args.get("y")
                    result = calculate(operation, x, y)
                    
                elif tool_name == "generate_chart_with_insight":
                    table_data = args.get("table_data", [])
                    user_query = args.get("user_query", "")
                    change_vis_num = args.get("change_vis_num", 1)
                    result = generate_chart_with_insight(table_data, user_query, change_vis_num)
                    
                else:
                    print(f"未知工具: {tool_name}")
                    continue
                
                print(f"工具结果:")
                print(json.dumps(result, ensure_ascii=False, indent=2))
                
                # 将结果返回给模型以获取最终响应
                messages = [
                    {"role": "user", "content": query},
                    response.model_dump(),
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_name,
                        "content": json.dumps(result, ensure_ascii=False)
                    }
                ]
                
                # 继续与模型对话，获取最终回答
                final_response = call_model(messages=messages)
                
                print("\n----- 最终响应 -----")
                print(final_response.choices[0].message.content)
                return final_response.choices[0].message.content
                
            except json.JSONDecodeError:
                print(f"参数解析失败: {tool_call.function.arguments}")
            except Exception as e:
                print(f"处理工具调用时出错: {str(e)}")
    else:
        print("\n模型没有调用工具，直接返回了答案。")
        return response.content if hasattr(response, 'content') else None

def main():
    parser = argparse.ArgumentParser(description='模型工具调用演示程序')
    parser.add_argument('--query', required=True, help='用户查询内容')
    parser.add_argument('--data', help='数据文件路径(用于图表生成等)')
    
    args = parser.parse_args()
    process_query(args.query, args.data)

if __name__ == "__main__":
    main()