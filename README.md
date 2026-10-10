# An-Open-Ebook-for-Diffusion

## Introduction

这是一本任意使用的电子书，主要面向熟悉数学分析，线代，机器学习的读者。其中很多地方用了ai辅助，但经过仔细审查应该没问题，主要还是批判性地看。其中流匹配部分还有待修改，可能以后会改一下。我直接把整个编辑的项目传上来，方便各路人士修改，多多指教。

This is an open ebook that anybody can read and revise if interested.

* Take it and revise it freely. Though at the moment only Chinese version is available, adopting a machine-translation is convenient.
* This book is aiming at readers who have grasped basic knowledge of calculus, linear algebra and machine learning
* AI does assist when it comes to typesetting and the simplifying proofs.
* This book is carefully checked since AI, but small bugs might still appear so be critical.
* Flow matching part is not satisfactory, this part would get a future modified edition.

The whole latex components are uploaded for the convenience of open editing.

## Illustration

### 扩散模型：从分布直觉到多模态生成

中文 LaTeX 电子书，面向熟悉数学分析、线性代数和机器学习的读者。

#### 阅读

成书 PDF：`扩散模型：从分布直觉到多模态生成.pdf`。

正文四章：

1. **生成的本质：从图像到分布**——分布与采样、高维几何、去噪、隐变量与隐空间，以及 VAE、GAN、AR、Flow、EBM 的关系。
2. **数学主线：从去噪回归到概率输运**——DDPM 前向边缘、后验、ELBO、噪声回归、score 与 Tweedie、Langevin、SDE、反向时间、概率流 ODE、连续流似然、Flow Matching 与引导。
3. **从数学到算法：扩散与流的设计谱系**——DDPM、DDIM、Score SDE、Improved DDPM、EDM、DPM-Solver、Flow Matching、Rectified Flow、蒸馏与一致性模型。
4. **从图像生成到多模态世界**——U-Net、文本条件、LDM、DiT、MM-DiT、编辑与控制、视频、统一多模态、音频、科学应用与未来方向。

五个附录补充概率工具、连续动力学、长证明、术语和阅读实验。目录、公式、章节、术语及参考文献均有链接；PDF 阅读器的“上一视图”可返回跳转前的位置。每个正文章节提供五道练习和解答思路。

文献核查截至 **2026-10-09**。近期论文明确区分预印本、技术报告和官方产品披露；未公开的商业架构不作猜测。未来方向是分析判断。教学图与解析例子由本项目编写，不冒充真实图像模型的训练或测评结果。

#### 源码

- `main.tex`：唯一编译入口。
- `book-style.tex`：电子书页幅、字体、颜色、教学框与链接设置。
- `chapters/`：四章正文。
- `appendices/`：附录。
- `references.bib`：去重后的正式参考文献。
- `references/`：按章节保留的原始文献记录。
- `qa/`：一手来源审计、公式检查与成书检查记录。
- `scripts/`：构建、文献合并与检查工具。
- `vendor/texmf/`：补齐本机缺少的公开 LaTeX 组件；不会修改系统安装。

#### 编译

使用 **XeLaTeX + Biber**。已有完整 TeX Live / MiKTeX 环境时，在项目目录运行：

```powershell
.\scripts\build.ps1
```

脚本顺序为 XeLaTeX → Biber → XeLaTeX → XeLaTeX，将构建文件放进 `build/` 并复制最终 PDF 到目录根。脚本使用项目私有依赖，禁用 shell escape，并在检测到 MiKTeX 时禁用自动包安装。本机 MiKTeX 在受限环境中需读取现有运行时配置；构建记录见 `qa/compile-environment.md`。

若系统已有全部模板依赖，也可手工运行以下标准命令。缺少组件或希望使用附带的 vendor 文件时，请使用上面的构建脚本，它会设置私有搜索路径；手工命令不自动使用 vendor。先在项目目录创建 `build/`：

```text
xelatex -no-shell-escape -output-directory=build main.tex
biber --input-directory=build --output-directory=build main
xelatex -no-shell-escape -output-directory=build main.tex
xelatex -no-shell-escape -output-directory=build main.tex
```

若本地环境缺少模板组件，请通过构建脚本使用附带的私有文件。Overleaf 上传源码包后，将主文件设为 `main.tex`，编译器设为 XeLaTeX，使用足够新的完整 TeX Live 环境；通常不需要额外下载私有组件。字体检测到宋体、微软雅黑和楷体全部存在时采用该组合，否则回退到 Fandol 中文字体。

#### 验证与边界

`scripts/verify_mathematics.py` 在低维解析设置中独立检查 DDPM 后验、v 参数化、VP 概率流系数、Gaussian CFM、似然符号和高斯稳态。`scripts/audit_book.py` 检查四章结构、引用键、术语标签、PDF 跳转目标和编译警告。它们需要 Python、NumPy、pypdf。

这些验证可以发现公式与排版中的明确问题，不能证明一本教材永无错误，也不是大模型训练实验。最终质量记录见 `qa/FINAL_REVIEW.md`。

#### 模板来源

采用 [ElegantBook v4.7](https://github.com/ElegantLaTeX/ElegantBook) 的原始类文件，遵循 **LPPL 1.3c 或更新版本**；许可证见 `ELEGANTBOOK-LICENSE.txt`。电子书定制位于独立样式文件，未修改原类。私有依赖来自公开 TeX Live / CTAN，保留文件头与包元数据中的版权和许可信息；引用论文的权利归原作者。
