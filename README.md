# AD Paper Radar · 工业视觉异常检测论文清单

追踪工业视觉异常检测、缺陷定位和分割。论文按会议或期刊及年份分组。点击 **查看 Tip** 可展开一句中文简介。

## 论文清单

<!-- PAPER-LIST:START -->

已收录 **49 篇** · 待筛选 **16 篇**

### AAAI 2026

| 论文 | 标签 | 链接 | Tip |
| --- | --- | --- | --- |
| [Towards High-Resolution 3D Anomaly Detection: A Scalable Dataset and Real-Time Framework for Subtle Industrial Defects](https://ojs.aaai.org/index.php/AAAI/article/view/37328) | <code>点云</code> <code>高分辨率</code> <code>工业基准</code> | [PDF](https://ojs.aaai.org/index.php/AAAI/article/download/37328/41290) | <details><summary>查看 Tip</summary><p>提出高分辨率点云缺陷基准 MiniShift 和轻量 Simple3D 方法，用于检测工业零件表面的微小三维异常。</p></details> |
| [IAD-R1: Reinforcing Consistent Reasoning in Industrial Anomaly Detection](https://ojs.aaai.org/index.php/AAAI/article/view/37588) | <code>多模态</code> <code>强化学习</code> <code>缺陷推理</code> | [PDF](https://ojs.aaai.org/index.php/AAAI/article/download/37588/41550) | <details><summary>查看 Tip</summary><p>采用两阶段后训练，先提升视觉语言模型对工业缺陷的感知，再强化缺陷判断与解释的一致性。</p></details> |

### CVPR 2026

| 论文 | 标签 | 链接 | Tip |
| --- | --- | --- | --- |
| [Defect Cue-Preserved Structural Feature Refinement for Few-Shot Anomaly Detection](https://openaccess.thecvf.com/content/CVPR2026/html/Jiang_Defect_Cue-Preserved_Structural_Feature_Refinement_for_Few-Shot_Anomaly_Detection_CVPR_2026_paper.html) | <code>少样本</code> <code>特征重建</code> <code>缺陷分割</code> | [PDF](https://openaccess.thecvf.com/content/CVPR2026/papers/Jiang_Defect_Cue-Preserved_Structural_Feature_Refinement_for_Few-Shot_Anomaly_Detection_CVPR_2026_paper.pdf) | <details><summary>查看 Tip</summary><p>在特征提取早期放大微弱缺陷线索，再引导重建和边界细化，减少小缺陷在深层特征中被抹去。</p></details> |
| [Geometry-Aligned and Anomaly-Aware Reconstruction for 3D Anomaly Detection](https://openaccess.thecvf.com/content/CVPR2026/html/Wu_Geometry-Aligned_and_Anomaly-Aware_Reconstruction_for_3D_Anomaly_Detection_CVPR_2026_paper.html) | <code>点云</code> <code>扩散重建</code> <code>缺陷定位</code> | [PDF](https://openaccess.thecvf.com/content/CVPR2026/papers/Wu_Geometry-Aligned_and_Anomaly-Aware_Reconstruction_for_3D_Anomaly_Detection_CVPR_2026_paper.pdf) | <details><summary>查看 Tip</summary><p>沿点云表面法向加入噪声，并为异常区域引入正常参考，减少三维扩散重建中的几何失真。</p></details> |
| [Omni-AD: A Large-scale and Versatile Benchmark for Industrial Anomaly Detection](https://openaccess.thecvf.com/content/CVPR2026/html/Shi_Omni-AD_A_Large-scale_and_Versatile_Benchmark_for_Industrial_Anomaly_Detection_CVPR_2026_paper.html) | <code>工业基准</code> <code>视觉问答</code> <code>缺陷定位</code> | [PDF](https://openaccess.thecvf.com/content/CVPR2026/papers/Shi_Omni-AD_A_Large-scale_and_Versatile_Benchmark_for_Industrial_Anomaly_Detection_CVPR_2026_paper.pdf) | <details><summary>查看 Tip</summary><p>构建覆盖多行业与产品类别的 Omni-AD 基准，同时评估传统异常检测和多模态模型的问答与定位能力。</p></details> |
| [FastRef: Fast Prototype Refinement for Few-shot Industrial Anomaly Detection](https://openaccess.thecvf.com/content/CVPR2026/html/Li_FastRef_Fast_Prototype_Refinement_for_Few-shot_Industrial_Anomaly_Detection_CVPR_2026_paper.html) | <code>少样本</code> <code>原型学习</code> <code>最优传输</code> | [PDF](https://openaccess.thecvf.com/content/CVPR2026/papers/Li_FastRef_Fast_Prototype_Refinement_for_Few-shot_Industrial_Anomaly_Detection_CVPR_2026_paper.pdf) | <details><summary>查看 Tip</summary><p>测试时从待检图像提取信息更新正常原型，再用最优传输抑制异常特征混入，适合正常参考图很少的场景。</p></details> |
| [UniSpector: Towards Universal Open-set Defect Recognition via Spectral-Contrastive Visual Prompting](https://openaccess.thecvf.com/content/CVPR2026/html/Kim_UniSpector_Towards_Universal_Open-set_Defect_Recognition_via_Spectral-Contrastive_Visual_Prompting_CVPR_2026_paper.html) | <code>开放集</code> <code>视觉提示</code> <code>缺陷定位</code> | [PDF](https://openaccess.thecvf.com/content/CVPR2026/papers/Kim_UniSpector_Towards_Universal_Open-set_Defect_Recognition_via_Spectral-Contrastive_Visual_Prompting_CVPR_2026_paper.pdf) | <details><summary>查看 Tip</summary><p>用空间与频谱特征构造可迁移的视觉提示，并提出开放集缺陷定位基准 Inspect Anything。</p></details> |
| [MoECLIP: Patch-Specialized Experts for Zero-shot Anomaly Detection](https://openaccess.thecvf.com/content/CVPR2026/html/Park_MoECLIP_Patch-Specialized_Experts_for_Zero-shot_Anomaly_Detection_CVPR_2026_paper.html) | <code>零样本</code> <code>CLIP</code> <code>混合专家</code> | [PDF](https://openaccess.thecvf.com/content/CVPR2026/papers/Park_MoECLIP_Patch-Specialized_Experts_for_Zero-shot_Anomaly_Detection_CVPR_2026_paper.pdf) · [代码](https://github.com/CoCoRessa/MoECLIP) | <details><summary>查看 Tip</summary><p>按图像块动态选择 LoRA 专家，为不同局部特征提供专门适配，同时保留 CLIP 对未见类别的迁移能力。</p></details> |
| [Towards Open-Vocabulary Industrial Defect Understanding with a Large-Scale Multimodal Dataset](https://openaccess.thecvf.com/content/CVPR2026/html/Ni_Towards_Open-Vocabulary_Industrial_Defect_Understanding_with_a_Large-Scale_Multimodal_Dataset_CVPR_2026_paper.html) | <code>工业数据集</code> <code>图文对齐</code> <code>开放词汇</code> | [PDF](https://openaccess.thecvf.com/content/CVPR2026/papers/Ni_Towards_Open-Vocabulary_Industrial_Defect_Understanding_with_a_Large-Scale_Multimodal_Dataset_CVPR_2026_paper.pdf) | <details><summary>查看 Tip</summary><p>发布工业缺陷图文数据集 IMDD-1M，包含细粒度位置与严重程度描述，可用于训练开放词汇质检模型。</p></details> |
| [UniMMAD: Unified Multi-Modal and Multi-Class Anomaly Detection via MoE-Driven Feature Decompression](https://openaccess.thecvf.com/content/CVPR2026/html/Zhao_UniMMAD_Unified_Multi-Modal_and_Multi-Class_Anomaly_Detection_via_MoE-Driven_Feature_CVPR_2026_paper.html) | <code>多模态</code> <code>多类别</code> <code>混合专家</code> | [PDF](https://openaccess.thecvf.com/content/CVPR2026/papers/Zhao_UniMMAD_Unified_Multi-Modal_and_Multi-Class_Anomaly_Detection_via_MoE-Driven_Feature_CVPR_2026_paper.pdf) · [代码](https://github.com/yuanzhao-CVLAB/UniMMAD) | <details><summary>查看 Tip</summary><p>先压缩不同模态的输入，再按类别和模态选择专家重建特征，让一个模型处理多种缺陷检测设置。</p></details> |
| [ADSeeker: A Knowledge-Grounded Reasoning Framework for Industry Anomaly Detection and Reasoning](https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_ADSeeker_A_Knowledge-Grounded_Reasoning_Framework_for_Industry_Anomaly_Detection_and_CVPR_2026_paper.html) | <code>多模态</code> <code>检索增强</code> <code>缺陷推理</code> | [PDF](https://openaccess.thecvf.com/content/CVPR2026/papers/Zhang_ADSeeker_A_Knowledge-Grounded_Reasoning_Framework_for_Industry_Anomaly_Detection_and_CVPR_2026_paper.pdf) | <details><summary>查看 Tip</summary><p>构建工业缺陷视觉知识库，根据待检图像检索相似案例与文档，让模型结合领域证据做质检推理。</p></details> |

### CVPR 2023

| 论文 | 标签 | 链接 | Tip |
| --- | --- | --- | --- |
| [WinCLIP: Zero-/Few-Shot Anomaly Classification and Segmentation](https://arxiv.org/abs/2303.14814) | <code>零样本</code> <code>少样本</code> <code>缺陷定位</code> | [PDF](https://arxiv.org/pdf/2303.14814) | <details><summary>查看 Tip</summary><p>将 CLIP 的图像、窗口与局部特征对齐到正常和异常文本，可做零样本定位，也支持少量正常图作参考。</p></details> |

### CVPR 2022

| 论文 | 标签 | 链接 | Tip |
| --- | --- | --- | --- |
| [Towards Total Recall in Industrial Anomaly Detection](https://arxiv.org/abs/2106.08265) | <code>记忆库</code> <code>仅正常样本</code> <code>缺陷定位</code> | [PDF](https://arxiv.org/pdf/2106.08265) · [代码](https://github.com/amazon-research/patchcore-inspection) | <details><summary>查看 Tip</summary><p>从正常图像中选取代表性局部特征构成记忆库，用特征距离检测和定位工业缺陷。</p></details> |

### ECCV 2026

| 论文 | 标签 | 链接 | Tip |
| --- | --- | --- | --- |
| [Global Logic and Local Search: Dual-Stream Multimodal In-Context Learning for Verifiable Industrial Anomaly Detection](https://eccv.ecva.net/virtual/2026/poster/5200) | <code>免训练</code> <code>多模态</code> <code>可追溯诊断</code> | [PDF](https://media.eventhosts.cc/Conferences/ECCV2026/pdfs/9365.pdf) | <details><summary>查看 Tip</summary><p>用全局分支核对部件与检验规则，用局部分支搜索细粒度图像证据，让缺陷判断可以追溯到具体区域。</p></details> |
| [O-VAD: Industrial Video Anomaly Detection through Object-Centric Tracking and Reasoning](https://eccv.ecva.net/virtual/2026/poster/4659) | <code>工业视频</code> <code>对象跟踪</code> <code>异常推理</code> | [PDF](https://media.eventhosts.cc/Conferences/ECCV2026/pdfs/6897.pdf) | <details><summary>查看 Tip</summary><p>跟踪生产视频中各物体的状态变化，再沿时间轨迹推理异常，适合检测静态图像难以识别的工序错误。</p></details> |
| [DeMuS: Learning Decoupled Matching and Scoring for Batch Zero-Shot Industrial Anomaly Detection](https://eccv.ecva.net/virtual/2026/poster/3717) | <code>零样本</code> <code>批内互评分</code> <code>部件匹配</code> | [PDF](https://media.eventhosts.cc/Conferences/ECCV2026/pdfs/2743.pdf) · [代码](https://github.com/evoLonation/DeMuS) | <details><summary>查看 Tip</summary><p>把部件对齐和异常评分拆成两个学习目标，在正常参考较少且产品姿态变化时减少错误匹配。</p></details> |
| [FuDU: A Fuzzy Dual-dimension Uncertainty Framework for Streaming Active Learning in Industrial Defect Detection](https://eccv.ecva.net/virtual/2026/poster/5087) | <code>工业质检</code> <code>主动学习</code> <code>不确定性</code> | [PDF](https://media.eventhosts.cc/Conferences/ECCV2026/pdfs/8772.pdf) · [代码](https://github.com/wangzhaoyang-508/FuDU) | <details><summary>查看 Tip</summary><p>同时估计整图和缺陷框的不确定性，用模糊推理选出值得人工复核和标注的流式样本。</p></details> |
| [Rethinking Continual Anomaly Detection on the Edge: Benchmarking Under Realistic Industrial Conditions](https://eccv.ecva.net/virtual/2026/poster/3516) | <code>持续学习</code> <code>边缘部署</code> <code>工业基准</code> | [PDF](https://media.eventhosts.cc/Conferences/ECCV2026/pdfs/1778.pdf) | <details><summary>查看 Tip</summary><p>用持续漂移和边缘设备实测评估质检模型，并给出基于冻结 DINOv3 和局部记忆检索的免训练基线。</p></details> |
| [Beyond Common Sense: Grounding Logical Anomaly Detection in Inspection Criteria](https://eccv.ecva.net/virtual/2026/poster/4468) | <code>逻辑异常</code> <code>检验规则</code> <code>多模态</code> | [PDF](https://media.eventhosts.cc/Conferences/ECCV2026/pdfs/6072.pdf) · [代码](https://github.com/tzjtatata/SCAN) | <details><summary>查看 Tip</summary><p>让模型逐条核查显式检验标准，并按规则分配强化学习奖励，用于判断装配或布局是否违反规范。</p></details> |

### ICLR 2026

| 论文 | 标签 | 链接 | Tip |
| --- | --- | --- | --- |
| [Foundation Visual Encoders Are Secretly Few-Shot Anomaly Detectors](https://proceedings.iclr.cc/paper_files/paper/2026/hash/9e47a0bc530cc88b09b7670d2c130a29-Abstract-Conference.html) | <code>少样本</code> <code>视觉基础模型</code> <code>跨类别</code> | [PDF](https://proceedings.iclr.cc/paper_files/paper/2026/file/9e47a0bc530cc88b09b7670d2c130a29-Paper-Conference.pdf) · [代码](https://github.com/ymxlzgy/FoundAD) | <details><summary>查看 Tip</summary><p>在视觉基础模型的嵌入空间学习投影，利用图像特征偏离自然图像分布的程度做跨类别少样本检测。</p></details> |
| [PIRN: Prototypical-based Intra-modal Reconstruction with Normality Communication for Multi-modal Anomaly Detection.](https://proceedings.iclr.cc/paper_files/paper/2026/hash/f7e7fabd73b3df96c54a320862afcb78-Abstract-Conference.html) | <code>少样本</code> <code>RGB 与点云</code> <code>原型重建</code> | [PDF](https://proceedings.iclr.cc/paper_files/paper/2026/file/f7e7fabd73b3df96c54a320862afcb78-Paper-Conference.pdf) | <details><summary>查看 Tip</summary><p>为 RGB 和三维模态建立正常原型，并在重建时交换正常线索，缓解少样本下跨模态对齐不可靠的问题。</p></details> |
| [JUDO: A Juxtaposed Domain-Oriented Multimodal Reasoner for Industrial Anomaly QA](https://proceedings.iclr.cc/paper_files/paper/2026/hash/92a7a03e1c716970848a4a86cc8243ee-Abstract-Conference.html) | <code>多模态</code> <code>视觉问答</code> <code>缺陷分割</code> | [PDF](https://proceedings.iclr.cc/paper_files/paper/2026/file/92a7a03e1c716970848a4a86cc8243ee-Paper-Conference.pdf) | <details><summary>查看 Tip</summary><p>并排比较正常参考图和待检图以定位缺陷，再通过监督微调和强化学习提升工业异常问答能力。</p></details> |
| [MRAD: Zero-Shot Anomaly Detection with Memory-Driven Retrieval](https://proceedings.iclr.cc/paper_files/paper/2026/hash/4c12e97f2e05304a451e18c9c945036f-Abstract-Conference.html) | <code>零样本</code> <code>记忆库</code> <code>跨域</code> | [PDF](https://proceedings.iclr.cc/paper_files/paper/2026/file/4c12e97f2e05304a451e18c9c945036f-Paper-Conference.pdf) · [代码](https://github.com/CROVO1026/MRAD) | <details><summary>查看 Tip</summary><p>将辅助数据的图像级和像素级特征存入记忆库，通过相似检索为新类别预测异常分数和位置。</p></details> |

### ICLR 2024

| 论文 | 标签 | 链接 | Tip |
| --- | --- | --- | --- |
| [AnomalyCLIP: Object-agnostic Prompt Learning for Zero-shot Anomaly Detection](https://arxiv.org/abs/2310.18961) | <code>零样本</code> <code>提示词学习</code> <code>跨类别泛化</code> | [PDF](https://arxiv.org/pdf/2310.18961) · [代码](https://github.com/zqhang/AnomalyCLIP) | <details><summary>查看 Tip</summary><p>学习与物体类别无关的正常和异常提示词，让 CLIP 能在未见类别中检测和定位缺陷。</p></details> |

### ICML 2026

| 论文 | 标签 | 链接 | Tip |
| --- | --- | --- | --- |
| [Remove the Ambiguity: Few-shot Multimodal Anomaly Detection Using Crossmodal Feature Replacer](https://proceedings.mlr.press/v306/guo26ai.html) | <code>少样本</code> <code>多模态</code> <code>特征重建</code> | [PDF](https://raw.githubusercontent.com/mlresearch/v306/main/assets/guo26ai/guo26ai.pdf) · [代码](https://github.com/Yuan-Honoka-Guo/CFR) | <details><summary>查看 Tip</summary><p>先进行 RGB 与三维特征的双向重建，再用高置信正常特征替换不可靠区域，避免模糊重建干扰缺陷判断。</p></details> |
| [Is Task-Specific Training Necessary for Anomaly Detection?](https://proceedings.mlr.press/v306/zhang26ck.html) | <code>免训练</code> <code>多类别</code> <code>记忆检索</code> | [PDF](https://raw.githubusercontent.com/mlresearch/v306/main/assets/zhang26ck/zhang26ck.pdf) · [代码](https://github.com/longkukuhi/RAD) | <details><summary>查看 Tip</summary><p>从正常图像建立局部特征库，用多层检索匹配待检图像块，检验多类别工业异常检测能否省去任务训练。</p></details> |
| [CoGeoAD: Hierarchical Color-Geometric Fusion with Multi-View Attention for Zero-Shot 3D Anomaly Detection](https://proceedings.mlr.press/v306/xu26bg.html) | <code>零样本</code> <code>三维质检</code> <code>多视角融合</code> | [PDF](https://raw.githubusercontent.com/mlresearch/v306/main/assets/xu26bg/xu26bg.pdf) | <details><summary>查看 Tip</summary><p>将多视角的颜色和几何信息对齐，用分层融合同时检测纹理和结构缺陷，在 MVTec 3D-AD 与 Eyecandies 上评估。</p></details> |

### IJCAI 2026

| 论文 | 标签 | 链接 | Tip |
| --- | --- | --- | --- |
| [GRASP: Enhancing Zero-Shot Multi-Modal Anomaly Detection via Geometric Refinement and Semantic Prompting](https://ijcai.org/proceedings/2026/185) | <code>零样本</code> <code>多模态</code> <code>结构缺陷</code> | [PDF](https://ijcai.org/proceedings/2026/0185.pdf) | <details><summary>查看 Tip</summary><p>用频域变换从点云构造深度输入，再融合局部视觉证据与文本提示，定位 RGB 中不易察觉的结构缺陷。</p></details> |

### IJCV 2026

| 论文 | 标签 | 链接 | Tip |
| --- | --- | --- | --- |
| [ResAD++: Towards Class Agnostic Anomaly Detection via Residual Feature Learning](https://doi.org/10.1007/s11263-026-02885-1) | <code>跨类别</code> <code>残差特征</code> <code>仅正常样本</code> | [PDF](https://link.springer.com/content/pdf/10.1007/s11263-026-02885-1.pdf) · [代码](https://github.com/xcyao00/ResAD) | <details><summary>查看 Tip</summary><p>匹配正常参考并用特征差构造残差，再学习跨类别的正常残差分布，支持对未见类别直接检测。</p></details> |
| [The MVTec AD 2 Dataset: Advanced Scenarios for Unsupervised Anomaly Detection](https://doi.org/10.1007/s11263-026-02743-0) | <code>工业基准</code> <code>微小缺陷</code> <code>光照变化</code> | [PDF](https://link.springer.com/content/pdf/10.1007/s11263-026-02743-0.pdf) | <details><summary>查看 Tip</summary><p>扩展 MVTec 基准，覆盖透明件、重叠件、微小缺陷和特殊光照，并提供光照变化场景用于测试鲁棒性。</p></details> |

### NeurIPS 2026

| 论文 | 标签 | 链接 | Tip |
| --- | --- | --- | --- |
| [GATE-AD: Graph Attention Network Encoding for Few-Shot Industrial Visual Anomaly Detection](https://neurips.cc/virtual/2026/poster/151322) | <code>少样本</code> <code>图注意力</code> <code>特征重建</code> | — | <details><summary>查看 Tip</summary><p>把局部图像特征建成近邻图，用图注意力重建正常的邻域关系，以重建误差检测缺陷。</p></details> |
| [AirIAD: Agentic Iterative Reasoning for Industrial Anomaly Detection](https://neurips.cc/virtual/2026/poster/153593) | <code>智能体</code> <code>多模态</code> <code>缺陷诊断</code> | — | <details><summary>查看 Tip</summary><p>让模型迭代调用局部放大和知识检索工具，交叉核对视觉与语义证据，逐步细化缺陷诊断。</p></details> |
| [M3-AD: Reflection-aware Multi-modal, Multi-category, and Multi-dimensional Benchmark and Framework for Industrial Anomaly Detection](https://neurips.cc/virtual/2026/poster/149620) | <code>工业基准</code> <code>多模态</code> <code>自我纠错</code> | — | <details><summary>查看 Tip</summary><p>提供用于训练和评估工业质检模型反思能力的数据，并让模型在初次判断不可靠时重新检查和修正结果。</p></details> |
| [Towards Explainable Industrial Anomaly Detection via Knowledge-Guided Latent Reasoning](https://neurips.cc/virtual/2026/poster/151471) | <code>可解释性</code> <code>知识检索</code> <code>潜空间推理</code> | — | <details><summary>查看 Tip</summary><p>检索产品类别的缺陷知识，用熵引导模型在潜空间迭代推理，并动态补入更有信息的局部图像特征。</p></details> |
| [InCLAD: A Continual Learning Benchmark for Industrial Visual Anomaly Detection](https://neurips.cc/virtual/2026/poster/139535) | <code>持续学习</code> <code>半监督</code> <code>工业基准</code> | [PDF](https://arxiv.org/pdf/2610.15032) | <details><summary>查看 Tip</summary><p>将不同工业零件组织成连续到达的任务，比较多种任务顺序下模型学习新零件时保留旧检测能力的程度。</p></details> |

### TIP 2026

| 论文 | 标签 | 链接 | Tip |
| --- | --- | --- | --- |
| [Hierarchical Dense Aggregation Network for Few-Shot Metal Surface Defect Segmentation](https://doi.org/10.1109/tip.2026.3728632) | <code>少样本</code> <code>金属表面</code> <code>缺陷分割</code> | [代码](https://github.com/VDT-2048/HDANet) | <details><summary>查看 Tip</summary><p>用正常与缺陷先验引导分割，再聚合多层特征抑制噪声，同时发布带像素标注的金属表面缺陷基准。</p></details> |
| [Few-Shot Strip Steel Surface Defect Segmentation via Pre-Trained Variational Auto-Encoder-Based Latent Gaussian Process Regression](https://doi.org/10.1109/tip.2026.3671617) | <code>少样本</code> <code>带钢表面</code> <code>缺陷分割</code> | — | <details><summary>查看 Tip</summary><p>结合预训练变分自编码器和潜空间高斯过程回归，用少量标注样本分割带钢表面缺陷。</p></details> |
| [Accurate Industrial Anomaly Detection and Localization Using Weakly-Supervised Residual Transformers](https://doi.org/10.1109/tip.2026.3659337) | <code>弱监督</code> <code>特征残差</code> <code>缺陷定位</code> | [代码](https://github.com/BeJane/WeakREST) | <details><summary>查看 Tip</summary><p>用弱标注异常样本训练残差 Transformer，在降低像素级标注成本的同时学习检测和定位工业缺陷。</p></details> |

### TPAMI 2026

| 论文 | 标签 | 链接 | Tip |
| --- | --- | --- | --- |
| [PCBClip: Vision-Language Defect Detection Model for Low-Sample Inspection Systems](https://doi.org/10.1109/tpami.2026.3711750) | <code>PCB 质检</code> <code>少标注</code> <code>视觉语言模型</code> | — | <details><summary>查看 Tip</summary><p>用局部图像块生成候选区域，以领域文本提示和正常样本约束减少少量粗标注对 PCB 缺陷检测的影响。</p></details> |
| [ZUMA: Training-Free Zero-Shot Unified Multimodal Anomaly Detection](https://doi.org/10.1109/tpami.2026.3658856) | <code>零样本</code> <code>多模态</code> <code>免训练</code> | — | <details><summary>查看 Tip</summary><p>通过跨域校准缩小 CLIP 与点云表征之间的差距，直接利用纹理和三维结构开展免训练异常检测。</p></details> |
| [MuSc-V2: Zero-Shot Multimodal Industrial Anomaly Classification and Segmentation With Mutual Scoring of Unlabeled Samples](https://doi.org/10.1109/tpami.2026.3688174) | <code>零样本</code> <code>多模态</code> <code>互评分</code> | [PDF](https://arxiv.org/pdf/2511.10047) · [代码](https://github.com/HUST-SLOW/MuSc-V2) | <details><summary>查看 Tip</summary><p>通过无标签样本之间的局部相似性互相评分，并融合二维与三维异常图以找回单一模态容易漏检的缺陷。</p></details> |

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
