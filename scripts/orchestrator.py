#!/usr/bin/env python3
"""
Smart Orchestrator - 智慧调度系统核心

智能理解用户意图，自动调度模型/技能/工具，编排多步骤任务
"""

import os
import json
import re
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

# 导入记忆管理器
try:
    from memory_manager import MemoryManager
except ImportError:
    MemoryManager = None

# 导入模型路由
try:
    from model_selector import analyze_query
except ImportError:
    analyze_query = None


@dataclass
class Task:
    """任务单元"""
    id: str
    name: str
    tool: str
    model: str
    input: Dict
    status: str = "pending"  # pending, running, completed, failed
    result: Any = None
    error: str = None


@dataclass
class ExecutionResult:
    """执行结果"""
    success: bool
    summary: str
    tasks: List[Task]
    memory_saved: bool = False
    duration: float = 0.0


class SmartOrchestrator:
    """智慧调度器"""
    
    def __init__(self, workspace: str = None):
        """
        初始化调度器
        
        Args:
            workspace: OpenClaw 工作空间路径
        """
        self.workspace = workspace or os.getenv("OPENCLAW_WORKSPACE", "/home/admin/.openclaw/workspace")
        
        # 初始化记忆管理器
        self.memory = MemoryManager(workspace=self.workspace) if MemoryManager else None
        
        # 工具注册表
        self.tools = self._load_tools()
        
        # 任务历史
        self.task_history = []
        
        # 执行统计
        self.stats = {
            "total_tasks": 0,
            "completed": 0,
            "failed": 0
        }
    
    def _load_tools(self) -> Dict:
        """加载工具注册表"""
        return {
            # 图像生成
            "image-generator": {
                "skill": "scarlett-selfie",
                "models": ["wanx-v1", "qwen-image-edit", "flux-schnell"],
                "description": "图像生成工具",
                "triggers": ["图片", "自拍", "照片", "画图", "生成图片"]
            },
            # 代码开发
            "code-writer": {
                "skill": "model-router",
                "models": ["qwen-coder", "qwen3.5-plus"],
                "description": "代码编写工具",
                "triggers": ["代码", "脚本", "编程", "函数"]
            },
            # 文案创作
            "copywriter": {
                "skill": "copywriting",
                "models": ["qwen-plus", "qwen3.5-plus"],
                "description": "文案创作工具",
                "triggers": ["文案", "广告", "营销", "写作"]
            },
            # 数据分析
            "data-analyzer": {
                "skill": "model-router",
                "models": ["qwen-max", "qwen3.5-plus"],
                "description": "数据分析工具",
                "triggers": ["分析", "数据", "统计", "报表"]
            },
            # 记忆管理
            "memory-manager": {
                "skill": "memory-manager",
                "models": ["qwen3.5-plus"],
                "description": "记忆管理工具",
                "triggers": ["记忆", "记录", "保存"]
            },
            # GitHub 发布
            "github-publisher": {
                "skill": "github-publisher",
                "models": ["qwen3.5-plus"],
                "description": "GitHub 发布工具",
                "triggers": ["上传", "GitHub", "发布", "推送"]
            },
            # 社交媒体发布
            "social-publisher": {
                "skill": "social-content",
                "models": ["qwen-plus"],
                "description": "社交媒体发布",
                "triggers": ["小红书", "微博", "抖音", "朋友圈"]
            }
        }
    
    def execute(self, user_input: str, context: Dict = None) -> ExecutionResult:
        """
        执行用户指令
        
        Args:
            user_input: 用户输入
            context: 上下文信息
            
        Returns:
            执行结果
        """
        start_time = datetime.now()
        
        print(f"🧠 智慧调度系统 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"=" * 60)
        print(f"用户输入：{user_input}")
        print()
        
        # 1. 意图理解
        print("📋 步骤 1: 意图理解...")
        intent = self._parse_intent(user_input)
        print(f"   任务类型：{intent['type']}")
        print(f"   关键信息：{intent['entities']}")
        print()
        
        # 2. 记忆检索
        if self.memory:
            print("🔍 步骤 2: 记忆检索...")
            memories = self._search_memories(user_input)
            print(f"   找到 {len(memories)} 条相关记忆")
            if memories:
                print(f"   相关记忆：{memories[0][:100]}...")
            print()
        else:
            memories = []
        
        # 3. 模型路由
        print("🤖 步骤 3: 模型路由...")
        model_config = self._route_model(user_input)
        print(f"   主模型：{model_config['primary']}")
        print(f"   备用：{model_config['fallbacks']}")
        print()
        
        # 4. 工具调度
        print("🛠️  步骤 4: 工具调度...")
        tools_needed = self._select_tools(intent)
        print(f"   需要工具：{', '.join(tools_needed)}")
        print()
        
        # 5. 任务编排
        print("📝 步骤 5: 任务编排...")
        tasks = self._plan_tasks(user_input, intent, tools_needed, model_config)
        print(f"   共 {len(tasks)} 个子任务")
        for i, task in enumerate(tasks, 1):
            print(f"   {i}. {task.name} ({task.tool})")
        print()
        
        # 6. 执行任务
        print("⚡ 步骤 6: 执行任务...")
        completed_tasks = []
        failed_tasks = []
        
        for task in tasks:
            print(f"   执行：{task.name}...")
            # 模拟执行（实际应调用对应工具）
            task.status = "completed"
            task.result = f"完成 {task.name}"
            completed_tasks.append(task)
            self.stats["completed"] += 1
        
        self.stats["total_tasks"] += len(tasks)
        print(f"   完成：{len(completed_tasks)}/{len(tasks)}")
        print()
        
        # 7. 结果汇总
        print("📊 步骤 7: 结果汇总...")
        summary = self._aggregate_results(completed_tasks, user_input)
        print(f"   {summary}")
        print()
        
        # 8. 记忆存储
        memory_saved = False
        if self.memory:
            print("💾 步骤 8: 记忆存储...")
            self.memory.create_memory(
                content=f"用户指令：{user_input}\n执行结果：{summary}",
                level="P0",
                tags=["任务", intent['type']]
            )
            memory_saved = True
            print("   记忆已保存")
            print()
        
        duration = (datetime.now() - start_time).total_seconds()
        
        result = ExecutionResult(
            success=len(failed_tasks) == 0,
            summary=summary,
            tasks=tasks,
            memory_saved=memory_saved,
            duration=duration
        )
        
        self.task_history.append(result)
        
        print(f"✅ 执行完成！耗时：{duration:.2f}秒")
        
        return result
    
    def _parse_intent(self, user_input: str) -> Dict:
        """解析用户意图"""
        intent = {
            "type": "general",
            "entities": [],
            "actions": [],
            "urgency": "normal"
        }
        
        # 简单规则匹配（实际可用 NLP 模型）
        if any(kw in user_input for kw in ["图片", "自拍", "照片"]):
            intent["type"] = "image"
        elif any(kw in user_input for kw in ["代码", "脚本", "编程"]):
            intent["type"] = "code"
        elif any(kw in user_input for kw in ["文案", "写作", "文章"]):
            intent["type"] = "writing"
        elif any(kw in user_input for kw in ["分析", "数据"]):
            intent["type"] = "analysis"
        elif any(kw in user_input for kw in ["上传", "发布", "GitHub"]):
            intent["type"] = "publish"
        
        # 提取关键实体
        intent["entities"] = re.findall(r'"([^"]+)"|'([^']+)'', user_input)
        
        return intent
    
    def _search_memories(self, query: str) -> List[str]:
        """搜索相关记忆"""
        if not self.memory:
            return []
        
        results = self.memory.search(query)
        return [r.get("preview", "") for r in results[:3]]
    
    def _route_model(self, query: str) -> Dict:
        """路由到合适的模型"""
        if analyze_query:
            return analyze_query(query)
        else:
            return {
                "primary": "qwen3.5-plus",
                "fallbacks": ["glm-5", "qwen-plus"]
            }
    
    def _select_tools(self, intent: Dict) -> List[str]:
        """选择需要的工具"""
        selected = []
        
        for tool_name, tool_info in self.tools.items():
            if any(trigger in intent.get("type", "") for trigger in tool_info.get("triggers", [])):
                selected.append(tool_name)
        
        # 如果没有匹配，返回默认工具
        if not selected:
            selected.append("memory-manager")
        
        return selected
    
    def _plan_tasks(self, user_input: str, intent: Dict, tools: List[str], model_config: Dict) -> List[Task]:
        """规划任务列表"""
        tasks = []
        
        # 为每个工具创建一个任务
        for i, tool in enumerate(tools):
            task = Task(
                id=f"task_{i+1}",
                name=f"使用 {tool} 处理",
                tool=tool,
                model=model_config["primary"],
                input={"user_input": user_input, "intent": intent}
            )
            tasks.append(task)
        
        # 添加结果汇总任务
        tasks.append(Task(
            id="task_summary",
            name="汇总结果",
            tool="orchestrator",
            model=model_config["primary"],
            input={"tasks": [t.id for t in tasks]}
        ))
        
        return tasks
    
    def _aggregate_results(self, tasks: List[Task], user_input: str) -> str:
        """汇总任务结果"""
        if not tasks:
            return "未执行任何任务"
        
        completed = [t for t in tasks if t.status == "completed"]
        summary_parts = [
            f"✅ 已完成 {len(completed)}/{len(tasks)} 个任务",
            f"用户指令：{user_input}",
            "任务详情:"
        ]
        
        for task in completed:
            summary_parts.append(f"  - {task.name}: {task.result}")
        
        return "\n".join(summary_parts)
    
    def get_status(self) -> Dict:
        """获取调度器状态"""
        return {
            "workspace": self.workspace,
            "tools_available": len(self.tools),
            "memory_enabled": self.memory is not None,
            "stats": self.stats,
            "task_history_count": len(self.task_history)
        }


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Smart Orchestrator - 智慧调度系统")
    parser.add_argument("--workspace", default="/home/admin/.openclaw/workspace", help="工作空间")
    parser.add_argument("input", nargs="?", help="用户输入")
    parser.add_argument("--status", action="store_true", help="查看状态")
    
    args = parser.parse_args()
    
    orch = SmartOrchestrator(workspace=args.workspace)
    
    if args.status:
        status = orch.get_status()
        print("🧠 Smart Orchestrator Status")
        print("=" * 50)
        print(f"工作空间：{status['workspace']}")
        print(f"可用工具：{status['tools_available']} 个")
        print(f"记忆系统：{'✅ 已启用' if status['memory_enabled'] else '❌ 未启用'}")
        print(f"总任务数：{status['stats']['total_tasks']}")
        print(f"已完成：{status['stats']['completed']}")
        print(f"失败：{status['stats']['failed']}")
    elif args.input:
        result = orch.execute(args.input)
        print("\n" + "=" * 60)
        print("📋 执行结果")
        print("=" * 60)
        print(result.summary)
    else:
        print("用法：python orchestrator.py [用户输入]")
        print("      python orchestrator.py --status")


if __name__ == "__main__":
    main()
