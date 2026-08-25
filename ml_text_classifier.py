# 作用：导入训练集和测试集拆分工具。
from sklearn.model_selection import train_test_split

# 作用：导入 Pipeline，将文本向量化和模型训练绑定为一个流程。
from sklearn.pipeline import Pipeline

# 作用：将文本转换为 TF-IDF 数值特征。
from sklearn.feature_extraction.text import TfidfVectorizer

# 作用：导入逻辑回归分类模型。
from sklearn.linear_model import LogisticRegression

# 作用：导入模型评估报告。
from sklearn.metrics import accuracy_score, classification_report


# 作用：创建轻量文本数据集。
# 每一条文字是一条用户反馈样本。
texts = [
    "Python 接口返回 500 错误",
    "数据库连接失败",
    "登录接口超时",
    "服务器无法启动",
    "程序出现异常堆栈",
    "API 返回数据为空",
    "如何修改个人头像",
    "请问课程什么时候开始",
    "我想了解会员价格",
    "如何更换绑定邮箱",
    "请介绍一下产品功能",
    "我想申请退款",
    "FastAPI 路由无法访问",
    "SQL 查询执行失败",
    "网页加载时出现错误",
    "如何查看历史订单",
    "怎样修改账户昵称",
    "请问支持哪些支付方式",
    "模型接口调用失败",
    "文件上传出现错误",
]

# 作用：创建每条文本对应的分类标签。
# 1 表示技术故障，0 表示普通咨询。
labels = [
    1, 1, 1, 1, 1, 1,
    0, 0, 0, 0, 0, 0,
    1, 1, 1, 0, 0, 0,
    1, 1,
]

# 作用：将文本和标签拆分为训练部分与测试部分。
# stratify=labels 保证训练集和测试集都尽量包含两种类别。
texts_train, texts_test, labels_train, labels_test = train_test_split(
    texts,
    labels,
    test_size=0.25,
    random_state=42,
    stratify=labels,
)

# 作用：创建文本分类流程。
text_classifier = Pipeline(
    steps=[
        # 作用：将中文文本切分为连续字符片段，并计算 TF-IDF。
        # 字符 n-gram 不要求额外安装中文分词工具。
        (
            "vectorizer",
            TfidfVectorizer(
                analyzer="char",
                ngram_range=(2, 4),
            ),
        ),

        # 作用：根据 TF-IDF 特征判断文本属于哪一类。
        (
            "classifier",
            LogisticRegression(
                max_iter=1000,
            ),
        ),
    ],
)

# 作用：只使用训练文本学习词语特征和分类规律。
text_classifier.fit(
    texts_train,
    labels_train,
)

# 作用：让训练好的模型预测测试文本的类别。
predicted_labels = text_classifier.predict(
    texts_test,
)

# 作用：计算测试集上的总体准确率。
accuracy = accuracy_score(
    labels_test,
    predicted_labels,
)

# 作用：输出总体准确率。
print(f"测试集准确率：{accuracy:.2%}")

# 作用：输出每个类别的详细评估结果。
print("\n文本分类评估报告：")
print(
    classification_report(
        labels_test,
        predicted_labels,
        target_names=["普通咨询", "技术故障"],
        zero_division=0,
    )
)

# 作用：创建几条从未出现在训练数据中的新文本。
new_texts = [
    "接口调用之后返回错误",
    "请问如何修改账户信息",
]

# 作用：使用训练好的模型预测新文本类别。
new_predictions = text_classifier.predict(
    new_texts,
)

# 作用：输出新文本及其预测结果。
print("\n新文本预测：")
for text, prediction in zip(new_texts, new_predictions):
    # 作用：将数字标签转换成可读的中文类别名称。
    category = "技术故障" if prediction == 1 else "普通咨询"

    # 作用：输出原始文本和模型判断。
    print(f"{text} → {category}")