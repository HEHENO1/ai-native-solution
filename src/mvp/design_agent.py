"""
MVP设计Agent实现
基于火山Trae框架的多Agent系统

功能：根据自然语言描述生成UI设计规范或界面草图
"""

import re
import json
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum


class UIComponent(Enum):
    """UI组件类型枚举"""
    HEADER = "header"
    FOOTER = "footer"
    NAVIGATION = "navigation"
    SIDEBAR = "sidebar"
    MAIN_CONTENT = "main_content"
    CARD = "card"
    BUTTON = "button"
    FORM = "form"
    TABLE = "table"
    LIST = "list"
    MODAL = "modal"
    CHART = "chart"
    SEARCH_BAR = "search_bar"


class ColorScheme:
    """颜色方案类"""
    
    def __init__(self, primary: str = "#3366CC", secondary: str = "#FF9933", 
                 background: str = "#FFFFFF", text: str = "#333333"):
        self.primary = primary
        self.secondary = secondary
        self.background = background
        self.text = text
    
    def to_dict(self) -> Dict[str, str]:
        """转换为字典"""
        return {
            "primary": self.primary,
            "secondary": self.secondary,
            "background": self.background,
            "text": self.text
        }


class DesignAgent:
    """MVP设计Agent类"""
    
    def __init__(self, agent_id: str = "mvp_design_agent_001"):
        """初始化设计Agent
        
        Args:
            agent_id: Agent唯一标识符
        """
        self.agent_id = agent_id
        self.component_templates = self._load_component_templates()
        self.layout_templates = self._load_layout_templates()
        self.color_palettes = self._load_color_palettes()
        
    def _load_component_templates(self) -> Dict[str, Dict[str, Any]]:
        """加载UI组件模板
        
        Returns:
            组件类型到模板内容的映射
        """
        templates = {}
        
        # 1. 头部模板
        templates[UIComponent.HEADER.value] = {
            "description": "页面顶部区域，通常包含logo、导航和用户信息",
            "html_template": """<header style="background-color: {primary_color}; color: white; padding: 16px;">
  <div style="display: flex; justify-content: space-between; align-items: center;">
    <div style="font-size: 24px; font-weight: bold;">{app_name}</div>
    <nav>
      <ul style="display: flex; list-style: none; gap: 20px;">
        <li><a href="#" style="color: white; text-decoration: none;">首页</a></li>
        <li><a href="#" style="color: white; text-decoration: none;">产品</a></li>
        <li><a href="#" style="color: white; text-decoration: none;">关于</a></li>
        <li><a href="#" style="color: white; text-decoration: none;">联系</a></li>
      </ul>
    </nav>
    <div>{user_info}</div>
  </div>
</header>""",
            "design_spec": {
                "height": "64px",
                "background_color": "primary_color",
                "text_color": "#FFFFFF",
                "padding": "16px",
                "components": ["logo", "navigation", "user_info"]
            }
        }
        
        # 2. 底部模板
        templates[UIComponent.FOOTER.value] = {
            "description": "页面底部区域，通常包含版权信息和链接",
            "html_template": """<footer style="background-color: #2C3E50; color: white; padding: 32px; margin-top: 40px;">
  <div style="max-width: 1200px; margin: 0 auto;">
    <div style="display: flex; justify-content: space-between;">
      <div>
        <h3 style="margin-bottom: 16px;">{app_name}</h3>
        <p>© {year} {app_name}. 保留所有权利.</p>
      </div>
      <div>
        <h4 style="margin-bottom: 16px;">快速链接</h4>
        <ul style="list-style: none;">
          <li><a href="#" style="color: #95A5A6; text-decoration: none;">隐私政策</a></li>
          <li><a href="#" style="color: #95A5A6; text-decoration: none;">服务条款</a></li>
          <li><a href="#" style="color: #95A5A6; text-decoration: none;">帮助中心</a></li>
        </ul>
      </div>
    </div>
  </div>
</footer>""",
            "design_spec": {
                "background_color": "#2C3E50",
                "text_color": "#FFFFFF",
                "padding": "32px",
                "components": ["copyright", "quick_links", "social_media"]
            }
        }
        
        # 3. 卡片模板
        templates[UIComponent.CARD.value] = {
            "description": "内容容器，用于展示相关信息块",
            "html_template": """<div style="background-color: white; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); padding: 24px; margin-bottom: 20px;">
  <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 16px;">
    <h3 style="margin: 0; color: {primary_color};">{card_title}</h3>
    {badge}
  </div>
  <div style="color: #666; line-height: 1.6;">
    {card_content}
  </div>
  <div style="margin-top: 20px;">
    {actions}
  </div>
</div>""",
            "design_spec": {
                "background_color": "#FFFFFF",
                "border_radius": "8px",
                "box_shadow": "0 2px 8px rgba(0,0,0,0.1)",
                "padding": "24px",
                "components": ["title", "content", "actions"]
            }
        }
        
        # 4. 按钮模板
        templates[UIComponent.BUTTON.value] = {
            "description": "交互按钮，用于触发操作",
            "html_template": """<button style="background-color: {primary_color}; color: white; border: none; border-radius: 4px; padding: 10px 20px; font-size: 14px; cursor: pointer; transition: background-color 0.3s;">
  {button_text}
</button>
<style>
button:hover {{
  background-color: {hover_color};
}}
</style>""",
            "design_spec": {
                "background_color": "primary_color",
                "text_color": "#FFFFFF",
                "border_radius": "4px",
                "padding": "10px 20px",
                "states": ["default", "hover", "active", "disabled"]
            }
        }
        
        # 5. 表单模板
        templates[UIComponent.FORM.value] = {
            "description": "数据输入表单，用于收集用户信息",
            "html_template": """<form style="background-color: white; padding: 24px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
  <h3 style="margin-bottom: 24px; color: {primary_color};">{form_title}</h3>
  
  <div style="margin-bottom: 16px;">
    <label style="display: block; margin-bottom: 8px; color: #555;">用户名</label>
    <input type="text" style="width: 100%; padding: 10px; border: 1px solid #DDD; border-radius: 4px;">
  </div>
  
  <div style="margin-bottom: 16px;">
    <label style="display: block; margin-bottom: 8px; color: #555;">邮箱</label>
    <input type="email" style="width: 100%; padding: 10px; border: 1px solid #DDD; border-radius: 4px;">
  </div>
  
  <div style="margin-bottom: 24px;">
    <label style="display: block; margin-bottom: 8px; color: #555;">消息</label>
    <textarea style="width: 100%; padding: 10px; border: 1px solid #DDD; border-radius: 4px; min-height: 100px;"></textarea>
  </div>
  
  <button type="submit" style="background-color: {primary_color}; color: white; border: none; border-radius: 4px; padding: 12px 24px; font-size: 16px; cursor: pointer;">
    提交
  </button>
</form>""",
            "design_spec": {
                "background_color": "#FFFFFF",
                "padding": "24px",
                "border_radius": "8px",
                "input_styles": {
                    "border": "1px solid #DDD",
                    "border_radius": "4px",
                    "padding": "10px"
                }
            }
        }
        
        return templates
    
    def _load_layout_templates(self) -> Dict[str, Dict[str, Any]]:
        """加载布局模板
        
        Returns:
            布局名称到模板内容的映射
        """
        templates = {}
        
        # 1. 单栏布局
        templates["single_column"] = {
            "description": "简单单栏布局，适合内容展示页",
            "html_template": """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{app_name}</title>
  <style>
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background-color: {background_color};
      color: {text_color};
    }}
    .container {{
      max-width: 1200px;
      margin: 0 auto;
      padding: 20px;
    }}
  </style>
</head>
<body>
  {header}
  
  <div class="container">
    {main_content}
  </div>
  
  {footer}
</body>
</html>""",
            "design_spec": {
                "type": "single_column",
                "max_width": "1200px",
                "sections": ["header", "main_content", "footer"],
                "responsive": True
            }
        }
        
        # 2. 两栏布局
        templates["two_column"] = {
            "description": "侧边栏加主内容的两栏布局",
            "html_template": """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{app_name}</title>
  <style>
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background-color: {background_color};
      color: {text_color};
    }}
    .container {{
      max-width: 1200px;
      margin: 0 auto;
      padding: 20px;
      display: flex;
      gap: 30px;
    }}
    .sidebar {{
      flex: 0 0 250px;
    }}
    .main-content {{
      flex: 1;
    }}
    @media (max-width: 768px) {{
      .container {{
        flex-direction: column;
      }}
      .sidebar {{
        width: 100%;
      }}
    }}
  </style>
</head>
<body>
  {header}
  
  <div class="container">
    <div class="sidebar">
      {sidebar_content}
    </div>
    <div class="main-content">
      {main_content}
    </div>
  </div>
  
  {footer}
</body>
</html>""",
            "design_spec": {
                "type": "two_column",
                "sidebar_width": "250px",
                "sections": ["header", "sidebar", "main_content", "footer"],
                "responsive": True,
                "mobile_layout": "single_column"
            }
        }
        
        # 3. 仪表板布局
        templates["dashboard"] = {
            "description": "多卡片网格布局，适合数据仪表板",
            "html_template": """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{app_name}</title>
  <style>
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background-color: {background_color};
      color: {text_color};
    }}
    .container {{
      max-width: 1400px;
      margin: 0 auto;
      padding: 20px;
    }}
    .dashboard-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 20px;
      margin-top: 20px;
    }}
  </style>
</head>
<body>
  {header}
  
  <div class="container">
    <h2 style="margin-bottom: 20px;">{dashboard_title}</h2>
    <div class="dashboard-grid">
      {dashboard_cards}
    </div>
  </div>
  
  {footer}
</body>
</html>""",
            "design_spec": {
                "type": "dashboard",
                "grid_columns": "responsive",
                "card_min_width": "300px",
                "sections": ["header", "dashboard_title", "dashboard_grid", "footer"],
                "responsive": True
            }
        }
        
        return templates
    
    def _load_color_palettes(self) -> Dict[str, ColorScheme]:
        """加载颜色调色板
        
        Returns:
            调色板名称到颜色方案的映射
        """
        palettes = {}
        
        # 1. 专业蓝
        palettes["professional_blue"] = ColorScheme(
            primary="#3366CC",
            secondary="#FF9933",
            background="#F5F7FA",
            text="#333333"
        )
        
        # 2. 现代绿
        palettes["modern_green"] = ColorScheme(
            primary="#28A745",
            secondary="#FFC107",
            background="#FFFFFF",
            text="#212529"
        )
        
        # 3. 深色模式
        palettes["dark_mode"] = ColorScheme(
            primary="#0D6EFD",
            secondary="#6C757D",
            background="#212529",
            text="#F8F9FA"
        )
        
        # 4. 活力橙
        palettes["vibrant_orange"] = ColorScheme(
            primary="#FD7E14",
            secondary="#20C997",
            background="#FFFFFF",
            text="#343A40"
        )
        
        return palettes
    
    def generate_design_spec(self, description: str, app_name: str = "我的应用") -> Dict[str, Any]:
        """根据描述生成UI设计规范
        
        Args:
            description: 自然语言描述
            app_name: 应用名称
            
        Returns:
            包含设计规范的字典
        """
        # 分析描述中的关键词
        desc_lower = description.lower()
        
        # 确定布局类型
        layout_type = "single_column"
        if "仪表板" in desc_lower or "dashboard" in desc_lower:
            layout_type = "dashboard"
        elif "侧边栏" in desc_lower or "两栏" in desc_lower or "sidebar" in desc_lower:
            layout_type = "two_column"
        
        # 确定颜色方案
        color_scheme = "professional_blue"
        if "深色" in desc_lower or "dark" in desc_lower:
            color_scheme = "dark_mode"
        elif "绿色" in desc_lower or "green" in desc_lower:
            color_scheme = "modern_green"
        elif "橙色" in desc_lower or "orange" in desc_lower:
            color_scheme = "vibrant_orange"
        
        # 确定需要的组件
        components_needed = []
        component_keywords = {
            "header": ["头部", "导航", "header", "top"],
            "footer": ["底部", "页脚", "footer", "bottom"],
            "card": ["卡片", "card", "区块", "模块"],
            "button": ["按钮", "button", "点击", "操作"],
            "form": ["表单", "输入", "form", "提交"]
        }
        
        for comp_name, keywords in component_keywords.items():
            for keyword in keywords:
                if keyword in desc_lower:
                    components_needed.append(comp_name)
                    break
        
        # 去重
        components_needed = list(set(components_needed))
        
        # 获取颜色方案实例
        colors = self.color_palettes[color_scheme]
        
        # 构建设计规范
        design_spec = {
            "app_name": app_name,
            "layout": self.layout_templates[layout_type]["design_spec"],
            "color_scheme": colors.to_dict(),
            "components": components_needed,
            "typography": {
                "font_family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
                "base_size": "16px",
                "heading_sizes": {
                    "h1": "2.5rem",
                    "h2": "2rem",
                    "h3": "1.5rem",
                    "h4": "1.25rem"
                }
            },
            "spacing": {
                "unit": "8px",
                "small": "8px",
                "medium": "16px",
                "large": "24px",
                "xlarge": "32px"
            },
            "border_radius": {
                "small": "4px",
                "medium": "8px",
                "large": "12px"
            }
        }
        
        return {
            "status": "success",
            "design_spec": design_spec,
            "agent_id": self.agent_id
        }
    
    def generate_html_sketch(self, description: str, app_name: str = "我的应用") -> Dict[str, Any]:
        """根据描述生成HTML界面草图
        
        Args:
            description: 自然语言描述
            app_name: 应用名称
            
        Returns:
            包含HTML代码的字典
        """
        # 生成设计规范
        design_result = self.generate_design_spec(description, app_name)
        
        if design_result["status"] != "success":
            return design_result
        
        design_spec = design_result["design_spec"]
        layout_type = design_spec["layout"]["type"]
        colors = design_spec["color_scheme"]
        components = design_spec["components"]
        
        # 获取布局模板
        layout_template = self.layout_templates[layout_type]["html_template"]
        
        # 构建组件HTML
        components_html = {}
        
        if "header" in components:
            header_template = self.component_templates["header"]["html_template"]
            components_html["header"] = header_template.format(
                primary_color=colors["primary"],
                app_name=app_name,
                user_info="<span>欢迎，用户</span>"
            )
        else:
            components_html["header"] = ""
        
        if "footer" in components:
            footer_template = self.component_templates["footer"]["html_template"]
            components_html["footer"] = footer_template.format(
                app_name=app_name,
                year="2026"
            )
        else:
            components_html["footer"] = ""
        
        # 构建主内容
        main_content = ""
        if "card" in components:
            card_template = self.component_templates["card"]["html_template"]
            main_content += card_template.format(
                primary_color=colors["primary"],
                card_title="示例卡片",
                badge="<span style='background-color: #28A745; color: white; padding: 4px 8px; border-radius: 12px; font-size: 12px;'>新</span>",
                card_content="这是一个示例卡片内容，用于展示设计效果。",
                actions="<button style='background-color: #3366CC; color: white; border: none; border-radius: 4px; padding: 8px 16px; margin-right: 8px;'>操作1</button><button style='background-color: #6C757D; color: white; border: none; border-radius: 4px; padding: 8px 16px;'>操作2</button>"
            )
        
        if "form" in components:
            form_template = self.component_templates["form"]["html_template"]
            main_content += form_template.format(
                primary_color=colors["primary"],
                form_title="示例表单"
            )
        
        # 如果没有具体内容，添加默认内容
        if not main_content:
            main_content = f"""
            <div style="text-align: center; padding: 60px 20px;">
              <h1 style="color: {colors['primary']};">欢迎使用 {app_name}</h1>
              <p style="color: #666; font-size: 18px; max-width: 600px; margin: 20px auto;">
                这是一个根据您的描述生成的界面草图，展示了基本的布局和设计元素。
              </p>
              <div style="margin-top: 30px;">
                <button style="background-color: {colors['primary']}; color: white; border: none; border-radius: 6px; padding: 12px 24px; font-size: 16px; margin-right: 10px;">
                  开始使用
                </button>
                <button style="background-color: #6C757D; color: white; border: none; border-radius: 6px; padding: 12px 24px; font-size: 16px;">
                  了解更多
                </button>
              </div>
            </div>
            """
        
        # 替换布局模板中的变量
        html_content = layout_template.format(
            app_name=app_name,
            background_color=colors["background"],
            text_color=colors["text"],
            primary_color=colors["primary"],
            header=components_html.get("header", ""),
            main_content=main_content,
            footer=components_html.get("footer", ""),
            sidebar_content="<h3>侧边栏</h3><p>这是侧边栏内容区域。</p>",
            dashboard_title="数据仪表板",
            dashboard_cards="""<div class="card">卡片1</div>
<div class="card">卡片2</div>
<div class="card">卡片3</div>
<div class="card">卡片4</div>"""
        )
        
        return {
            "status": "success",
            "html_content": html_content,
            "design_spec": design_spec,
            "agent_id": self.agent_id
        }
    
    def get_supported_components(self) -> Dict[str, List[str]]:
        """获取支持的UI组件列表
        
        Returns:
            组件统计信息
        """
        component_count = len(self.component_templates)
        layout_count = len(self.layout_templates)
        palette_count = len(self.color_palettes)
        
        return {
            "total_components": component_count,
            "total_layouts": layout_count,
            "total_color_palettes": palette_count,
            "component_names": list(self.component_templates.keys()),
            "layout_names": list(self.layout_templates.keys()),
            "color_palette_names": list(self.color_palettes.keys()),
            "agent_id": self.agent_id
        }


