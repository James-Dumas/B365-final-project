data = read.csv(file.choose(),stringsAsFactors=FALSE, sep=",")
class(data)
View(data)

library(dplyr)
library(tidyr)
library(ggplot2)
library(Metrics)
library(FactoMineR)
library(car)


# delete 1st column (indexes)
df = data[-1]

#####################
# linear regression #
#####################


# With one attribute at a time

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


# Linear regression with every attribute
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


##############################
# Multiple Linear Regression #
##############################

# Pair plots
############
pairs(df, pch = 18, col = "steelblue")


# Multiple regression
#####################

names = colnames(df)
Y = as.matrix(Final.Price)

for (d in rep(2:6)){
  for (i in rep(1:6)) {
    if (d+i < 8){
      X = as.matrix(df[,d:(d+i)])    
      xnames = paste0(names[d:(d+i)])
      fmla <- as.formula(paste("Final.Price ~ ", paste(xnames, collapse= "+")))
      fit = lm(fmla, data = df)
      cat("For the variables",names[d:(d+i)] ,"adjusted R squared is",summary(fit)$adj.r.square, "\n")
      # Homoscedasticity?
      plot(fitted(fit), residuals(fit))
      abline(h = 0, lty = 2)
      title(names[d:(d+i)])
      # Normal distribution?
      qqnorm(fitted(fit))
      qqline(fitted(fit))
      # independance?
      print(durbinWatsonTest(fit))      
    }
  }
}


################################
# Weighted Multiple Regression #
################################

# homoscedasticity is not met, nor is normal distribution, so we can apply a log transformation and perform a weighted regression

logdf = log(df + 0.000000001) # not an ideal solution, but will eliminate problematic zeros
head(logdf)
Y = as.matrix(logdf$Final.Price)

for (d in rep(2:6)){
  for (i in rep(1:6)) {
    if (d+i < 8){
      X = as.matrix(logdf[,d:(d+i)])
      xnames = paste0(names[d:(d+i)])
      fmla <- as.formula(paste("Final.Price ~ ", paste(xnames, collapse= "+")))
      fit = lm(fmla, data = logdf)
      
      # weight:
      wt <- 1 / lm(abs(fit$residuals) ~ fit$fitted.values)$fitted.values^2
      model <- lm(fmla, data = logdf, weights=wt)
      cat("For the variables",names[d:(d+i)] ,"adjusted R squared is",summary(model)$adj.r.square, "\n")
      
      # Homoscedasticity?
      plot(fitted(model), residuals(model))
      abline(h = 0, lty = 2)
      title(names[d:(d+i)])
      # Normal distribution?
      qqnorm(fitted(model))
      qqline(fitted(model))
      # independance?
      print(durbinWatsonTest(model))
    }
  }
}


#########################
# Polynomial Regression #
#########################

df.shuffled <- df[sample(nrow(df[,1:7])),]

K <- 10 
degree <- 5
folds <- cut(seq(1,nrow(df.shuffled)),breaks=K,labels=FALSE)
# mean square error
mse = matrix(data=NA,nrow=K,ncol=degree)

# K-fold cross validation
for(i in 1:K){
  testIndexes <- which(folds==i,arr.ind=TRUE)
  testData <- df.shuffled[testIndexes, ]
  trainData <- df.shuffled[-testIndexes, ]
  
  # cross-validation
  for (j in 1:degree){
    fit.train = lm(Final.Price ~ poly(Bidders,j), data=trainData)
    fit.test = predict(fit.train, newdata=testData)
    mse[i,j] = mean((fit.test-testData$Final.Price)^2) 
  }
}

# fit best model
best = lm(Final.Price ~ poly(Bidders,2, raw=T), data=df)
summary(best)

# plot
ggplot(df, aes(x=Bidders, y=Final.Price)) + 
  geom_point() +
  stat_smooth(method='lm', formula = y ~ poly(x,2), size = 1) + 
  xlab('SD of price difference between consecutive bids') +
  ylab('Final Price')


################################
# Principal Component Analysis #        Python Implementation is more complete
############################## #

dff = df[1:7]

#pca = PCA(df, scale.unit=TRUE, ncp=2, graph=T)
pca=PCA(dff, quanti.sup=1)
plot(pca,habillage= "Final.Price",select="cos2 0.6")
