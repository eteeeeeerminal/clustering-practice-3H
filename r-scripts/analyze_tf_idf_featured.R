install.packages("data.table")
library("data.table")

label_dat <- read.table("data/pos_ratio_featured.tsv", sep="\t", header=T, fileEncoding="utf-8")
label_vec <- label_dat[, 4]


dat <- fread("data/tf_idf_featured.tsv", encoding="UTF-8", sep = "\t", header=T)
data_vecs <- data.matrix(dat)[, 2:34254]
source("r-scripts/clustering.R")

print("TF-IDFの特徴量によるクラスタリング")
print("k-means そのままTF-IDFの重みを使う")
km1 <- my_kmeans(data_vecs, 3, label_vec, try_time=10, show_pairs_plot=F)
km1 <- my_kmeans(scale(data_vecs), 3, label_vec, try_time=10, show_pairs_plot=F)

print("k-means 特異値分解で16次元に圧縮したベクトルを使う")
xsvd <- svd(data_vecs)
v <- t(xsvd$v)[c(1:16), ]
rx <- data_vecs %*% t(v)
km2 <- my_kmeans(rx, 3, label_vec, try_time=10)
km2 <- my_kmeans(scale(rx), 3, label_vec, try_time=10)


print("k-means 特異値分解で3次元に圧縮したベクトルを使う")
v <- t(xsvd$v)[c(1:3), ]
rx <- data_vecs %*% t(v)
km3 <- my_kmeans(rx, 3, label_vec, try_time=10)
km3 <- my_kmeans(scale(rx), 3, label_vec, try_time=10)
