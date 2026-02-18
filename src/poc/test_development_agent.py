"""
开发Agent原型测试脚本
用于验证POC原型的功能正确性
"""

import unittest
import sys
import os

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from development_agent import DevelopmentAgent


class TestDevelopmentAgent(unittest.TestCase):
    """开发Agent测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.agent = DevelopmentAgent()
    
    def test_agent_initialization(self):
        """测试Agent初始化"""
        self.assertEqual(self.agent.agent_id, "dev_agent_001")
        self.assertIn("calculate_average", self.agent.code_templates)
        self.assertIn("find_max_min", self.agent.code_templates)
    
    def test_generate_code_success(self):
        """测试成功生成代码"""
        test_cases = [
            ("计算数字列表的平均值", "calculate_average"),
            ("查找最大值和最小值", "find_max_min"),
            ("过滤偶数", "filter_even_numbers"),
            ("反转字符串", "string_reverse"),
            ("生成斐波那契数列", "fibonacci_sequence"),
            ("算平均", "calculate_average"),
            ("最大最小", "find_max_min"),
        ]
        
        for description, expected_template in test_cases:
            with self.subTest(description=description):
                result = self.agent.generate_code(description)
                self.assertEqual(result["status"], "success")
                self.assertEqual(result["template"], expected_template)
                self.assertIn("def ", result["generated_code"])
    
    def test_generate_code_error(self):
        """测试无法识别的描述"""
        result = self.agent.generate_code("这是一个无法识别的功能描述")
        self.assertEqual(result["status"], "error")
        self.assertIn("error_message", result)
        self.assertIn("suggestions", result)
    
    def test_validate_code_syntax(self):
        """测试代码语法验证"""
        # 测试有效代码
        valid_code = "def hello():\n    return 'world'"
        validation = self.agent.validate_code(valid_code)
        self.assertTrue(validation["syntax_valid"])
        self.assertIsNone(validation["compilation_error"])
        
        # 测试无效代码
        invalid_code = "def hello(:\n    return 'world'"  # 缺少括号
        validation = self.agent.validate_code(invalid_code)
        self.assertFalse(validation["syntax_valid"])
        self.assertIsNotNone(validation["compilation_error"])
    
    def test_generate_test_cases(self):
        """测试生成测试用例"""
        test_cases = self.agent.generate_test_cases("calculate_average")
        self.assertIn("inputs", test_cases)
        self.assertIn("expected_outputs", test_cases)
        self.assertEqual(len(test_cases["inputs"]), 3)
        self.assertEqual(len(test_cases["expected_outputs"]), 3)
        
        # 测试不存在的模板
        empty_cases = self.agent.generate_test_cases("nonexistent")
        self.assertEqual(len(empty_cases["inputs"]), 0)
        self.assertEqual(len(empty_cases["expected_outputs"]), 0)
    
    def test_integration_workflow(self):
        """测试完整工作流程"""
        # 1. 生成代码
        result = self.agent.generate_code("计算平均值")
        self.assertEqual(result["status"], "success")
        
        # 2. 验证代码语法
        validation = self.agent.validate_code(result["generated_code"])
        self.assertTrue(validation["syntax_valid"])
        
        # 3. 获取测试用例
        test_cases = self.agent.generate_test_cases(result["template"])
        self.assertGreater(len(test_cases["inputs"]), 0)
        
        print(f"\n✅ 完整工作流程测试通过")
        print(f"模板: {result['template']}")
        print(f"测试用例数量: {len(test_cases['inputs'])}")


class TestActualCodeExecution(unittest.TestCase):
    """实际代码执行测试"""
    
    def setUp(self):
        self.agent = DevelopmentAgent()
    
    def test_execute_generated_code(self):
        """执行生成的代码并验证功能"""
        # 生成计算平均值的代码
        result = self.agent.generate_code("计算平均值")
        
        if result["status"] == "success":
            # 动态执行生成的代码
            code = result["generated_code"]
            namespace = {}
            
            try:
                exec(code, namespace)
                
                # 获取生成的函数
                func_name = "calculate_average"
                if func_name in namespace:
                    func = namespace[func_name]
                    
                    # 测试函数功能
                    test_inputs = [[1, 2, 3], [10, 20, 30], []]
                    expected_outputs = [2.0, 20.0, 0.0]
                    
                    for test_input, expected in zip(test_inputs, expected_outputs):
                        actual = func(test_input)
                        self.assertAlmostEqual(actual, expected, places=5,
                                               msg=f"输入 {test_input} 期望 {expected} 实际 {actual}")
                    
                    print(f"✅ 生成的代码执行测试通过")
                else:
                    self.fail(f"函数 {func_name} 未在生成的代码中找到")
                    
            except Exception as e:
                self.fail(f"执行生成的代码时出错: {e}")


def run_performance_test():
    """运行性能测试"""
    print("\n" + "="*50)
    print("性能测试")
    print("="*50)
    
    agent = DevelopmentAgent()
    
    import time
    
    # 测试响应时间
    test_descriptions = [
        "计算平均值",
        "查找最大值最小值",
        "过滤偶数",
        "反转字符串",
        "生成斐波那契数列"
    ]
    
    for desc in test_descriptions:
        start_time = time.time()
        result = agent.generate_code(desc)
        end_time = time.time()
        
        if result["status"] == "success":
            print(f"✅ {desc}: {((end_time - start_time)*1000):.2f} 毫秒")
        else:
            print(f"❌ {desc}: 失败")


if __name__ == "__main__":
    print("开发Agent原型测试")
    print("-" * 40)
    
    # 运行单元测试
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestDevelopmentAgent)
    suite.addTests(loader.loadTestsFromTestCase(TestActualCodeExecution))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 运行性能测试
    if result.wasSuccessful():
        run_performance_test()
    
    # 输出测试总结
    print("\n" + "="*50)
    print("测试总结")
    print("="*50)
    print(f"运行测试: {result.testsRun}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("✅ 所有测试通过")
    else:
        print("❌ 测试失败")
        sys.exit(1)