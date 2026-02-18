"""
MVP测试Agent实现
基于火山Trae框架的多Agent系统

功能：为生成的代码自动创建单元测试用例，验证功能正确性
"""

import re
import ast
from typing import Dict, List, Optional, Any
from development_agent import DevelopmentAgent


class TestAgent:
    """MVP测试Agent类"""
    
    def __init__(self, agent_id: str = "mvp_test_agent_001"):
        """初始化测试Agent
        
        Args:
            agent_id: Agent唯一标识符
        """
        self.agent_id = agent_id
        self.dev_agent = DevelopmentAgent()
        self.test_templates = self._load_test_templates()
        
    def _load_test_templates(self) -> Dict[str, Dict[str, str]]:
        """加载测试模板
        
        Returns:
            模板名称到测试模板内容的映射
        """
        templates = {}
        
        # 1. 计算平均值测试模板
        templates["calculate_average"] = {
            "python": """import unittest

class TestCalculateAverage(unittest.TestCase):
    def test_calculate_average_normal(self):
        from generated_code import calculate_average
        result = calculate_average([1, 2, 3, 4, 5])
        self.assertEqual(result, 3.0)
    
    def test_calculate_average_empty(self):
        from generated_code import calculate_average
        result = calculate_average([])
        self.assertEqual(result, 0.0)
    
    def test_calculate_average_single(self):
        from generated_code import calculate_average
        result = calculate_average([10])
        self.assertEqual(result, 10.0)

if __name__ == '__main__':
    unittest.main()
"""
        }
        
        # 2. 查找最大最小值测试模板
        templates["find_max_min"] = {
            "python": """import unittest

class TestFindMaxMin(unittest.TestCase):
    def test_find_max_min_normal(self):
        from generated_code import find_max_min
        max_val, min_val = find_max_min([5, 2, 8, 1, 9])
        self.assertEqual(max_val, 9)
        self.assertEqual(min_val, 1)
    
    def test_find_max_min_empty(self):
        from generated_code import find_max_min
        max_val, min_val = find_max_min([])
        self.assertIsNone(max_val)
        self.assertIsNone(min_val)
    
    def test_find_max_min_single(self):
        from generated_code import find_max_min
        max_val, min_val = find_max_min([7])
        self.assertEqual(max_val, 7)
        self.assertEqual(min_val, 7)

if __name__ == '__main__':
    unittest.main()
"""
        }
        
        # 3. 过滤偶数测试模板
        templates["filter_even_numbers"] = {
            "python": """import unittest

class TestFilterEvenNumbers(unittest.TestCase):
    def test_filter_even_numbers_mixed(self):
        from generated_code import filter_even_numbers
        result = filter_even_numbers([1, 2, 3, 4, 5, 6])
        self.assertEqual(result, [2, 4, 6])
    
    def test_filter_even_numbers_no_even(self):
        from generated_code import filter_even_numbers
        result = filter_even_numbers([1, 3, 5])
        self.assertEqual(result, [])
    
    def test_filter_even_numbers_all_even(self):
        from generated_code import filter_even_numbers
        result = filter_even_numbers([2, 4, 6])
        self.assertEqual(result, [2, 4, 6])

if __name__ == '__main__':
    unittest.main()
"""
        }
        
        # 4. 字符串反转测试模板
        templates["string_reverse"] = {
            "python": """import unittest

class TestStringReverse(unittest.TestCase):
    def test_string_reverse_normal(self):
        from generated_code import string_reverse
        result = string_reverse("hello")
        self.assertEqual(result, "olleh")
    
    def test_string_reverse_empty(self):
        from generated_code import string_reverse
        result = string_reverse("")
        self.assertEqual(result, "")
    
    def test_string_reverse_special_chars(self):
        from generated_code import string_reverse
        result = string_reverse("python3!")
        self.assertEqual(result, "!3nohtyp")

if __name__ == '__main__':
    unittest.main()
"""
        }
        
        # 5. 斐波那契数列测试模板
        templates["fibonacci_sequence"] = {
            "python": """import unittest

class TestFibonacciSequence(unittest.TestCase):
    def test_fibonacci_sequence_normal(self):
        from generated_code import fibonacci_sequence
        result = fibonacci_sequence(5)
        self.assertEqual(result, [0, 1, 1, 2, 3])
    
    def test_fibonacci_sequence_small(self):
        from generated_code import fibonacci_sequence
        result = fibonacci_sequence(1)
        self.assertEqual(result, [0])
    
    def test_fibonacci_sequence_zero(self):
        from generated_code import fibonacci_sequence
        result = fibonacci_sequence(0)
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
"""
        }
        
        # 6. 快速排序测试模板
        templates["quicksort"] = {
            "python": """import unittest

class TestQuicksort(unittest.TestCase):
    def test_quicksort_normal(self):
        from generated_code import quicksort
        result = quicksort([5, 2, 8, 1, 9])
        self.assertEqual(result, [1, 2, 5, 8, 9])
    
    def test_quicksort_empty(self):
        from generated_code import quicksort
        result = quicksort([])
        self.assertEqual(result, [])
    
    def test_quicksort_sorted(self):
        from generated_code import quicksort
        result = quicksort([1, 2, 3, 4, 5])
        self.assertEqual(result, [1, 2, 3, 4, 5])

if __name__ == '__main__':
    unittest.main()
"""
        }
        
        # 7. 读取文件测试模板
        templates["read_file"] = {
            "python": """import unittest
import tempfile
import os

class TestReadFile(unittest.TestCase):
    def test_read_file_normal(self):
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("测试内容")
            temp_path = f.name
        
        try:
            from generated_code import read_file
            result = read_file(temp_path)
            self.assertEqual(result, "测试内容")
        finally:
            os.unlink(temp_path)
    
    def test_read_file_not_found(self):
        from generated_code import read_file
        result = read_file("/nonexistent/path/file.txt")
        self.assertIn("不存在", result)

if __name__ == '__main__':
    unittest.main()
"""
        }
        
        # 8. HTTP GET测试模板
        templates["http_get"] = {
            "python": """import unittest
from unittest.mock import patch, Mock

class TestHttpGet(unittest.TestCase):
    @patch('generated_code.requests.get')
    def test_http_get_success(self, mock_get):
        # 模拟响应
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "测试内容"
        mock_response.headers = {'Content-Type': 'text/html'}
        mock_get.return_value = mock_response
        
        from generated_code import http_get
        result = http_get("http://example.com")
        
        self.assertEqual(result["status_code"], 200)
        self.assertIn("测试内容", result["content"])
    
    @patch('generated_code.requests.get')
    def test_http_get_error(self, mock_get):
        mock_get.side_effect = Exception("连接失败")
        
        from generated_code import http_get
        result = http_get("http://example.com")
        
        self.assertIn("error", result)
        self.assertIn("连接失败", result["error"])

if __name__ == '__main__':
    unittest.main()
"""
        }
        
        # 9. 数据库查询测试模板
        templates["database_query"] = {
            "python": """import unittest
import sqlite3
import tempfile
import os

class TestDatabaseQuery(unittest.TestCase):
    def test_database_query_normal(self):
        # 创建临时数据库
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = f.name
        
        try:
            # 创建测试表和数据
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE users (id INTEGER, name TEXT)")
            cursor.execute("INSERT INTO users VALUES (1, 'Alice')")
            cursor.execute("INSERT INTO users VALUES (2, 'Bob')")
            conn.commit()
            conn.close()
            
            from generated_code import database_query
            result = database_query(db_path, "SELECT * FROM users")
            
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0], (1, 'Alice'))
        finally:
            os.unlink(db_path)

if __name__ == '__main__':
    unittest.main()
"""
        }
        
        # 10. 正则表达式邮箱测试模板
        templates["regex_email"] = {
            "python": """import unittest

class TestRegexEmail(unittest.TestCase):
    def test_extract_emails_normal(self):
        from generated_code import extract_emails
        text = "联系邮箱: test@example.com 和 admin@site.org"
        result = extract_emails(text)
        
        self.assertEqual(len(result), 2)
        self.assertIn("test@example.com", result)
        self.assertIn("admin@site.org", result)
    
    def test_extract_emails_no_email(self):
        from generated_code import extract_emails
        text = "这个文本没有邮箱地址"
        result = extract_emails(text)
        
        self.assertEqual(len(result), 0)

if __name__ == '__main__':
    unittest.main()
"""
        }
        
        # 11. 日期格式化测试模板
        templates["date_format"] = {
            "python": """import unittest

class TestDateFormat(unittest.TestCase):
    def test_format_date_normal(self):
        from generated_code import format_date
        result = format_date("2026-02-16")
        self.assertEqual(result, "2026年02月16日")
    
    def test_format_date_custom_format(self):
        from generated_code import format_date
        result = format_date("2026-02-16", output_format="%d/%m/%Y")
        self.assertEqual(result, "16/02/2026")
    
    def test_format_date_invalid(self):
        from generated_code import format_date
        result = format_date("无效日期")
        self.assertEqual(result, "日期格式错误")

if __name__ == '__main__':
    unittest.main()
"""
        }
        
        # 其他场景的测试模板...
        
        return templates
    
    def generate_test_code(self, template_name: str, language: str = "python") -> Dict[str, Any]:
        """为指定模板生成测试代码
        
        Args:
            template_name: 模板名称
            language: 目标编程语言
            
        Returns:
            包含测试代码和相关信息的字典
        """
        if template_name not in self.test_templates:
            return {
                "status": "error",
                "error_message": f"不支持的模板: {template_name}",
                "supported_templates": list(self.test_templates.keys()),
                "agent_id": self.agent_id
            }
        
        template_data = self.test_templates[template_name]
        
        if language not in template_data:
            return {
                "status": "error",
                "error_message": f"模板 {template_name} 不支持语言: {language}",
                "supported_languages": list(template_data.keys()),
                "agent_id": self.agent_id
            }
        
        test_code = template_data[language]
        
        return {
            "status": "success",
            "template": template_name,
            "language": language,
            "test_code": test_code,
            "agent_id": self.agent_id
        }
    
    def analyze_and_test(self, code_description: str, language: str = "python") -> Dict[str, Any]:
        """分析代码描述并生成完整的测试套件
        
        Args:
            code_description: 代码功能描述
            language: 目标编程语言
            
        Returns:
            包含生成代码和测试代码的完整结果
        """
        # 1. 生成代码
        dev_result = self.dev_agent.generate_code(code_description, language)
        
        if dev_result["status"] != "success":
            return {
                "status": "error",
                "error_message": f"开发Agent生成失败: {dev_result.get('error_message', '未知错误')}",
                "agent_id": self.agent_id
            }
        
        # 2. 生成测试代码
        test_result = self.generate_test_code(dev_result["template"], language)
        
        if test_result["status"] != "success":
            return {
                "status": "partial_success",
                "dev_result": dev_result,
                "test_error": test_result["error_message"],
                "agent_id": self.agent_id
            }
        
        # 3. 生成完整的工作流程文件
        workflow_code = self._create_workflow_file(dev_result, test_result)
        
        return {
            "status": "success",
            "dev_result": dev_result,
            "test_result": test_result,
            "workflow_code": workflow_code,
            "agent_id": self.agent_id
        }
    
    def _create_workflow_file(self, dev_result: Dict, test_result: Dict) -> str:
        """创建完整的工作流程文件，包含生成代码和测试代码
        
        Args:
            dev_result: 开发Agent结果
            test_result: 测试Agent结果
            
        Returns:
            完整的工作流程代码
        """
        template_name = dev_result["template"]
        language = dev_result["language"]
        generated_code = dev_result["generated_code"]
        test_code = test_result["test_code"]
        
        workflow = f"""# 多Agent系统工作流程文件
# 生成时间: 2026-02-16
# 模板: {template_name}
# 语言: {language}
# 开发Agent: {dev_result['agent_id']}
# 测试Agent: {test_result['agent_id']}

# ============== 生成的代码 ==============
{generated_code}

# ============== 生成的测试代码 ==============
{test_code}

# ============== 执行脚本 ==============
if __name__ == '__main__':
    print("开始执行测试...")
    import subprocess
    import sys
    
    # 保存生成代码到临时文件
    with open('generated_code.py', 'w', encoding='utf-8') as f:
        f.write('{generated_code.replace("'", "\\'").replace('"', '\\"')}')
    
    # 保存测试代码到临时文件
    with open('test_generated_code.py', 'w', encoding='utf-8') as f:
        f.write('{test_code.replace("'", "\\'").replace('"', '\\"')}')
    
    # 执行测试
    try:
        result = subprocess.run([sys.executable, '-m', 'unittest', 'test_generated_code.py'], 
                              capture_output=True, text=True, timeout=10)
        print(result.stdout)
        if result.returncode == 0:
            print("✅ 所有测试通过！")
        else:
            print(f"❌ 测试失败: {{result.stderr}}")
    except Exception as e:
        print(f"执行测试时发生错误: {{str(e)}}")
"""
        return workflow
    
    def get_supported_test_scenes(self) -> Dict[str, List[str]]:
        """获取支持的测试场景列表
        
        Returns:
            场景统计信息
        """
        scene_count = len(self.test_templates)
        languages = set()
        
        for template_data in self.test_templates.values():
            for lang in template_data.keys():
                languages.add(lang)
        
        return {
            "total_test_scenes": scene_count,
            "supported_languages": list(languages),
            "test_scene_names": list(self.test_templates.keys()),
            "agent_id": self.agent_id
        }


