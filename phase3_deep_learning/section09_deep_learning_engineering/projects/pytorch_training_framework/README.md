# PyTorch Training Framework

轻量、原生、可运行的参考工程。核心代码不依赖练习TODO、Lightning、Web、数据库或Docker。安装仓库 `.[dev,deep-learning]` 后，`training_framework` 是与原仓库dataset_inspector相同方式的公开模块别名，真实实现位于src/training_framework。

## 学习目标与任务拆分
1. config/seed：严格YAML校验、路径规则、复现边界。
2. datasets/models：固定输入输出规范，隔离数据、模型、训练。
3. engine：原生zero_grad/forward/backward/step与独立validation。
4. utils：样本加权指标、early stopping、CSV/JSONL和state_dict checkpoint。
5. CLI：训练、验证、推理、从epoch边界恢复。
6. 对照连续训练与恢复训练的权重和指标，解释不同而不是掩盖断言。

## 结构与职责
```text
configs/ default.yaml mlp.yaml cnn.yaml
src/training_framework/
  config.py seed.py cli.py
  datasets/ synthetic.py image_folder.py __init__.py
  models/ mlp.py cnn.py __init__.py
  engine/ trainer.py evaluator.py predictor.py optim.py
  utils/ metrics.py checkpoint.py logger.py early_stopping.py
scripts/generate_demo_data.py
tests/
checkpoints/ logs/ outputs/
```
MLP/CNN与部分小工具复用Phase3参考项目，共享实现不属于练习答案。各项目均可从已安装仓库独立调用。

## 运行（以下在项目目录）
先在仓库根安装依赖，再进入项目目录；同一个虚拟环境应保持激活。
```bash
cd phase3_deep_learning/section09_deep_learning_engineering/projects/pytorch_training_framework
python -m training_framework.cli train --config configs/default.yaml
python -m training_framework.cli evaluate --config configs/default.yaml --checkpoint checkpoints/best.pt
python -m phase3_deep_learning.section09_deep_learning_engineering.projects.pytorch_training_framework.scripts.generate_demo_data --root outputs/demo_images --sample sample.jpg
python -m training_framework.cli predict --checkpoint checkpoints/best.pt --input sample.jpg
python -m training_framework.cli train --config configs/default.yaml --resume checkpoints/latest.pt --epochs 5
```
也可从仓库根执行：
```bash
python -m training_framework.cli train --config phase3_deep_learning/section09_deep_learning_engineering/projects/pytorch_training_framework/configs/default.yaml --run-dir /tmp/python_lab_phase3_framework --epochs 2
```
--run-dir是明确的输出覆盖选项，相对路径相对于当前工作目录；配置内相对run_dir/data.root相对于configs的父目录。新训练拒绝覆盖已有best/latest，请选择新目录或显式--resume。epochs是训练总上限，恢复时从保存epoch+1开始；epochs未增大时不会伪造新epoch。

## 数据、模型与增强
默认synthetic：240张[1,16,16] float32图片、int64标签、3类，固定seed，train/val索引互斥并保存outputs/split.json。MLP输出[B,K] logits；CNN含Conv/BN/ReLU/Pool/Dropout和自适应池化。
ImageFolder示例配置（新建configs/folder.yaml）：
```yaml
run_dir: outputs/folder_run
data:
  kind: image_folder
  root: outputs/demo_images
  val_ratio: 0.2
model:
  name: cnn
  input_shape: [3, 32, 32]
  num_classes: 3
```
输入须是类别子目录；使用自定义PIL Dataset，排序标签、验证损坏图片、训练随机裁剪/flip、验证确定性。data.kind不能悄悄触发下载。图片原内容和split一起计算fingerprint，恢复时改文件会报错。映射和Normalize随checkpoint保存，单图推理不需要config也不访问网络。

## Checkpoint 与日志
- checkpoints/latest.pt：每epoch边界的完整状态；best.pt：最小val_loss的完整状态。
- 保存model/optimizer/scheduler/scaler、epoch、best_metric/best_epoch、early stopping、配置、类别、预处理、RNG、train/val Generator状态、数据指纹及history。
- load显式weights_only=True、map_location=cpu，再加载白名单MLP/CNN并迁移device；从不执行checkpoint中的自定义import或序列化模型。
- resume允许增大epochs、改变输出位置/device/threads；其余训练/数据配置变化报错。迁移输出位置时保留原best.pt和latest.pt在一起；保持已达到的early stopping状态。
- logs/metrics.csv和metrics.jsonl记录epoch、train/val loss、accuracy、样本数、学习率、epoch duration和amp_enabled。恢复从checkpoint重建history，修复不完整日志，避免重复epoch。
- outputs/learning_curves.png是真实训练曲线；当前支持epoch边界恢复，不承诺任意batch中途无缝恢复。

## 设备与可选功能
默认CPU，--device auto会依次检查CUDA/MPS/CPU。明确指定不可用设备报错，不写死cuda。
training.amp只在CUDA设备启用；CPU/MPS自动禁用并记录amp_enabled=false。gradient_accumulation支持最后一个不满窗口和短batch，按实际样本数归一化，AMP先unscale再clip。CPU测试不能证明CUDA/MPS真实硬件正确性；更换硬件、PyTorch版本或worker策略不保证位级复现。
TensorBoard与Profiler为学习扩展，当前不加入额外依赖或声称已实现。

## 测试与最终验收
在仓库根运行：
```bash
python -m pytest phase3_deep_learning/section09_deep_learning_engineering/projects/pytorch_training_framework/tests
```
- CPU MLP和CNN完成训练、验证并产生best/latest与图表。
- 连续3epoch与1epoch+恢复到3epoch得到相同权重、loss、accuracy、LR和停止计数（同一CPU环境）。
- 最后短batch的累积梯度等于单大batch参考，验证loss按样本加权。
- checkpoint重载预测、unsafe模块pickle拒绝、配置错误被捕获。
- 旧run不被意外覆盖；JSONL损坏可从checkpoint恢复。
- synthetic与ImageFolder均不联网，API职责清晰。
