# 3
import pandas as pd
plastic = pd.read_csv('C:\\Users\\WIN10\\Desktop\\LEARNING\\DS\\forecast\\PlasticSales.csv')
month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'] 
# Performing EDA
import numpy as np
plastic["t"] = np.arange(1,61)
plastic["t_square"] = plastic["t"]*plastic["t"]
plastic["log_Sales"] = np.log(plastic["Sales"])
plastic.columns
plastic.info()
p = plastic["Month"][0]
p[0:3]
plastic['month']= 0
for i in range(60):
    p = plastic["Month"][i]
    plastic['month'][i]= p[0:3]
month_dummies = pd.DataFrame(pd.get_dummies(plastic['month']))
Plastic1 = pd.concat([plastic, month_dummies], axis = 1)
# Visualization - Time plot
Plastic1.Sales.plot()
# Splitting the data into train and test
Train = Plastic1.head(52)
Test =Plastic1.tail(8)
# Linear Model
import statsmodels.formula.api as smf 
linear_model = smf.ols('Sales ~ t', data=Train).fit()
pred_linear =  pd.Series(linear_model.predict(pd.DataFrame(Test['t'])))
rmse_linear = np.sqrt(np.mean((np.array(Test['Sales']) - np.array(pred_linear))**2))
rmse_linear
# Exponential Model
Exp = smf.ols('log_Sales ~ t', data = Train).fit()
pred_Exp = pd.Series(Exp.predict(pd.DataFrame(Test['t'])))
rmse_Exp = np.sqrt(np.mean((np.array(Test['Sales']) - np.array(np.exp(pred_Exp)))**2))
rmse_Exp
# Quadratic Model
Quad = smf.ols('Sales ~ t+t_square', data=Train).fit()
pred_Quad = pd.Series(Quad.predict(Test[["t","t_square"]]))
rmse_Quad = np.sqrt(np.mean((np.array(Test['Sales'])-np.array(pred_Quad))**2))
rmse_Quad
# Additive seasonality Model
add_sea = smf.ols('Sales ~ Jan+Feb+Mar+Apr+May+Jun+Jul+Aug+Sep+Oct+Nov', data=Train).fit()
pred_add_sea = pd.Series(add_sea.predict(Test[['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov']]))
rmse_add_sea = np.sqrt(np.mean((np.array(Test['Sales'])-np.array(pred_add_sea))**2))
rmse_add_sea
# Multiplicative Seasonality Model
Mul_sea = smf.ols('log_Sales ~ Jan+Feb+Mar+Apr+May+Jun+Jul+Aug+Sep+Oct+Nov',data = Train).fit()
pred_Mult_sea = pd.Series(Mul_sea.predict(Test))
rmse_Mult_sea = np.sqrt(np.mean((np.array(Test['Sales']) - np.array(np.exp(pred_Mult_sea)))**2))
rmse_Mult_sea
# Additive Seasonality Quadratic Trend 
add_sea_Quad = smf.ols('Sales ~ t+t_square+Jan+Feb+Mar+Apr+May+Jun+Jul+Aug+Sep+Oct+Nov',data=Train).fit()
pred_add_sea_quad = pd.Series(add_sea_Quad.predict(Test[['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','t','t_square']]))
rmse_add_sea_quad = np.sqrt(np.mean((np.array(Test['Sales'])-np.array(pred_add_sea_quad))**2))
rmse_add_sea_quad 
# Multiplicative Seasonality Linear Trend  
Mul_Add_sea = smf.ols('log_Sales ~ t+Jan+Feb+Mar+Apr+May+Jun+Jul+Aug+Sep+Oct+Nov',data = Train).fit()
pred_Mult_add_sea = pd.Series(Mul_Add_sea.predict(Test))
rmse_Mult_add_sea = np.sqrt(np.mean((np.array(Test['Sales'])-np.array(np.exp(pred_Mult_add_sea)))**2))
rmse_Mult_add_sea 
# Testing 
data = {"MODEL":pd.Series(["rmse_linear","rmse_Exp","rmse_Quad","rmse_add_sea","rmse_add_sea_quad","rmse_Mult_sea","rmse_Mult_add_sea"]),"RMSE_Values":pd.Series([rmse_linear,rmse_Exp,rmse_Quad,rmse_add_sea,rmse_add_sea_quad,rmse_Mult_sea,rmse_Mult_add_sea])}
table_rmse=pd.DataFrame(data)
table_rmse
# 'rmse_Mult_add_sea' has the least value among the models prepared so far Predicting new values 
predict_data = pd.read_excel("C:\\Users\\WIN10\\Desktop\\LEARNING\\DS\\forecast\\Predict_new.xlsx")
model_full = smf.ols('log_Sales ~ t+Jan+Feb+Mar+Apr+May+Jun+Jul+Aug+Sep+Oct+Nov',data = Train).fit()
pred_new  = pd.Series(model_full.predict(predict_data))
pred_new
predict_data["forecasted_result"] = pd.Series(pred_new)
