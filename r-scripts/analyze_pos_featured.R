dat <- read.table("data/pos_ratio_featured.tsv", sep="\t", header=T, fileEncoding="utf-8")
source("r-scripts/clustering.R")

print("仮名率と品詞率によるクラスタリング")
print("k-means 標準化なし")
km1 <- my_kmeans(dat[8:14], 3, dat[, 4], try_time=10)

print("k-means 標準化あり")
km2 <- my_kmeans(scale(dat[8:14]), 3, dat[, 4], try_time=10)
