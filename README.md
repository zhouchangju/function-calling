# Function Calling 工具调用示例项目

本项目展示了如何通过大语言模型的function calling功能实现智能工具调用。系统会根据用户输入自动判断需要调用的工具，获取结果后返回最终答复。

项目采用了火山引擎的LLM API，参考：[Function Calling 使用说明](https://www.volcengine.com/docs/82379/1262342)

## 项目特点

- **自动工具选择**：无需手动指定工具类型，模型自动根据用户问题选择最合适的工具
- **模块化设计**：每个工具独立封装，便于扩展和维护
- **多种工具支持**：
  - 天气查询：获取指定地区的天气信息
  - 数学计算：执行基本的加减乘除运算
  - 图表生成：分析数据并生成可视化建议和洞察

## 项目结构

```
/function-calling/
│
├── main.py               # 主程序入口
├── tools/                # 工具模块目录
│   ├── __init__.py       # 工具包初始化文件
│   ├── weather.py        # 天气查询工具
│   ├── calculator.py     # 计算工具
│   └── chart_generator.py # 图表生成工具
└── README.md             # 项目文档
```

## 工具说明

### 1. 天气查询工具

- **功能**：获取指定地点的天气信息
- **参数**：
  - `location`: 地点名称（必填，如"北京"）
  - `unit`: 温度单位（可选，"摄氏度"或"华氏度"）
- **返回**：包含天气信息的JSON对象

### 2. 计算工具

- **功能**：执行基本的数学运算
- **参数**：
  - `operation`: 运算类型（必填，"加"、"减"、"乘"、"除"）
  - `x`: 第一个数值（必填）
  - `y`: 第二个数值（必填）
- **返回**：包含计算结果的JSON对象

### 3. 图表生成工具

- **功能**：分析表格数据并生成可视化建议和洞察
- **参数**：
  - `table_data`: 表格数据数组（必填）
  - `user_query`: 用户查询（必填，指明可视化意图）
  - `change_vis_num`: 图表建议数量（可选，默认为1）
- **返回**：包含图表参数和洞察的JSON对象

## 安装与配置

1. 克隆本项目
2. 安装依赖
   ```bash
   pip install -U 'volcengine-python-sdk[ark]'
   ```
3. 设置环境变量(火山引擎的API密钥)
   ```bash
   export ARK_API_KEY="您的API密钥"
   ```

## 使用方法

### 命令行使用

```bash
# 基本查询（系统自动选择工具）
python main.py --query "杭州今天天气如何？"

# 数学计算查询
python main.py --query "25乘以25等于多少？"

# 带数据文件的图表生成查询
python main.py --query "分析销售趋势" --data data.json

# 贴近真实场景的测试
python main.py --query "从2007年到2016年，公司在AI研发上的支出节节攀升。2007年，研发费用是6.9亿美元 ，到了2016年，已达14.6亿美元，这十年间几乎翻了一倍。" --data data/sale.json
```

### 数据文件格式

用于图表生成的数据文件应为JSON格式，例如：

```json
[
  {"月份": "2023-01", "销售额": 1200, "地区": "华东"},
  {"月份": "2023-02", "销售额": 1500, "地区": "华东"},
  {"月份": "2023-03", "销售额": 1800, "地区": "华东"}
]
```

## 技术实现

系统实现的核心流程：

1. 接收用户查询并解析可能附带的数据
2. 向模型发送查询请求，并提供所有可用工具的定义
3. 模型根据查询内容自动选择合适的工具并提供必要参数
4. 系统解析模型返回的工具调用请求，执行对应的工具函数
5. 将工具执行结果返回给模型进行解析
6. 模型基于工具结果生成最终人类可读的回答
7. 将最终回答显示给用户

## 扩展开发

### 添加新工具

1. 在`tools`目录下创建新的工具文件，如`new_tool.py`
2. 实现工具函数和工具定义函数
3. 在`tools/__init__.py`中导入并导出新工具
4. 在`main.py`中的`tools`列表添加新工具定义
5. 在`handle_tool_calls`函数中添加新工具的处理逻辑

## 使用的技术

- **Python**: 主要开发语言
- **火山引擎API**: 用于访问大语言模型
- **Function Calling**: 模型的工具调用能力

## 注意事项

- 本项目中的天气查询为模拟实现，实际应用中应对接真实天气API
- 图表生成提供的洞察为预设内容，实际应用中应基于数据分析生成
- API密钥应妥善保管，避免泄露或公开在代码中

## 许可证

本项目采用 MIT 许可证 