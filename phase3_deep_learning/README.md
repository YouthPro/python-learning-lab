# Phase 3 — Deep Learning with PyTorch

从可微Tensor到可恢复训练工程。只追加新阶段，不修改Phase1/2的练习或项目。

| Section | 练习 | 可运行项目 |
|---|---:|---|
| [07 Fundamentals](section07_pytorch_fundamentals/README.md) | 18 | MLP、FashionMNIST MLP |
| [08 Data & Models](section08_data_pipeline_and_models/README.md) | 15 | Image Pipeline、CNN、ResNet18 Transfer |
| [09 Engineering](section09_deep_learning_engineering/README.md) | 10 | Training Framework |

## 环境
Python3.11+。先按[官方安装选择器](https://pytorch.org/get-started/locally/)选择CPU/CUDA/MPS兼容的Torch/Torchvision，不固定任何CUDA版本，再在仓库根安装：
```bash
python -m pip install -e '.[dev,deep-learning]'
```
Linux纯CPU示例（其他平台按官方选择器）：
```bash
python -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
python -m pip install -e '.[dev,deep-learning]'
```
Torchvision包声明与Torch的版本依赖，安装后运行 `python -c "import torch, torchvision; print(torch.__version__, torchvision.__version__)"` 验证；pip check检查其余依赖。

## 练习与项目分离
43题都是签名+文档+TODO+测试，没有练习答案；18+15+10分别包含至少3个CPU用例。项目是真实参考实现，不导入练习。共享工程工具在common/，学习时先做练习再读项目。
```bash
pytest                         # 项目与仓库检查；默认排除exercise
pytest -m exercise             # 未实现TODO显式XFAIL
pytest -m exercise --strict-exercises  # TODO直接失败
pytest --cov                   # 覆盖率；TODO未覆盖不能算完成
```
没有deep-learning可选依赖时可显式运行Phase1/2路径；完整测试需要安装可选组，缺依赖不会被静默记成成功。

## 下载与离线边界
只有Fashion/CNN项目的--download，或迁移项目的--download-data/--pretrained允许下载。所有导入、默认测试、synthetic训练和已保存checkpoint推理不联网。自动测试拦截网络并使用内存Tensor或临时PIL图，num_workers进程IPC不被阻断。

## 学习与验收
详见[阶段学习指南](../docs/phase3_learning_guide.md)和各项目README。设备选择默认CPU，auto检测加速器；AMP仅CUDA。相同种子在固定环境复现，不承诺跨硬件版本。框架检查epoch边界完整恢复，best和latest含义分开。

兼容原评分器：显式指定某节的练习tests路径时保留原练习收集行为；默认无参数pytest仍只测项目。显式-m始终优先。
