# 作用：导入教学数据集 Iris。
from sklearn.datasets import load_iris

# 作用：将数据分成训练集和测试集。
from sklearn.model_selection import train_test_split

# 作用：构建由多个处理步骤组成的机器学习流程。
from sklearn.pipeline import make_pipeline

# 作用：对数值特征进行标准化。
from sklearn.preprocessing import StandardScaler

# 作用：导入一个用于分类任务的逻辑回归模型。
from sklearn.linear_model import LogisticRegression

# 作用：导入分类准确率和详细评估报告。
from sklearn.metrics import accuracy_score, classification_report


# 作用：加载 Iris 数据集。
dataset = load_iris()

# 作用：取得特征矩阵 X。
# 每一行代表一朵花，每一列代表一个测量特征。
features = dataset.data

# 作用：取得标签 y。
# 标签表示这朵花属于哪一种类别。
labels = dataset.target

# 作用：将数据拆分为训练部分和测试部分。
# test_size=0.2 表示 20% 数据用于最终测试。
# random_state=42 保证每次拆分结果一致，方便复现。
features_train, features_test, labels_train, labels_test = train_test_split(
    features,
    labels,
    test_size=0.2,
    random_state=42,
    stratify=labels,
)

# 作用：创建机器学习流程。
# 第一步标准化特征，第二步使用逻辑回归完成分类。
model = make_pipeline(
    StandardScaler(),
    LogisticRegression(max_iter=1000),
)

# 作用：让模型根据训练数据学习特征与标签之间的关系。
model.fit(features_train, labels_train)

# 作用：让训练好的模型预测测试集的类别。
predicted_labels = model.predict(features_test)

# 作用：计算预测正确的比例。
accuracy = accuracy_score(labels_test, predicted_labels)

# 作用：输出模型准确率。
print(f"测试集准确率：{accuracy:.2%}")

# 作用：输出每个类别的 Precision、Recall 和 F1 指标。
print("\n详细评估报告：")
print(
    classification_report(
        labels_test,
        predicted_labels,
        target_names=dataset.target_names,
    )
)