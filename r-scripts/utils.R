myentropy0 <- function (pv) {
  p1 <- pv/sum(pv)
  p2 <- p1[p1 != 0]
  sum(p2 * log(p2))
}

myentropy <- function (ct) {
  -sum(
    (rowSums(ct)/sum(ct)) * apply(ct,1,myentropy0)
  ) / log(ncol(ct))
}

mypurity <- function (ct) {
  sum(apply(ct,1,max)) / sum (ct)
}

myrecall <- function (ct, h, k) {
  ct[h, k] / sum(ct[h,])
}

myprecision <- function (ct, h, k) {
  ct[h, k] / sum(ct[,k])
}

myf0 <- function (ct, h, k) {
  r <- myrecall(ct, h, k)
  p <- myprecision(ct, h, k)
  2*r*p/(r+p)
}

#myf <- function (ct) {
#  ft <- # 後回し
#    sum(
#      (rowSums(ct)/sum(ct)) * apply(ct, 1, max)
#    )
#}

myeval <- function (myans, ansfile) {
  goldans <- scan(ansfile, what="character")
  ct <- table(myans, goldans)
  cat("Entropy: ", myentropy(ct), "\n")
  cat("Purity : ", mypurity(ct), "\n")
}

mykmval_slow <- function (x, clsn, ans) {
  N <- nrow(x)
  val <- 0
  for (cl in 1:clsn) {
    g <- c(1:N)[ans==cl]
    cen <- apply(x[g,],2,sum) / length(g)
    val <- val + sum(apply(x[g,],1,function (x) sum((x-cen)**2)))
  }
  return(val)
}

mykmvalcore <- function (x, N, X, ans) {
  g <- c(1:N)[ans==x]
  cen <- colSums(X[g,])/length(g)
  return(sum(apply(X[g,],1, function(x) sum((x-cen)**2))))
}

mykmval <- function (X, clsn, ans) {
  N <- nrow(X)
  a <- matrix(c(1:clsn), ncol=1)
  return (sum(apply(a, 1, function(x) mykmvalcore(x, N, X, ans))))
}
