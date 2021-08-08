import streamlit as st
import pandas as pd
import altair as alt
import streamlit.components.v1 as components

# Some Chart code copied from: https://github.com/thecraigoneill/gravitymodel/blob/main/streamlit_app.py

st.image("https://github.com/ChristopherDavisUCI/Math_CEO/blob/main/Python_MathCEO/Mizu/images/mizu.png?raw=true",width=300)

st.title("The region of Mizu :sunglasses:")

with st.sidebar:
    st.write("In the region of Mizu, x and y are always whole numbers")
    x = st.slider('Choose a value of x (side length of the orange continent)', 1, 20, 2)
    y = st.slider('Choose a value of y (side length of the green continent)', 1, 20, 3, key="original")
    a = st.empty()
    a.write("We don't allow x + y > 20.")
    if x + y > 20:
        bad_values = True
        a.write(":broken_heart: You set x + y > 20 so the app won't work :broken_heart:")
        y = 20-x
    else:
        bad_values = False

box = pd.DataFrame({'x1': [0], 'x2': [x], 'y1': [0], 'y2': [x]})

opacity = 0.6

domain = (0,20)
axis = alt.Axis(values=list(range(21)))
domain = domain

c = alt.Chart(box).mark_rect(fill='orange', stroke='orange',opacity=opacity).encode(
alt.X('x1', scale=alt.Scale(domain = domain),title="",axis=axis),
alt.Y('y1', scale=alt.Scale(domain = domain),axis=axis,title=""),
x2='x2',
y2='y2')

box = pd.DataFrame({'x1': [0], 'x2': [x], 'y1': [x], 'y2': [x+y]})

ocean1 = alt.Chart(box).mark_rect(fill='cyan', stroke='cyan').encode(
alt.X('x1', scale=alt.Scale(domain = domain),axis=axis,title=""),
alt.Y('y1', scale=alt.Scale(domain = domain),axis=axis),
x2='x2',
y2='y2')

box = pd.DataFrame({'x1': [x], 'x2': [x+y], 'y1': [x], 'y2': [x+y]})

d = alt.Chart(box).mark_rect(fill='green', stroke='green',opacity=opacity).encode(
alt.X('x1', scale=alt.Scale(domain = domain),axis=axis),
alt.Y('y1', scale=alt.Scale(domain = domain),axis=axis),
x2='x2',
y2='y2')

box = pd.DataFrame({'x1': [x], 'x2': [x+y], 'y1': [0], 'y2': [x]})

ocean2 = alt.Chart(box).mark_rect(fill='cyan', stroke='cyan').encode(
alt.X('x1', scale=alt.Scale(domain = domain),axis=axis),
alt.Y('y1', scale=alt.Scale(domain = domain),axis=axis),
x2='x2',
y2='y2')


text_box = pd.DataFrame({'x': [x/2,x,x+y/2,x], 'y': [x,x/2,x,x+y/2], 'text': ["x","x","y","y"]})

text = alt.Chart(text_box).mark_text(dx=0,dy=0).encode(
    x = alt.X('x', scale=alt.Scale(domain = domain),axis=axis),
    y = alt.Y('y', scale=alt.Scale(domain = domain),axis=axis),
    text = 'text',
    size = alt.value(14)
)

e = alt.layer(c,d,ocean1,ocean2,text).properties(
    width=300,
    height=300
)

st.markdown('''The region of Mizu consists of: 
* a square orange continent, with integer side length x;
* a square green continent, with integer side length y;
* and two rectangular oceans.\n
See the picture below.  Mizu is the total square, consisting of all three colors.  Mizu's planet is a flat 20x20 square, so $x + y \leq 20$.''')

st.altair_chart(e)

st.write("Use the side-bar on the left to control the continents.")

st.header("The Questions")

if 'answered' not in st.session_state:
    st.session_state['answered'] = []

yes = ":white_check_mark:"
no = "⬜️"

qns = 10

options = [i for i in range(1,qns+1)]



b = st.empty()


