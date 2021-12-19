source("r-scripts/utils.R")

my_kmeans <- function (data_vecs, cluster_n, label_vec, try_time=1, show_pairs_plot=T) {
  # k-means を複数回実行する処理
  # km_list <- lapply(c(1:try_time), function(x){
  #   kmeans(data_vecs, 3, nstart=x)
  # })
  # km_evals <- lapply(km_list, function(x){
  #  x$tot.withinss
  #})
  #best_km <- km_list[[which.min(km_evals)]]
  
  # nstartを指定すれば自動で初期値を変えて実行してくれる
  best_km <- kmeans(data_vecs, 3, nstart=try_time)

  if(show_pairs_plot) {
    pairs(data_vecs, col=best_km$cluster)
  }
  ct <- table(best_km$cluster, label_vec)
  print(ct)
  
  cat("Entropy: ", myentropy(ct), "\n")
  cat("Purity : ", mypurity(ct), "\n")

  best_km
}