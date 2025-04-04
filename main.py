import streamlit as st
from streamlit_lottie import st_lottie
import pandas as pd, math
import scraping
# import scrapping22
import requests, sentiment_analyses
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Campus Reviewer", layout="wide")

    
with st.sidebar:
    menu = option_menu(
            menu_title="Menu",  # No title for the top menu (can be set to a title if desired)
            options=["Home", "College"],  # Options for the menu
            icons=["house", "book"],  # Icons to display with each option
            menu_icon="cast",  # Icon for the menu
            default_index=0,  # Default index (first option is "Home")
        )
    st.markdown(
    '# Made with ❤️ by [Harkirat Singh](https://www.instagram.com/harkiratsingh.ssjb/)'
    )
    st.image("ab.gif")
    
st.markdown(
    """
    <style>
    /* General Reset */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Body */
    body {
        font-family: 'Arial', sans-serif;
        background-color: #121212;
        color: #e0e0e0;
    }

    /* Header */
    header[data-testid="stHeader"] {
        height: 0;
    }

    /* Title and Subheading */
    .big-title {
        font-size: 3.5rem;
        color: #ff4081;
        font-weight: 700;
        text-align: center;
        letter-spacing: 1px;
        margin-top: 20px;
        text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
    }
    
    .sub-heading {
        font-size: 1.6rem;
        text-align: center;
        margin-top: 10px;
        color: #cccccc;
    }

    /* Information Text */
    .info {
        font-size: 1.1rem;
        text-align: center;
        color: #b0b0b0;
        margin-bottom: 20px;
    }

    /* Score Box */
    .score {
        font-size: 2.4rem;
        text-align: center;
        margin-bottom: 30px;
        font-weight: 600;
        color: #ffeb3b;
    }

    /* Input Box */
    .input-box {
        width: 75%;
        padding: 12px;
        font-size: 1.2rem;
        border-radius: 15px;
        border: 2px solid #ff4081;
        background-color: #333333;
        color: #e0e0e0;
        margin: 15px auto;
        outline: none;
        transition: all 0.3s ease;
    }

    .input-box:focus {
        border-color: #ff80ab;
        background-color: #444444;
    }

    /* Radio Buttons */
    .stRadio > div {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        gap: 20px;
        justify-content: center;
    }

    .stRadio div[role='radiogroup'] > label > div:first-child {
        display: none;
    }

    .stRadio label {
        background: rgba(255, 64, 129, 0.2);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        color: #ffffff;
        padding: 16px 30px;
        border-radius: 25px;
        border: 1px solid rgba(255, 64, 129, 0.4);
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
        font-size: 1.1rem;
    }

    .stRadio label:hover {
        background: rgba(255, 64, 129, 0.4);
        color: #ffeb3b;
        border-color: rgba(255, 64, 129, 0.6);
        transform: scale(1.05);
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
    }

    .stRadio div[role='radiogroup'] > label[data-selected="true"] {
        background: #ff4081;
        border-color: #ff80ab;
        color: #121212;
        font-weight: 600;
        box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.3);
    }

    .stRadio div[role='radiogroup'] > label[data-selected="true"]:hover {
        background: #ff80ab;
        border-color: #ff4081;
        transform: scale(1.05);
        box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.4);
    }

    /* Cards */
    .card {
        background-color: #1e1e1e;
        padding: 25px;
        margin-bottom: 20px;
        border-radius: 20px;
        box-shadow: 0px 6px 10px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .card:hover {
        transform: scale(1.03);
        box-shadow: 0px 10px 15px rgba(0, 0, 0, 0.3);
    }

    .card p {
        font-size: 1.1rem;
        color: #b0b0b0;
        line-height: 1.6;
    }

    /* Button */
    .stButton > button {
        background-color: #ff4081;
        color: #ffffff;
        font-size: 1.2rem;
        font-weight: 600;
        padding: 12px 30px;
        border-radius: 50px;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #ff80ab;
        transform: scale(1.05);
        box-shadow: 0px 6px 10px rgba(0, 0, 0, 0.3);
    }

    </style>
    """,
    unsafe_allow_html=True
)

