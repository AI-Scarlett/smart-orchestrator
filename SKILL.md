---
name: smart-orchestrator
description: 智慧调度系统。智能理解用户意图，自动调度模型/技能/工具，编排多步骤任务，汇总结果反馈。
---

# Smart Orchestrator - 智慧调度系统

## 核心理念

**一句话，全自动** - 用户只需说一句话，系统自动：
1. 理解意图
2. 检索记忆
3. 选择模型
4. 调度工具
5. 编排执行
6. 汇总反馈

## 系统架构

```
用户输入
    ↓
┌─────────────────────────────────┐
│  1. 意图理解 (Intent Parser)   │
│     - 任务类型识别              │
│     - 关键信息提取              │
│     - 上下文关联                │
└─────────────┬───────────────────┘
              ↓
┌─────────────────────────────────┐
│  2. 记忆检索 (Memory Search)    │
│     - 相关记忆查询              │
│     - 用户偏好加载              │
│     - 历史任务参考              │
└─────────────┬───────────────────┘
              ↓
┌─────────────────────────────────┐
│  3. 模型路由 (Model Router)     │
│     - 场景识别                  │
│     - 模型选择 (1 主 +2 备)      │
│     - 成本优化                  │
└─────────────┬───────────────────┘
              ↓
┌─────────────────────────────────┐
│  4. 工具调度 (Tool Dispatcher)  │
│     - 技能选择                  │
│     - 工具调用                  │
│     - 并行/串行编排             │
└─────────────┬───────────────────┘
              ↓
┌─────────────────────────────────┐
│  5. 执行监控 (Task Monitor)     │
│     - 进度跟踪                  │
│     - 错误处理                  │
│     - 降级策略                  │
└─────────────┬───────────────────┘
              ↓
┌─────────────────────────────────┐
│  6. 结果汇总 (Result Aggregator)│
│     - 多源结果整合              │
│     - 格式化输出                │
│     - 记忆存储                  │
└─────────────────────────────────┘
```

## 使用方式

### 命令行

```bash
python scripts/orchestrator.py "帮我写个 Python 脚本分析 Excel 数据，然后生成报告"
```

### Python 调用

```python
from orchestrator import SmartOrchestrator

orch = SmartOrchestrator()
result = orch.execute("帮我安排明天的会议，并准备相关材料")
print(result.summary)
```

## 任务编排示例

### 示例 1: 数据分析任务
**用户**: "分析这个月的销售数据，生成报告并发到群里"

**系统调度**:
1. 记忆检索 → 查找销售数据文件位置
2. 模型选择 → qwen-max (数据分析)
3. 工具调用 → data-analyzer 技能
4. 模型选择 → qwen-plus (报告写作)
5. 工具调用 → report-generator
6. 消息发送 → qqbot/telegram

### 示例 2: 内容创作任务
**用户**: "写个营销文案，配张图，发到小红书"

**系统调度**:
1. 模型选择 → qwen-plus (文案创作)
2. 工具调用 → copywriting-skill
3. 模型选择 → wanx-v1 (图像生成)
4. 工具调用 → image-generator
5. 工具调用 → xiaohongshu-publisher

## 文件结构

```
smart-orchestrator/
├── SKILL.md
├── README.md
├── scripts/
│   ├── orchestrator.py       # 核心编排器
│   ├── intent_parser.py      # 意图识别
│   └── task_planner.py       # 任务规划
├── tools/
│   ├── tool_registry.py      # 工具注册表
│   └── executors/            # 执行器
└── references/
    └── orchestration-guide.md
```

## 配置

### 工具注册

在 `tools/tool_registry.py` 中注册可用工具：

```python
TOOLS = {
    "image-generator": {
        "skill": "scarlett-selfie",
        "models": ["wanx-v1", "qwen-image-edit"],
        "endpoint": "generate_image"
    },
    "code-writer": {
        "skill": "model-router",
        "models": ["qwen-coder"],
        "endpoint": "write_code"
    }
}
```

### 模型路由集成

自动集成 `model-router` skill 的 8 大场景配置。

### 记忆系统集成

自动集成 `memory-manager` skill 的分层记忆。

## 许可证

MIT License

## 作者

丝佳丽 Scarlett - AI Love World 项目
