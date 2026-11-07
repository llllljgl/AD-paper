# DeepSeek 论文收集对照验收

报告整理于 2026-11-07。实际 API 运行于 2026-11-06 北京时间 17:25–17:28，继续整理时没有重复调用 API。

[查看 GitHub Actions 运行及原始附件](https://github.com/llllljgl/AD-paper/actions/runs/42194896234)

## 结论

在本次核实的 56 篇相关论文参考集中，现有清单已收录 41 篇，确认漏收 15 篇，参考集内漏收比例为 **15 / 56 = 26.8%**。其中 14 篇已经在候选库，1 篇没有进入候选库。已收录 41 篇暂未发现确定误收。

这不是领域总体漏检率。参考集由现有清单、本轮候选和独立补查组成，并非穷尽清单，也不是随机样本。模型建议不等于正确答案，未核实条目不进入分母。

## 范围与方法

固定基线 `7dfd81eeb2954a533ce35e5e380c4a1eb9177960`，论文数据 SHA-256 为 `2f761d7e9880e55efb31d0ea137c2dfc99e6940570d497e1b6ec87bb1ca51fdd`。对照期间生产数据、README 和常规收集规则均保持不变。

选择 CVPR、ICLR、TPAMI、TIP 的 2026 正式记录。会议使用官方目录，期刊使用 Crossref 出版元数据。执行现有的每来源两条 DeepSeek 搜索，再与目录匹配。共扫描 11,425 条记录，生成 112 篇候选。全部候选均已存在于基线候选库，没有新候选由这八次搜索补入。

诊断阶段重新补取全部候选详情，放开日常每来源 12 篇详情、每轮 60 次模型调用的限制。对全部有摘要的候选使用现有 deepseek-flash 提示词重新判断，包括已收录、已排除和被范围词规则挡住的候选。范围规则仅记录结果，不阻止诊断复核。

实际完成 8 次搜索和 112 次模型调用，111 篇取得判断，其中 57 篇 keep、54 篇 reject，1 篇缺公开摘要未送审。模型调用数包含格式重试。所有来源扫描成功。独立复核使用官方摘要、作者项目页、仓库说明及少量 arXiv HTML 实验段落，没有下载 PDF。

## 结果

| 来源 | 扫描目录记录 | 本轮候选 | 原已收录 | 确认漏收 | 参考集内漏收比例 |
| --- | ---: | ---: | ---: | ---: | ---: |
| CVPR 2026 | 4,041 | 54 | 27 | 6 | 6 / 33 = 18.2% |
| ICLR 2026 | 5,348 | 29 | 4 | 0 | 0 / 4 = 0% |
| TPAMI 2026 | 1,216 | 11 | 3 | 2 | 2 / 5 = 40.0% |
| TIP 2026 | 820 | 18 | 7 | 7 | 7 / 14 = 50.0% |
| 合计 | 11,425 | 112 | 41 | 15 | 15 / 56 = 26.8% |

TPAMI 的两篇漏收包含一篇独立补查发现的论文，它不在本轮 112 篇候选中。ICLR 的 0% 只表示本参考集中未确认漏收，不能解释为已经收全。

拆分发现与发布环节，在这 56 篇参考论文中，55 篇已进入候选库，1 篇未进入候选库。候选发现阶段的已知遗漏为 1 / 56 = 1.8%，公开清单的漏收为 15 / 56 = 26.8%。

## 15 篇确认漏收及依据

| 来源 | 论文 | 原状态 | 复核依据 |
| --- | --- | --- | --- |
| CVPR | [AnomalyVFM -- Transforming Vision Foundation Models into Zero-Shot Anomaly Detectors](https://openaccess.thecvf.com/content/CVPR2026/html/Fucka_AnomalyVFM_--_Transforming_Vision_Foundation_Models_into_Zero-Shot_Anomaly_Detectors_CVPR_2026_paper.html) | 待处理 | 作者项目页明确说明在九个工业检测数据集上评测。 [证据](https://maticfuc.github.io/anomaly_vfm/) |
| CVPR | [InvAD: Inversion-based Reconstruction-Free Anomaly Detection with Diffusion Models](https://openaccess.thecvf.com/content/CVPR2026/html/Sakai_InvAD_Inversion-based_Reconstruction-Free_Anomaly_Detection_with_Diffusion_Models_CVPR_2026_paper.html) | 待处理 | 更新后的作者预印本摘要明确包含工业与医学异常检测基准。 [证据](https://arxiv.org/abs/2504.05662) |
| CVPR | [Anomaly as Non-Conformity via Training-Free Graph Laplacian Energy Minimization](https://openaccess.thecvf.com/content/CVPR2026/html/Seo_Anomaly_as_Non-Conformity_via_Training-Free_Graph_Laplacian_Energy_Minimization_CVPR_2026_paper.html) | 待处理 | 作者公开 HTML 正文实验部分明确使用 MVTec AD 与 VisA。 [证据](https://arxiv.org/html/2605.28428v1) |
| CVPR | [A Semantically Disentangled Unified Model for Multi-category 3D Anomaly Detection](https://openaccess.thecvf.com/content/CVPR2026/html/Kim_A_Semantically_Disentangled_Unified_Model_for_Multi-category_3D_Anomaly_Detection_CVPR_2026_paper.html) | 待处理 | 官方摘要明确描述点云缺陷检测，并使用 Real3D-AD 与 Anomaly-ShapeNet。 [证据](https://openaccess.thecvf.com/content/CVPR2026/html/Kim_A_Semantically_Disentangled_Unified_Model_for_Multi-category_3D_Anomaly_Detection_CVPR_2026_paper.html) |
| CVPR | [GS-CLIP: Zero-shot 3D Anomaly Detection by Geometry-Aware Prompt and Synergistic View Representation Learning](https://openaccess.thecvf.com/content/CVPR2026/html/Deng_GS-CLIP_Zero-shot_3D_Anomaly_Detection_by_Geometry-Aware_Prompt_and_Synergistic_CVPR_2026_paper.html) | 待处理 | 作者仓库的数据准备部分明确包含 MVTec 3D-AD、Eyecandies 与 Real3D-AD。 [证据](https://github.com/zhushengxinyue/GS-CLIP) |
| CVPR | [Reasoning-Driven Anomaly Detection and Localization with Image-Level Supervision](https://openaccess.thecvf.com/content/CVPR2026/html/Jin_Reasoning-Driven_Anomaly_Detection_and_Localization_with_Image-Level_Supervision_CVPR_2026_paper.html) | 待处理 | 作者公开 HTML 正文列出 MVTec AD、WFDD、SDD 等工业检测实验。 [证据](https://arxiv.org/html/2603.27179v1) |
| TPAMI | [Learning Topology-Aware Representations via Test-Time Adaptation for Anomaly Segmentation](https://doi.org/10.1109/tpami.2026.3710196) | 待处理 | 出版摘要明确列出 MVTec AD、VisA、Real-IAD、MVTec LOCO 等评测。 [证据](https://doi.org/10.1109/tpami.2026.3710196) |
| TIP | [Improving Unsupervised Ultrasonic Image Anomaly Detection via Frequency-Spatial Feature Filtering and Gaussian Mixture Modeling](https://doi.org/10.1109/tip.2026.3659292) | 待处理 | 出版摘要明确针对芯片封装的超声 C 扫描缺陷图像，另有 MVTec AD 与 VisA 评测。 [证据](https://ieeexplore.ieee.org/document/11372587/) |
| TIP | [Unified Anomaly Detection via Multi-Scale Contrasted Memory](https://doi.org/10.1109/tip.2026.3663923) | 待处理 | 出版摘要明确报告工业检测评估，方法输出空间异常图。 [证据](https://doi.org/10.1109/tip.2026.3663923) |
| TIP | [Adapting Domain-Aware Knowledge to Vision-Language Model for Zero-Shot Anomaly Detection](https://doi.org/10.1109/tip.2026.3671665) | 待处理 | 出版摘要明确包含工业数据集，并报告图像级与像素级检测。 [证据](https://doi.org/10.1109/tip.2026.3671665) |
| TIP | [“Stones From Other Hills Can Polish Jade”: Zero-Shot Anomaly Synthesis via Cross-Domain Anomaly Injection](https://doi.org/10.1109/tip.2026.3675432) | 待处理 | 出版摘要明确针对工业图像的零样本异常合成，为工业异常检测提供训练样本。 [证据](https://doi.org/10.1109/tip.2026.3675432) |
| TIP | [Advancing Pre-Trained Teacher: Towards Robust Feature Discrepancy for Anomaly Detection](https://doi.org/10.1109/tip.2026.3683277) | 待处理 | 出版摘要明确提出工业异常检测框架，评测包含 MVTec、VisA 与 MVTec3D-RGB。 [证据](https://doi.org/10.1109/tip.2026.3683277) |
| TIP | [Region-Prompt-Guided Anomaly Detection With Entropy-Based Consistency Modeling](https://doi.org/10.1109/tip.2026.3709516) | 待处理 | 出版摘要明确针对多类别工业视觉异常检测，列出五个工业基准。 [证据](https://doi.org/10.1109/tip.2026.3709516) |
| TIP | [UAD: A Unified Model for Zero-Shot Anomaly Detection](https://doi.org/10.1109/tip.2026.3718433) | 待处理 | 出版摘要明确包含缺陷检测领域的图像检测与分割评估，同时涵盖医学领域。 [证据](https://doi.org/10.1109/tip.2026.3718433) |
| TPAMI | [Unification of Closed-Open Industrial Detection Scenarios: New Large-Scale Benchmarks, Challenges and Baselines](https://doi.org/10.1109/tpami.2026.3680569) | 候选库不存在 | 出版记录和作者预印本共同确认该文为工业缺陷检测基准与方法研究。标题没有命中旧初筛词，目录记录原本没有摘要。 [证据](https://arxiv.org/abs/2606.07953) |

## 误收与模型错误

本轮复核原已收录 41 篇，均在相应官方目录中，暂未确认存在方向或会议归属误收。观察到的误收为 0 / 41，不代表总体误收率为零，也不证明每篇代码链接和摘要细节均正确。早期 41 篇中有 20 篇没有保存摘要，本轮已在验收附件中补取，生产库尚未写回。

DeepSeek 否定了已收录的 Dual-Prototype-Guided Multi-task Learning for Unsupervised Anomaly Detection and Classification，理由是没有明确工业数据集评估。但官方摘要结尾明确说明评估涵盖工业与医学数据集。此处确认是本轮模型误拒，不能据此删除论文。

[官方摘要](https://openaccess.thecvf.com/content/CVPR2026/html/Luo_Dual-Prototype-Guided_Multi-task_Learning_for_Unsupervised_Anomaly_Detection_and_Classification_CVPR_2026_paper.html)

UniMMAD 与 FECDTAD 的摘要没有列清工业基准，独立检查作者实现后确认包含工业数据集配置。

[UniMMAD 配置](https://github.com/yuanzhao-CVLAB/UniMMAD/blob/main/config.json) · [FECDTAD 数据集说明](https://github.com/Mazeqi/FECDTAD)

## 仍未确认的条目

DeepSeek 共提出 17 篇可能漏收，其中 14 篇已确认，下面 3 篇保留不确定。独立补查另外确认 1 篇，得到上述 15 篇总数。

- [Anomaly-Related Residual Fields for Cross-domain Anomaly Detection](https://openaccess.thecvf.com/content/CVPR2026/html/Gao_Anomaly-Related_Residual_Fields_for_Cross-domain_Anomaly_Detection_CVPR_2026_paper.html)。DeepSeek 建议收录，但本轮读到的官方摘要未明确给出工业场景或具体工业基准。缺少足够独立证据，暂不计入确认漏收。
- [Wavelet-Driven 3D Anomaly Detection under Pose-Agnostic and Sparse-View](https://openaccess.thecvf.com/content/CVPR2026/html/Shao_Wavelet-Driven_3D_Anomaly_Detection_under_Pose-Agnostic_and_Sparse-View_CVPR_2026_paper.html)。DeepSeek 建议收录，但本轮读到的官方摘要未明确给出工业场景或具体工业基准。缺少足够独立证据，暂不计入确认漏收。
- [Hunting Normality from Query Sample via Residual Learning for Generalist Anomaly Detection](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_Hunting_Normality_from_Query_Sample_via_Residual_Learning_for_Generalist_CVPR_2026_paper.html)。DeepSeek 建议收录，但本轮读到的官方摘要未明确给出工业场景或具体工业基准。缺少足够独立证据，暂不计入确认漏收。

另有 TIP 的 UniNAD 缺公开摘要，本轮未作模型判定。SFR-Net 的市政管道场景、VLM-SubtleBench 的跨领域视觉比较评测、通用扩散异常检测综述等属于范围边界，本次不计入确认漏收。对这些方向需要另行明确一致的收录口径。

## 已定位的问题

1. **范围词规则挡住相关论文。** 14 篇原候选库内的确认漏收中，有 8 篇在本轮补齐摘要后仍通不过当前规则。包括缺少 Real3D-AD 别名，以及摘要省略工业领域词、只写通用视觉任务等情况。需要补充公开证据并再次判断，不能长期只挂起。
2. **待处理队列积压。** 其余 6 篇已经有摘要且通过范围词规则，仍未发布。常规运行有 60 次调用预算，必须区分处理额度耗尽和真正缺证据，监控积压年龄。
3. **目录初筛缺词且没有摘要补救。** TPAMI 的 Unification of Closed-Open Industrial Detection Scenarios 在目录里有记录，但原始摘要为空，标题未命中 anomaly、defect 或 industrial inspection。它未进入候选，后续 LLM 根本看不到。
4. **DeepSeek 搜索覆盖不足。** 八条固定查询返回结果经当前匹配规则仅对应 14 篇目标候选，全部是已收录论文，其中 CVPR 10、ICLR 3、TPAMI 1、TIP 0。结果含其他年份、其他期刊、PDF 片段及重复链接。该数量衡量搜索加匹配流程，不等于搜索引擎本身的召回率。不能用这两条查询替代官方目录。
5. **模型判断与证据有偏差。** 一篇已收录论文被错误排除；部分建议收录理由声称有工业评测，但给模型的摘要没有明确写出。需要要求模型附证据位置，并把缺证据与明确不相关分开。

## 建议的修复顺序

先扩大候选初筛对 industrial detection、视觉质检及三维数据集别名的覆盖，再补齐公开摘要、项目页和作者仓库证据。范围词应帮助排序与提示风险，避免把相关候选永久挡在模型之前。随后处理积压、保存判断依据，并将本次确认案例保留为回归样本。最后再扩展搜索词、查询分组和 URL 匹配，提高搜索补漏能力。

本次仅完成验收及证据归档，没有修改生产筛选规则，也没有自动收录或删除上述论文。

逐条模型输出和验收指标保存在 [结构化报告](2026-11-07-deepseek-audit.json)。原始搜索、目录和摘要快照在 Actions 附件中保留 30 天。
