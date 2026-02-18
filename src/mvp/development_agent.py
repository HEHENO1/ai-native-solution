"""
MVP开发Agent实现
基于火山Trae框架的多Agent系统 - 扩展版

功能：根据自然语言描述生成多种编程语言的代码模块，支持15+种常见编程场景
"""

import re
import json
from typing import Dict, List, Optional, Any, Union
from datetime import datetime


class DevelopmentAgent:
    """MVP开发Agent类"""
    
    def __init__(self, agent_id: str = "mvp_dev_agent_001"):
        """初始化开发Agent
        
        Args:
            agent_id: Agent唯一标识符
        """
        self.agent_id = agent_id
        self.code_templates = self._load_code_templates()
        self.supported_patterns = self._get_supported_patterns()
        
    def _load_code_templates(self) -> Dict[str, Dict[str, Any]]:
        """加载多语言代码模板
        
        Returns:
            模板名称到模板内容（含多语言）的映射
        """
        templates = {}
        
        # 1. 计算平均值
        templates["calculate_average"] = {
            "python": """def calculate_average(numbers: list) -> float:
    \"\"\"计算列表中数字的平均值
    
    Args:
        numbers: 数字列表
        
    Returns:
        平均值
    \"\"\"
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)
""",
            "javascript": """function calculateAverage(numbers) {
    // 计算数组中数字的平均值
    if (!numbers || numbers.length === 0) {
        return 0;
    }
    const sum = numbers.reduce((acc, curr) => acc + curr, 0);
    return sum / numbers.length;
}
""",
            "java": """public class AverageCalculator {
    public static double calculateAverage(double[] numbers) {
        // 计算数组中数字的平均值
        if (numbers == null || numbers.length == 0) {
            return 0.0;
        }
        double sum = 0.0;
        for (double num : numbers) {
            sum += num;
        }
        return sum / numbers.length;
    }
}
"""
        }
        
        # 2. 查找最大最小值
        templates["find_max_min"] = {
            "python": """def find_max_min(numbers: list) -> tuple:
    \"\"\"查找列表中的最大值和最小值
    
    Args:
        numbers: 数字列表
        
    Returns:
        (最大值, 最小值)
    \"\"\"
    if not numbers:
        return (None, None)
    return max(numbers), min(numbers)
""",
            "javascript": """function findMaxMin(numbers) {
    // 查找数组中的最大值和最小值
    if (!numbers || numbers.length === 0) {
        return [null, null];
    }
    let max = numbers[0];
    let min = numbers[0];
    for (let i = 1; i < numbers.length; i++) {
        if (numbers[i] > max) max = numbers[i];
        if (numbers[i] < min) min = numbers[i];
    }
    return [max, min];
}
"""
        }
        
        # 3. 过滤偶数
        templates["filter_even_numbers"] = {
            "python": """def filter_even_numbers(numbers: list) -> list:
    \"\"\"过滤列表中的偶数
    
    Args:
        numbers: 数字列表
        
    Returns:
        偶数列表
    \"\"\"
    return [num for num in numbers if num % 2 == 0]
"""
        }
        
        # 4. 字符串反转
        templates["string_reverse"] = {
            "python": """def string_reverse(text: str) -> str:
    \"\"\"反转字符串
    
    Args:
        text: 输入字符串
        
    Returns:
        反转后的字符串
    \"\"\"
    return text[::-1]
""",
            "javascript": """function stringReverse(text) {
    // 反转字符串
    return text.split('').reverse().join('');
}
"""
        }
        
        # 5. 斐波那契数列
        templates["fibonacci_sequence"] = {
            "python": """def fibonacci_sequence(n: int) -> list:
    \"\"\"生成斐波那契数列
    
    Args:
        n: 生成数列的长度
        
    Returns:
        斐波那契数列列表
    \"\"\"
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    sequence = [0, 1]
    for i in range(2, n):
        sequence.append(sequence[i-1] + sequence[i-2])
    return sequence
"""
        }
        
        # 6. 快速排序算法
        templates["quicksort"] = {
            "python": """def quicksort(arr: list) -> list:
    \"\"\"快速排序算法实现
    
    Args:
        arr: 待排序列表
        
    Returns:
        排序后的列表
    \"\"\"
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quicksort(left) + middle + quicksort(right)
"""
        }
        
        # 7. 读取文件内容
        templates["read_file"] = {
            "python": """def read_file(filepath: str) -> str:
    \"\"\"读取文件内容
    
    Args:
        filepath: 文件路径
        
    Returns:
        文件内容字符串
    \"\"\"
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f\"文件 {filepath} 不存在\"
    except Exception as e:
        return f\"读取文件时发生错误: {str(e)}\"
"""
        }
        
        # 8. 发送HTTP GET请求
        templates["http_get"] = {
            "python": """import requests

def http_get(url: str) -> dict:
    \"\"\"发送HTTP GET请求
    
    Args:
        url: 请求URL
        
    Returns:
        响应结果字典
    \"\"\"
    try:
        response = requests.get(url, timeout=10)
        return {
            "status_code": response.status_code,
            "content": response.text[:500] if response.text else "",
            "headers": dict(response.headers)
        }
    except Exception as e:
        return {
            "error": str(e),
            "status_code": None
        }
"""
        }
        
        # 9. 数据库查询
        templates["database_query"] = {
            "python": """import sqlite3

def database_query(db_path: str, query: str) -> list:
    \"\"\"执行数据库查询
    
    Args:
        db_path: 数据库文件路径
        query: SQL查询语句
        
    Returns:
        查询结果列表
    \"\"\"
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception as e:
        return [{"error": str(e)}]
"""
        }
        
        # 10. 正则表达式匹配邮箱
        templates["regex_email"] = {
            "python": """import re

def extract_emails(text: str) -> list:
    \"\"\"从文本中提取邮箱地址
    
    Args:
        text: 输入文本
        
    Returns:
        邮箱地址列表
    \"\"\"
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}'
    return re.findall(email_pattern, text)
"""
        }
        
        # 11. 日期格式化
        templates["date_format"] = {
            "python": """from datetime import datetime

def format_date(date_str: str, input_format: str = "%Y-%m-%d", output_format: str = "%Y年%m月%d日") -> str:
    \"\"\"日期格式化
    
    Args:
        date_str: 日期字符串
        input_format: 输入格式
        output_format: 输出格式
        
    Returns:
        格式化后的日期字符串
    \"\"\"
    try:
        date_obj = datetime.strptime(date_str, input_format)
        return date_obj.strftime(output_format)
    except ValueError:
        return "日期格式错误"
"""
        }
        
        # 12. 生成柱状图
        templates["bar_chart"] = {
            "python": """import matplotlib.pyplot as plt
import numpy as np

def create_bar_chart(data: dict, title: str = "柱状图") -> str:
    \"\"\"生成柱状图
    
    Args:
        data: 数据字典 {标签: 值}
        title: 图表标题
        
    Returns:
        保存的文件路径
    \"\"\"
    try:
        plt.figure(figsize=(10, 6))
        labels = list(data.keys())
        values = list(data.values())
        
        x_pos = np.arange(len(labels))
        plt.bar(x_pos, values, color='skyblue')
        plt.xticks(x_pos, labels, rotation=45)
        plt.title(title)
        plt.tight_layout()
        
        filepath = "bar_chart.png"
        plt.savefig(filepath)
        plt.close()
        return f"图表已保存到: {filepath}"
    except Exception as e:
        return f"生成图表时发生错误: {str(e)}"
"""
        }
        
        # 13. 配置文件解析
        templates["config_parser"] = {
            "python": """import json
import yaml

def parse_config(config_str: str, format_type: str = "json") -> dict:
    \"\"\"解析配置文件
    
    Args:
        config_str: 配置字符串
        format_type: 配置格式 (json, yaml)
        
    Returns:
        配置字典
    \"\"\"
    try:
        if format_type == "json":
            return json.loads(config_str)
        elif format_type == "yaml":
            return yaml.safe_load(config_str)
        else:
            return {"error": f"不支持的格式: {format_type}"}
    except Exception as e:
        return {"error": str(e)}
"""
        }
        
        # 14. 日志记录
        templates["logging_setup"] = {
            "python": """import logging

def setup_logging(log_file: str = "app.log", level: str = "INFO") -> logging.Logger:
    \"\"\"设置日志记录
    
    Args:
        log_file: 日志文件路径
        level: 日志级别
        
    Returns:
        配置好的logger对象
    \"\"\"
    # 转换日志级别
    log_level = getattr(logging, level.upper(), logging.INFO)
    
    # 创建logger
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    
    # 避免重复添加handler
    if not logger.handlers:
        # 文件handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        
        # 控制台handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        
        # 设置格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger
"""
        }
        
        # 15. 错误处理装饰器
        templates["error_handler"] = {
            "python": """def error_handler(default_return=None):
    \"\"\"错误处理装饰器
    
    Args:
        default_return: 发生错误时返回的默认值
        
    Returns:
        装饰器函数
    \"\"\"
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"函数 {func.__name__} 执行出错: {str(e)}")
                return default_return
        return wrapper
    return decorator

# 使用示例
@error_handler(default_return=0)
def divide(a, b):
    return a / b
"""
        }
        
        # 16. 链表实现
        templates["linked_list"] = {
            "python": """class ListNode:
    \"\"\"链表节点类\"\"\"
    def __init__(self, value=0, next_node=None):
        self.value = value
        self.next = next_node

class LinkedList:
    \"\"\"链表实现\"\"\"
    def __init__(self):
        self.head = None
    
    def append(self, value):
        \"\"\"在链表末尾添加节点\"\"\"
        new_node = ListNode(value)
        if not self.head:
            self.head = new_node
            return
        
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
    
    def display(self):
        \"\"\"显示链表内容\"\"\"
        values = []
        current = self.head
        while current:
            values.append(str(current.value))
            current = current.next
        return " -> ".join(values) if values else "空链表"
"""
        }
        
        # 17. 二叉树遍历
        templates["binary_tree"] = {
            "python": """class TreeNode:
    \"\"\"二叉树节点类\"\"\"
    def __init__(self, value=0, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

class BinaryTree:
    \"\"\"二叉树实现\"\"\"
    def __init__(self, root_value=0):
        self.root = TreeNode(root_value)
    
    def preorder_traversal(self, node=None):
        \"\"\"前序遍历\"\"\"
        if node is None:
            node = self.root
        result = []
        if node:
            result.append(node.value)
            result.extend(self.preorder_traversal(node.left))
            result.extend(self.preorder_traversal(node.right))
        return result
    
    def inorder_traversal(self, node=None):
        \"\"\"中序遍历\"\"\"
        if node is None:
            node = self.root
        result = []
        if node:
            result.extend(self.inorder_traversal(node.left))
            result.append(node.value)
            result.extend(self.inorder_traversal(node.right))
        return result
"""
        }
        
        # 18. 缓存装饰器
        templates["cache_decorator"] = {
            "python": """from functools import wraps

def cache_decorator(func):
    \"\"\"缓存装饰器 - 存储函数调用结果\"\"\"
    cache = {}
    
    @wraps(func)
    def wrapper(*args):
        # 创建缓存键
        cache_key = str(args)
        
        if cache_key in cache:
            print(f"缓存命中: {func.__name__}{args}")
            return cache[cache_key]
        
        result = func(*args)
        cache[cache_key] = result
        print(f"缓存添加: {func.__name__}{args}")
        return result
    
    return wrapper

# 使用示例
@cache_decorator
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""
        }
        
        # 19. REST API端点
        templates["rest_api"] = {
            "python": """from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/calculate', methods=['POST'])
def calculate_endpoint():
    \"\"\"计算端点API\"\"\"
    try:
        data = request.get_json()
        
        if not data or 'numbers' not in data:
            return jsonify({"error": "缺少numbers参数"}), 400
        
        numbers = data['numbers']
        operation = data.get('operation', 'average')
        
        if operation == 'average':
            if not numbers:
                result = 0.0
            else:
                result = sum(numbers) / len(numbers)
            return jsonify({"result": result, "operation": operation})
        else:
            return jsonify({"error": f"不支持的操作: {operation}"}), 400
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
"""
        }
        
        # 20. 数据类定义
        templates["dataclass_definition"] = {
            "python": """from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Product:
    \"\"\"产品数据类\"\"\"
    id: int
    name: str
    price: float
    category: str = "其他"
    tags: List[str] = field(default_factory=list)
    
    def display_info(self) -> str:
        \"\"\"显示产品信息\"\"\"
        return f\"产品: {self.name}, 价格: ¥{self.price:.2f}, 分类: {self.category}\"

@dataclass
class Customer:
    \"\"\"客户数据类\"\"\"
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    is_vip: bool = False
    
    def contact_info(self) -> str:
        \"\"\"联系信息\"\"\"
        return f\"{self.name} ({self.email})\"
"""
        }
        
        return templates
    
    def _get_supported_patterns(self) -> Dict[str, List[str]]:
        """获取支持的自然语言模式
        
        Returns:
            模板名称到关键词列表的映射
        """
        return {
            "calculate_average": ["平均", "平均值", "平均数", "算平均", "平均计算", "average", "mean"],
            "find_max_min": ["最大", "最小", "最大值", "最小值", "极值", "最值", "max", "min"],
            "filter_even_numbers": ["偶数", "过滤偶数", "筛选偶数", "偶数值", "even numbers"],
            "string_reverse": ["反转", "反转字符串", "字符串反转", "倒序", "reverse"],
            "fibonacci_sequence": ["斐波那契", "fibonacci", "黄金分割数列"],
            "quicksort": ["排序", "快速排序", "quicksort", "quick sort"],
            "read_file": ["读取文件", "读文件", "文件读取", "read file"],
            "http_get": ["http请求", "http get", "发送请求", "网络请求"],
            "database_query": ["数据库", "数据库查询", "sql", "query database"],
            "regex_email": ["邮箱", "电子邮件", "email", "正则表达式", "regex"],
            "date_format": ["日期", "日期格式化", "格式化日期", "format date"],
            "bar_chart": ["柱状图", "条形图", "图表", "bar chart", "可视化"],
            "config_parser": ["配置文件", "解析配置", "config", "json配置"],
            "logging_setup": ["日志", "日志记录", "logging", "日志配置"],
            "error_handler": ["错误处理", "异常处理", "装饰器", "error handling"],
            "linked_list": ["链表", "linked list", "数据结构"],
            "binary_tree": ["二叉树", "树遍历", "binary tree", "tree traversal"],
            "cache_decorator": ["缓存", "缓存装饰器", "cache", "memoization"],
            "rest_api": ["rest api", "api端点", "flask", "web服务"],
            "dataclass_definition": ["数据类", "dataclass", "类定义", "model"]
        }
    
    def generate_code(self, description: str, language: str = "python") -> Dict[str, Any]:
        """根据自然语言描述和指定语言生成代码
        
        Args:
            description: 自然语言描述
            language: 目标编程语言 (python, javascript, java)
            
        Returns:
            包含生成代码和相关信息的字典
        """
        # 转换为小写便于匹配
        desc_lower = description.lower()
        lang_lower = language.lower()
        
        # 查找匹配的模板
        matched_template = None
        for template_name, patterns in self.supported_patterns.items():
            for pattern in patterns:
                if pattern.lower() in desc_lower:
                    matched_template = template_name
                    break
            if matched_template:
                break
        
        if not matched_template:
            # 如果没有精确匹配，尝试模糊匹配
            for template_name in self.code_templates.keys():
                if template_name.lower() in desc_lower:
                    matched_template = template_name
                    break
        
        if matched_template:
            # 获取指定语言的模板
            template_data = self.code_templates[matched_template]
            
            if lang_lower in template_data:
                generated_code = template_data[lang_lower]
                return {
                    "status": "success",
                    "template": matched_template,
                    "language": language,
                    "generated_code": generated_code,
                    "description": description,
                    "agent_id": self.agent_id,
                    "supported_scenes": list(self.code_templates.keys())
                }
            else:
                # 如果指定语言不支持，返回默认语言
                default_lang = "python"
                generated_code = template_data.get(default_lang, "")
                return {
                    "status": "partial_success",
                    "template": matched_template,
                    "language": default_lang,
                    "generated_code": generated_code,
                    "description": description,
                    "agent_id": self.agent_id,
                    "message": f"模板不支持语言 '{language}'，已返回 {default_lang} 版本",
                    "supported_scenes": list(self.code_templates.keys())
                }
        else:
            # 返回错误信息
            return {
                "status": "error",
                "error_message": f"无法识别描述: {description}",
                "suggestions": list(self.code_templates.keys()),
                "supported_languages": ["python", "javascript", "java"],
                "agent_id": self.agent_id
            }
    
    def validate_code(self, code: str) -> Dict[str, bool]:
        """简单验证生成的代码语法
        
        Args:
            code: 要验证的代码
            
        Returns:
            验证结果字典
        """
        try:
            # 尝试编译代码检查语法
            compile(code, '<string>', 'exec')
            return {
                "syntax_valid": True,
                "compilation_error": None
            }
        except SyntaxError as e:
            return {
                "syntax_valid": False,
                "compilation_error": str(e)
            }
    
    def get_supported_scenes(self) -> Dict[str, List[str]]:
        """获取支持的场景列表
        
        Returns:
            场景统计信息
        """
        scene_count = len(self.code_templates)
        languages = set()
        
        for template_data in self.code_templates.values():
            for lang in template_data.keys():
                languages.add(lang)
        
        return {
            "total_scenes": scene_count,
            "supported_languages": list(languages),
            "scene_names": list(self.code_templates.keys()),
            "agent_id": self.agent_id
        }


if __name__ == "__main__":
    # 简单的命令行交互
    agent = DevelopmentAgent()
    print("MVP开发Agent已启动")
    stats = agent.get_supported_scenes()
    print(f"支持 {stats['total_scenes']} 种代码生成场景")
    print(f"支持语言: {', '.join(stats['supported_languages'])}")
    print("\n部分场景示例:")
    for i, scene in enumerate(list(stats['scene_names'])[:10], 1):
        print(f"  {i}. {scene}")
    
    while True:
        print("\n" + "=" * 50)
        description = input("请输入功能描述 (输入 'quit' 退出): ")
        if description.lower() == 'quit':
            break
        
        language = input("请输入目标语言 (python/javascript/java, 默认python): ")
        if not language:
            language = "python"
        
        result = agent.generate_code(description, language)
        
        if result["status"] in ["success", "partial_success"]:
            print(f"\n✅ 生成成功 - 模板: {result['template']}, 语言: {result['language']}")
            print("生成的代码:")
            print("-" * 60)
            print(result["generated_code"])
            print("-" * 60)
            
            # 验证代码语法
            validation = agent.validate_code(result["generated_code"])
            if validation["syntax_valid"]:
                print("✅ 代码语法验证通过")
            else:
                print(f"⚠️  代码语法验证失败: {validation['compilation_error']}")
        else:
            print(f"\n❌ 生成失败: {result['error_message']}")
            print("建议尝试以下场景:", ", ".join(result["suggestions"][:5]))