if __name__ == "__main__":
    # 简单的命令行交互
    agent = DesignAgent()
    print("MVP设计Agent已启动")
    stats = agent.get_supported_components()
    print(f"支持 {stats['total_components']} 种UI组件")
    print(f"支持 {stats['total_layouts']} 种布局方案")
    print(f"支持 {stats['total_color_palettes']} 种颜色调色板")
    
    while True:
        print("\n" + "=" * 50)
        print("1. 生成UI设计规范")
        print("2. 生成HTML界面草图")
        print("3. 查看支持的组件")
        print("4. 退出")
        
        choice = input("请选择操作 (1-4): ")
        
        if choice == "1":
            description = input("请输入界面描述: ")
            app_name = input("请输入应用名称 (默认'我的应用'): ") or "我的应用"
            
            result = agent.generate_design_spec(description, app_name)
            
            if result["status"] == "success":
                print("\n✅ 设计规范生成成功！")
                design_spec = result["design_spec"]
                
                print(f"\n应用名称: {design_spec['app_name']}")
                print(f"布局类型: {design_spec['layout']['type']}")
                print("\n颜色方案:")
                for color_name, color_value in design_spec['color_scheme'].items():
                    print(f"  {color_name}: {color_value}")
                
                print(f"\n所需组件: {', '.join(design_spec['components'])}")
                
                # 保存设计规范
                with open(f"design_spec_{design_spec['app_name']}.json", 'w', encoding='utf-8') as f:
                    json.dump(design_spec, f, ensure_ascii=False, indent=2)
                print(f"设计规范已保存到: design_spec_{design_spec['app_name']}.json")
                
            else:
                print(f"\n❌ 生成失败: {result.get('error_message', '未知错误')}")
                
        elif choice == "2":
            description = input("请输入界面描述: ")
            app_name = input("请输入应用名称 (默认'我的应用'): ") or "我的应用"
            
            result = agent.generate_html_sketch(description, app_name)
            
            if result["status"] == "success":
                print("\n✅ HTML界面草图生成成功！")
                
                # 保存HTML文件
                html_filename = f"ui_sketch_{app_name}.html"
                with open(html_filename, 'w', encoding='utf-8') as f:
                    f.write(result["html_content"])
                
                print(f"HTML文件已保存到: {html_filename}")
                print("\n预览提示: 您可以在浏览器中打开该文件查看界面效果")
                
                # 显示部分HTML代码
                html_preview = result["html_content"][:500]
                print(f"\nHTML代码预览 (前500字符):")
                print("-" * 60)
                print(html_preview + "..." if len(result["html_content"]) > 500 else html_preview)
                print("-" * 60)
                
            else:
                print(f"\n❌ 生成失败: {result.get('error_message', '未知错误')}")
                
        elif choice == "3":
            stats = agent.get_supported_components()
            print(f"\n支持的UI组件 ({stats['total_components']}种):")
            for i, comp in enumerate(stats["component_names"], 1):
                print(f"  {i}. {comp}")
            
            print(f"\n支持的布局方案 ({stats['total_layouts']}种):")
            for i, layout in enumerate(stats["layout_names"], 1):
                print(f"  {i}. {layout}")
            
            print(f"\n支持的颜色调色板 ({stats['total_color_palette_names']}种):")
            for i, palette in enumerate(stats["color_palette_names"], 1):
                print(f"  {i}. {palette}")
                
        elif choice == "4":
            print("退出设计Agent")
            break
        else:
            print("无效选择，请重试")