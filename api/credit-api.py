from fastapi import FastAPI
from fastapi import Request
from numpy import log
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
    
    revolving = data['RevolvingUtilizationOfUnsecuredLines']
    age = data['age']
    num_times_30_59 = data['NumberOfTime30-59DaysPastDueNotWorse']
    debt_ratio = data['DebtRatio']
    monthly_income = data['MonthlyIncome']
    open_cred_lines = data['NumberOfOpenCreditLinesAndLoans']
    num_times_90_worse = data['NumberOfTimes90DaysLate']
    real_estate_loans = data['NumberRealEstateLoansOrLines']
    num_times_60_89 = data['NumberOfTime60-89DaysPastDueNotWorse']
    num_dependents = data['NumberOfDependents']
    type_customer = data['TypeCustomer']
    log_income = log(monthly_income + 1)
    log_log_revolving = log(log(revolving + 1) + 1)
    log_debt_ratio = log(debt_ratio + 1)

    data_order = [revolving,
                  age,
                  num_times_30_59,
                  debt_ratio,
                  monthly_income,
                  open_cred_lines,
                  num_times_90_worse,
                  real_estate_loans,
                  num_times_60_89,
                  num_dependents,
                  type_customer,
                  log_income,
                  log_log_revolving,
                  log_debt_ratio]

    model = load_model()
    scaler = load_scaler()
    label = ['Approved', 'Rejected']

    try:
        scaled_data = scaler.transform([data_order])
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