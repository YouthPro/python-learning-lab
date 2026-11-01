# Section 06 练习题目录

约定优先于习惯性题解：按这里的排序、返回类型、缺失值和边界行为实现。

## 01. Train Test Split

- 难度：Medium
- 知识点：train_test_split
- 文件：[exercises/preprocessing.py](exercises/preprocessing.py)

```python
def split_dataset(X: np.ndarray, y: np.ndarray, random_state: int = 42) -> tuple
```

按 test_size=0.2、shuffle=True 划分；返回 X_train,X_test,y_train,y_test；random_state 可配置。

输入输出示例：10 行 → 8 训练/2 测试；5 行 → 4/1

边界条件：空输入抛 ValueError；相同种子结果一致。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 02. Feature Scaling

- 难度：Medium
- 知识点：StandardScaler
- 文件：[exercises/preprocessing.py](exercises/preprocessing.py)

```python
def scale_features(X: np.ndarray) -> tuple[np.ndarray, StandardScaler]
```

仅把传入的训练矩阵进行 fit_transform，返回 (scaled,scaler)；未来测试集必须用此 scaler.transform。

输入输出示例：[[1],[3]] → [[-1],[1]]；常量列 → 全零

边界条件：空训练输入抛 ValueError；使用 ddof=0。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 03. Missing Value Pipeline

- 难度：Medium
- 知识点：SimpleImputer, Pipeline
- 文件：[exercises/preprocessing.py](exercises/preprocessing.py)

```python
def build_preprocessing_pipeline() -> Pipeline
```

返回未拟合 Pipeline，命名步骤 imputer（median、keep_empty_features=True）与 scaler（StandardScaler）；每次调用返回独立实例。

输入输出示例：[[1],[NaN],[3]] → 填 2 再标准化；全缺失列 → 填 0

边界条件：不能在构建函数内拟合；交叉验证时将完整预处理放进模型 Pipeline。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 04. Regression Metrics

- 难度：Medium
- 知识点：MAE, MSE, R2
- 文件：[exercises/model_evaluation.py](exercises/model_evaluation.py)

```python
def regression_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]
```

返回 mae、mse、r2 三个 Python float；采用 sklearn.metrics 定义。

输入输出示例：[1,2],[1,2] → {mae:0,mse:0,r2:1}；[0,2],[1,1] → {mae:1,mse:1,r2:0}

边界条件：至少两个样本；空输入抛 ValueError；常量目标遵循 force_finite 默认语义。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 05. Classification Metrics

- 难度：Medium
- 知识点：accuracy, precision, recall, F1
- 文件：[exercises/model_evaluation.py](exercises/model_evaluation.py)

```python
def classification_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]
```

二分类标签 0/1，返回 accuracy、precision、recall、f1；precision/recall/f1 使用 zero_division=0。

输入输出示例：[0,1],[0,1] → 全 1；[0,0],[0,0] → accuracy=1，其余 0

边界条件：空输入抛 ValueError；此题仅二分类。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 06. Confusion Matrix

- 难度：Medium
- 知识点：ConfusionMatrixDisplay
- 文件：[exercises/model_evaluation.py](exercises/model_evaluation.py)

```python
def plot_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray) -> tuple[Figure, Axes]
```

固定标签顺序 [0,1]，绘制 2×2 混淆矩阵并设置标题，返回 fig,ax。

输入输出示例：[0,1],[0,1] → 单位对角计数；全 0 → 右下角 0

边界条件：即使只出现一个类别也必须有两个标签；不 show。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 07. Cross Validation

- 难度：Medium
- 知识点：cross_val_score, KFold
- 文件：[exercises/model_selection.py](exercises/model_selection.py)

```python
def evaluate_cv(model, X: np.ndarray, y: np.ndarray, random_state: int = 42) -> np.ndarray
```

使用 KFold(n_splits=3,shuffle=True,random_state=...) 和 scoring=r2 返回三折分数；传入完整回归 Pipeline 以避免泄漏。

输入输出示例：线性数据+LinearRegression → 三个 1；噪声数据 → 三个分数

边界条件：至少 3 行；不拟合调用方模型，固定划分。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 08. Hyperparameter Search

- 难度：Medium
- 知识点：GridSearchCV
- 文件：[exercises/model_selection.py](exercises/model_selection.py)

```python
def search_best_params(model, params: dict, X: np.ndarray, y: np.ndarray, random_state: int = 42) -> GridSearchCV
```

以相同三折 KFold、scoring=r2、refit=True 拟合 GridSearchCV，返回搜索对象；参数名支持 Pipeline 的 step__param。

输入输出示例：Ridge,alpha=[.1,1] → fitted search；单候选 → 一个结果

边界条件：只传训练数据；error_score=raise，空参数字典合法。

提示：先运行对应测试，理解返回结构，再查官方文档。
