# 自动生成数据

从仓库根目录执行 `python scripts/generate_datasets.py --seed 42`。文件包括 ecommerce/ 三张带质量问题的 CSV、housing.csv、classification.csv、vectors.npy、regression.npz、两次训练日志、sample.txt、sample.png 和 manifest.json。

仅生成不依赖 sklearn 的数据时添加 `--only core`。生成脚本可指定 --output 目录；同种子与相同依赖版本的结果一致。此处的数据是教学模拟数据，不代表真实业务。