if __name__ == "__main__":
    # 简单的命令行交互
    agent = TestAgent()
    print("MVP测试Agent已启动")
    stats = agent.get_supported_test_scenes()
    print(f"支持 {stats['total_test_scenes']} 种测试场景")
    print(f"支持语言: {', '.join(stats['supported_languages'])}")
    
    while True:
        print("\n" + "=" * 50)
        print("1. 分析描述并生成完整测试")
        print("2. 为指定模板生成测试代码")
        print("3. 查看支持的测试场景")
        print("4. 退出")
        
        choice = input("请选择操作 (1-4): ")
        
        if choice == "1":
            description = input("请输入代码功能描述: ")
            language = input("请输入目标语言 (默认python): ") or "python"
            
            result = agent.analyze_and_test(description, language)
            
            if result["status"] == "success":
                print("\n✅ 生成成功！")
                print(f"模板: {result['dev_result']['template']}")
                print(f"语言: {result['dev_result']['language']}")
                
                # 显示部分代码
                dev_code = result["dev_result"]["generated_code"]
                print(f"\n生成代码预览 (前5行):")
                for i, line in enumerate(dev_code.split('\n')[:5], 1):
                    print(f"  {i}: {line}")
                if len(dev_code.split('\n')) > 5:
                    print(f"  ... (共{len(dev_code.split('\n'))}行)")
                
                # 保存工作流程文件
                with open(f"workflow_{result['dev_result']['template']}.py", 'w', encoding='utf-8') as f:
                    f.write(result["workflow_code"])
                print(f"完整工作流程已保存到: workflow_{result['dev_result']['template']}.py")
                
            else:
                print(f"\n❌ 生成失败: {result.get('error_message', '未知错误')}")
                
        elif choice == "2":
            template_name = input("请输入模板名称: ")
            language = input("请输入目标语言 (默认python): ") or "python"
            
            result = agent.generate_test_code(template_name, language)
            
            if result["status"] == "success":
                print("\n✅ 测试代码生成成功！")
                print(f"模板: {result['template']}")
                print(f"语言: {result['language']}")
                print("\n测试代码预览:")
                print("-" * 60)
                print(result["test_code"])
                print("-" * 60)
            else:
                print(f"\n❌ 生成失败: {result['error_message']}")
                
        elif choice == "3":
            stats = agent.get_supported_test_scenes()
            print(f"\n支持的测试场景 ({stats['total_test_scenes']}种):")
            for i, scene in enumerate(stats["test_scene_names"], 1):
                print(f"  {i}. {scene}")
                
        elif choice == "4":
            print("退出测试Agent")
            break
        else:
            print("无效选择，请重试")