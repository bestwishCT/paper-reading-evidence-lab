# 93.33%与80%能相乘吗：ELI5两级验证

读评估论文时，两个看似都很高的验证率很容易被乘成“可靠率”。我用ALCE的claim生成与NLI验证把这个错误拆开。本文给出核对后的科学答案、一次基础提示和一次核查提示的真实新调用，以及无需联网的教学检查。不是原论文实验复现。

## 两个百分比检查不同对象

不能把93.33%与80%相乘后宣称ELI5评估端到端可靠。ALCE附录A（物理14、印刷6478）先人工写3对训练集QA示例，每对3条sub-claims，作为text-davinci-003的提示示范。这是in-context demonstrations，不是重新训练生成模型。论文另抽40个答案，得到120条生成claim；每条只有同时“与问题相关、忠实于原答案”才打1，112条通过，8条未通过。93.33%是claim质量率。

第二个检查在相同问题上，对40个模型输出及其claim组成的120对，人工标注蕴含，再以人工标签为gold衡量TRUE的分类准确率，报告80%。它不是模型答题正确率，也不是NLI预测为蕴含的比例。相同问题、相同数量，不等于两项错误独立，更不等于已公开逐项联合标注。

|阶段|检查单位|通过含义|不能直接保证|
|---|---|---|---|
|生成claim|120条claim|相关且忠实于gold|覆盖gold的所有事实|
|NLI|120个output–claim对|预测与人工蕴含标签一致|每次判定都正确、输出无额外错误|

§3.2物理4（6468）的方向是`模型输出 → gold-derived sub-claim`，前者为premise；不是引用段落→输出句子的citation recall。三条claim近似答案的几个方面，平均14词、通常一句，并不穷尽长答案。要估计“claim合格且NLI判对”的联合概率，需要对齐的逐项质量标签与NLI对错；要估计“输出覆盖正确事实”，还要明确覆盖事件，不能把NLI accuracy当作该事件。

离线算例在假想的同一个120行总体上保留边际112与96，改变两类错误重合程度，联合通过数可以为88至96；独立假设才给89.6的期望。这个范围展示边际不足以决定联合，**不是作者实测端到端区间**；80%按报告精度解释为96/120只用于教学。代码没有跑TRUE、重新生claim或校正作者指标。

## 本次两组原答的核查

baseline D1/D2恢复示例和分母，D3拒绝直接相乘，D4方向正确；但D3把“claim合格且NLI判对”进一步写成“且预测蕴含”，悄悄换了事件，条件独立也不能让accuracy直接等于正例概率。workflow D2也正确区分两阶段，D3同样出现联合事件定义不清；D4额外引入citation concat，不是claim recall的输入，容易再混淆。

两组D1均说未给完整prompt，需要收窄为“本次所供页未给”；作者指出Table22有完整示例，不能把选页未包含说成论文没有。baseline的A-P14:36–43覆盖112和质量判据，49–60覆盖NLI验证，可回查；D1另引A-P4:44–46不足以单独说明三个示范，必须以A-P14:26–33为准。workflow全部ID写成完整SOURCE标题，机械定位失败，原答保留。此个案没有显示工作流让结果更可靠。


![必要原页，关键内容已在正文转写](17-source-page.png)

## 方法为什么这样设计

先为D1–D4写[任务](17-task.txt)与不发给模型的[标准](17-criteria.md)，核对必要页，再以[冻结哈希](17-protocol-lock.json)锁定六个文件。baseline只收任务与编号原文；workflow增加[通用核查流程](17-workflow.txt)，其余材料、问题、JSON要求、模型权限、180秒超时相同。按[协议](17-protocol.md)固定先baseline后workflow，不挑样本、不删失败。行号使每个断言可回查，但验证器只判断范围，不判断蕴含、单位或跨页限定，所以正文另作非盲语义审计。

两组没有给方法组额外gold或证据，criteria均不发送。但处理提示更长、运行顺序未随机化、服务snapshot/seed/temperature不可锁定，且每组只有一次，因此不报告统计显著、稳定增益或费用优势。本次看到了共享的定位故障，不能包装成方法胜利。

|条件|实际模型|墙钟秒（含预检）|输入token|输出token|机械检查|
|---|---|---:|---:|---:|---|
|baseline|chenkun/gpt-5-mini|24.348|3196|3369|ranges_valid|
|workflow|chenkun/gpt-5-mini|33.419|3322|4263|range_errors|

原始completion ID、模型与usage见各metadata。工具Bohrium原生CLI2.8.1，gpt-5-mini请求、photon；实际模型如表。服务没有逐次货币扣费，cost=null，不等于免费。全部10个调用中本篇仅包含自己的两次记录；其它题不进入本材料包。

## 复做：先离线检查，再选是否调用模型

下载本目录的文件，Python3标准库即可。文件前缀仅为同一仓库隔离五份作品；冻结锁中的原始文件名应加前缀`17-`后查找，其字节未改。

```sh
python 17-worked-example.py
python 17-validate.py 17-sources.json 17-baseline-output.json
python 17-validate.py 17-sources.json 17-workflow-output.json
```

离线算例预期逐字段等于[保存结果](17-worked-example-result.json)，是教学计算，不是新GPU/NLI/问答实验。验证器ranges_valid退出0、range_errors或invalid_json退出1；本次状态如上表，失败是预期保存事实而非安装故障。机械通过仍需逐项对照[编号原文](17-numbered.txt)与正文核查。

重新阅读需自行从玻尔官方渠道安装对应系统原生CLI、登录并确认额度；在保持原件不变的新目录运行：

```sh
python 17-replay.py --bohr /absolute/path/to/bohr --condition baseline --out fresh-baseline
python 17-replay.py --bohr /absolute/path/to/bohr --condition workflow --out fresh-workflow
```

脚本先dry-run逐字核对message，真实调用保留请求/原答/响应/usage/stderr，不覆盖已有out。非语义UUID不同，结果不保证相同。Windows用原生exe避免.cmd多行截断，命令行不得超系统长度；只从子进程移除代理变量，不改系统配置。source_id失败应先被拒绝，不能静默把整段标题映射回ID冒充原答成功。

后续拟修复方式：提示显式列出允许ID并提供字段示例，要求只输出ID值；解析器拒绝标题、页码后缀和未知ID。此方式**本篇尚未追加调用验证**；保存workflow保持原样，以便别人复核本次实际失败。

## 文件导航

核心输入为[task](17-task.txt)、[workflow](17-workflow.txt)、[sources](17-sources.json)、[编号文本](17-numbered.txt)，[协议](17-protocol.md)与[验收标准](17-criteria.md)先于调用冻结。baseline/workflow各自的-request.txt是实际message，-preflight.json保存dry-run，-response.json为余额脱敏后的完整响应，-output.json为原答，-metadata.json为模型与usage，-stderr.txt保留stderr，-validation.json为严格定位结果。正文核查与原答分开，无静默修答案。

来源版本、许可与个人贡献见[SOURCES](17-SOURCES.md)。读者若仅核查关键结论，无需运行模型；材料离线齐全。Codex协助设计、运行和非盲审计；没有新的人类独立评审、原论文训练或部署收益测量。
