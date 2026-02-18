"""
POC原型演示脚本
展示基于火山Trae框架的多Agent系统技术验证
"""

import os
import sys
import json
from typing import Dict, List, Any

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from development_agent import DevelopmentAgent


class SimpleCoordinator:
    """简单协调器原型
    
    模拟主协调Agent的基本功能，负责任务分解和结果整合
    """
    
    def __init__(self):
        self.agents = {
            "development": DevelopmentAgent("dev_agent_001"),
            # 注：测试Agent和设计Agent在此POC中暂不实现
            # 仅作为架构概念展示
        }
        
    def process_task(self, task_description: str) -> Dict[str, Any]:
        """处理用户任务
        
        Args:
            task_description: 任务描述
            
        Returns:
            处理结果
        """
        print(f"\n📋 接收任务: {task_description}")
        
        # 简单任务分解逻辑
        if any(keyword in task_description.lower() for keyword in ["代码", "编程", "开发", "函数", "程序"]):
            print("🔍 识别为开发任务，分配给开发Agent...")
            
            # 调用开发Agent
            dev_result = self.agents["development"].generate_code(task_description)
            
            if dev_result["status"] == "success":
                print(f"✅ 开发Agent成功生成代码")
                print(f"📊 模板: {dev_result['template']}")
                
                # 验证代码语法
                validation = self.agents["development"].validate_code(dev_result["generated_code"])
                
                return {
                    "task_type": "development",
                    "status": "completed",
                    "agent_id": dev_result["agent_id"],
                    "generated_code": dev_result["generated_code"],
                    "syntax_valid": validation["syntax_valid"],
                    "compilation_error": validation["compilation_error"],
                    "test_cases": self.agents["development"].generate_test_cases(dev_result["template"])
                }
            else:
                return {
                    "task_type": "development",
                    "status": "failed",
                    "error": dev_result["error_message"],
                    "suggestions": dev_result["suggestions"]
                }
        else:
            return {
                "task_type": "unknown",
                "status": "failed",
                "error": "无法识别任务类型"
            }


def showcase_development_agent():
    """展示开发Agent功能"""
    print("\n" + "="*60)
    print("开发Agent功能展示")
    print("="*60)
    
    agent = DevelopmentAgent()
    
    # 展示支持的模板
    print("\n📚 支持的功能模板:")
    for i, template in enumerate(agent.code_templates.keys(), 1):
        patterns = agent.supported_patterns.get(template, [])
        print(f"  {i}. {template}: {', '.join(patterns[:3])}")
    
    # 演示代码生成
    test_scenarios = [
        "我需要一个计算数字平均值的函数",
        "请帮我写一个查找最大最小值的函数",
        "生成一个过滤偶数的函数",
        "创建一个字符串反转的函数",
        "写一个生成斐波那契数列的函数"
    ]
    
    print("\n🚀 代码生成演示:")
    for scenario in test_scenarios:
        print(f"\n📝 需求: {scenario}")
        result = agent.generate_code(scenario)
        
        if result["status"] == "success":
            print(f"  ✅ 匹配模板: {result['template']}")
            
            # 显示前几行代码
            code_lines = result["generated_code"].split('\n')
            print("  📄 生成代码预览:")
            for i, line in enumerate(code_lines[:6]):
                if line.strip():
                    print(f"    {line}")
            if len(code_lines) > 6:
                print(f"    ... (共 {len(code_lines)} 行)")
            
            # 验证语法
            validation = agent.validate_code(result["generated_code"])
            if validation["syntax_valid"]:
                print("  ✅ 语法验证通过")
            else:
                print(f"  ⚠️  语法错误: {validation['compilation_error']}")
        else:
            print(f"  ❌ 错误: {result['error_message']}")


