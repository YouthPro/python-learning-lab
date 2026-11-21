# Section 08 题目目录

只提供骨架、Hint与测试，不提供练习参考答案。

## 01 Custom Dataset

- 函数/类：`CustomDataset`；文件：`exercises/dataset_dataloader.py`
- 难度 Advanced；学习目标：Implement len/getitem and optional input transform; validate equal lengths.
- Input Shape → Output Shape：[N,*S], [N] -> item [*S], scalar label
- Expected dtype：inputs preserved; labels long
- 梯度 / 计算图：dataset does not detach tensor inputs
- Hint：Check labels remain paired after transform.
- 至少三个 CPU 参数用例，预训练测试始终 weights=None。

## 02 Dataset Split

- 函数/类：`split_indices`；文件：`exercises/dataset_dataloader.py`
- 难度 Advanced；学习目标：Return (train,val) disjoint shuffled indices, floor(size*val_ratio) validation; size>=0, ratio in [0,1). Do not alter global RNG.
- Input Shape → Output Shape：[N] index space -> lists N-floor(N*r),floor(N*r)
- Expected dtype：Python ints
- 梯度 / 计算图：no graph
- Hint：Use a local generator and test that seed changes ordering.
- 至少三个 CPU 参数用例，预训练测试始终 weights=None。

## 03 Class Weights

- 函数/类：`compute_class_weights`；文件：`exercises/dataset_dataloader.py`
- 难度 Advanced；学习目标：Inverse frequency N/(K*count); absent classes have zero weight; empty labels return zeros. Valid labels [0,K).
- Input Shape → Output Shape：[N] -> [K]
- Expected dtype：labels long, output float32 CPU
- 梯度 / 计算图：no gradient required
- Hint：Count missing classes without dividing by zero.
- 至少三个 CPU 参数用例，预训练测试始终 weights=None。

## 04 Padding Collate

- 函数/类：`pad_collate`；文件：`exercises/dataset_dataloader.py`
- 难度 Advanced；学习目标：Right-pad 1D sequences with zero. Return inputs,lengths,targets. Empty sequences allowed; empty batch raises ValueError.
- Input Shape → Output Shape：B sequences [Li] -> inputs[B,maxL], lengths[B], targets[B]
- Expected dtype：inputs preserved; lengths/targets long
- 梯度 / 计算图：padding should preserve paths if input needs gradients
- Hint：Separate sequence lengths from padding value.
- 至少三个 CPU 参数用例，预训练测试始终 weights=None。

## 05 Image Manifest

- 函数/类：`build_image_manifest`；文件：`exercises/dataset_dataloader.py`
- 难度 Advanced；学习目标：Sorted immediate class directories (including empty) define labels. Recursively list png/jpg/jpeg/bmp files, case-insensitive, sorted relative paths; no image decoding. Return path(relative str),label,class_name.
- Input Shape → Output Shape：class directories -> M metadata rows
- Expected dtype：strings and integer labels
- 梯度 / 计算图：no graph
- Hint：File suffix is not proof of image validity; projects check corruption separately.
- 至少三个 CPU 参数用例，预训练测试始终 weights=None。

## 06 DataLoader Factory

- 函数/类：`build_dataloader`；文件：`exercises/dataset_dataloader.py`
- 难度 Advanced；学习目标：Create CPU loader, retain final short batch; batch_size>0, num_workers>=0. pin_memory=False for this CPU contract.
- Input Shape → Output Shape：items[*S] -> batches[B,*S]
- Expected dtype：preserve dataset dtypes
- 梯度 / 计算图：loader collates; training controls graph
- Hint：shuffle training only; understand worker subprocesses vs batches.
- 至少三个 CPU 参数用例，预训练测试始终 weights=None。

## 07 Conv Output Size

- 函数/类：`conv2d_output_size`；文件：`exercises/cnn_architecture.py`
- 难度 Advanced；学习目标：One spatial axis, floor((I+2P-D*(K-1)-1)/S+1); positive I/K/S/D, P>=0 and output>=1.
- Input Shape → Output Shape：scalar I -> scalar O, apply separately to H/W
- Expected dtype：Python int
- 梯度 / 计算图：no graph
- Hint：Derive effective kernel size with dilation.
- 至少三个 CPU 参数用例，预训练测试始终 weights=None。

## 08 Build CNN

