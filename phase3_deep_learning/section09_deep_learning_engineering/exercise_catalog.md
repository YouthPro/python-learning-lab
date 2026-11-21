# Section 09 题目目录

练习的扁平配置用于独立学习；最终项目使用带校验的分层配置。所有函数保留TODO，类的方法也不提供答案。

## 01 Set Random Seed

- 函数/类：`seed_everything`；`exercises/reproducibility.py`
- 难度 Advanced；目标：Seed Python random, NumPy and Torch (and CUDA if available); same-environment reproducibility, not across platforms.
- Input Shape → Output Shape：seed scalar -> None
- Expected dtype：Python int
- 梯度与计算图：no graph
- Hint：Seed all RNGs; distinguish deterministic algorithms from seeds.
- 至少三个CPU用例；文件测试使用临时目录。

## 02 Experiment Config

- 函数/类：`validate_config`；`exercises/reproducibility.py`
- 难度 Advanced；目标：Minimal flat exercise config: required epochs,batch_size positive integers (not bool),learning_rate finite positive; defaults seed=42/device=cpu, supported device cpu/cuda/mps/auto. Return new dict; invalid raises ValueError.
- Input Shape → Output Shape：mapping -> validated mapping
- Expected dtype：primitive scalars
- 梯度与计算图：no graph
- Hint：Read YAML with safe_load outside this function; reject nan and strings as numeric values.
- 至少三个CPU用例；文件测试使用临时目录。

## 03 Average Meter

- 函数/类：`AverageMeter`；`exercises/training_utilities.py`
- 难度 Advanced；目标：Maintain sum,count,avg; update(value,n=1) is sample-weighted; n>=0; reset all to zero.
- Input Shape → Output Shape：scalar values+counts -> scalar average
- Expected dtype：Python float/int
- 梯度与计算图：store scalars, never tensor graphs
- Hint：The last batch may be shorter.
- 至少三个CPU用例；文件测试使用临时目录。

## 04 Early Stopping

- 函数/类：`EarlyStopping`；`exercises/training_utilities.py`
- 难度 Advanced；目标：Minimize loss; patience>=1,min_delta>=0; update(loss)->bool after patience consecutive non-improvements. Strict loss < best-min_delta counts as improvement.
- Input Shape → Output Shape：epoch scalar loss -> bool
- Expected dtype：float/bool
- 梯度与计算图：no graph
- Hint：Reset bad-epoch counter on improvement; loss must be finite.
- 至少三个CPU用例；文件测试使用临时目录。

## 05 Gradient Clipping

- 函数/类：`clip_gradients`；`exercises/training_utilities.py`
- 难度 Advanced；目标：Clip parameter gradient L2 norm in-place; return total norm before clipping; max_norm>0.
- Input Shape → Output Shape：parameter grads [*S] -> scalar norm
- Expected dtype：gradient dtypes preserved; result float
- 梯度与计算图：no new graph; operates after backward
- Hint：Clip gradients, not parameter values; AMP needs unscale first.
- 至少三个CPU用例；文件测试使用临时目录。

## 06 Optimizer Factory

- 函数/类：`build_optimizer`；`exercises/training_utilities.py`
- 难度 Advanced；目标：config name adam/sgd and positive lr; optional momentum for SGD; include only requires_grad parameters; unknown name raises ValueError.
- Input Shape → Output Shape：module parameters -> optimizer
- Expected dtype：parameter dtypes preserved
- 梯度与计算图：optimizer step changes parameters, not forward graph
- Hint：Frozen parameters must not be optimized.
- 至少三个CPU用例；文件测试使用临时目录。

## 07 Scheduler Factory

- 函数/类：`build_scheduler`；`exercises/training_utilities.py`
- 难度 Advanced；目标：name step/plateau/none; step_size/gamma for StepLR, factor/patience for ReduceLROnPlateau. none returns None. Unknown raises ValueError.
- Input Shape → Output Shape：optimizer/config -> scheduler or None
- Expected dtype：Python floats
- 梯度与计算图：no graph
- Hint：Step after optimizer update; plateau expects validation metric.
- 至少三个CPU用例；文件测试使用临时目录。

## 08 Save Checkpoint

- 函数/类：`save_checkpoint`；`exercises/checkpointing.py`
- 难度 Advanced；目标：Save model/optimizer/scheduler state_dicts, epoch and best_metric. Never serialize entire model. Create parent directory.
- Input Shape → Output Shape：parameter tensors -> file
- Expected dtype：tensors+primitive containers
- 梯度与计算图：saved states not computational graph
- Hint：Keep schema keys explicit; scheduler may be None.
- 至少三个CPU用例；文件测试使用临时目录。

## 09 Load Checkpoint

- 函数/类：`load_checkpoint`；`exercises/checkpointing.py`
- 难度 Advanced；目标：torch.load with explicit weights_only=True/map_location; restore supplied objects and return loaded metadata. Do not load arbitrary pickled modules.
- Input Shape → Output Shape：file -> restored shapes + metadata
- Expected dtype：model dtypes unchanged
- 梯度与计算图：no forward graph
- Hint：state_dict restores parameters; restoring optimizer/scheduler is separate.
- 至少三个CPU用例；文件测试使用临时目录。

## 10 JSONL Experiment Logger

- 函数/类：`log_experiment`；`exercises/checkpointing.py`
- 难度 Advanced；目标：Append exactly one UTF-8 JSON object and newline, preserve existing records, reject non-finite JSON floats.
- Input Shape → Output Shape：metric mapping -> one line
- Expected dtype：JSON primitives
- 梯度与计算图：convert values beforehand; no graph storage
- Hint：Serialize before appending so invalid records do not partially corrupt a log.
- 至少三个CPU用例；文件测试使用临时目录。
