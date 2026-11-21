# Section 07 题目目录

每题是独立 TODO；测试定义契约，不包含参考函数实现。使用 `pytest -m exercise` 运行；`--strict-exercises` 将未完成题目记为失败。

## 01 Tensor Factory

- 文件：`exercises/tensor_operations.py`；签名：`create_tensor`
- 难度：Medium → Advanced；学习目标：Copy input into a new CPU tensor; dtype=None uses Torch inference. No alias to source storage.
- Input Shape → Output Shape：rectangular data [*S] -> [*S]
- Expected dtype：inferred or explicit dtype
- 梯度与计算图：new leaf, requires_grad=False
- Hint / 梯度推导提示：Compare tensor construction with as_tensor; validate dtype in tests.
- CPU 测试：至少三个参数用例，检查数值、shape 与相关梯度语义。

## 02 Shape Transformation

- 文件：`exercises/tensor_operations.py`；签名：`transform_tensor`
- 难度：Medium → Advanced；学习目标：Reshape, allowing one inferred -1; support non-contiguous inputs.
- Input Shape → Output Shape：[*S], same element count -> [*shape]
- Expected dtype：same as x
- 梯度与计算图：preserve autograd connection for floating input
- Hint / 梯度推导提示：Think about when view requires contiguous memory.
- CPU 测试：至少三个参数用例，检查数值、shape 与相关梯度语义。

## 03 Add Batch Dimension

- 文件：`exercises/tensor_operations.py`；签名：`add_batch_dim`
- 难度：Medium → Advanced；学习目标：Insert one singleton axis, including negative dimensions; do not remove existing axes.
- Input Shape → Output Shape：[d0,...] -> singleton inserted at dim
- Expected dtype：same as x
- 梯度与计算图：preserve computation graph
- Hint / 梯度推导提示：Read the legal range of unsqueeze dimensions.
- CPU 测试：至少三个参数用例，检查数值、shape 与相关梯度语义。

## 04 Last Dimension Normalization

- 文件：`exercises/tensor_operations.py`；签名：`normalize_last_dim`
- 难度：Medium → Advanced；学习目标：Normalize each last-axis row with population std (correction=0), dividing by std clamped below by eps. Constants become zeros; eps>0.
- Input Shape → Output Shape：[...,D], D>=1 -> same
- Expected dtype：floating input, preserve dtype
- 梯度与计算图：preserve graph; avoid in-place operations
- Hint / 梯度推导提示：Keep reduced axes for broadcasting; explain singleton std.
- CPU 测试：至少三个参数用例，检查数值、shape 与相关梯度语义。

## 05 Masked Row Selection

- 文件：`exercises/tensor_operations.py`；签名：`select_rows`
- 难度：Medium → Advanced；学习目标：Select rows using a bool [N] mask; preserve row order.
- Input Shape → Output Shape：[N,*S] and [N] -> [M,*S]
- Expected dtype：x dtype; mask bool
- 梯度与计算图：selected values retain gradient paths
- Hint / 梯度推导提示：Check mask length and dtype; M may be zero.
- CPU 测试：至少三个参数用例，检查数值、shape 与相关梯度语义。

## 06 Pairwise Cosine Similarity

- 文件：`exercises/tensor_operations.py`；签名：`pairwise_cosine_similarity`
- 难度：Medium → Advanced；学习目标：Return all pairwise cosines; zero-norm vectors have similarity zero using norm clamp 1e-8.
- Input Shape → Output Shape：[N,D], [M,D] -> [N,M]
- Expected dtype：matching floating dtype
- 梯度与计算图：preserve both input graphs
- Hint / 梯度推导提示：Sketch matrix multiplication axes before coding.
- CPU 测试：至少三个参数用例，检查数值、shape 与相关梯度语义。

## 07 Recursive Device Transfer

- 文件：`exercises/tensor_operations.py`；签名：`move_to_device`
- 难度：Medium → Advanced；学习目标：Transfer tensors recursively in dict/list/tuple; keep structure, keys and non-tensor leaves. Do not mutate input containers.
- Input Shape → Output Shape：nested tensor [*S] -> identical shapes
- Expected dtype：preserve each tensor dtype
- 梯度与计算图：Tensor.to preserves graph; CPU->CPU may return same tensor
- Hint / 梯度推导提示：Use type checks; strings must not be treated as sequences.
- CPU 测试：至少三个参数用例，检查数值、shape 与相关梯度语义。