- 函数/类：`build_cnn`；文件：`exercises/cnn_architecture.py`
- 难度 Advanced；学习目标：At least two Conv/ReLU blocks and pooling, adaptive final pooling to support varying sizes; output logits.
- Input Shape → Output Shape：[B,C,H,W], H/W>=16 -> [B,K]
- Expected dtype：float32, model float32
- 梯度 / 计算图：trainable graph
- Hint：Avoid a Linear input size tied to 28x28.
- 至少三个 CPU 参数用例，预训练测试始终 weights=None。

## 09 Residual Block

- 函数/类：`build_residual_block`；文件：`exercises/cnn_architecture.py`
- 难度 Advanced；学习目标：Return same-shape block with output ReLU(x+F(x)); F contains two padded 3x3 convolutions and ReLU between them. No normalization required.
- Input Shape → Output Shape：[B,C,H,W] -> same
- Expected dtype：float32
- 梯度 / 计算图：both skip and residual preserve gradient
- Hint：Use out-of-place addition; test F=0 and negative x.
- 至少三个 CPU 参数用例，预训练测试始终 weights=None。

## 10 Top K Accuracy

- 函数/类：`topk_accuracy`；文件：`exercises/cnn_architecture.py`
- 难度 Advanced；学习目标：Fraction of samples whose label is among top k; require N>0 and 1<=k<=K.
- Input Shape → Output Shape：[N,K],[N] -> float in [0,1]
- Expected dtype：float logits; long targets
- 梯度 / 计算图：metric must not retain graph
- Hint：Top-k along class axis, not batch axis.
- 至少三个 CPU 参数用例，预训练测试始终 weights=None。

## 11 Freeze Backbone

- 函数/类：`freeze_backbone`；文件：`exercises/transfer_learning.py`
- 难度 Advanced；学习目标：ResNet-style model: freeze every parameter except fc; fc remains trainable; return same model. Mode unchanged.
- Input Shape → Output Shape：module -> unchanged
- Expected dtype：parameter dtypes preserved
- 梯度 / 计算图：backbone requires_grad=False, head=True
- Hint：Frozen parameters and frozen BatchNorm running stats are distinct.
- 至少三个 CPU 参数用例，预训练测试始终 weights=None。

## 12 Unfreeze Last Blocks

- 函数/类：`unfreeze_last_n_blocks`；文件：`exercises/transfer_learning.py`
- 难度 Advanced；学习目标：Reset backbone frozen; unfreeze last n of layer1..layer4, n in [0,4]; fc trainable, stem stays frozen. Return model.
- Input Shape → Output Shape：module -> unchanged
- Expected dtype：parameter dtypes preserved
- 梯度 / 计算图：last n stages and head track parameter grads
- Hint：n=0 must not accidentally select all via [-0:].
- 至少三个 CPU 参数用例，预训练测试始终 weights=None。

## 13 Replace Classifier

- 函数/类：`replace_classifier`；文件：`exercises/transfer_learning.py`
- 难度 Advanced；学习目标：Replace ResNet fc with trainable Linear(old in_features,K), keep device/dtype and other parameters.
- Input Shape → Output Shape：old logits[B,1000] -> [B,K]
- Expected dtype：preserve model dtype/device
- 梯度 / 计算图：new head trainable
- Hint：Do not hard-code feature width; no network request.
- 至少三个 CPU 参数用例，预训练测试始终 weights=None。

## 14 Build Image Transforms

- 函数/类：`build_transforms`；文件：`exercises/transfer_learning.py`
- 难度 Advanced；学习目标：PIL RGB conversion; training random resized crop/flip, evaluation deterministic resize; ToTensor and ImageNet mean/std.
- Input Shape → Output Shape：PIL arbitrary grayscale/RGB -> [3,S,S]
- Expected dtype：float32
- 梯度 / 计算图：input transform has no autograd graph
- Hint：Train/val must not share random augmentation; ImageNet weights expect matching normalization.
- 至少三个 CPU 参数用例，预训练测试始终 weights=None。

## 15 Predict Batch

- 函数/类：`predict_batch`；文件：`exercises/transfer_learning.py`
- 难度 Advanced；学习目标：Return CPU softmax probabilities, no gradients; preserve previous train/eval mode.
- Input Shape → Output Shape：[B,C,H,W] -> [B,K]
- Expected dtype：float32 by default
- 梯度 / 计算图：no graph
- Hint：eval alone does not disable gradients.
- 至少三个 CPU 参数用例，预训练测试始终 weights=None。
