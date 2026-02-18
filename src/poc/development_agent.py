"""
开发Agent原型实现
基于火山Trae框架的多Agent系统技术验证

功能：根据自然语言描述生成简单Python代码模块
"""

import re
from typing import Dict, List, Optional


class DevelopmentAgent:
    """开发Agent原型类"""
    
    def __init__(self, agent_id: str = "dev_agent_001"):
        """初始化开发Agent
        
        Args:
            agent_id: Agent唯一标识符
        """
        self.agent_id = agent_id
        self.code_templates = self._load_code_templates()
        self.supported_patterns = self._get_supported_patterns()
        
    def _load_code_templates(self) -> Dict[str, str]:
        """加载代码模板
        
        Returns:
            模板名称到模板内容的映射
        """
        return {
            "calculate_average": """def calculate_average(numbers: list) -> float:
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
            "find_max_min": """def find_max_min(numbers: list) -> tuple:
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
            "filter_even_numbers": """def filter_even_numbers(numbers: list) -> list:
    \"\"\"过滤列表中的偶数
    
    Args:
        numbers: 数字列表
        
    Returns:
        偶数列表
    \"\"\"
    return [num for num in numbers if num % 2 == 0]
""",
            "string_reverse": """def string_reverse(text: str) -> str:
    \"\"\"反转字符串
    
    Args:
        text: 输入字符串
        
    Returns:
        反转后的字符串
    \"\"\"
    return text[::-1]
""",
            "fibonacci_sequence": """def fibonacci_sequence(n: int) -> list:
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
    
    def _get_supported_patterns(self) -> Dict[str, List[str]]:
        """获取支持的自然语言模式
        
        Returns:
            模板名称到关键词列表的映射
        """
        return {
            "calculate_average": ["平均", "平均值", "平均数", "算平均", "平均计算"],
            "find_max_min": ["最大", "最小", "最大值", "最小值", "极值", "最值"],
            "filter_even_numbers": ["偶数", "过滤偶数", "筛选偶数", "偶数值"],
            "string_reverse": ["反转", "反转字符串", "字符串反转", "倒序"],
            "fibonacci_sequence": ["斐波那契", "fibonacci", "黄金分割数列"]
        }
    
    def generate_code(self, description: str) -> Dict[str, str]:
        """根据自然语言描述生成代码
        
        Args:
            description: 自然语言描述
            
        Returns:
            包含生成代码和相关信息的字典
        """
        # 转换为小写便于匹配
        desc_lower = description.lower()
        
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
            generated_code = self.code_templates[matched_template]
            return {
                "status": "success",
                "template": matched_template,
                "generated_code": generated_code,
                "description": description,
                "agent_id": self.agent_id
            }
        else:
            # 返回一个默认的模板或错误信息
            return {
                "status": "error",
                "error_message": f"无法识别描述: {description}",
                "suggestions": list(self.code_templates.keys()),
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
    
    def generate_test_cases(self, template_name: str) -> Dict[str, List]:
        """为指定模板生成测试用例
        
        Args:
            template_name: 模板名称
            
        Returns:
            测试用例字典
        """
        test_cases = {
            "calculate_average": {
                "inputs": [[1, 2, 3, 4, 5], [], [10, 20, 30]],
                "expected_outputs": [3.0, 0.0, 20.0]
            },
            "find_max_min": {
                "inputs": [[5, 2, 8, 1, 9], [10], []],
                "expected_outputs": [(9, 1), (10, 10), (None, None)]
            },
            "filter_even_numbers": {
                "inputs": [[1, 2, 3, 4, 5, 6], [1, 3, 5], [2, 4, 6]],
                "expected_outputs": [[2, 4, 6], [], [2, 4, 6]]
            },
            "string_reverse": {
                "inputs": ["hello", "python", "AI"],
                "expected_outputs": ["olleh", "nohtyp", "IA"]
            },
            "fibonacci_sequence": {
                "inputs": [5, 1, 10],
                "expected_outputs": [[0, 1, 1, 2, 3], [0], [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]]
            }
        }
        
        return test_cases.get(template_name, {"inputs": [], "expected_outputs": []})


if __name__ == "__main__":
    # 简单的命令行交互
    agent = DevelopmentAgent()
    print("开发Agent原型已启动")
    print("支持的功能: 计算平均值、查找最大最小值、过滤偶数、反转字符串、生成斐波那契数列")
    
    while True:
        description = input("\n请输入功能描述 (输入 'quit' 退出): ")
        if description.lower() == 'quit':
            break
        
        result = agent.generate_code(description)
        
        if result["status"] == "success":
            print(f"\n✅ 生成成功 - 模板: {result['template']}")
            print("生成的代码:")
            print("-" * 40)
            print(result["generated_code"])
            print("-" * 40)
            
            # 验证代码语法
            validation = agent.validate_code(result["generated_code"])
            if validation["syntax_valid"]:
                print("✅ 代码语法验证通过")
            else:
                print(f"⚠️  代码语法验证失败: {validation['compilation_error']}")
        else:
            print(f"\n❌ 生成失败: {result['error_message']}")
            print("建议尝试以下关键词:", ", ".join(result["suggestions"]))