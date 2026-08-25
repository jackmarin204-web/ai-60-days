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

# 作用：导入交叉验证函数，用多个数据划分评估模型稳定性。
from sklearn.model_selection import cross_val_score

# 作用：导入混淆矩阵计算函数。
from sklearn.metrics import confusion_matrix

# 作用：导入永远预测多数类别的基线模型。
from sklearn.dummy import DummyClassifier

# 作用：导入决策树分类器。
from sklearn.tree import DecisionTreeClassifier

# 作用：导入随机森林分类器。
from sklearn.ensemble import RandomForestClassifier

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

# 作用：使用 5 折交叉验证评估模型。
# features 和 labels 会被分成 5 份，每一份轮流作为验证集。
cross_validation_scores = cross_val_score(
    model,
    features,
    labels,
    cv=5,
    scoring="accuracy",
)

# 作用：计算 5 次验证结果的平均准确率。
cross_validation_mean = cross_validation_scores.mean()

# 作用：计算 5 次验证结果的标准差。
# 标准差越小，说明模型在不同数据划分下越稳定。
cross_validation_std = cross_validation_scores.std()

# 作用：输出每一折的准确率。
print("\n每一折的交叉验证准确率：")
print(cross_validation_scores)

# 作用：输出平均准确率和稳定性波动。
print(
    f"交叉验证平均准确率：{cross_validation_mean:.2%}"
)
print(
    f"交叉验证标准差：{cross_validation_std:.2%}"
)



# 作用：让模型根据训练数据学习特征与标签之间的关系。
model.fit(features_train, labels_train)

# 作用：让训练好的模型预测测试集的类别。
predicted_labels = model.predict(features_test)
# 作用：根据真实标签和预测标签统计分类结果。
confusion = confusion_matrix(
    labels_test,
    predicted_labels,
)

# 作用：输出混淆矩阵。
print("\n混淆矩阵：")
print(confusion)

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

# 作用：创建多个候选模型，准备在相同数据上进行比较。
candidate_models = {
    # 作用：创建一个最简单的基线模型。
    "多数类基线": DummyClassifier(
        strategy="most_frequent",
    ),

    # 作用：创建带标准化步骤的逻辑回归模型。
    "逻辑回归": make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=1000),
    ),

    # 作用：创建限制树深度的决策树，降低过拟合风险。
    "决策树": DecisionTreeClassifier(
        max_depth=3,
        random_state=42,
    ),

    # 作用：创建由多棵决策树组成的随机森林。
    "随机森林": RandomForestClassifier(
        n_estimators=100,
        random_state=42,
    ),
}


# 作用：输出模型比较标题。
print("\n模型交叉验证比较：")

# 作用：逐个取出模型名称和模型对象。
for model_name, candidate_model in candidate_models.items():
    # 作用：对当前模型执行 5 折交叉验证。
    model_scores = cross_val_score(
        candidate_model,
        features,
        labels,
        cv=5,
        scoring="accuracy",
    )

    # 作用：计算当前模型 5 折准确率的平均值。
    model_mean_score = model_scores.mean()

    # 作用：计算当前模型准确率的标准差，衡量稳定性。
    model_std_score = model_scores.std()

    # 作用：输出当前模型的平均成绩和波动范围。
    print(
        f"{model_name}："
        f"平均准确率={model_mean_score:.2%}，"
        f"标准差={model_std_score:.2%}"
    )

    # 作用：定义要测试的决策树深度。
# 深度越大，模型能学习的规则越复杂。
tree_depths = [1, 2, 3, 5, 10]


# 作用：输出不同树深度的实验标题。
print("\n不同决策树深度的训练集与测试集表现：")


# 作用：逐个测试不同的决策树深度。
for tree_depth in tree_depths:
    # 作用：创建当前深度的决策树模型。
    depth_model = DecisionTreeClassifier(
        max_depth=tree_depth,
        random_state=42,
    )

    # 作用：使用训练集训练当前深度的决策树。
    depth_model.fit(
        features_train,
        labels_train,
    )

    # 作用：计算模型在训练集上的准确率。
    train_accuracy = depth_model.score(
        features_train,
        labels_train,
    )

    # 作用：计算模型在从未参与训练的测试集上的准确率。
    test_accuracy = depth_model.score(
        features_test,
        labels_test,
    )

    # 作用：输出当前深度的训练表现和测试表现。
    print(
        f"树深度={tree_depth}："
        f"训练准确率={train_accuracy:.2%}，"
        f"测试准确率={test_accuracy:.2%}"
    )