"""
MVP协调器实现
基于火山Trae框架的多Agent系统

功能：接收任务、分解任务、分配给开发/测试/设计Agent，并整合结果
"""

import re
import json
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum

from development_agent import DevelopmentAgent
from test_agent import TestAgent
from design_agent import DesignAgent


class TaskType(Enum):
    """任务类型枚举"""
    CODE_GENERATION = "code_generation"      # 代码生成任务
    TEST_GENERATION = "test_generation"      # 测试生成任务
    UI_DESIGN = "ui_design"                  # UI设计任务
    FULL_STACK = "full_stack"                # 全栈任务（包含代码、测试、设计）


class TaskPriority(Enum):
    """任务优先级枚举"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Task:
    """任务类"""
    
    def __init__(self, task_id: str, description: str, task_type: TaskType,
                 priority: TaskPriority = TaskPriority.MEDIUM,
                 language: str = "python", app_name: str = "我的应用"):
        """初始化任务
        
        Args:
            task_id: 任务唯一标识符
            description: 任务描述
            task_type: 任务类型
            priority: 任务优先级
            language: 目标编程语言
            app_name: 应用名称（设计任务用）
        """
        self.task_id = task_id
        self.description = description
        self.task_type = task_type
        self.priority = priority
        self.language = language
        self.app_name = app_name
        self.status = "pending"  # pending, processing, completed, failed
        self.results = {}
        self.created_at = "2026-02-16T08:53:00"
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "task_id": self.task_id,
            "description": self.description,
            "task_type": self.task_type.value,
            "priority": self.priority.value,
            "language": self.language,
            "app_name": self.app_name,
            "status": self.status,
            "results": self.results,
            "created_at": self.created_at
        }


class Coordinator:
    """MVP协调器类"""
    
    def __init__(self, coordinator_id: str = "mvp_coordinator_001"):
        """初始化协调器
        
        Args:
            coordinator_id: 协调器唯一标识符
        """
        self.coordinator_id = coordinator_id
        self.dev_agent = DevelopmentAgent()
        self.test_agent = TestAgent()
        self.design_agent = DesignAgent()
        self.task_queue = []
        self.completed_tasks = []
        self.task_counter = 0
        
    def _generate_task_id(self) -> str:
        """生成任务ID"""
        self.task_counter += 1
        return f"task_{self.task_counter:04d}"
    
    def _analyze_task_description(self, description: str) -> Tuple[TaskType, str, str]:
        """分析任务描述，确定任务类型和参数
        
        Args:
            description: 任务描述
            
        Returns:
            (任务类型, 语言, 应用名称)
        """
        desc_lower = description.lower()
        
        # 确定语言
        language = "python"
        if "javascript" in desc_lower or "js" in desc_lower:
            language = "javascript"
        elif "java" in desc_lower:
            language = "java"
        
        # 确定应用名称（从描述中提取或使用默认）
        app_name = "我的应用"
        # 简单提取：如果描述中包含"XXX应用"或"XXX系统"
        app_match = re.search(r'["\']?([^"\'\n]+)["\']?(?:应用|系统|平台)', description)
        if app_match:
            app_name = app_match.group(1)
        
        # 确定任务类型
        task_type = TaskType.CODE_GENERATION
        
        # 关键词匹配
        test_keywords = ["测试", "单元测试", "测试用例", "test", "unittest"]
        design_keywords = ["界面", "UI", "设计", "草图", "布局", "design", "ui"]
        code_keywords = ["代码", "编程", "函数", "实现", "code", "program", "function"]
        
        has_test = any(keyword in desc_lower for keyword in test_keywords)
        has_design = any(keyword in desc_lower for keyword in design_keywords)
        has_code = any(keyword in desc_lower for keyword in code_keywords)
        
        if has_test and has_design and has_code:
            task_type = TaskType.FULL_STACK
        elif has_test and has_code:
            task_type = TaskType.TEST_GENERATION
        elif has_design:
            task_type = TaskType.UI_DESIGN
        elif has_code:
            task_type = TaskType.CODE_GENERATION
        
        return task_type, language, app_name
    
    def create_task(self, description: str, priority: str = "medium") -> Dict[str, Any]:
        """创建新任务
        
        Args:
            description: 任务描述
            priority: 任务优先级
            
        Returns:
            任务信息字典
        """
        # 分析任务描述
        task_type, language, app_name = self._analyze_task_description(description)
        
        # 创建任务对象
        task_id = self._generate_task_id()
        task = Task(
            task_id=task_id,
            description=description,
            task_type=task_type,
            priority=TaskPriority(priority),
            language=language,
            app_name=app_name
        )
        
        # 加入队列
        self.task_queue.append(task)
        
        return {
            "status": "success",
            "task": task.to_dict(),
            "coordinator_id": self.coordinator_id
        }
    
    def process_task(self, task_id: str) -> Dict[str, Any]:
        """处理指定任务
        
        Args:
            task_id: 任务ID
            
        Returns:
            处理结果字典
        """
        # 查找任务
        task = None
        for t in self.task_queue:
            if t.task_id == task_id:
                task = t
                break
        
        if not task:
            return {
                "status": "error",
                "error_message": f"任务不存在: {task_id}",
                "coordinator_id": self.coordinator_id
            }
        
        # 更新状态
        task.status = "processing"
        
        try:
            # 根据任务类型处理
            if task.task_type == TaskType.CODE_GENERATION:
                result = self._process_code_generation(task)
            elif task.task_type == TaskType.TEST_GENERATION:
                result = self._process_test_generation(task)
            elif task.task_type == TaskType.UI_DESIGN:
                result = self._process_ui_design(task)
            elif task.task_type == TaskType.FULL_STACK:
                result = self._process_full_stack(task)
            else:
                result = {
                    "status": "error",
                    "error_message": f"不支持的任务类型: {task.task_type}"
                }
            
            # 保存结果
            task.results = result
            task.status = "completed"
            
            # 移动任务到完成队列
            self.task_queue.remove(task)
            self.completed_tasks.append(task)
            
            return {
                "status": "success",
                "task": task.to_dict(),
                "results": result,
                "coordinator_id": self.coordinator_id
            }
            
        except Exception as e:
            task.status = "failed"
            task.results = {"error": str(e)}
            
            return {
                "status": "error",
                "error_message": f"处理任务时发生错误: {str(e)}",
                "task": task.to_dict(),
                "coordinator_id": self.coordinator_id
            }
    
    def _process_code_generation(self, task: Task) -> Dict[str, Any]:
        """处理代码生成任务
        
        Args:
            task: 任务对象
            
        Returns:
            处理结果
        """
        # 调用开发Agent
        dev_result = self.dev_agent.generate_code(task.description, task.language)
        
        return {
            "agent_type": "development",
            "result": dev_result,
            "files_generated": ["generated_code.py"] if dev_result["status"] == "success" else []
        }
    
    def _process_test_generation(self, task: Task) -> Dict[str, Any]:
        """处理测试生成任务
        
        Args:
            task: 任务对象
            
        Returns:
            处理结果
        """
        # 先分析描述，确定要测试的代码模板
        desc_lower = task.description.lower()
        template_name = None
        
        # 简单的模板名称提取
        templates = self.dev_agent.get_supported_scenes()["scene_names"]
        for template in templates:
            if template.lower() in desc_lower:
                template_name = template
                break
        
        if not template_name:
            # 如果无法确定，使用默认模板
            template_name = "calculate_average"
        
        # 调用测试Agent
        test_result = self.test_agent.generate_test_code(template_name, task.language)
        
        # 如果测试生成成功，同时生成对应的代码
        if test_result["status"] == "success":
            dev_result = self.dev_agent.generate_code(template_name, task.language)
            
            return {
                "agent_type": "test",
                "test_result": test_result,
                "code_result": dev_result,
                "files_generated": ["generated_code.py", "test_generated_code.py"]
            }
        else:
            return {
                "agent_type": "test",
                "test_result": test_result,
                "files_generated": []
            }
    
    def _process_ui_design(self, task: Task) -> Dict[str, Any]:
        """处理UI设计任务
        
        Args:
            task: 任务对象
            
        Returns:
            处理结果
        """
        # 调用设计Agent
        design_result = self.design_agent.generate_design_spec(task.description, task.app_name)
        
        # 同时生成HTML草图
        html_result = self.design_agent.generate_html_sketch(task.description, task.app_name)
        
        return {
            "agent_type": "design",
            "design_result": design_result,
            "html_result": html_result,
            "files_generated": [
                f"design_spec_{task.app_name}.json",
                f"ui_sketch_{task.app_name}.html"
            ] if design_result["status"] == "success" else []
        }
    
    def _process_full_stack(self, task: Task) -> Dict[str, Any]:
        """处理全栈任务（包含代码、测试、设计）
        
        Args:
            task: 任务对象
            
        Returns:
            处理结果
        """
        # 分解任务描述，提取各部分
        desc_lower = task.description.lower()
        
        # 提取代码部分描述（假设）
        code_desc = task.description
        test_desc = "为生成的代码创建单元测试"
        design_desc = f"为{task.app_name}设计用户界面"
        
        # 并行处理（简化版本，实际串行处理）
        # 1. 代码生成
        dev_result = self.dev_agent.generate_code(code_desc, task.language)
        
        # 2. 测试生成（基于代码模板）
        template_name = None
        if dev_result["status"] == "success":
            template_name = dev_result["template"]
            test_result = self.test_agent.generate_test_code(template_name, task.language)
        else:
            test_result = {"status": "error", "error_message": "代码生成失败，无法生成测试"}
        
        # 3. 设计生成
        design_result = self.design_agent.generate_design_spec(design_desc, task.app_name)
        html_result = self.design_agent.generate_html_sketch(design_desc, task.app_name)
        
        # 整合结果
        return {
            "agent_type": "full_stack",
            "code_generation": dev_result,
            "test_generation": test_result,
            "ui_design": {
                "design": design_result,
                "html": html_result
            },
            "files_generated": [
                "generated_code.py",
                "test_generated_code.py",
                f"design_spec_{task.app_name}.json",
                f"ui_sketch_{task.app_name}.html"
            ] if all(r["status"] == "success" for r in [dev_result, test_result, design_result]) else []
        }
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """获取任务状态
        
        Args:
            task_id: 任务ID
            
        Returns:
            任务状态信息
        """
        # 在队列中查找
        for task in self.task_queue:
            if task.task_id == task_id:
                return {
                    "status": "success",
                    "task": task.to_dict(),
                    "coordinator_id": self.coordinator_id
                }
        
        # 在完成队列中查找
        for task in self.completed_tasks:
            if task.task_id == task_id:
                return {
                    "status": "success",
                    "task": task.to_dict(),
                    "coordinator_id": self.coordinator_id
                }
        
        return {
            "status": "error",
            "error_message": f"任务不存在: {task_id}",
            "coordinator_id": self.coordinator_id
        }
    
    def list_tasks(self, status_filter: str = None) -> Dict[str, Any]:
        """列出所有任务
        
        Args:
            status_filter: 状态过滤条件
            
        Returns:
            任务列表
        """
        all_tasks = []
        
        # 添加待处理任务
        for task in self.task_queue:
            task_dict = task.to_dict()
            task_dict["queue_position"] = self.task_queue.index(task)
            all_tasks.append(task_dict)
        
        # 添加已完成任务
        for task in self.completed_tasks:
            task_dict = task.to_dict()
            task_dict["completion_time"] = "2026-02-16T09:00:00"  # 简化处理
            all_tasks.append(task_dict)
        
        # 状态过滤
        if status_filter:
            filtered_tasks = [t for t in all_tasks if t["status"] == status_filter]
        else:
            filtered_tasks = all_tasks
        
        return {
            "status": "success",
            "total_tasks": len(all_tasks),
            "filtered_tasks": len(filtered_tasks),
            "tasks": filtered_tasks,
            "coordinator_id": self.coordinator_id
        }
    
    def get_system_stats(self) -> Dict[str, Any]:
        """获取系统统计信息
        
        Returns:
            统计信息字典
        """
        # 获取各Agent的支持能力
        dev_stats = self.dev_agent.get_supported_scenes()
        test_stats = self.test_agent.get_supported_test_scenes()
        design_stats = self.design_agent.get_supported_components()
        
        return {
            "status": "success",
            "coordinator_id": self.coordinator_id,
            "task_statistics": {
                "pending": len([t for t in self.task_queue if t.status == "pending"]),
                "processing": len([t for t in self.task_queue if t.status == "processing"]),
                "completed": len(self.completed_tasks),
                "failed": len([t for t in self.completed_tasks if t.status == "failed"])
            },
            "agent_capabilities": {
                "development_agent": {
                    "total_scenes": dev_stats["total_scenes"],
                    "supported_languages": dev_stats["supported_languages"]
                },
                "test_agent": {
                    "total_test_scenes": test_stats["total_test_scenes"],
                    "supported_languages": test_stats["supported_languages"]
                },
                "design_agent": {
                    "total_components": design_stats["total_components"],
                    "total_layouts": design_stats["total_layouts"],
                    "total_color_palettes": design_stats["total_color_palettes"]
                }
            }
        }


if __name__ == "__main__":
    # 简单的命令行交互
    coordinator = Coordinator()
    print("MVP协调器已启动")
    print("支持的任务类型: 代码生成、测试生成、UI设计、全栈任务")
    
    while True:
        print("\n" + "=" * 60)
        print("1. 创建新任务")
        print("2. 处理任务")
        print("3. 查看任务状态")
        print("4. 列出所有任务")
        print("5. 查看系统统计")
        print("6. 退出")
        
        choice = input("请选择操作 (1-6): ")
        
        if choice == "1":
            description = input("请输入任务描述: ")
            priority = input("请输入优先级 (low/medium/high/critical, 默认medium): ") or "medium"
            
            result = coordinator.create_task(description, priority)
            
            if result["status"] == "success":
                task = result["task"]
                print(f"\n✅ 任务创建成功!")
                print(f"任务ID: {task['task_id']}")
                print(f"任务类型: {task['task_type']}")
                print(f"优先级: {task['priority']}")
                print(f"语言: {task['language']}")
                print(f"应用名称: {task['app_name']}")
            else:
                print(f"\n❌ 任务创建失败: {result.get('error_message', '未知错误')}")
                
        elif choice == "2":
            task_id = input("请输入要处理的任务ID: ")
            
            print(f"正在处理任务 {task_id}...")
            result = coordinator.process_task(task_id)
            
            if result["status"] == "success":
                task = result["task"]
                print(f"\n✅ 任务处理完成!")
                print(f"任务状态: {task['status']}")
                print(f"生成文件: {result.get('results', {}).get('files_generated', [])}")
                
                # 显示部分结果
                if "results" in result:
                    print("\n处理结果摘要:")
                    for key, value in result["results"].items():
                        if key != "files_generated":
                            print(f"  {key}: {value.get('status', 'N/A')}")
            else:
                print(f"\n❌ 任务处理失败: {result.get('error_message', '未知错误')}")
                
        elif choice == "3":
            task_id = input("请输入任务ID: ")
            
            result = coordinator.get_task_status(task_id)
            
            if result["status"] == "success":
                task = result["task"]
                print(f"\n任务状态:")
                print(f"任务ID: {task['task_id']}")
                print(f"描述: {task['description']}")
                print(f"类型: {task['task_type']}")
                print(f"状态: {task['status']}")
                print(f"创建时间: {task['created_at']}")
                
                if task["status"] == "completed" and task["results"]:
                    print(f"结果文件: {task['results'].get('files_generated', [])}")
            else:
                print(f"\n❌ 查询失败: {result.get('error_message', '未知错误')}")
                
        elif choice == "4":
            status_filter = input("请输入状态过滤 (pending/processing/completed/failed, 默认全部): ")
            if not status_filter:
                status_filter = None
            
            result = coordinator.list_tasks(status_filter)
            
            if result["status"] == "success":
                print(f"\n任务列表 (共{result['total_tasks']}个, 过滤后{result['filtered_tasks']}个):")
                
                if result["tasks"]:
                    for task in result["tasks"]:
                        print(f"\n  ID: {task['task_id']}")
                        print(f"  描述: {task['description'][:50]}...")
                        print(f"  类型: {task['task_type']}, 状态: {task['status']}")
                        
                        if "queue_position" in task:
                            print(f"  队列位置: {task['queue_position']}")
                else:
                    print("  没有符合条件的任务")
            else:
                print(f"\n❌ 查询失败: {result.get('error_message', '未知错误')}")
                
        elif choice == "5":
            result = coordinator.get_system_stats()
            
            if result["status"] == "success":
                stats = result
                print(f"\n📊 系统统计信息:")
                print(f"协调器ID: {stats['coordinator_id']}")
                
                print(f"\n任务统计:")
                task_stats = stats['task_statistics']
                print(f"  待处理: {task_stats['pending']}")
                print(f"  处理中: {task_stats['processing']}")
                print(f"  已完成: {task_stats['completed']}")
                print(f"  已失败: {task_stats['failed']}")
                
                print(f"\nAgent能力:")
                agent_caps = stats['agent_capabilities']
                dev_cap = agent_caps['development_agent']
                test_cap = agent_caps['test_agent']
                design_cap = agent_caps['design_agent']
                
                print(f"  开发Agent: {dev_cap['total_scenes']}种场景, 支持{len(dev_cap['supported_languages'])}种语言")
                print(f"  测试Agent: {test_cap['total_test_scenes']}种测试场景")
                print(f"  设计Agent: {design_cap['total_components']}种组件, {design_cap['total_layouts']}种布局")
                
            else:
                print(f"\n❌ 查询失败: {result.get('error_message', '未知错误')}")
                
        elif choice == "6":
            print("退出协调器")
            break
        else:
            print("无效选择，请重试")