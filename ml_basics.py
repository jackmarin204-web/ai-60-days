# 作用：导入 Pandas，用于将数据组织成表格并进行分析。
import pandas as pd

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

# 作用：取得标签 y。
# 作用：根据数据集提供的特征名称创建列名列表。
feature_names = dataset.feature_names

# 作用：将 NumPy 特征矩阵转换成 Pandas 表格。
# 每一行代表一个样本，每一列代表一个特征。
features_dataframe = pd.DataFrame(
    features,
    columns=feature_names,
)

# 作用：将数字标签转换为人类可读的花名称。
# dataset.target_names[labels] 会把 0、1、2 转换成具体类别名称。
species_names = dataset.target_names[labels]

# 作用：将类别名称作为新列加入特征表。
features_dataframe["species"] = species_names

# 作用：输出数据集的行数和列数。
# shape[0] 表示行数，shape[1] 表示列数。
print(f"数据行数：{features_dataframe.shape[0]}")
print(f"数据列数：{features_dataframe.shape[1]}")

# 作用：显示前 5 行数据，检查数据读取是否正常。
print("\n前 5 行数据：")
print(features_dataframe.head())

# 作用：检查每一列是否存在缺失值。
# isna() 会标记空值；sum() 会统计每列空值数量。
print("\n各列缺失值数量：")
print(features_dataframe.isna().sum())

# 作用：统计每种花分别有多少样本。
# value_counts() 会计算分类列中每个类别出现的次数。
print("\n类别分布：")
print(features_dataframe["species"].value_counts())

# 作用：统计数值列的平均值、标准差、最小值和最大值。
print("\n数值特征统计：")
print(features_dataframe.describe())

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