# AD Paper Radar · 工业视觉异常检测论文清单

追踪工业视觉异常检测、缺陷定位和分割。论文按会议或期刊及年份分组。点击 **查看 Tip** 可展开一句中文简介。

## 论文清单

<!-- PAPER-LIST:START -->

已收录 **11 篇** · 待筛选 **16 篇**

### CVPR 2023

| 论文 | 标签 | 链接 | Tip |
| --- | --- | --- | --- |
| [WinCLIP: Zero-/Few-Shot Anomaly Classification and Segmentation](https://arxiv.org/abs/2303.14814) | <code>零样本</code> <code>少样本</code> <code>缺陷定位</code> | [PDF](https://arxiv.org/pdf/2303.14814) | <details><summary>查看 Tip</summary><p>将 CLIP 的图像、窗口与局部特征对齐到正常和异常文本，可做零样本定位，也支持少量正常图作参考。</p></details> |

### CVPR 2022

| 论文 | 标签 | 链接 | Tip |
| --- | --- | --- | --- |
| [Towards Total Recall in Industrial Anomaly Detection](https://arxiv.org/abs/2106.08265) | <code>记忆库</code> <code>仅正常样本</code> <code>缺陷定位</code> | [PDF](https://arxiv.org/pdf/2106.08265) · [代码](https://github.com/amazon-research/patchcore-inspection) | <details><summary>查看 Tip</summary><p>从正常图像中选取代表性局部特征构成记忆库，用特征距离检测和定位工业缺陷。</p></details> |

### ICLR 2024

| 论文 | 标签 | 链接 | Tip |
| --- | --- | --- | --- |
| [AnomalyCLIP: Object-agnostic Prompt Learning for Zero-shot Anomaly Detection](https://arxiv.org/abs/2310.18961) | <code>零样本</code> <code>提示词学习</code> <code>跨类别泛化</code> | [PDF](https://arxiv.org/pdf/2310.18961) · [代码](https://github.com/zqhang/AnomalyCLIP) | <details><summary>查看 Tip</summary><p>学习与物体类别无关的正常和异常提示词，让 CLIP 能在未见类别中检测和定位缺陷。</p></details> |

### WACV 2027

| 论文 | 标签 | 链接 | Tip |
| --- | --- | --- | --- |
| [Flownomaly: Single-Step Conditional-Mean Recovery for Few-Shot Anomaly Detection](https://arxiv.org/abs/2610.32964) | <code>少样本</code> <code>流匹配</code> <code>缺陷定位</code> | [PDF](https://arxiv.org/pdf/2610.32964) · [代码](https://github.com/b-rbmp/Flownomaly) | <details><summary>查看 Tip</summary><p>在 DINOv2 特征空间用条件流匹配单步恢复正常局部特征，再以恢复残差检测和定位少样本工业缺陷。</p></details> |

### arXiv 2026

| 论文 | 标签 | 链接 | Tip |
| --- | --- | --- | --- |
| [Beyond CLIP: Calibrated (Few-Shot) Defect Detection With System One Decision Models](https://arxiv.org/abs/2610.41199) | <code>少样本</code> <code>概率校准</code> <code>工业质检</code> | [PDF](https://arxiv.org/pdf/2610.41199) | <details><summary>查看 Tip</summary><p>用每类少量参考图做制造质检，自动改进分类文本描述，并校准缺陷概率以辅助判定。</p></details> |
| [Cross-Encoder Anchor Refinement for Zero-Shot Anomaly Detection](https://arxiv.org/abs/2610.39727) | <code>零样本</code> <code>特征融合</code> <code>缺陷定位</code> | [PDF](https://arxiv.org/pdf/2610.39727) | <details><summary>查看 Tip</summary><p>在构建正常和异常原型前融合卷积与视觉 Transformer 的局部特征，用于跨类别的细粒度异常定位。</p></details> |
| [Prototype-Guided Dynamic Domain Modulation and a Large-Scale Multi-SKU Benchmark for Shampoo Bottle Surface Defect Detection](https://arxiv.org/abs/2610.38194) | <code>表面缺陷</code> <code>跨产品</code> <code>数据集</code> | [PDF](https://arxiv.org/pdf/2610.38194) | <details><summary>查看 Tip</summary><p>提出多款洗发水瓶表面缺陷基准 Bottle-SKU，并用产品原型动态调整检测模型，以适应不同瓶型的外观差异。</p></details> |
| [SGDB: Semantic-Geometric Decoupling and Evidence Binding for Logical Anomaly Detection](https://arxiv.org/abs/2610.34897) | <code>逻辑异常</code> <code>MVTec LOCO</code> <code>可解释性</code> | [PDF](https://arxiv.org/pdf/2610.34897) · [代码](https://github.com/Qybc/SGDB) | <details><summary>查看 Tip</summary><p>分开识别零件和测量几何属性，再依据明确规则判断装配配置是否异常，并给出可追溯的告警证据。</p></details> |
| [Do Words Matter? What Text Contributes to Few and Full-Shot Vision-Language Anomaly Detection](https://arxiv.org/abs/2610.34610) | <code>视觉语言模型</code> <code>提示词</code> <code>方法分析</code> | [PDF](https://arxiv.org/pdf/2610.34610) | <details><summary>查看 Tip</summary><p>通过理论分析和替换实验拆解文本提示在视觉语言异常检测中的作用，并在工业基准上检验类别锚点几何的影响。</p></details> |
| [Real-Time Conveyor Belt Defect Detection via Edge TPU-Accelerated YOLOv11 on Raspberry Pi 5](https://arxiv.org/abs/2610.34304) | <code>表面缺陷</code> <code>边缘部署</code> <code>YOLO</code> | [PDF](https://arxiv.org/pdf/2610.34304) | <details><summary>查看 Tip</summary><p>把量化后的 YOLOv11n 部署到 Raspberry Pi 5 和 Coral Edge TPU，用于输送带表面缺陷的实时检测。</p></details> |
| [Agentic Ensemble with Vision-Language Models for Visual Anomaly Detection](https://arxiv.org/abs/2610.28560) | <code>视觉语言模型</code> <code>集成</code> <code>缺陷定位</code> | [PDF](https://arxiv.org/pdf/2610.28560) | <details><summary>查看 Tip</summary><p>用视觉语言模型判断多个检测器意见不一致的样本，再选择如何融合图像分数和像素异常图。</p></details> |

<!-- PAPER-LIST:END -->
