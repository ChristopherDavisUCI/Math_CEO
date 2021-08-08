import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

rng = np.random.default_rng()

img_bull = 'https://github.com/ChristopherDavisUCI/Math_CEO/blob/main/Python_MathCEO/BearBull2/images/bull.png?raw=true'
img_bear = 'https://github.com/ChristopherDavisUCI/Math_CEO/blob/main/Python_MathCEO/BearBull2/images/bear.png?raw=true'
img_straight = 'https://github.com/ChristopherDavisUCI/Math_CEO/blob/main/Python_MathCEO/BearBull2/images/straight.png?raw=true'

animal_dict = {"Bull":img_bull, "Bear":img_bear, "Straight":img_straight}

series_comm = pd.read_csv("https://raw.githubusercontent.com/ChristopherDavisUCI/Math_CEO/main/Python_MathCEO/BearBull2/commodities.csv",usecols=[0,1],index_col=0,thousands=",",
                          squeeze=True,dtype={"Commodity":"string","Price":"float64"})

st.title("Bear Markets and Bull Markets")

cols = st.beta_columns([x for _ in range(5) for x in [1.3,1]])

for i in range(0,len(cols),2):
    with cols[i]:
        st.image("https://github.com/ChristopherDavisUCI/Math_CEO/blob/main/Python_MathCEO/BearBull2/images/bear.png?raw=true")

    with cols[i+1]:
        st.image("https://github.com/ChristopherDavisUCI/Math_CEO/blob/main/Python_MathCEO/BearBull2/images/bull.png?raw=true")

st.header("Introduction")

st.markdown('''
    The price of a commodity is shown for a variety of days. 
    If the price is lower than it was 5 days ago, we call it a "bear" market.
    If the price is higher than it was 5 days ago, we call it a "bull" market.
    (Why these names?  Imagine a bull pushing someone up into the air... higher!  Imagine a bear dragging someone down to the ground... lower!)
    <br><br>For example,
    in the sample picture, we are in a bull market on Day 12, because the price is higher than it was on Day 7. 
    Notice how the price on Day 11 doesn't matter, only the price on Day 7, because we only care about the price five days earlier.  Do you see why Day 7 is a bear market?
    ''', unsafe_allow_html=True)

st.image("https://github.com/ChristopherDavisUCI/Math_CEO/blob/main/Python_MathCEO/BearBull2/images/sample1.png?raw=true", use_column_width='auto')

st.markdown('''
    The first five prices represent neither bear markets nor bull markets, because we don't know what the price was five days earlier.  The values for all the other days in this sample market are shown below.
''')

st.image("https://github.com/ChristopherDavisUCI/Math_CEO/blob/main/Python_MathCEO/BearBull2/images/sample2.png?raw=true", use_column_width='auto')

st.header("Your challenge")

def get_score(x,animal):
    if animal == "Bear":
        other = "Bull"
    else:
        other = "Bear"
    if x == animal_dict[animal]:
        return 1
    elif x == animal_dict[other]:
        return -0.5
    else:
        return 0

interval = 5

def choose_image(row):
    if row["Bear"]:
        return img_bear
    elif row["Bull"]:
        return img_bull
    else:
        return img_straight

def get_comm(name, pts):
    price = series_comm[name]
    prices = price+price*(0.1*np.random.randn(pts)).cumsum()
    return [round(x,2) for x in prices]

def make_chart(name,pts,animal):
    max_score = 0
    while max_score == 0:
        df = pd.DataFrame({'x':range(1,pts+1),'y':get_comm(name, pts),'img':np.zeros(pts)})
        df["Bear"] = False
        df["Bull"] = False
        df.loc[interval:,'Bull'] = (df.iloc[:-interval]['y'].to_numpy() < df.iloc[interval:]['y'].to_numpy())
        df.loc[interval:,'Bear'] = (df.iloc[:-interval]['y'].to_numpy() > df.iloc[interval:]['y'].to_numpy())
        df["img"] = df.apply(choose_image, axis=1)
        df.loc[:,'score'] = df['img'].map(lambda x: get_score(x,animal))

        max_score = (df['img']==animal_dict[animal]).sum()

    answers_selection = alt.selection_multi(on='click', toggle=False, empty='none',fields = ['x'], init=[{'x':1}])

    base = alt.Chart(df).mark_image(width=20,height=20).encode(
        x=alt.X('x:O', axis = alt.Axis(title="Day",labelAngle=0,tickCount=len(df),labelOverlap="parity")),
        y=alt.Y('y', axis = alt.Axis(title="Price in Dollars"), scale=alt.Scale(zero=False)),
        tooltip = [alt.Tooltip('x',title="Day"),alt.Tooltip('y',title="Price", format='$,.2f')],
        size = alt.value(50)
    ).properties(
        width=700,
        height=300
    )

    base = base.add_selection(
        answers_selection
    )

    base = base.encode(
        url=alt.condition(answers_selection, 'img', alt.value(img_straight))
    )

    text = alt.Chart(df).transform_filter(answers_selection).mark_text(
        align='left',
        baseline='top',
    ).encode(
        x=alt.value(5),
        y=alt.value(-30),
        color = alt.condition(f"datum.total_score == {max_score}",alt.value("green"),alt.value("black")),
        text = alt.condition(f"datum.total_score == {max_score}",alt.value("You win!! "*5),'text:N'),
        size = alt.condition(f"datum.total_score == {max_score}",alt.value(30),alt.value(14))
    ).transform_aggregate(
        total_score='sum(score)'
    ).transform_calculate(
        text=f'Click all of the {animal}s.  Your current score: '+alt.datum.total_score
    )

    comb = alt.layer(base,text).properties(
        title={
          "text": f"Price of {name}",
          "subtitle": [f"Maximum possible score: {max_score}",""],
          "color": "black",
          "fontSize": 18,
          "subtitleFontSize":14,
          "subtitleColor": "green"
        },
    )

    st.write(comb)
    return None




st.markdown('''
    In each of the charts below, you are asked to click on either the
    days with a bull market or the days with a bear market.  Try to do this visually, but sometimes it's "too close to call", and then you
    can put your mouse over the faces to see the exact numbers.<br><br>
    **Warning!**  If you click an incorrect face, you won't be able to get the maximum possible score.  You get 1 point for a correct click and you lose 0.5 points for an incorrect click.
''', unsafe_allow_html=True)

st.button("Get new charts")

empty_list = []

no_charts = 10

comms = rng.choice(series_comm.index,replace=False,size=no_charts + 1)

for i in range(no_charts):
    animal = rng.choice(["Bear","Bull"])
    st.markdown("---")
    st.write("")
    make_chart(comms[i],10+2*i,animal)

animal = rng.choice(["Bear","Bull"])
st.markdown("---")
st.header("The ultimate test :skull:")
st.write("")
st.write("")
make_chart(comms[i+1],100,animal)