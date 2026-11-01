# Text Analyzer

## 项目目标与需求

使用逐行生成器分析多个 TXT，统计字符、总词数、过滤后的词频、Top 20、Bigram 和 Trigram，保存 JSON 与 CSV。

## 输入数据

一个或多个 UTF-8 TXT；连续英文字母为单词，统一小写。原始字符数包含换行；总词数在停用词过滤前统计，unique_words 与 n-gram 在过滤后统计。

## 文件结构

reader.py → tokenizer.py → ngram.py → analyzer.py → reporter.py → cli.py 每个项目的测试位于 tests/，不依赖练习的 TODO 实现。

## 运行方法

先在仓库根目录完成环境安装，再生成数据。下列命令均在根目录运行：

```bash
python scripts/generate_datasets.py
python -m phase1_python_programming.section01_data_structures.projects.text_analyzer.src.text_analyzer.cli datasets/generated/sample.txt phase1_python_programming/section01_data_structures/projects/text_analyzer/data/sample.txt --stop-words data --output datasets/processed/text_analysis
```

只生成 NumPy/标准库数据时，可用 `python scripts/generate_datasets.py --only core`。
输出命令均接受 `--help`，具体输入/输出路径可通过参数覆盖。File Toolkit 默认只展示计划；需要写入时添加 `--apply`。Cleaning Pipeline 拒绝覆盖已存在的输出 CSV，重复运行前更换输出文件名。

## 预期输出

analysis.json 与 word_frequency.csv；每个文件的 n-gram 不与下个文件连接，文件内部跨行连接。

## 验收标准

词频与 n-gram 正确；空文件合法；过滤停用词；多个文件可合并；不能整体 read/readlines，大文件测试禁止这两个调用。

```bash
python -m pytest phase1_python_programming/section01_data_structures/projects/text_analyzer/tests -q
```

## 学习任务

先读 README 并执行小样例，再逐模块阅读实现，补充一个未覆盖的边界测试，最后在不改变契约的前提下改进实现。请先独立完成本 Section 的练习再阅读项目实现。