def showcase_coordinator_workflow():
    """展示协调器工作流程"""
    print("\n" + "="*60)
    print("多Agent协调工作流程展示")
    print("="*60)
    
    coordinator = SimpleCoordinator()
    
    # 模拟用户任务
    tasks = [
        "开发一个计算平均值的函数",
        "编写一个过滤偶数的程序",
        "我需要一个字符串处理工具"
    ]
    
    for task in tasks:
        print(f"\n🔧 处理任务: {task}")
        result = coordinator.process_task(task)
        
        if result["status"] == "completed":
            print(f"  ✅ 任务完成")
            print(f"  👤 执行Agent: {result['agent_id']}")
            print(f"  ✅ 语法检查: {'通过' if result['syntax_valid'] else '失败'}")
            
            # 显示测试用例信息
            test_cases = result["test_cases"]
            if test_cases["inputs"]:
                print(f"  🧪 生成测试用例: {len(test_cases['inputs'])} 个")
            
            # 显示部分代码
            code_preview = result["generated_code"].split('\n')[0]
            print(f"  📝 代码: {code_preview}...")
        else:
            print(f"  ❌ 任务失败: {result.get('error', '未知错误')}")


def run_interactive_demo():
    """运行交互式演示"""
    print("\n" + "="*60)
    print("火山Trae多Agent系统POC原型 - 交互式演示")
    print("="*60)
    
    print("""
🌟 原型概述:
基于火山Trae框架的多Agent系统技术验证，展示了开发Agent的
核心代码生成能力，模拟了多Agent协作的基本工作流程。

🛠️ 主要组件:
1. 开发Agent - 根据自然语言描述生成Python代码
2. 简单协调器 - 任务分解和结果整合
3. 测试框架 - 验证生成代码的功能正确性
""")
    
    agent = DevelopmentAgent()
    coordinator = SimpleCoordinator()
    
    while True:
        print("\n" + "-"*60)
        print("请选择演示模式:")
        print("1. 开发Agent代码生成")
        print("2. 协调器工作流程")
        print("3. 运行完整测试")
        print("4. 退出演示")
        
        choice = input("\n请输入选项 (1-4): ").strip()
        
        if choice == "1":
            print("\n🔧 开发Agent代码生成模式")
            print("请输入自然语言描述，例如: '计算平均值的函数'")
            description = input("描述: ").strip()
            
            if description:
                result = agent.generate_code(description)
                
                if result["status"] == "success":
                    print(f"\n✅ 生成成功!")
                    print(f"📋 模板: {result['template']}")
                    print("\n📄 生成的代码:")
                    print("-" * 40)
                    print(result["generated_code"])
                    print("-" * 40)
                    
                    # 验证语法
                    validation = agent.validate_code(result["generated_code"])
                    if validation["syntax_valid"]:
                        print("✅ 语法验证通过")
                    else:
                        print(f"⚠️  语法错误: {validation['compilation_error']}")
                else:
                    print(f"\n❌ 生成失败: {result['error_message']}")
                    print("💡 建议尝试以下关键词:")
                    for suggestion in result["suggestions"][:5]:
                        print(f"  - {suggestion}")
        
        elif choice == "2":
            print("\n🤖 协调器工作流程模式")
            print("请输入任务描述，例如: '开发一个数据处理程序'")
            task = input("任务: ").strip()
            
            if task:
                result = coordinator.process_task(task)
                
                print(f"\n📊 任务处理结果:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif choice == "3":
            print("\n🧪 运行完整测试...")
            os.system(f"cd {os.path.dirname(os.path.abspath(__file__))} && python test_development_agent.py")
        
        elif choice == "4":
            print("\n👋 感谢使用，演示结束!")
            break
        
        else:
            print("❌ 无效选项，请重试")


def main():
    """主函数"""
    print("🌋 火山Trae多Agent系统POC原型演示")
    
    # 展示开发Agent功能
    showcase_development_agent()
    
    # 展示协调器工作流程
    showcase_coordinator_workflow()
    
    # 运行交互式演示
    run_interactive_demo()


if __name__ == "__main__":
    main()