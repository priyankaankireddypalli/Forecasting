# 2
import pandas as pd
# Importing the dataset 
cococola = pd.read_excel("C:\\Users\\WIN10\\Desktop\\LEARNING\\DS\\forecast\\CocaCola_Sales_Rawdata.xlsx")
quarter = ['Q1','Q2','Q3','Q4'] 
# Performing the EDA
import numpy as np
cococola["t"] = np.arange(1,43)
cococola["t_square"] = cococola["t"]*cococola["t"]
cococola["log_Sales"] = np.log(cococola["Sales"])
cococola.columns
cococola.info()
p = cococola["Quarter"][0]
p[0:3]
cococola['quarter']= 0
for i in range(42):
    p = cococola["Quarter"][i]
    cococola['quarter'][i]= p[0:3]
# Creating dummy variables    
quarter_dummies = pd.DataFrame(pd.get_dummies(cococola['quarter']))
cococola1 = pd.concat([cococola, quarter_dummies], axis = 1)
# Visualization - Time plot
cococola1.Sales.plot()
# Splitting the data into train and test
Train = cococola1.head(34)
Test = cococola1.tail(8)
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
# Additive seasonality model
add_sea = smf.ols('Sales ~ Q1_+Q2_+Q3_+Q4_', data=Train).fit()
pred_add_sea = pd.Series(add_sea.predict(Test[['Q1_','Q2_','Q3_','Q4_']]))
rmse_add_sea = np.sqrt(np.mean((np.array(Test['Sales'])-np.array(pred_add_sea))**2))
rmse_add_sea
# Multiplicative Seasonality Model
Mul_sea = smf.ols('log_Sales ~Q1_+Q2_+Q3_+Q4_',data = Train).fit()
pred_Mult_sea = pd.Series(Mul_sea.predict(Test))
rmse_Mult_sea = np.sqrt(np.mean((np.array(Test['Sales']) - np.array(np.exp(pred_Mult_sea)))**2))
rmse_Mult_sea
# Additive Seasonality Quadratic Trend 
add_sea_Quad = smf.ols('Sales ~ t+t_square+Q1_+Q2_+Q3_+Q4_',data=Train).fit()
pred_add_sea_quad = pd.Series(add_sea_Quad.predict(Test[['Q1_','Q2_','Q3_','Q4_','t','t_square']]))
rmse_add_sea_quad = np.sqrt(np.mean((np.array(Test['Sales'])-np.array(pred_add_sea_quad))**2))
rmse_add_sea_quad 
# Multiplicative Seasonality Linear Trend  
Mul_Add_sea = smf.ols('log_Sales ~ t+Q1_+Q2_+Q3_+Q4_',data = Train).fit()
pred_Mult_add_sea = pd.Series(Mul_Add_sea.predict(Test))
rmse_Mult_add_sea = np.sqrt(np.mean((np.array(Test['Sales'])-np.array(np.exp(pred_Mult_add_sea)))**2))
rmse_Mult_add_sea 
# Testing 
data = {"MODEL":pd.Series(["rmse_linear","rmse_Exp","rmse_Quad","rmse_add_sea","rmse_add_sea_quad","rmse_Mult_sea","rmse_Mult_add_sea"]),"RMSE_Values":pd.Series([rmse_linear,rmse_Exp,rmse_Quad,rmse_add_sea,rmse_add_sea_quad,rmse_Mult_sea,rmse_Mult_add_sea])}
table_rmse=pd.DataFrame(data)
table_rmse
# 'rmse_add_sea_quad' has the least value among the models prepared so far Predicting new values 