option = st.selectbox(
 'Choose a question to answer',
    options, format_func=lambda n: f"Question {n}")

def f(qn):
    temp = 1
    if qn == temp:
        st.write("Using the sliders on the left of the screen, draw a possible Mizu which has total ocean area 30.")
        st.write("The total *ocean* area is currently: " +str(2*x*y))
        if 2*x*y == 30:
            if temp not in st.session_state["answered"]:
                st.session_state["answered"].append(temp)
                st.write("Good work!")
    temp = 2
    if qn == temp:
        st.write("Draw a possible Mizu which has orange continent with area 36 and which has green continent with area 13 more than that.")
        if (x == 6) and (y == 7):
            if temp not in st.session_state["answered"]:
                st.session_state["answered"].append(temp)
                st.write("Good work!")
    temp = 3
    if qn == temp:
        st.write("Assume x = 3 and x+y = 7.  Answer the following questions.")
        a1 = st.number_input("What is the area of the orange continent?", value = 0)
        a2 = st.number_input("What is the area of the green continent?", value = 0)
        a3 = st.number_input("What is the total area of Mizu (including the oceans)?", value = 0)
        checked = st.button("Check")
        if (a1 == 9) and (a2 == 16) and (a3 == 49):
            st.session_state["answered"].append(temp)
            st.write("Good work!")
        elif checked:
            st.write("At least one of the answers is not correct") 
        
    temp = 4
    if qn == temp:
        st.write("Draw a possible Mizu where the total area of Mizu is 400 (the entire 20x20 grid) and where the total ocean area is as small as possible.")
        if (x+y == 20) and ((x == 1) or (y == 1)) and not bad_values:
            st.session_state["answered"].append(temp)
            st.write("Good work!")

    temp = 5
    if qn == temp:
        st.write("Draw a possible Mizu where the total ocean area equals the area of the orange continent.")
        if x == 2*y:
            st.session_state["answered"].append(temp)
            st.write("Good work!")

    temp = 6
    if qn == temp:
        st.write("Which of the following is a formula for the area of one of the oceans?")
        a1 = st.radio("Single ocean:", options=["x+y","xy","2xy", "x^2 + y^2"], key="single ocean")
        a2 = st.radio("Single ocean:", options=["x+y","xy","2xy", "x^2 + y^2"])
        if (a1 == "xy") and (a2 == "2xy"):
            st.session_state["answered"].append(temp)
            st.write("Good work!")

    temp = 7
    if qn == temp:
        st.write("If we know the area of the orange continent is smaller than 30, how many possibilities are there for the area of the orange continent?")
        a1 = st.number_input("How many possibilities", value = 0)
        checked = st.button("Check")
        if (a1 == 5):
            st.session_state["answered"].append(temp)
            st.write("Good work!")
        elif checked:
            st.write("Keep trying!")

    temp = 8
    if qn == temp:
        st.write("Is the total ocean area always an even number?")
        a1 = st.radio("Always even:", options=["yes","no"], key="even", index=1)
        st.write("Is the value of (x+y)^2 - x^2 - y^2 always an even number?")
        a2 = st.radio("Always even:", options=["yes","no"], key="even2", index=1)
        if (a1 == "yes") and (a2 == "yes"):
            st.session_state["answered"].append(temp)
            st.write("Good work!")

    temp = 9
    if qn == temp:
        st.write("Draw a possible Mizu where the difference in areas between the continents is 33.")
        if abs(x**2-y**2) == 33:
            st.session_state["answered"].append(temp)
            st.write("Good work!")

    temp = 10
    if qn == temp:
        st.write("Draw a possible Mizu which has ocean area as big as possible.")
        if (x == 10) and (y == 10):
            if temp not in st.session_state["answered"]:
                st.session_state["answered"].append(temp)
                st.write("Good work!")

f(option)

check_boxes = ""
for opt in options:
    solved = yes if opt in st.session_state['answered'] else no
    check_boxes += f"Q{opt}&nbsp{solved}&nbsp&nbsp&nbsp "

b.markdown(check_boxes)
