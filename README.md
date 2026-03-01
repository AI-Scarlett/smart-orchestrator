# Smart Orchestrator

🧠 智慧调度系统 - 一句话，全自动完成任务

## 功能

- ✅ 智能意图理解
- ✅ 记忆检索关联
- ✅ 模型自动路由
- ✅ 工具智能调度
- ✅ 多步骤任务编排
- ✅ 结果自动汇总

## 安装

```bash
cd /home/admin/.openclaw/skills/
git clone https://github.com/AI-Scarlett/smart-orchestrator.git
```

## 快速开始

### 命令行

```bash
# 执行任务
python scripts/orchestrator.py "帮我写个 Python 脚本分析 Excel 数据"

# 查看状态
python scripts/orchestrator.py --status
```

### Python 调用

```python
from orchestrator import SmartOrchestrator

orch = SmartOrchestrator()
result = orch.execute("帮我安排明天的会议，并准备相关材料")
print(result.summary)
```

## 系统架构

```
用户输入 → 意图理解 → 记忆检索 → 模型路由 → 工具调度 → 执行监控 → 结果汇总
```

## 可用工具

| 工具 | 用途 | 触发词 |
|------|------|--------|
| image-generator | 图像生成 | 图片、自拍、照片 |
| code-writer | 代码编写 | 代码、脚本、编程 |
| copywriter | 文案创作 | 文案、广告、营销 |
| data-analyzer | 数据分析 | 分析、数据、统计 |
| memory-manager | 记忆管理 | 记忆、记录、保存 |
| github-publisher | GitHub 发布 | 上传、GitHub、发布 |
| social-publisher | 社交媒体 | 小红书、微博、抖音 |

## 示例

### 示例 1: 数据分析

**用户**: "分析这个月的销售数据，生成报告"

**系统调度**:
1. 记忆检索 → 查找数据文件
2. 模型选择 → qwen-max
3. 工具调用 → data-analyzer
4. 结果汇总 → 生成报告

### 示例 2: 内容创作 + 发布

**用户**: "写个营销文案，配张图，发到小红书"

**系统调度**:
1. 文案创作 → qwen-plus + copywriter
2. 图像生成 → wanx-v1 + image-generator
3. 发布 → social-publisher

### 示例 3: 代码开发

**用户**: "帮我写个 Python 脚本处理 Excel，然后上传到 GitHub"

**系统调度**:
1. 代码编写 → qwen-coder + code-writer
2. GitHub 发布 → github-publisher

## 集成技能

- **model-router** - 模型路由 (8 大场景 + 主备配置)
- **memory-manager** - 记忆管理 (P0/P1/P2 生命周期)
- **github-publisher** - GitHub 发布

## API 参考

### SmartOrchestrator 类

- `execute(user_input, context)` - 执行用户指令
- `get_status()` - 获取状态
- `_parse_intent(input)` - 意图解析
- `_search_memories(query)` - 记忆检索
- `_route_model(query)` - 模型路由
- `_select_tools(intent)` - 工具选择
- `_plan_tasks(...)` - 任务规划
- `_aggregate_results(tasks, input)` - 结果汇总

## 许可证

MIT License

## 作者

丝佳丽 Scarlett - AI Love World 项目