if menu == "Home":
    st.markdown('<div class="big-title">Campus Reviewer</div>', unsafe_allow_html=True)

    # Title of the web app
    # st.title("College Review Sentiment Analysis")

    # Introduction to the project
    st.write(
        """
        ## Welcome to the College Review Sentiment Analyzer!
        
        This project performs **sentiment analysis** on reviews written about colleges.
        It shows the **positive**, **negative**, and **neutral** sentiment of the reviews.
        Along with that it shows viualizations of the reviews that it analyzes and much more

        ### How to Use:
        1. Click on **College** to get started.
        2. Select the name of the college you want to analyze.
        3. The app will tell you whether the review is positive, negative, or neutral and
            it will also show a visualization of the reviews.
        """
    )
    @st.cache_data
    def load_url(url: str):
        r = requests.get(url)
        return r.json()

    st.container(height=10,border=False)
    col_file1,x, col_file2,y, col_file3 = st.columns([2,1,2,1,2])
    with col_file1:
            file1 = load_url("https://lottie.host/5a0b66ba-5a69-4fec-b58b-f53e15dea1db/RcvHRDxn8N.json")
            st_lottie(file1)
            st.markdown('<div>Explore among top institutions that align with your goals</div>', unsafe_allow_html=True)
    with col_file2:
            st.container(height=30,border=False)
            file2 = load_url("https://lottie.host/06dee71d-38fd-4d62-af20-74508d3e6d7e/dNum9fEsDF.json")
            st_lottie(file2)
            st.container(height=35,border=False)
            st.markdown('<div>Analyze sentiment and feedback regarding the institute from various sources</div>', unsafe_allow_html=True)
    with col_file3:
            file3 = load_url("https://lottie.host/9b3fdd1a-a026-4e72-9c6a-61e7d02f49ad/fdrAxdNkQS.json")
            st_lottie(file3)
            st.markdown('<div>Select The Best Institute for your career</div>', unsafe_allow_html=True)

    
