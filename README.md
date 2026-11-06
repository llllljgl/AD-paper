# AD Paper Radar · 工业视觉异常检测论文清单

追踪工业视觉异常检测、缺陷定位和分割。清单按会议和期刊整理，组内按年份从新到旧排列。标签用于快速扫读，点击 **查看 Tip** 可展开一句中文简介。

## 论文清单

<!-- PAPER-LIST:START -->

已收录 **11 篇** · 待筛选 **16 篇**

### CVPR

| 年份 | 论文 | 标签 | 链接 | Tip |
| --- | --- | --- | --- | --- |
| 2023 | [WinCLIP: Zero-/Few-Shot Anomaly Classification and Segmentation](https://arxiv.org/abs/2303.14814) | <code>零样本</code> <code>少样本</code> <code>缺陷定位</code> | [PDF](https://arxiv.org/pdf/2303.14814) | <details><summary>查看 Tip</summary><p>将 CLIP 的图像、窗口与局部特征对齐到正常和异常文本，可做零样本定位，也支持少量正常图作参考。</p></details> |
| 2022 | [Towards Total Recall in Industrial Anomaly Detection](https://arxiv.org/abs/2106.08265) | <code>记忆库</code> <code>仅正常样本</code> <code>缺陷定位</code> | [PDF](https://arxiv.org/pdf/2106.08265) · [代码](https://github.com/amazon-research/patchcore-inspection) | <details><summary>查看 Tip</summary><p>从正常图像中选取代表性局部特征构成记忆库，用特征距离检测和定位工业缺陷。</p></details> |

### ICLR

| 年份 | 论文 | 标签 | 链接 | Tip |
| --- | --- | --- | --- | --- |
| 2024 | [AnomalyCLIP: Object-agnostic Prompt Learning for Zero-shot Anomaly Detection](https://arxiv.org/abs/2310.18961) | <code>零样本</code> <code>提示词学习</code> <code>跨类别泛化</code> | [PDF](https://arxiv.org/pdf/2310.18961) · [代码](https://github.com/zqhang/AnomalyCLIP) | <details><summary>查看 Tip</summary><p>学习与物体类别无关的正常和异常提示词，让 CLIP 能在未见类别中检测和定位缺陷。</p></details> |

### WACV

| 年份 | 论文 | 标签 | 链接 | Tip |
| --- | --- | --- | --- | --- |
| 2027 | [Flownomaly: Single-Step Conditional-Mean Recovery for Few-Shot Anomaly Detection](https://arxiv.org/abs/2610.32964) | <code>少样本</code> <code>流匹配</code> <code>缺陷定位</code> | [PDF](https://arxiv.org/pdf/2610.32964) · [代码](https://github.com/b-rbmp/Flownomaly) | <details><summary>查看 Tip</summary><p>在 DINOv2 特征空间用条件流匹配单步恢复正常局部特征，再以恢复残差检测和定位少样本工业缺陷。</p></details> |

### arXiv

| 年份 | 论文 | 标签 | 链接 | Tip |
| --- | --- | --- | --- | --- |
| 2026 | [Beyond CLIP: Calibrated (Few-Shot) Defect Detection With System One Decision Models](https://arxiv.org/abs/2610.41199) | <code>少样本</code> <code>概率校准</code> <code>工业质检</code> | [PDF](https://arxiv.org/pdf/2610.41199) | <details><summary>查看 Tip</summary><p>用每类少量参考图做制造质检，自动改进分类文本描述，并校准缺陷概率以辅助判定。</p></details> |
| 2026 | [Cross-Encoder Anchor Refinement for Zero-Shot Anomaly Detection](https://arxiv.org/abs/2610.39727) | <code>零样本</code> <code>特征融合</code> <code>缺陷定位</code> | [PDF](https://arxiv.org/pdf/2610.39727) | <details><summary>查看 Tip</summary><p>在构建正常和异常原型前融合卷积与视觉 Transformer 的局部特征，用于跨类别的细粒度异常定位。</p></details> |
| 2026 | [Prototype-Guided Dynamic Domain Modulation and a Large-Scale Multi-SKU Benchmark for Shampoo Bottle Surface Defect Detection](https://arxiv.org/abs/2610.38194) | <code>表面缺陷</code> <code>跨产品</code> <code>数据集</code> | [PDF](https://arxiv.org/pdf/2610.38194) | <details><summary>查看 Tip</summary><p>提出多款洗发水瓶表面缺陷基准 Bottle-SKU，并用产品原型动态调整检测模型，以适应不同瓶型的外观差异。</p></details> |
| 2026 | [SGDB: Semantic-Geometric Decoupling and Evidence Binding for Logical Anomaly Detection](https://arxiv.org/abs/2610.34897) | <code>逻辑异常</code> <code>MVTec LOCO</code> <code>可解释性</code> | [PDF](https://arxiv.org/pdf/2610.34897) · [代码](https://github.com/Qybc/SGDB) | <details><summary>查看 Tip</summary><p>分开识别零件和测量几何属性，再依据明确规则判断装配配置是否异常，并给出可追溯的告警证据。</p></details> |
| 2026 | [Do Words Matter? What Text Contributes to Few and Full-Shot Vision-Language Anomaly Detection](https://arxiv.org/abs/2610.34610) | <code>视觉语言模型</code> <code>提示词</code> <code>方法分析</code> | [PDF](https://arxiv.org/pdf/2610.34610) | <details><summary>查看 Tip</summary><p>通过理论分析和替换实验拆解文本提示在视觉语言异常检测中的作用，并在工业基准上检验类别锚点几何的影响。</p></details> |
| 2026 | [Real-Time Conveyor Belt Defect Detection via Edge TPU-Accelerated YOLOv11 on Raspberry Pi 5](https://arxiv.org/abs/2610.34304) | <code>表面缺陷</code> <code>边缘部署</code> <code>YOLO</code> | [PDF](https://arxiv.org/pdf/2610.34304) | <details><summary>查看 Tip</summary><p>把量化后的 YOLOv11n 部署到 Raspberry Pi 5 和 Coral Edge TPU，用于输送带表面缺陷的实时检测。</p></details> |
| 2026 | [Agentic Ensemble with Vision-Language Models for Visual Anomaly Detection](https://arxiv.org/abs/2610.28560) | <code>视觉语言模型</code> <code>集成</code> <code>缺陷定位</code> | [PDF](https://arxiv.org/pdf/2610.28560) | <details><summary>查看 Tip</summary><p>用视觉语言模型判断多个检测器意见不一致的样本，再选择如何融合图像分数和像素异常图。</p></details> |

<!-- PAPER-LIST:END -->

年份优先采用 arXiv 元数据中的会议或期刊年份。仅有预印本信息的论文归入 **arXiv**，按首次提交年份排列。代码链接来自原始摘要或作者备注。Tip 基于论文摘要整理。

## 自动更新

把本项目推送到 GitHub 仓库的 `main` 分支，仓库首页会展示这份 README。GitHub Actions 计划每周一北京时间 **09:23** 抓取候选、筛选、生成标签和 Tip，再把清单及数据提交到仓库。

1. 在仓库 **Settings → Secrets and variables → Actions** 添加 Secret `OPENAI_API_KEY`，启用 Agent 筛选和简介生成。可通过仓库 Variable `OPENAI_MODEL` 覆盖默认模型。
2. 打开 **Actions → Update paper list → Run workflow** 手动更新。`since` 和 `until` 可用于补抓指定日期，日期按 UTC 计算，包含起止日。留空则增量抓取。

未配置 Key 或勾选 `no_llm` 时只抓取候选。待筛选和已排除的记录保存在 [论文数据](data/papers.json) 中。工作流需要 `contents: write` 提交更新，仓库策略或分支保护可能限制自动推送。

## 本地维护

需要 Python 3.9+，使用标准库。`build` 根据已有数据重建 README 的论文清单区块。

```bash
python3 -m radar build
python3 -m unittest discover -s tests -v
```

抓取和补抓分别使用 `python3 -m radar collect` 和 `python3 -m radar collect --since 2026-10-01 --until 2026-10-31`，随后运行 `build`。本地 Agent 从 `OPENAI_API_KEY` 环境变量读取密钥。维护者可编辑 `data/papers.json` 中的 `status`、`tags` 和 `summary_zh`，再生成清单。

在 [配置](config.json) 中可以调整检索式和筛选范围。首次抓取默认回看 14 天，后续从上次成功位置回看 3 天继续抓取。同一 arXiv ID 的论文合并，抓到更新版本时重新筛选。当前数据源为 arXiv，会议和期刊归属取自其元数据，覆盖范围取决于作者提供的信息。
