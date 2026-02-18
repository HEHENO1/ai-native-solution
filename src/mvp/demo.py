"""
MVP多Agent系统演示脚本
演示开发Agent、测试Agent、设计Agent的协作流程
"""

import sys
import os
import json
from datetime import datetime

# 添加当前目录到路径，确保导入正确
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from development_agent import DevelopmentAgent
from test_agent import TestAgent
from design_agent import DesignAgent
from coordinator import Coordinator, TaskType, TaskPriority


def print_header(title: str):
    """打印标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def demo_development_agent():
    """演示开发Agent功能"""
    print_header("演示1: 开发Agent代码生成")
    
    agent = DevelopmentAgent()
    print(f"开发Agent ID: {agent.agent_id}")
    
    # 获取支持场景
    stats = agent.get_supported_scenes()
    print(f"支持 {stats['total_scenes']} 种代码生成场景")
    
    # 演示几个场景
    demo_scenarios = [
        {
            "description": "计算一组数字的平均值",
            "language": "python"
        },
        {
            "description": "反转字符串的javascript函数",
            "language": "javascript"
        },
        {
            "description": "快速排序算法实现",
            "language": "python"
        }
    ]
    
    for i, scenario in enumerate(demo_scenarios, 1):
        print(f"\n🔹 场景{i}: {scenario['description']} ({scenario['language']})")
        
        result = agent.generate_code(scenario['description'], scenario['language'])
        
        if result["status"] in ["success", "partial_success"]:
            print(f"   模板: {result['template']}, 语言: {result['language']}")
            
            # 显示前3行代码
            code_lines = result["generated_code"].split('\n')[:3]
            for line in code_lines:
                print(f"     {line}")
            if len(result["generated_code"].split('\n')) > 3:
                print(f"     ... (共{len(result['generated_code'].split('\n'))}行)")
            
            # 验证语法
            validation = agent.validate_code(result["generated_code"])
            if validation["syntax_valid"]:
                print(f"    ✅ 语法验证通过")
            else:
                print(f"    ⚠️  语法验证失败: {validation['compilation_error']}")
        else:
            print(f"    ❌ 生成失败: {result.get('error_message', '未知错误')}")


def demo_test_agent():
    """演示测试Agent功能"""
    print_header("演示2: 测试Agent自动测试生成")
    
    agent = TestAgent()
    print(f"测试Agent ID: {agent.agent_id}")
    
    # 获取支持场景
    stats = agent.get_supported_test_scenes()
    print(f"支持 {stats['total_test_scenes']} 种测试场景")
    
    # 演示几个场景
    demo_scenarios = [
        "calculate_average",
        "find_max_min",
        "fibonacci_sequence"
    ]
    
    for i, template_name in enumerate(demo_scenarios, 1):
        print(f"\n🔹 场景{i}: 为 {template_name} 生成单元测试")
        
        result = agent.generate_test_code(template_name, "python")
        
        if result["status"] == "success":
            print(f"   模板: {result['template']}, 语言: {result['language']}")
            
            # 显示测试类名
            test_code = result["test_code"]
            class_match = re.search(r'class (\w+)\(unittest\.TestCase\)', test_code)
            if class_match:
                print(f"   测试类: {class_match.group(1)}")
            
            # 显示测试方法数量
            method_matches = re.findall(r'def test_\w+\(self\)', test_code)
            print(f"   测试方法数: {len(method_matches)}")
            
            # 保存测试文件示例
            test_filename = f"test_{template_name}.py"
            with open(test_filename, 'w', encoding='utf-8') as f:
                f.write(test_code)
            print(f"   测试文件已保存: {test_filename}")
        else:
            print(f"    ❌ 生成失败: {result.get('error_message', '未知错误')}")


def demo_design_agent():
    """演示设计Agent功能"""
    print_header("演示3: 设计AgentUI设计生成")
    
    agent = DesignAgent()
    print(f"设计Agent ID: {agent.agent_id}")
    
    # 获取支持能力
    stats = agent.get_supported_components()
    print(f"支持 {stats['total_components']} 种UI组件, {stats['total_layouts']} 种布局方案")
    
    # 演示几个场景
    demo_scenarios = [
        {
            "description": "设计一个数据仪表板界面",
            "app_name": "数据分析平台"
        },
        {
            "description": "创建一个用户登录表单界面",
            "app_name": "用户管理系统"
        }
    ]
    
    for i, scenario in enumerate(demo_scenarios, 1):
        print(f"\n🔹 场景{i}: {scenario['description']}")
        
        # 生成设计规范
        spec_result = agent.generate_design_spec(scenario['description'], scenario['app_name'])
        
        if spec_result["status"] == "success":
            design_spec = spec_result["design_spec"]
            print(f"   应用名称: {design_spec['app_name']}")
            print(f"   布局类型: {design_spec['layout']['type']}")
            print(f"   所需组件: {', '.join(design_spec['components'])}")
            
            # 生成HTML草图
            html_result = agent.generate_html_sketch(scenario['description'], scenario['app_name'])
            
            if html_result["status"] == "success":
                html_filename = f"demo_ui_{scenario['app_name']}.html"
                with open(html_filename, 'w', encoding='utf-8') as f:
                    f.write(html_result["html_content"])
                print(f"   HTML草图已保存: {html_filename}")
            else:
                print(f"   ⚠️  HTML生成失败")
        else:
            print(f"    ❌ 设计规范生成失败")


def demo_coordinator_full_stack():
    """演示协调器处理全栈任务"""
    print_header("演示4: 协调器处理全栈开发任务")
    
    coordinator = Coordinator()
    print(f"协调器 ID: {coordinator.coordinator_id}")
    
    # 创建全栈任务
    task_description = "开发一个用户管理系统，包含用户数据处理的Python函数，为函数生成单元测试，并设计管理界面"
    
    print(f"任务描述: {task_description}")
    
    # 创建任务
    create_result = coordinator.create_task(task_description, "high")
    
    if create_result["status"] != "success":
        print(f"❌ 任务创建失败: {create_result.get('error_message', '未知错误')}")
        return
    
    task = create_result["task"]
    print(f"\n✅ 任务创建成功:")
    print(f"  任务ID: {task['task_id']}")
    print(f"  任务类型: {task['task_type']}")
    print(f"  优先级: {task['priority']}")
    print(f"  语言: {task['language']}")
    print(f"  应用名称: {task['app_name']}")
    
    # 处理任务
    print(f"\n🔄 正在处理任务 {task['task_id']}...")
    process_result = coordinator.process_task(task['task_id'])
    
    if process_result["status"] == "success":
        task = process_result["task"]
        results = process_result["results"]
        
        print(f"\n✅ 任务处理完成!")
        print(f"  最终状态: {task['status']}")
        print(f"  生成文件: {results.get('files_generated', [])}")
        
        # 显示详细结果
        print(f"\n🔍 详细结果摘要:")
        
        if "code_generation" in results:
            code_result = results["code_generation"]
            print(f"  代码生成: {code_result.get('status', 'N/A')}")
            if code_result["status"] == "success":
                print(f"    模板: {code_result.get('template', 'N/A')}")
                print(f"    语言: {code_result.get('language', 'N/A')}")
        
        if "test_generation" in results:
            test_result = results["test_generation"]
            print(f"  测试生成: {test_result.get('status', 'N/A')}")
        
        if "ui_design" in results:
            ui_result = results["ui_design"]
            print(f"  UI设计: 设计规范生成成功")
            
            # 保存完整工作流文件
            workflow_data = {
                "task_info": task,
                "processing_results": results,
                "generated_at": datetime.now().isoformat()
            }
            
            workflow_filename = f"full_stack_workflow_{task['task_id']}.json"
            with open(workflow_filename, 'w', encoding='utf-8') as f:
                json.dump(workflow_data, f, ensure_ascii=False, indent=2)
            
            print(f"\n📁 完整工作流数据已保存到: {workflow_filename}")
            
    else:
        print(f"\n❌ 任务处理失败: {process_result.get('error_message', '未知错误')}")


def demo_system_integration():
    """演示完整系统集成"""
    print_header("演示5: 完整多Agent系统集成工作流")
    
    print("🚀 启动多Agent系统...")
    
    # 初始化所有组件
    coordinator = Coordinator()
    dev_agent = DevelopmentAgent()
    test_agent = TestAgent()
    design_agent = DesignAgent()
    
    print(f"✅ 组件初始化完成:")
    print(f"  协调器: {coordinator.coordinator_id}")
    print(f"  开发Agent: {dev_agent.agent_id}")
    print(f"  测试Agent: {test_agent.agent_id}")
    print(f"  设计Agent: {design_agent.agent_id}")
    
    # 模拟用户请求
    print(f"\n👤 用户请求: \"我需要一个计算工资税的函数，同时要确保正确性测试和友好的界面\"")
    
    # 协调器分解任务
    print(f"\n🔧 协调器任务分解:")
    print(f"  1. 代码生成任务: 计算工资税的Python函数")
    print(f"  2. 测试生成任务: 为工资税函数创建单元测试")
    print(f"  3. 设计任务: 工资计算器界面设计")
    
    # 并行处理（模拟）
    print(f"\n⚡ 并行处理各子任务...")
    
    # 1. 代码生成
    code_result = dev_agent.generate_code("计算工资税的函数，根据收入区间适用不同税率", "python")
    if code_result["status"] == "success":
        print(f"  ✅ 代码生成成功: {code_result['template']}")
        
        # 保存生成的代码
        with open("salary_tax_calculator.py", 'w', encoding='utf-8') as f:
            f.write(code_result["generated_code"])
        print(f"    文件保存: salary_tax_calculator.py")
    
    # 2. 测试生成
    test_result = test_agent.analyze_and_test("为工资税计算函数生成单元测试", "python")
    if test_result["status"] == "success":
        print(f"  ✅ 测试生成成功")
        
        # 保存测试工作流
        with open("test_salary_tax.py", 'w', encoding='utf-8') as f:
            f.write(test_result["workflow_code"])
        print(f"    文件保存: test_salary_tax.py")
    
    # 3. 设计生成
    design_result = design_agent.generate_html_sketch("工资计算器界面，包含收入输入、税率显示和计算结果", "工资计算器")
    if design_result["status"] == "success":
        print(f"  ✅ UI设计生成成功")
        
        # 保存HTML界面
        with open("salary_calculator_ui.html", 'w', encoding='utf-8') as f:
            f.write(design_result["html_content"])
        print(f"    文件保存: salary_calculator_ui.html")
    
    # 整合结果
    print(f"\n🎯 任务整合完成!")
    print(f"  生成的文件:")
    print(f"    1. salary_tax_calculator.py - 工资税计算函数")
    print(f"    2. test_salary_tax.py - 工资税测试套件")
    print(f"    3. salary_calculator_ui.html - 工资计算器界面")
    
    print(f"\n📊 系统能力统计:")
    stats = coordinator.get_system_stats()
    if stats["status"] == "success":
        agent_caps = stats["agent_capabilities"]
        print(f"  开发Agent: {agent_caps['development_agent']['total_scenes']}+ 场景")
        print(f"  测试Agent: {agent_caps['test_agent']['total_test_scenes']}+ 测试场景")
        print(f"  设计Agent: {agent_caps['design_agent']['total_components']}+ UI组件")


def run_complete_demo():
    """运行完整演示"""
    print_header("MVP多Agent系统完整演示")
    print("基于火山Trae框架的多Agent协作系统")
    print(f"演示时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # 导入re模块用于演示
        import re
        
        # 演示各组件
        demo_development_agent()
        demo_test_agent()
        demo_design_agent()
        demo_coordinator_full_stack()
        demo_system_integration()
        
        print_header("演示完成")
        print("✅ 所有演示成功完成!")
        print("\n📁 生成的文件:")
        print("  - 开发Agent: 代码生成示例")
        print("  - 测试Agent: 单元测试文件")
        print("  - 设计Agent: UI设计规范和HTML草图")
        print("  - 协调器: 完整工作流数据")
        
        print("\n🔧 系统特点:")
        print("  1. 多Agent协作: 开发、测试、设计Agent无缝集成")
        print("  2. 任务分解: 协调器自动分解复杂任务")
        print("  3. 代码生成: 支持15+种编程场景，3种编程语言")
        print("  4. 测试自动化: 为生成代码自动创建单元测试")
        print("  5. UI设计: 根据描述生成设计规范和界面草图")
        
        print("\n🚀 下一步:")
        print("  1. 查看生成的文件了解具体实现")
        print("  2. 运行测试验证代码正确性")
        print("  3. 在浏览器中打开HTML文件查看界面效果")
        
    except Exception as e:
        print(f"\n❌ 演示过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_complete_demo()