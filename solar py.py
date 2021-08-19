# 4
import pandas as pd
# Importing the dataset
solar= pd.read_csv("C:\\Users\\WIN10\\Desktop\\LEARNING\\DS\\forecast\\solarpowercumuldaybyday2.csv")
month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'] 
# Performing EDA
import numpy as np
solar["t"] = np.arange(1,2559)
solar["t_square"] =solar["t"]*solar["t"]
solar["log_cum_power"] = np.log(solar["cum_power"])
solar.columns
solar.info()       
p = solar["date"][0]
p[2:5]
solar['months']= 0
for i in range(2558):
    p = solar["date"][i]
    solar['months'][i]= p[2:5]
# Creating dummy variables
month_dummies = pd.DataFrame(pd.get_dummies(solar['months']))
solar1 = pd.concat([solar, month_dummies], axis = 1)
# Visualization - Time plot
solar1.cum_power.plot()
# Splitting the data into test and train
Train = solar1.head(2000)
Test = solar1.tail(558)
Train = Train.rename(columns={'/01': 'Jan', '/02': 'Feb','/03': 'Mar','/04': 'Apr','/05': 'May','/06': 'Jun','/07': 'Jul','/08': 'Aug','/09': 'Sep','/10': 'Oct','/11': 'Nov','/12': 'Dec','01/': 'Jan', '02/': 'Feb','03/': 'Mar','04/': 'Apr','05/': 'May','06/': 'Jun','07/': 'Jul','08/': 'Aug','09/': 'Sep','10/': 'Oct','11/': 'Nov','12/': 'Dec'})
Test = Test.rename(columns={'/01': 'Jan', '/02': 'Feb','/03': 'Mar','/04': 'Apr','/05': 'May','/06': 'Jun','/07': 'Jul','/08': 'Aug','/09': 'Sep','/10': 'Oct','/11': 'Nov','/12': 'Dec','01/': 'Jan', '02/': 'Feb','03/': 'Mar','04/': 'Apr','05/': 'May','06/': 'Jun','07/': 'Jul','08/': 'Aug','09/': 'Sep','10/': 'Oct','11/': 'Nov','12/': 'Dec'})
# Linear Model
import statsmodels.formula.api as smf 
linear_model = smf.ols('cum_power ~ t', data=Train).fit()
pred_linear =  pd.Series(linear_model.predict(pd.DataFrame(Test['t'])))
rmse_linear = np.sqrt(np.mean((np.array(Test['cum_power']) - np.array(pred_linear))**2))
rmse_linear
# Exponential Model
Exp = smf.ols('log_cum_power ~ t', data = Train).fit()
pred_Exp = pd.Series(Exp.predict(pd.DataFrame(Test['t'])))
rmse_Exp = np.sqrt(np.mean((np.array(Test['cum_power']) - np.array(np.exp(pred_Exp)))**2))
rmse_Exp
# Quadratic Model
Quad = smf.ols('cum_power~ t+t_square', data=Train).fit()
pred_Quad = pd.Series(Quad.predict(Test[["t","t_square"]]))
rmse_Quad = np.sqrt(np.mean((np.array(Test['cum_power'])-np.array(pred_Quad))**2))
rmse_Quad
# Additive seasonality Model
add_sea = smf.ols('cum_power ~ Jan+Feb+Mar+Apr+May+Jun+Jul+Aug+Sep+Oct+Nov+Dec', data=Train).fit()
pred_add_sea = pd.Series(add_sea.predict(Test[['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']]))
rmse_add_sea = np.sqrt(np.mean((np.array(Test['cum_power'])-np.array(pred_add_sea))**2))
rmse_add_sea
# Multiplicative Seasonality Model
Mul_sea = smf.ols('log_cum_power~ Jan+Feb+Mar+Apr+May+Jun+Jul+Aug+Sep+Oct+Nov',data = Train).fit()
pred_Mult_sea = pd.Series(Mul_sea.predict(Test))
rmse_Mult_sea = np.sqrt(np.mean((np.array(Test['cum_power']) - np.array(np.exp(pred_Mult_sea)))**2))
rmse_Mult_sea
# Additive Seasonality Quadratic Trend 
add_sea_Quad = smf.ols('cum_power ~ t+t_square+Jan+Feb+Mar+Apr+May+Jun+Jul+Aug+Sep+Oct+Nov',data=Train).fit()
pred_add_sea_quad = pd.Series(add_sea_Quad.predict(Test[['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','t','t_square']]))
rmse_add_sea_quad = np.sqrt(np.mean((np.array(Test['cum_power'])-np.array(pred_add_sea_quad))**2))
rmse_add_sea_quad 
# Multiplicative Seasonality Linear Trend  
Mul_Add_sea = smf.ols('log_cum_power ~ t+Jan+Feb+Mar+Apr+May+Jun+Jul+Aug+Sep+Oct+Nov',data = Train).fit()
pred_Mult_add_sea = pd.Series(Mul_Add_sea.predict(Test))
rmse_Mult_add_sea = np.sqrt(np.mean((np.array(Test['cum_power'])-np.array(np.exp(pred_Mult_add_sea)))**2))
rmse_Mult_add_sea 
# Testing 
data = {"MODEL":pd.Series(["rmse_linear","rmse_Exp","rmse_Quad","rmse_add_sea","rmse_add_sea_quad","rmse_Mult_sea","rmse_Mult_add_sea"]),"RMSE_Values":pd.Series([rmse_linear,rmse_Exp,rmse_Quad,rmse_add_sea,rmse_add_sea_quad,rmse_Mult_sea,rmse_Mult_add_sea])}
table_rmse=pd.DataFrame(data)
table_rmse
# 'rmse_add_sea_quad' has the least value among the models prepared so far Predicting new values 

