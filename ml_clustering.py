# 作用：导入 Iris 轻量教学数据集。
from sklearn.datasets import load_iris

# 作用：导入标准化工具，让不同特征处于相近尺度。
from sklearn.preprocessing import StandardScaler

# 作用：导入 K-Means 聚类算法。
from sklearn.cluster import KMeans

# 作用：导入轮廓系数，用于评估聚类质量。
from sklearn.metrics import silhouette_score

# 作用：导入 Counter，用于统计每个簇包含多少样本。
from collections import Counter


# 作用：加载 Iris 数据集。
dataset = load_iris()

# 作用：取得不包含类别答案的特征矩阵。
# 无监督学习只使用 features，不使用真实 labels。
features = dataset.data

# 作用：创建标准化器。
scaler = StandardScaler()

# 作用：只根据特征数据计算标准化规则，并完成转换。
scaled_features = scaler.fit_transform(features)

# 作用：创建 K-Means 模型，要求把样本分成 3 个簇。
# n_init=10 表示用 10 组不同初始中心尝试，选择效果较好的一组。
# random_state=42 保证每次运行结果尽量一致。
kmeans_model = KMeans(
    n_clusters=3,
    n_init=10,
    random_state=42,
)

# 作用：训练 K-Means，并返回每条样本所属的簇编号。
cluster_labels = kmeans_model.fit_predict(scaled_features)

# 作用：计算轮廓系数，评价聚类内部紧密程度和簇间分离程度。
silhouette = silhouette_score(
    scaled_features,
    cluster_labels,
)

# 作用：统计每个簇包含的样本数量。
cluster_counts = Counter(cluster_labels)

# 作用：输出数据集的基本信息。
print(f"样本数量：{len(features)}")
print(f"特征数量：{features.shape[1]}")
print(f"簇数量：{kmeans_model.n_clusters}")

# 作用：输出每个簇的样本数量。
print("\n各簇样本数量：")
for cluster_id, sample_count in sorted(cluster_counts.items()):
    # 作用：显示簇编号和该簇的样本数量。
    print(f"簇 {cluster_id}：{sample_count} 条样本")

# 作用：输出聚类质量指标。
print(f"\n轮廓系数：{silhouette:.3f}")

# 作用：输出 K-Means 找到的三个中心点。
print("\n标准化空间中的簇中心：")
print(kmeans_model.cluster_centers_)