## 08 NumPy Interoperability

- 文件：`exercises/tensor_operations.py`；签名：`to_numpy`
- 难度：Medium → Advanced；学习目标：Return detached independent CPU NumPy copy. bfloat16 converts to float32; other NumPy-compatible dtypes preserved.
- Input Shape → Output Shape：[*S] -> numpy [*S]
- Expected dtype：NumPy equivalent, bfloat16 -> float32
- 梯度与计算图：explicitly detach; returned array has no graph
- Hint / 梯度推导提示：Explain why direct numpy fails on requires_grad=True or CUDA.
- CPU 测试：至少三个参数用例，检查数值、shape 与相关梯度语义。

## 09 Scalar Gradient

梯度过程：把标量多项式看作三条分支相加，各分支分别使用幂函数求导，再由加法节点累加局部导数。先在纸上展开导数，并用正数、负数、零代入检验；返回梯度时断开图，避免修改调用者的 `.grad`。

- 文件：`exercises/autograd.py`；签名：`compute_scalar_gradient`
- 难度：Medium → Advanced；学习目标：Differentiate f(x)=x^3+2*x^2+3*x for a scalar floating tensor; return detached derivative without modifying caller x.grad.
- Input Shape → Output Shape：[] -> []
- Expected dtype：same floating dtype
- 梯度与计算图：construct fresh leaf, backward then detach result
- Hint / 梯度推导提示：On paper: derivative of each power, then add. Avoid wrapping an existing graph accidentally.
- CPU 测试：至少三个参数用例，检查数值、shape 与相关梯度语义。

## 10 Vector Gradient

梯度过程：先对每个坐标计算平方与线性项，再求和成为标量。求和节点向每个坐标传播单位上游梯度，各坐标独立应用链式法则，因此梯度的 shape 与输入一致。直接对非标量调用 `backward()` 时需要额外的上游梯度。

- 文件：`exercises/autograd.py`；签名：`compute_vector_gradient`
- 难度：Medium → Advanced；学习目标：Differentiate scalar f(x)=sum(x*x+3*x); return detached gradient, do not modify caller x.grad.
- Input Shape → Output Shape：[*S] -> [*S]
- Expected dtype：same floating dtype
- 梯度与计算图：build scalar reduction before backward
- Hint / 梯度推导提示：Each coordinate contributes independently; explain the chain rule through sum.
- CPU 测试：至少三个参数用例，检查数值、shape 与相关梯度语义。

## 11 Gradient Accumulation

梯度过程：每次对平方函数构造新的前向图，反向结果都会加到叶子的 `.grad` 上；第二次反向后得到两次贡献之和。清空梯度后，第三次只保留新一次的贡献。保存各阶段观察值时应避免与后续变化的梯度存储共享。

- 文件：`exercises/autograd.py`；签名：`gradient_accumulation_demo`
- 难度：Medium → Advanced；学习目标：For fresh scalar leaf and f=x^2, return detached copies: first gradient after one backward, accumulated after second fresh graph backward, after_zero after clearing grad and one more backward. Keys first/accumulated/after_zero.
- Input Shape → Output Shape：[] -> three scalar tensors
- Expected dtype：same floating dtype
- 梯度与计算图：fresh graph per backward; snapshots must not alias .grad
- Hint / 梯度推导提示：Track addition into .grad, then explain why clearing it changes the third result.
- CPU 测试：至少三个参数用例，检查数值、shape 与相关梯度语义。

## 12 Detach Tensor

梯度过程：`detach()` 产生共享存储但没有历史边的张量，后续仅依赖该张量的计算不能反传至原输入。`no_grad()` 只控制上下文中新执行操作的记录，并不会修改上下文之前已有张量的计算图。请分别画出这两种情形的图。

- 文件：`exercises/autograd.py`；签名：`detach_tensor`
- 难度：Medium → Advanced；学习目标：Return detached tensor sharing storage, not a clone. Explain contrast with no_grad context for future operations.
- Input Shape → Output Shape：[*S] -> same
- Expected dtype：same as x
- 梯度与计算图：requires_grad=False, grad_fn=None
- Hint / 梯度推导提示：Detach affects this tensor; no_grad affects operations in its context.
- CPU 测试：至少三个参数用例，检查数值、shape 与相关梯度语义。

