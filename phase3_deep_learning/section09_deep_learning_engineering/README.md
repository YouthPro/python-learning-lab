# Section 09 — Deep Learning Engineering

## 学习目标与知识
Advanced：将随机数、配置、训练循环、监控、停止策略、保存恢复和独立推理组成小型原生PyTorch工程，而不是复刻高级框架。
种子不代表跨硬件/版本位级复现；DataLoader自己的Generator也需保存。Checkpoint包括模型、optimizer、scheduler、epoch；恢复从下一epoch开始，日志不能重复。保存state_dict而不是整个模型，显式weights_only=True与map_location。

## 推荐顺序与每题目标
先做01—02配置和随机数，再03—07训练辅助，最后08—10保存日志；完成[毕业项目](projects/pytorch_training_framework/README.md)。完整shape/dtype/计算图契约和Hint见[题目目录](exercise_catalog.md)。

| ID | 题目 / 函数 | 学习目标 |
|---|---|---|
| 01 | Set Random Seed / `seed_everything` | Seed all RNGs; distinguish deterministic algorithms from seeds. |
| 02 | Experiment Config / `validate_config` | Read YAML with safe_load outside this function; reject nan and strings as numeric values. |
| 03 | Average Meter / `AverageMeter` | The last batch may be shorter. |
| 04 | Early Stopping / `EarlyStopping` | Reset bad-epoch counter on improvement; loss must be finite. |
| 05 | Gradient Clipping / `clip_gradients` | Clip gradients, not parameter values; AMP needs unscale first. |
| 06 | Optimizer Factory / `build_optimizer` | Frozen parameters must not be optimized. |
| 07 | Scheduler Factory / `build_scheduler` | Step after optimizer update; plateau expects validation metric. |
| 08 | Save Checkpoint / `save_checkpoint` | Keep schema keys explicit; scheduler may be None. |
| 09 | Load Checkpoint / `load_checkpoint` | state_dict restores parameters; restoring optimizer/scheduler is separate. |
| 10 | JSONL Experiment Logger / `log_experiment` | Serialize before appending so invalid records do not partially corrupt a log. |

## 项目要求与完成标准
毕业项目必须在CPU完成synthetic训练、验证、预测、CSV/JSONL日志、best/latest保存、恢复optimizer/scheduler/停止计数，并可切换MLP/CNN。ImageFolder保持train随机增强、validation确定性；输入shape与标签数受配置校验。测试不依赖GPU、数据或权重下载。

## 测试
```bash
python -m pytest phase3_deep_learning/section09_deep_learning_engineering
python -m pytest phase3_deep_learning/section09_deep_learning_engineering -m exercise
python -m pytest phase3_deep_learning/section09_deep_learning_engineering -m exercise --strict-exercises
```
TODO默认在练习模式XFAIL，不能算答题通过。项目参考实现不导入TODO。

## 常见错误与 Debug
- 恢复后轨迹不同：确认model/optimizer/scheduler/RNG/shuffle Generator都恢复，先固定CPU、workers=0和同一环境。
- loss曲线重复epoch：以checkpoint的history为权威重建CSV/JSONL，而不是盲目append。
- AMP崩溃：CUDA可用且选中时才启用；先unscale再裁剪。
- gradient accumulation尾组过小：按真实样本数归一化，不固定除以累积步数。
- best和latest混用：best用于验证选择，latest用于继续；保留两者，禁止意外覆写既有run。
- yaml配置无效：检查类型与键名，safe_load后仍需值域校验；bool不能充当epochs。

## 官方资源
- [Checkpoint](https://pytorch.org/tutorials/recipes/recipes/saving_and_loading_a_general_checkpoint.html)
- [AMP](https://pytorch.org/tutorials/recipes/recipes/amp_recipe.html)
- [TensorBoard（可选扩展）](https://pytorch.org/tutorials/recipes/recipes/tensorboard_with_pytorch.html)
- [Profiler（可选扩展）](https://pytorch.org/tutorials/recipes/recipes/profiler_recipe.html)
- [Reproducibility](https://docs.pytorch.org/docs/stable/notes/randomness.html)
