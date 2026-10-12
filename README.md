# rag-qa-service

> 上传 PDF 就能问答、答案带页码出处；并在同一套数据上做「切分策略 / 向量库 / 推理后端」三组性能对比。
> 前一半用来投 AI 应用岗，后一半用来投 AI Infra 的验证与性能岗。

## 五问定义（写不出来就别开工）

1. **做什么**：上传 PDF → 提问 → 返回带页码出处的答案。
2. **给谁用、解决什么**：给备考/读文献的人；解决「长文档里找不到答案、且不知道答案出处」。
3. **跑通标准**：支持 10+ 页 PDF；提问 P95 < 3 秒（本地小模型）/ < 1.5 秒（API）；答案标注页码；`docker compose up` 一键起。
4. **怎么证明做得好**：30 题自建评测集（检索命中率 + 答案正确率）+ 延迟 P50/P95 + 并发 QPS + 3 组对比实验表。
5. **交付什么**：本仓库 + README（架构图）+ benchmark 报告 + 30 秒演示录屏 + 1 篇技术博客。

## 进度

- [ ] W1 立项与环境（本文件 + 仓库骨架）✅ 本地已完成，待推送
- [ ] W2 最小链路：PDF → 切分 → embedding → 检索 → 回答（命令行）
- [ ] W3 答案带出处引用 + 换 Chroma
- [ ] W4 接入本地/校内模型 + Streamlit 界面
- [ ] W5 30 题评测集 + 评测脚本
- [ ] W6 FastAPI 服务化 + locust 压测（P50/P95、QPS）
- [ ] W7 对比实验①：切分策略（512/1024 × overlap 0/128）
- [ ] W8 对比实验②：向量库（Chroma / pgvector / FAISS）
- [ ] W9 对比实验③：推理后端（vLLM / HF / API）+ 有无 Rerank
- [ ] W12 收尾：架构图 + 一键复现 + 测试
- [ ] W13 benchmark 报告 + 技术博客

## 目录规划

```
rag-qa-service/
├── README.md
├── .gitignore
├── pyproject.toml        # 依赖（用 uv 管理）
├── src/
│   ├── ingest.py         # PDF 解析与切分
│   ├── embed.py          # 向量化
│   ├── store.py          # 向量库封装（Chroma 起步）
│   ├── rag.py            # 检索 + 生成（带出处）
│   └── api.py            # FastAPI 接口
├── eval/
│   ├── questions.jsonl   # 30 题评测集（含参考答案要点）
│   └── run_eval.py       # 评测脚本（命中率/正确率/延迟）
├── bench/                # 压测与对比实验脚本
│   └── locustfile.py
├── data/                 # 测试用 PDF（不入库）
└── docs/
    ├── arch.png          # 架构图
    └── benchmark.md      # 对比实验报告
```

## 技术栈

Python 3.12（用 uv 管理）· FastAPI · Streamlit · LangChain 或 LlamaIndex（只选一个）· bge-small-zh（ModelScope 下载）· Chroma → pgvector / FAISS · Ollama / vLLM · Docker Compose · locust

## 环境说明（本机 2026-10-12 实测）

- git 2.50.1 ✅、uv 0.12.22 ✅、node v26.7.0 ✅
- 系统 python 只有 3.9.6 ⚠️ → 用 `uv python install 3.12` 装一个项目专用版本
- Docker ❌ 未安装（W1 待办）
- 校内免费模型平台：https://ai.cuhk.edu.cn/chat/ （GLM 5.3 Flash / Qwen3.8 27B），项目起步阶段可先用它，省 API 费用
