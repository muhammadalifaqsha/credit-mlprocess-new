from fastapi import FastAPI
from fastapi import Request
from numpy import log
from pandas import DataFrame
import pickle
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    response = {
        "status": 200,
        "messages": "The Credit Approval API is up!"
    }
    return response

# =====
# 1. Loading Model
# 2. Loading label = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']
# 3. predict Model = sepal_length, sepal_width, petal_length, petal_width 


def load_model():
    try: 
        pickle_file = open('model/model1.pkl', 'rb')
        classifier = pickle.load(pickle_file)
        return classifier
    except Exception as e:
        response = {
            'status':204,
            'messages': str(e)
        }
        return response
    
def load_scaler():
    try: 
        pickle_file = open('model/scaler1.pkl', 'rb')
        scaler = pickle.load(pickle_file)
        return scaler
    except Exception as e:
        response = {
            'status':204,
            'messages': str(e)
        }
        return response

def scaler_transform(data, scaler):
    data_scaled = scaler.transform(data)
    data_scaled = DataFrame(data_scaled)
    data_scaled.columns = data.columns
    data_scaled.index = data.index

    return data_scaled
    
@app.get('/check')
async def check():
    model = load_model()
    scaler = load_scaler()
    if model['status'] == 204 or scaler['status'] == 204:
        messages = 'Model is not ready to use' + model['messages']
    else:
        messages = 'Model is ready to use'
    return messages

@app.post("/predict")
async def predict(data: Request):

    # load request
    data = await data.json()
    
    data['LogMonthlyIncome'] = log(data['MonthlyIncome'] + 1)
    data['LogLogRevolvingUtilizationOfUnsecuredLines'] = log(log(data['RevolvingUtilizationOfUnsecuredLines'] + 1) + 1) 
    data['LogDebtRatio'] = log(data['DebtRatio'] + 1e-05)

    data_df = DataFrame(data)

    # data_order = [revolving,
    #               age,
    #               num_times_30_59,
    #               debt_ratio,
    #               monthly_income,
    #               open_cred_lines,
    #               num_times_90_worse,
    #               real_estate_loans,
    #               num_times_60_89,
    #               num_dependents,
    #               type_customer,
    #               log_income,
    #               log_log_revolving,
    #               log_debt_ratio]

    model = load_model()
    scaler = load_scaler()
    label = ['Approved', 'Rejected']

    try:
        scaled_data = scaler_transform(data_df, scaler)
        prediction = model.predict(scaled_data) #[[0]] --> [  [0]  ]  
        response = {
            'status': 200,
            'input': data_order,
            'prediction': label[prediction[0]]
        }
    except Exception as e:
        response = {
            'status': 204,
            'messages': str(e)
        }
    return response
    
if __name__ == "__main__":
    uvicorn.run("credit-api:app", host = "0.0.0.0", port = 8000)
