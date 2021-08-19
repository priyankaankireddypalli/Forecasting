# 3
library(readr)
# Importing the dataset
plasticsales <- read.csv('C:\\Users\\WIN10\\Desktop\\LEARNING\\DS\\forecast\\PlasticSales.csv') 
View(plasticsales) 
# # Performing EDA
plasticsales["t"] <- c(1:60)
View(plasticsales)
plasticsales["t_square"] <- plasticsales["t"] * plasticsales["t"]
plasticsales["log_Sales"] <- log(plasticsales["Sales"])
# Creating 12 dummy variables
X <- data.frame(outer(rep(month.abb,length = 60), month.abb,"==") + 0 )
colnames(X) <- month.abb # Assigning month names
View(X)
plasticsalesn <- cbind(plasticsales, X)
colnames(plasticsalesn)
View(plasticsalesn)
attach(plasticsalesn)
# Splitting the data into train and test
train <- plasticsalesn[1:48, ]
test <- plasticsalesn[49:60, ]
# Linear Model
linear_model <- lm(Sales ~ t, data = train)
summary(linear_model)
linear_pred <- data.frame(predict(linear_model, interval = 'predict', newdata = test))
rmse_linear <- sqrt(mean((test$Sales  - linear_pred$fit)^2, na.rm = T))
rmse_linear
# Exponential Model
expo_model <- lm(log_Sales ~ t, data = train)
summary(expo_model)
expo_pred <- data.frame(predict(expo_model, interval = 'predict', newdata = test))
rmse_expo <- sqrt(mean((test$Sales - exp(expo_pred$fit))^2, na.rm = T))
rmse_expo
# Quadratic Model
Quad_model <- lm(Sales ~ t + t_square, data = train)
summary(Quad_model)
Quad_pred <- data.frame(predict(Quad_model, interval = 'predict', newdata = test))
rmse_Quad <- sqrt(mean((test$Sales-Quad_pred$fit)^2, na.rm = T))
rmse_Quad
# Additive Seasonality Model
sea_add_model <- lm(Sales ~ Jan + Feb + Mar + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov + Dec, data = train)
summary(sea_add_model)
sea_add_pred <- data.frame(predict(sea_add_model, newdata = test, interval = 'predict'))
rmse_sea_add <- sqrt(mean((test$Sales - sea_add_pred$fit)^2, na.rm = T))
rmse_sea_add
# Multiplicative Seasonality Model
multi_sea_model <- lm(log_Sales ~ Jan + Feb + Mar + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov, data = train)
summary(multi_sea_model)
multi_sea_pred <- data.frame(predict(multi_sea_model, newdata = test, interval = 'predict'))
rmse_multi_sea <- sqrt(mean((test$Sales - exp(multi_sea_pred$fit))^2, na.rm = T))
rmse_multi_sea
# Additive Seasonality with Quadratic Trend 
Add_sea_Quad_model <- lm(Sales ~ t + t_square + Jan + Feb + Mar + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov, data = train)
summary(Add_sea_Quad_model)
Add_sea_Quad_pred <- data.frame(predict(Add_sea_Quad_model, interval = 'predict', newdata = test))
rmse_Add_sea_Quad <- sqrt(mean((test$Sales - Add_sea_Quad_pred$fit)^2, na.rm=T))
rmse_Add_sea_Quad
# Preparing table on model and it's RMSE values 
table_rmse <- data.frame(c("rmse_linear", "rmse_expo", "rmse_Quad", "rmse_sea_add", "rmse_Add_sea_Quad", "rmse_multi_sea"), c(rmse_linear, rmse_expo, rmse_Quad, rmse_sea_add, rmse_Add_sea_Quad, rmse_multi_sea))
colnames(table_rmse) <- c("model", "RMSE")
View(table_rmse)
# Additive seasonality with Quadratic Trend has least RMSE value
write.csv(plasticsalesn, file = "Sales.csv", row.names = F)
getwd()