elif menu == "College":
    @st.cache_data
    def load_url(url: str):
        r = requests.get(url)
        return r.json()

    df = pd.read_csv('college_data.csv')

    st.markdown('<div class="big-title">Campus Reviewer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-heading">Analyze feedback from various colleges</div>', unsafe_allow_html=True)

    col1,col2,col3 = st.columns([1,2,1])
    with col2:
        college_names = df['name'].values
        college_input = st.selectbox("", options=college_names, index=None, placeholder="Enter College Name")

    def plot(data):
        fig = px.bar(
            data, 
            x='Sentiment',
            color='Sentiment',
            color_discrete_map={'Positive': '#3a5a40', 'Slightly Positive': '#588157', 'Neutral': '#dad7cd','Slightly Negative': '#CB8585' ,'Negative': '#B83737'},
            template='plotly_white',
        )
        fig.update_layout(
            yaxis_title='Number of Reviews',
            margin=dict(l=20, r=20, t=50, b=20)
        )
        fig.update_traces(hovertemplate='Sentiment: %{x}<br>Count: %{y}')
        st.plotly_chart(fig, use_container_width=True)

        option = data['Sentiment'].unique()
        selected_category = st.radio("", options=option,key="Sentiment_choice",index=None,label_visibility='hidden')


        st.subheader("You can see summary of each sentiment here.")
        if selected_category:
            text = data[data['Sentiment'] == selected_category].Text.values

            rowval = min(math.ceil(len(text)/2), 5)
            textcol1, textcol2 = st.columns(2)
            for i in range(min(len(text),10)):
                if i<rowval:
                    with textcol1:
                        st.markdown(f"""<div class="card"><p>{text[i]}</p></div>""",unsafe_allow_html=True)
                else:
                    with textcol2:
                        st.markdown(f"""<div class="card"><p>{text[i]}</p></div>""",unsafe_allow_html=True)

    @st.cache_data
    def calculate_all(df):
        total_reviews = len(df)
        positive = len(df[df['Sentiment'] == 'Positive'])
        negative = len(df[df['Sentiment'] == 'Negative'])
        neutral = len(df[df['Sentiment'] == 'Neutral'])
        slight_positive = len(df[df['Sentiment'] == 'Slightly Positive'])
        slight_negative = len(df[df['Sentiment'] == 'Slightly Negative'])
        return total_reviews,positive,negative,neutral,slight_positive,slight_negative

    # def overview(df,title):
    #     total_reviews,positive,negative,neutral,slight_positive,slight_negative = calculate_all(df)
    #     if (positive+slight_positive) == 0:
    #         positive = 0
    #     else:
    #         positive = ((positive+slight_positive)*100)//total_reviews
    #     if (negative+slight_negative) == 0:
    #         negative = 0
    #     else:
    #         negative = ((negative+slight_negative)* 100)//total_reviews
    #     # try:
    #     #     neutral = (neutral* 100)//total_reviews
    #     # except:
    #     #     neutral = 0
    #     neutral = (neutral* 100)//total_reviews
    #     st.metric(title, f"{positive}% Positive", f"{neutral}% Neutral, {negative}% Negative")

    def overview(df, title):
        total_reviews = len(df)
        if total_reviews == 0:
            st.warning(f"No reviews found for {title}. Unable to calculate sentiment.")
            return

        positive = len(df[df['Sentiment'] == 'Positive'])
        negative = len(df[df['Sentiment'] == 'Negative'])
        neutral = len(df[df['Sentiment'] == 'Neutral'])
        slight_positive = len(df[df['Sentiment'] == 'Slightly Positive'])
        slight_negative = len(df[df['Sentiment'] == 'Slightly Negative'])

        if (positive + slight_positive) == 0:
            positive_percent = 0
        else:
            positive_percent = ((positive + slight_positive) * 100) // total_reviews

        if (negative + slight_negative) == 0:
            negative_percent = 0
        else:
            negative_percent = ((negative + slight_negative) * 100) // total_reviews

        neutral_percent = (neutral * 100) // total_reviews

        st.metric(title, f"{positive_percent}% Positive", f"{neutral_percent}% Neutral, {negative_percent}% Negative")


    @st.cache_data
    def show_details(df):
        total_reviews,positive,negative,neutral,slight_positive,slight_negative = calculate_all(df)
        st.metric("Total reviews", total_reviews)
        st.metric("Positive", positive)
        st.metric("Negative", negative)
        st.metric("Neutral", neutral)
        st.metric("Slightly Positive", slight_positive)
        st.metric("Slightly Negative", slight_negative)

    @st.cache_data
    def calculate_main(df1,df2,df3,df4,df5):
        tr1,p1,n1,ne1,sp1,sn1 = calculate_all(df1)
        tr2,p2,n2,ne2,sp2,sn2 = calculate_all(df2)
        tr3,p3,n3,ne3,sp3,sn3 = calculate_all(df3)
        tr4,p4,n4,ne4,sp4,sn4 = calculate_all(df4)
        tr5,p5,n5,ne5,sp5,sn5 = calculate_all(df5)
        p = p1+p2+p3+p4+p5+sp1+sp2+sp3+sp4+sp5
        n = n1+n2+n3+n4+n5+sn1+sn2+sn3+sn4+sn5
        ne = ne1+ne2+ne3+ne4+ne5
        tr = tr1+tr2+tr3+tr4+tr5
        return tr,p,n,ne

    def pie(df1,df2,df3,df4,df5):
        tr, p,n,ne = calculate_main(df1,df2,df3,df4,df5)
        values = [p,n,ne]
        fig = go.Figure(data=[go.Pie(
            labels=['Positive','Negative','Neutral'],
            values=values,
        )])
        fig.update_traces(marker=dict(line=dict(color='#000000', width=1.5)))
        st.plotly_chart(fig)

    @st.cache_data
    def overview_details(Infra_df,Academics_df,Placements_df, Campus_Life_df, Anything_Else_df):
        st.container(height=30,border=False)
        st.subheader(f"Overview of {college_input}")
        Infracol, Academiccol, Placementcol = st.columns(3)
        with Infracol:
            overview(Infra_df,"Infrastructure")
        with Academiccol:
            overview(Academics_df,"Academics")
        with Placementcol:
            overview(Placements_df,"Placements")
        piecol,extra, statementcol = st.columns([3,1,3])
        with piecol:
            pie(Infra_df,Academics_df,Placements_df, Campus_Life_df, Anything_Else_df)
        with statementcol:
            st.container(height=70,border=False)
            tr, pos, neg, neut = calculate_main(Infra_df,Academics_df,Placements_df, Campus_Life_df, Anything_Else_df)
            overall_percentage = (pos*100)//tr
            st.markdown(f'<div class="info">Overall Score : <div class="score">{overall_percentage}%</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info">Overall Positive Reviews for {college_input} : {pos}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info">Overall Negative Reviews for {college_input} : {neg}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info">Overall Neutral Reviews for {college_input} : {neut}</div>', unsafe_allow_html=True)


    if college_input:
        with st.spinner("Collecting Reviews... Please wait."):
            # data = scraping.scrap(df[df["name"] == college_input].id.values[0])
            data=scraping.scrap(df[df["name"] == college_input].id.values[0])
        with st.spinner("Analysing Reviews..."):
            Infra_df, Academics_df, Placements_df, Campus_Life_df, Anything_Else_df = sentiment_analyses.sentiment(data)

        overview_details(Infra_df,Academics_df,Placements_df, Campus_Life_df, Anything_Else_df)
        
        st.subheader(f'Detailed Review Analysis of {college_input}')
        option = st.radio('',('Infrastructure', 'Academics', 'Placements', 'Campus Life', 'Anything Else'),index=0,label_visibility="hidden")


        col_df,col_detail = st.columns([9,1])
        val = Infra_df
        if option == 'Infrastructure':
            val = Infra_df
        elif option == 'Academics':
            val = Academics_df
        elif option == 'Placements':
            val = Placements_df
        elif option == 'Campus Life':
            val = Campus_Life_df
        elif option == 'Anything Else':
            val = Anything_Else_df

        with col_df:
            st.subheader(option)
            plot(val)
        with col_detail:
            show_details(val)

    else:
        st.container(height=10,border=False)
        col_file1,x, col_file2,y, col_file3 = st.columns([2,1,2,1,2])
        with col_file1:
            file1 = load_url("https://lottie.host/5a0b66ba-5a69-4fec-b58b-f53e15dea1db/RcvHRDxn8N.json")
            st_lottie(file1)
            st.markdown('<div class="sub-heading">Explore among top institutions that align with your goals</div>', unsafe_allow_html=True)
        with col_file2:
            st.container(height=50,border=False)
            file2 = load_url("https://lottie.host/06dee71d-38fd-4d62-af20-74508d3e6d7e/dNum9fEsDF.json")
            st_lottie(file2)
            st.container(height=45,border=False)
            st.markdown('<div class="sub-heading">Analyze sentiment and feedback regarding the institute from various sources</div>', unsafe_allow_html=True)
        with col_file3:
            file3 = load_url("https://lottie.host/9b3fdd1a-a026-4e72-9c6a-61e7d02f49ad/fdrAxdNkQS.json")
            st_lottie(file3)
            st.markdown('<div class="sub-heading">Select The Best Institute for your career</div>', unsafe_allow_html=True)
        


    st.markdown('<div style="text-align: center; margin-top: 50px; font-size: 0.9rem; color: #6c757d;">Powered by Streamlit | © 2024 College Review Analyzer</div>', unsafe_allow_html=True)


