# Image Processor

## 项目目标与需求

Pillow 仅负责图片读写，使用 NumPy 实现灰度、亮度、对比度、归一化、裁剪、90° 整数倍旋转及批处理。

## 输入数据

二维灰度 (H,W) 或 RGB (H,W,3)。uint8 范围 0..255；float32 范围 0..1；拒绝空图片与非有限数。

## 文件结构

src/image_processor.py；tests/test_image_processor.py。validate、纯数组变换与批量 I/O 分开。 每个项目的测试位于 tests/，不依赖练习的 TODO 实现。

## 运行方法

先在仓库根目录完成环境安装，再生成数据。下列命令均在根目录运行：

```bash
python scripts/generate_datasets.py
python -m phase2_data_science.section03_numpy.projects.image_processor.src.image_processor datasets/generated/sample.png --operation grayscale --output datasets/processed/images
python -m phase2_data_science.section03_numpy.projects.image_processor.src.image_processor datasets/generated/sample.png --operation crop --box 0 0 16 16 --output datasets/processed/crops
```

只生成 NumPy/标准库数据时，可用 `python scripts/generate_datasets.py --only core`。
输出命令均接受 `--help`，具体输入/输出路径可通过参数覆盖。File Toolkit 默认只展示计划；需要写入时添加 `--apply`。Cleaning Pipeline 拒绝覆盖已存在的输出 CSV，重复运行前更换输出文件名。

## 预期输出

输出目录中的 PNG；裁剪按 (left,top,right,bottom)，旋转 k 为顺时针次数。API normalize 返回 float32，保存图片时转换回 uint8。

## 验收标准

每个变换有数值断言；像素裁剪、dtype 保持、亮度/对比度因子非负；灰度权重 [.299,.587,.114]；对比度围绕各通道均值调整。

```bash
python -m pytest phase2_data_science/section03_numpy/projects/image_processor/tests -q
```

## 学习任务

先读 README 并执行小样例，再逐模块阅读实现，补充一个未覆盖的边界测试，最后在不改变契约的前提下改进实现。请先独立完成本 Section 的练习再阅读项目实现。
