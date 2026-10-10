# 全书协作约定

书名：《扩散模型：从分布直觉到多模态生成》。中文教材，面向熟悉数学分析、线性代数、机器学习的读者。四个正文章节，附录独立。语气亲切而严谨，避免仅作综述或堆砌论文。所有解释为原创；论文摘要只作简短归纳，引用支持关键历史与技术来源。

## 符号与时间

- 离散 DDPM：x_0 数据，x_k (k=1,...,K) 含噪样本；beta_k、alpha_k=1-beta_k、abar_k=prod alpha_j；epsilon~N(0,I)。LaTeX 写作 \bar\alpha_k。
- 连续扩散：t∈[0,1] 从数据到噪声，x_t=a(t)x_0+b(t)epsilon。score s_t(x)=nabla_x log p_t(x)。生成时积分 t:1→0。
- Flow Matching：用 tau∈[0,1] 从噪声到数据，Z 噪声、X 数据，Y_tau=(1-tau)Z+tau X，速度 u_tau。明确 tau=1-t 是反向时钟但路径未必相同。
- v-prediction：a^2+b^2=1 时 v=a epsilon-b x_0，不能把它不加限定地叫 ODE 速度。
- 条件 c；模型参数 theta；维数 d；数据分布 p_data；噪声分布 p_noise。

## LaTeX

主类 ElegantBook，XeLaTeX，biblatex/biber。可用 amsmath/amssymb, booktabs, tabularx, longtable, tikz, pgfplots, enumitem, tcolorbox。图宽 <=\linewidth，表格用 tabularx 或分栏，公式长则 align 拆行。避免长英文小节标题。章节文件只写内容，从 \chapter 开始；不要 preamble。

统一宏：\E (期望), \R, \N (正态分布), \KL, \dd (直立微分), \norm{...}, \ip{a}{b}, \pdata, \pnoise, \score, \eps, \vtheta, \utheta, \grad, \divg。

统一盒子：\begin{intuitionbox}{标题}...\end{intuitionbox}；同理 keybox, cautionbox, examplebox, derivationbox；正文保持完整段落，盒子仅放关键结论。\term{中文名}{gl:label} 链接术语附录。\readingguide{...} 为章首导读。\chaptertakeaway{...} 为章末回顾。\begin{exercisebox}{标题}...\end{exercisebox} 为练习，答案可在本章末简要列出。

交叉链接：正文标签 ch:concepts,ch:math,ch:methods,ch:applications；数学小节 sec:ddpm-forward,sec:ddpm-elbo,sec:score,sec:sde,sec:pfode,sec:flowmatching,sec:guidance,sec:parameterization；公式 eq:forward-marginal,eq:posterior,eq:elbo,eq:simple-loss,eq:dsm,eq:reverse-sde,eq:pfode,eq:cfm,eq:cfg；附录 app:probability,app:stochastic,app:proofs,app:glossary,app:exercises。

预定术语标签（可引用这些）：gl:distribution,gl:density,gl:manifold,gl:latent,gl:kl,gl:elbo,gl:score,gl:sde,gl:ode,gl:brownian,gl:ito,gl:fp,gl:continuity,gl:coupling,gl:transport,gl:cfg,gl:attention,gl:token,gl:vae,gl:gan,gl:flow,gl:ar,gl:snr,gl:fid,gl:distillation,gl:patch,gl:likelihood,gl:jacobian,gl:markov,gl:conditional,gl:divergence,gl:lipschitz,gl:stiffness,gl:entropy,gl:reparameterization,gl:perceptual,gl:equivariance,gl:bridge。

## 分工

concepts：chapters/01-concepts.tex + references/concepts.bib + qa/concepts-sources.md。
methods：chapters/03-methods.tex + references/methods.bib + qa/methods-sources.md。
applications：chapters/04-applications.tex + references/applications.bib + qa/applications-sources.md。
root：主文件/模板、第二章、附录、图、编译与检查。

引用键需前缀 c_,m_,a_,r_ 避免冲突。每章目标：概念 9000–14000 中文字、方法 10000–15000 中文字、应用 10000–15000 中文字（不硬凑字数，以充分解释为先）。每章至少 2 个原创教学图或对比表，至少 3 道带解答思路的练习。不要直接引入未经解释的必要术语。近年材料截至 2026-10-09，区分论文、技术报告、官方产品披露和前瞻推断。不要称未经核实的模型为最新/最优。
