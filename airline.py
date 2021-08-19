# 1
import pandas as pd
# Importing the dataset
airlines = pd.read_excel("C:\\Users\\WIN10\\Desktop\\LEARNING\\DS\\forecast\\AirlinesData.xlsx")
month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
# Performing EDA
import numpy as np
airlines["t"] = np.arange(1,97)
airlines["t_square"] =airlines["t"]*airlines["t"]
airlines["log_Passengers"] = np.log(airlines["Passengers"])
airlines.columns
airlines.info()       
p = airlines["Month"][0]
p[0:3]
airlines['months']= 0
for i in range(96):
    p = airlines["Month"][i]
    airlines['months'][i]= p[0:3]
# Creating Dummy variables    
month_dummies = pd.DataFrame(pd.get_dummies(airlines['months']))
airlines1 = pd.concat([airlines, month_dummies], axis = 1)
# Visualization - Time plot
airlines1.Passengers.plot()
# Splitting the data into train and test
Train = airlines1.head(82)
Test = airlines1.tail(14)
# Linear Model
import statsmodels.formula.api as smf 
linear_model = smf.ols('Passengers ~ t', data=Train).fit()
pred_linear =  pd.Series(linear_model.predict(pd.DataFrame(Test['t'])))
rmse_linear = np.sqrt(np.mean((np.array(Test['Passengers']) - np.array(pred_linear))**2))
rmse_linear
# Exponential Model
Exp = smf.ols('log_Passengers ~ t', data = Train).fit()
pred_Exp = pd.Series(Exp.predict(pd.DataFrame(Test['t'])))
rmse_Exp = np.sqrt(np.mean((np.array(Test['Passengers']) - np.array(np.exp(pred_Exp)))**2))
rmse_Exp
# Quadratic Model
Quad = smf.ols('Passengers ~ t+t_square', data=Train).fit()
pred_Quad = pd.Series(Quad.predict(Test[["t","t_square"]]))
rmse_Quad = np.sqrt(np.mean((np.array(Test['Passengers'])-np.array(pred_Quad))**2))
rmse_Quad
# Additive seasonality model
add_sea = smf.ols('Passengers ~ Jan+Feb+Mar+Apr+May+Jun+Jul+Aug+Sep+Oct+Nov', data=Train).fit()
pred_add_sea = pd.Series(add_sea.predict(Test[['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov']]))
rmse_add_sea = np.sqrt(np.mean((np.array(Test['Passengers'])-np.array(pred_add_sea))**2))
rmse_add_sea
# Multiplicative Seasonality Model
Mul_sea = smf.ols('Passengers  ~ Jan+Feb+Mar+Apr+May+Jun+Jul+Aug+Sep+Oct+Nov',data = Train).fit()
pred_Mult_sea = pd.Series(Mul_sea.predict(Test))
rmse_Mult_sea = np.sqrt(np.mean((np.array(Test['Passengers']) - np.array(np.exp(pred_Mult_sea)))**2))
rmse_Mult_sea
# Additive Seasonality Quadratic Trend 
add_sea_Quad = smf.ols('Passengers ~ t+t_square+Jan+Feb+Mar+Apr+May+Jun+Jul+Aug+Sep+Oct+Nov',data=Train).fit()
pred_add_sea_quad = pd.Series(add_sea_Quad.predict(Test[['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','t','t_square']]))
rmse_add_sea_quad = np.sqrt(np.mean((np.array(Test['Passengers'])-np.array(pred_add_sea_quad))**2))
rmse_add_sea_quad 
# Multiplicative Seasonality Linear Trend  
Mul_Add_sea = smf.ols('Passengers ~ t+Jan+Feb+Mar+Apr+May+Jun+Jul+Aug+Sep+Oct+Nov',data = Train).fit()
pred_Mult_add_sea = pd.Series(Mul_Add_sea.predict(Test))
rmse_Mult_add_sea = np.sqrt(np.mean((np.array(Test['Passengers'])-np.array(np.exp(pred_Mult_add_sea)))**2))
rmse_Mult_add_sea 
# Testing 
data = {"MODEL":pd.Series(["rmse_linear","rmse_Exp","rmse_Quad","rmse_add_sea","rmse_add_sea_quad","rmse_Mult_sea","rmse_Mult_add_sea"]),"RMSE_Values":pd.Series([rmse_linear,rmse_Exp,rmse_Quad,rmse_add_sea,rmse_add_sea_quad,rmse_Mult_sea,rmse_Mult_add_sea])}
table_rmse=pd.DataFrame(data)
table_rmse
# 'rmse_add_sea_quad' has the least value among the models prepared so far Predicting new values 
predict_data = pd.read_excel("C:\\Users\\rammo\\Downloads\\DS\\Forecasting\\Predict_new.xlsx")
model_full = smf.ols('Passengers ~ t+t_square+Jan+Feb+Mar+Apr+May+Jun+Jul+Aug+Sep+Oct+Nov',data=Train).fit()
pred_new  = pd.Series(model_full.predict(predict_data))
pred_new
predict_data["forecasted_result"] = pd.Series(pred_new)