## 13 Freeze Parameters

梯度过程：冻结参数表示不为这些叶子累计参数梯度；如果输入需要梯度，链式法则仍可穿过冻结层传向输入。`eval()` 改变 Dropout、BatchNorm 的行为，并不关闭梯度；对整次前向使用 `no_grad()` 才会阻止该次图的构建。

- 文件：`exercises/autograd.py`；签名：`freeze_parameters`
- 难度：Medium → Advanced；学习目标：Freeze all parameters in-place and return model; do not change train/eval mode. Input gradients can still exist.
- Input Shape → Output Shape：module tensors [*S] -> same parameter shapes
- Expected dtype：parameter dtypes unchanged
- 梯度与计算图：parameter grads disabled; graph through differentiable inputs may remain
- Hint / 梯度推导提示：requires_grad and eval control different behavior; explain BatchNorm/dropout.
- CPU 测试：至少三个参数用例，检查数值、shape 与相关梯度语义。

## 14 Build MLP

- 文件：`exercises/neural_network.py`；签名：`build_mlp`
- 难度：Medium → Advanced；学习目标：Return Linear/ReLU MLP, final Linear logits, no final Softmax; [] permits linear classifier. Positive dimensions.
- Input Shape → Output Shape：[B,input_dim] -> [B,num_classes]
- Expected dtype：float32 by default
- 梯度与计算图：trainable parameters and graph
- Hint / 梯度推导提示：List layer dimensions first; CrossEntropyLoss expects logits.
- CPU 测试：至少三个参数用例，检查数值、shape 与相关梯度语义。

## 15 Count Parameters

- 文件：`exercises/neural_network.py`；签名：`count_parameters`
- 难度：Medium → Advanced；学习目标：Count ALL parameter elements, including frozen parameters.
- Input Shape → Output Shape：module -> scalar int
- Expected dtype：Python int
- 梯度与计算图：do not alter gradients
- Hint / 梯度推导提示：Buffers are not parameters; specify whether frozen parameters count.
- CPU 测试：至少三个参数用例，检查数值、shape 与相关梯度语义。

## 16 One Training Epoch

- 文件：`exercises/neural_network.py`；签名：`train_one_epoch`
- 难度：Medium → Advanced；学习目标：Train one epoch with mean-reduced classification loss; zero/backward/step per batch. Return sample-weighted loss, accuracy, samples. Empty loader raises ValueError.
- Input Shape → Output Shape：batches [B,*S], targets [B] -> statistics
- Expected dtype：float inputs, long targets; Python stats
- 梯度与计算图：training gradients enabled; no graph in returned stats
- Hint / 梯度推导提示：Set train mode, transfer both tensors; last batch may be smaller.
- CPU 测试：至少三个参数用例，检查数值、shape 与相关梯度语义。

## 17 Model Evaluation

- 文件：`exercises/neural_network.py`；签名：`evaluate`
- 难度：Medium → Advanced；学习目标：Evaluate mean-loss classification without any gradients; sample-weighted loss/accuracy/samples, restore previous mode; empty loader raises ValueError.
- Input Shape → Output Shape：batches [B,*S] -> statistics
- Expected dtype：float inputs, long targets
- 梯度与计算图：no_grad/inference_mode; no parameter or grad mutation
- Hint / 梯度推导提示：eval does not disable autograd by itself; multiply mean loss by batch size.
- CPU 测试：至少三个参数用例，检查数值、shape 与相关梯度语义。

## 18 Probability Prediction

- 文件：`exercises/neural_network.py`；签名：`predict_proba`
- 难度：Medium → Advanced；学习目标：Return concatenated CPU softmax probabilities in loader order, restore mode. Loader yields (inputs, targets); empty raises ValueError.
- Input Shape → Output Shape：batches -> [N,num_classes]
- Expected dtype：floating output, rows sum to 1
- 梯度与计算图：no graph, requires_grad=False
- Hint / 梯度推导提示：Apply softmax over classes, not batch; detach before moving outputs.
- CPU 测试：至少三个参数用例，检查数值、shape 与相关梯度语义。
