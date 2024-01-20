import streamlit as st
import openai
from streamlit_chat import message

# تعيين مفتاح API الخاص بـ OpenAI
openai.api_key = "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"

def api_calling(prompt, score):
    context = "You are an expert in environment and carbon footprint. "
    if score < 80:
        context += "The user needs advice on reducing carbon footprint. "
    prompt = context + prompt
    completions = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return completions.choices[0].text.strip()

def calculate_score(selections):
    points = {"Wind energy": 20, "Solar energy": 15, "Electricity from the grid": 10, "Natural gas": 5,
              "Walking": 20, "Bicycle/Electric bike": 15, "Public transport": 10, "Car": 5,
              "Vegetarian": 20, "Mixed with moderate meat consumption": 15, "Mixed with high meat consumption": 10, "Meat only": 5,
              "From 1 to 5": 20, "From 5 to 10": 15, "From 10 to 15": 10, "More than 15": 5}
    return sum(points[sel] for sel in selections)
st.title("EcoShift")
st.title("Let's work together to identify and reduce your daily carbon footprint")

# استبيان
st.header("Environmental Impact Survey")
questions = [
    "What is your primary source of energy today?",
    "What is your main mode of transportation today?",
    "What is your dietary system?",
    "How much do you consume packaged and processed products today?"
]
options = [
    ["Wind energy", "Solar energy", "Electricity from the grid", "Natural gas"],
    ["Walking", "Bicycle/Electric bike", "Public transport", "Car"],
    ["Vegetarian", "Mixed with moderate meat consumption", "Mixed with high meat consumption", "Meat only"],
    ["From 1 to 5", "From 5 to 10", "From 10 to 15", "More than 15"]
]

# تخزين اختيارات الاستبيان
if 'selections' not in st.session_state:
    st.session_state.selections = [None] * len(questions)

for i, question in enumerate(questions):
    st.session_state.selections[i] = st.radio(question, options[i], key=f'q{i}')

# تقديم الاستبيان وعرض النتيجة
if st.button("Submit Survey"):
    score = calculate_score(st.session_state.selections)
    st.session_state.score = score
    st.write(f"Your total score is: {score}")
else:
    score = st.session_state.get('score', None)

# شاتبوت
st.header("Chat With Eco")
user_input = st.text_input("Write here", key="input_chat")

if user_input and score is not None:
    output = api_calling(user_input, score)
    message(user_input, key="user_input", avatar_style="icons")
    message(output, avatar_style="miniavs", is_user=True, key="bot_response")
