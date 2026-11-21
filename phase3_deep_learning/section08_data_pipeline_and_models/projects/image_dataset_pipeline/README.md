# image_dataset_pipeline

可独立运行的参考项目，安装仓库 `.[dev,deep-learning]` 后从仓库根目录运行。

## 任务拆分与结构
1. 检查输入/标签与数据划分。
2. 实现并验证数据和模型模块。
3. 调用原生训练循环（不导入练习TODO）。
4. 保存产物，检查结果和边界。

`src/` 分离数据、模型与命令；`tests/` 为CPU离线测试；`scripts/` 存放相关生成入口。共享工具位于 `phase3_deep_learning/common/`。

## 数据与运行
输入类目录 bird/cat/dog，自己实现 DirectoryImages，不依赖 ImageFolder。提供损坏检查、RGB/Resize/随机裁剪/随机水平翻转/Normalize、train-only class counts/weights、DataLoader和精确split清单。
```bash
python -m phase3_deep_learning.section08_data_pipeline_and_models.projects.image_dataset_pipeline --generate-demo --root outputs/phase3/demo_images --output outputs/phase3/splits.json
python -m phase3_deep_learning.section08_data_pipeline_and_models.projects.image_dataset_pipeline --root outputs/phase3/demo_images --workers 1 --output outputs/phase3/splits_worker.json
```
支持自定义目录；不带--generate-demo只读原图。生成器只覆盖自己命名的generated_*.png，不删除用户自备文件；同参数重跑相同。改变样本数请用新目录。data/demo附带seed=42自动生成的6张图片，也可使用 scripts/generate_demo_data 模块。
验收：损坏图片明确出现在errors；标签排序稳定；split互斥且可复现；验证transform稳定；支持短batch和worker进程。类别权重只用train计算，缺失类别权重0。

## 测试
```bash
python -m pytest phase3_deep_learning/section08_data_pipeline_and_models/projects/image_dataset_pipeline/tests
```
