

dat = read.csv(file.choose(),stringsAsFactors=FALSE, sep=",")
class(dat)
View(dat)

library(dplyr)
library(tidyr)
library(ggplot2)
library(Metrics)
library(FactoMineR)

# delete useless 1st column (indexes)
df = dat[-1]
attach(df)



# regression with 1 to 6 attributes
#################################
n = nrow(X);

Y = as.matrix(Final.Price)
for (d in 1:6) {
  X = as.matrix(df[,2:(2+d-1)]);  
  a = solve(t(X) %*% X, t(X) %*% Y)  
  yhat = X %*% a	 
  error = Y - yhat
  sse = sum(error*error)
  cat("with ", d, " variables  got sse of ", sse, "\n");
}




# regression with every attribute
#################################
X = as.matrix(df[,2:7])
names = colnames(df)
Y = as.matrix(Final.Price)
n = length(Y)
a = solve(t(X) %*% X, t(X) %*% Y)
print(a)

Yhat = X %*% a
error = Y - Yhat
sse = sum(error**2)
print(sse)




# regression with 1 attribute at a time 
#######################################

sses = rep(0,6)
As = rep(0,6)

for (i in c(2:7)) {
  

X = as.matrix(df[,i])
print(length(X)==length(Y))
Y = as.matrix(Final.Price)
n = length(Y)
a = solve(t(X) %*% X, t(X) %*% Y)
As[i-1] = a

Yhat = X %*% a
error = Y - Yhat
sse = sum(error**2)
sses[i-1] = sse

xbar = sum(X)/n
ybar = sum(Y)/n
xybar = sum(X*Y)/n
xsqbar = sum(X*X)/n

b = (ybar*xsqbar-xbar*xybar)/ (xsqbar - xbar*xbar) 
print(b)
a = (ybar - b)/xbar
print(a)

newplot = ggplot(df, aes(x=df[,i], y=Final.Price)) + 
  geom_point() +
  stat_smooth(method='lm', formula = y ~ x, size = 1) + 
  xlab(names[i]) +
  ylab('Final Price')
show(newplot)
}

sses
names[which.min(sses)+1]



# Principal Component Analysis - python implementation is more complete
############################## 

dff = df[1:7]
View(dff)

#pca = PCA(df, scale.unit=TRUE, ncp=2, graph=T)
pca=PCA(dff, quanti.sup=1)
plot(pca,habillage= "Final.Price",select="cos2 0.6")



#############
# polynomial#  prices won't decrease so doesn't really make sense ¯\_(ツ)_/¯
#############


df.shuffled <- df[sample(nrow(df[,1:7])),]

K <- 10 

#define degree of polynomials to fit
degree <- 5

#create k equal-sized folds
folds <- cut(seq(1,nrow(df.shuffled)),breaks=K,labels=FALSE)

#create object to hold MSE's of models
mse = matrix(data=NA,nrow=K,ncol=degree)

#Perform K-fold cross validation
for(i in 1:K){
  
  #training and testing data
  testIndexes <- which(folds==i,arr.ind=TRUE)
  testData <- df.shuffled[testIndexes, ]
  trainData <- df.shuffled[-testIndexes, ]
  
  #k-fold cv to evaluate models
  for (j in 1:degree){
    fit.train = lm(Final.Price ~ poly(Bidders,j), data=trainData)
    fit.test = predict(fit.train, newdata=testData)
    mse[i,j] = mean((fit.test-testData$Final.Price)^2) 
  }
}

#find MSE for each degree 
colMeans(mse)

# fit best model
best = lm(Final.Price ~ poly(Bidders,2, raw=T), data=df)
summary(best)

# plot
ggplot(df, aes(x=Bidders, y=Final.Price)) + 
  geom_point() +
  stat_smooth(method='lm', formula = y ~ poly(x,2), size = 1) + 
  xlab('SD of price difference between consecutive bids') +
  ylab('Final Price')
