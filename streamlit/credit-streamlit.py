import streamlit as st
import requests


st.title("Give Me Some Credit!")
st.subheader("Enter your information as stated below")

# create form
with st.form(key="credit_form"):
    type_customer = st.number_input(
        label = "1. Input your Customer Type (0 if Personal, 1 if Business):",
        help = "Example value: 0"
    )

    age = st.number_input(
        label = "2. Input your Age:",
        help = "Example value: 34"
    )

    monthly_income = st.number_input(
        label = "3. Input your Monthly Income (0 if no definite value):",
        help = "Example value: 2000"
    )

    num_dependents = st.number_input(
        label = "4. Input how many Dependents you have:",
        help = "Example value: 3"
    )

    debt_ratio = st.number_input(
        label = "5. Input your current Debt Ratio:",
        help = "Example value: 0.6"
    )

    open_cred_lines = st.number_input(
        label = "6. Input your current number of Open Credits and Loans:",
        help = "Example value: 2"
    )

    revolving = st.number_input(
        label = "7. Input your current total balance on credit cards divided by the sum of credit limits:",
        help = "Example value: 0.7"
    )

    real_estate_loans = st.number_input(
        label = "8. Input how many Real Estate Loans you currently have:",
        help = "Example value: 1"
    )

    num_times_30_59 = st.number_input(
        label = "9. Input how many times you have been 30-59 days past due (but no worse) in the last 2 years:",
        help = "Example value: 0"
    )

    num_times_60_89 = st.number_input(
        label = "10. Input how many times you have been 60-89 days past due (but no worse) in the last 2 years:",
        help = "Example value: 0"
    )

    num_times_90_worse = st.number_input(
        label = "11. Input how many times you have been 90 days or more past due in the last 2 years:",
        help = "Example value: 0"
    )

    # button submit
    submitted = st.form_submit_button('predict!')

    if submitted:
        # collect data from form
        form_data = {
            'RevolvingUtilizationOfUnsecuredLines': revolving,
            'age': age,
            'NumberOfTime30-59DaysPastDueNotWorse': num_times_30_59,
            'DebtRatio': debt_ratio,
            'MonthlyIncome': monthly_income,
            'NumberOfOpenCreditLinesAndLoans': open_cred_lines,
            'NumberOfTimes90DaysLate': num_times_90_worse,
            'NumberRealEstateLoansOrLines': real_estate_loans,
            'NumberOfTime60-89DaysPastDueNotWorse': num_times_60_89,
            'NumberOfDependents': num_dependents,
            'TypeCustomer': type_customer
        }
        
        # sending the data to api service
        with st.spinner("Sending data to prediction server... please wait..."):
            predict_url = "http://api:8000/predict"
            res = requests.post(predict_url, json= form_data).json()

        # parse the prediction result
        if res['status'] == 200:
            st.success(f"Your Credit is: {res['prediction']}")
        else:
            st.error(f"ERROR predicting the data.. please check your code {res}")


