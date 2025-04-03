#!/usr/bin/env python
# -*- coding: utf-8 -*-

from volcenginesdkarkruntime import Ark
import os
import json

def init_client():
    """初始化API客户端"""
    api_key = os.environ.get("ARK_API_KEY")
    if not api_key:
        raise ValueError("环境变量ARK_API_KEY未设置")
    
    return Ark(api_key=api_key)

def call_model(prompt=None, model_name="deepseek-v3-250324", tools=None, messages=None):
    """调用模型并获取响应
    
    Args:
        prompt (str, optional): 提示内容，若提供则会被转换为单条用户消息
        model_name (str): 模型名称，默认为"deepseek-v3-250324"
        tools (list): 工具定义列表，默认为None
        messages (list): 消息列表，优先级高于prompt
    
    Returns:
        模型响应对象
    """
    client = init_client()
    
    kwargs = {
        "model": model_name,
    }
    
    # 优先使用messages参数，如果没有提供则使用prompt构建单条消息
    if messages:
        kwargs["messages"] = messages
    elif prompt:
        kwargs["messages"] = [{"role": "user", "content": prompt}]
    else:
        raise ValueError("必须提供prompt或messages参数之一")
    
    if tools:
        kwargs["tools"] = tools
    
    try:
        return client.chat.completions.create(**kwargs)
    except Exception as e:
        print(f"调用模型时出错: {str(e)}")
        raise

def extract_json_from_response(response):
    """从模型响应中提取JSON
    
    Args:
        response (str): 模型响应文本
    
    Returns:
        解析后的JSON对象，如果解析失败则返回None
    """
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        # 如果响应不是有效的JSON，尝试提取JSON部分
        import re
        json_pattern = r'```json\s*([\s\S]*?)\s*```'
        matches = re.findall(json_pattern, response)
        
        if matches:
            try:
                return json.loads(matches[0])
            except json.JSONDecodeError:
                print("无法解析提取的JSON内容")
        
        print("无法从响应中解析JSON")
        return None 