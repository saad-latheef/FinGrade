# app.py

from flask import Flask, render_template, request, jsonify
import random
import google.generativeai as genai
import os
from dotenv import load_dotenv




 

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction='You are an expert in the field of finance you have to answer any finance related questions within 4 to 5 sentences, youre a finance advisor in india so also predict where to invest if asked')

income=0
savings=0

app = Flask(__name__)
app.secret_key = 'your_secret_key'


# Simulated AI overview
def get_refreshed_advice(income,savings, total_expenses):
    advice= ''
    incom=str(income)
    savin = str(savings)
    expen = str(total_expenses)
    message = 'Create a two sentence review on my expense is '+expen+' savings is '+savin+' income is '+incom+'Write an opinion.'
    response = model.generate_content(message)
    if response:
        advice = response.text

    return advice
# Simulated AI model for expense prediction
def predict_expenses(past_expenses):
    average = sum(past_expenses) / len(past_expenses) if past_expenses else 0
    return round(average * (1 + (random.random() - 0.5) * 0.2), 2)

# Simulated AI model for investment advice
def get_investment_advice(risk, amount, income, savings):
    responses1=''
    responses2=''
    responses3=''
    amnt=str(amount)
    message1='I am willing to invest on low risk with an amount of '+amnt+' what is your opinion and where should i invest? My current income is '+income+ 'and savings is '+savings
    message2='I am willing to invest on medium risk with an amount of '+amnt+' what is your opinion and where should i invest? My current income is '+income+ 'and savings is '+savings
    message3='I am willing to invest on high risk with an amount of '+amnt+' what is your opinion and where should i invest? My current income is '+income+ 'and savings is '+savings
    if risk=='low':
        response = model.generate_content(message1)
        responses1 = response.text
    if risk=='medium':
        response = model.generate_content(message2)
        responses2 = response.text
    if risk=='high':
        response = model.generate_content(message3)
        responses3 = response.text
    
    advice_options = {
        'low': responses1,
        'medium': responses2,
        'high': responses3
    }
    return advice_options.get(risk, "Invalid risk level provided.")

#AI product advice
def get_product_advice(prdct, deposit, further, lyear, income, savings):
    depo= str(deposit)
    furt=str(further)
    ly=str(lyear)
    incom=str(income)
    saving=str(savings)
    message = 'I have an income of '+incom+' and life savings of '+saving+' . what if I want to acquire '+prdct+' to which I have a down payment of INR '+depo+' also INR '+furt+' per month for the next '+ly+' years. Do consider the inflation in the market and depreciation of the product I am buying if any.'
    response = model.generate_content(message)
    if response:
        advice = response.text

    return advice    

# Simulated AI chatbot responses
def get_chatbot_response(message):
    response = model.generate_content(message)
    responses = response.text

    return responses

# Sample data (in-memory)
expenses_data = [

]
advices=''

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    global advices
    advices=''
    total_expenses = sum(item['amount'] for item in expenses_data)
    remaining_budget = income - total_expenses
    if request.method == 'GET':
        global savings
        advices = get_refreshed_advice(income, savings, total_expenses)
    return render_template('dashboard.html',
                           income=income,
                           expenses=expenses_data,
                           savings=savings,
                           total_expenses=total_expenses,
                           remaining_budget=remaining_budget,advice=advices)



@app.route('/expenses', methods=['GET', 'POST'])
def expenses():
    global expenses_data
    if request.method == 'POST':
        category = request.form.get('category')
        amount = float(request.form.get('amount', 0))
        if category and amount:
            expenses_data.append({'category': category, 'amount': amount})
    return render_template('expenses.html', expenses=expenses_data)

@app.route('/investments', methods=['GET', 'POST'])
def investments():
    global savings
    global income
    savin= str(savings)
    incom = str(income)
    risk = None
    amount = 0
    advice = ""
    if request.method == 'POST':
        risk = request.form.get('risk')
        amount = float(request.form.get('amount', 0))
        advice = get_investment_advice(risk, amount, incom, savin)
    return render_template('investments.html', advice=advice)

@app.route('/ai_assistant', methods=['GET', 'POST'])
def ai_assistant():
    chat_messages = []
    if request.method == 'POST':
        user_message = request.form.get('message')
        if user_message:
            chat_messages.append({'sender': 'user', 'text': user_message})
            bot_response = get_chatbot_response(user_message)
            chat_messages.append({'sender': 'bot', 'text': bot_response})
    return render_template('ai_assistant.html', chat_messages=chat_messages)

@app.route('/user_details', methods=['GET', 'POST'])
def user_details():
    global savings
    global income
    if request.method == 'POST':
        Name = str(request.form.get('name11', 0))
        income = float(request.form.get('income1', 0))
        savings = float(request.form.get('expense1', 0))
    return render_template('user_details.html', income=income, savings=savings)

@app.route('/product',methods=['GET','POST'])
def product():
    global advices
    global savings
    global income
    if request.method == 'POST':
        advices=''
        prdct = str(request.form.get('seek', 0))
        deposit = float(request.form.get('depo', 0))
        further = float(request.form.get('furth', 0))
        lyear = float(request.form.get('year', 0))
        if prdct:
            advices = get_product_advice(prdct, deposit, further, lyear, income, savings )
    return render_template('product.html', advice=advices)

@app.route('/bank')
def bank():
    return render_template('bank.html')


@app.route('/api/predict_expenses', methods=['POST'])
def api_predict_expenses():
    data = request.get_json()
    past_expenses = data.get('past_expenses', [])
    prediction = predict_expenses(past_expenses)
    return jsonify({'prediction': prediction})

@app.route('/api/get_chatbot_response', methods=['POST'])
def api_get_chatbot_response():
    data = request.get_json()
    message = data.get('message', '')
    response = get_chatbot_response(message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
