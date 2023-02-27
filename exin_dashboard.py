import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ~~~~~~~~~~~~Load the data for Bar Chart 
data = pd.read_csv('https://raw.githubusercontent.com/Deymomanka/data_by_continent/main/inColumn_bycontinent.csv')
df = pd.DataFrame(data)
# df['2021'] = df['2021'].str.replace(',', '')
# df['2021'] = df['2021'].astype(int)
df.iloc[:, 1:] = df.iloc[:, 1:].apply(lambda x: x.str.replace(',', '').astype(int))

# ~~~~~~~~~~~~Load the data for Area chart 
data2 = pd.read_csv('https://raw.githubusercontent.com/Deymomanka/data_by_continent/main/inColumn_bycountry.csv')
df2 = pd.DataFrame(data2)
# df['2021'] = df['2021'].str.replace(',', '')
# df['2021'] = df['2021'].astype(int)
df2.iloc[:, 2:] = df2.iloc[:, 2:].apply(lambda x: x.str.replace(',', '').astype(int))


st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
st.sidebar.header("Dashboard `経常収支` (Japan's Balance of Payments)")


st.sidebar.subheader("Total")
# Define your dictionary
my_dict = {"2014": 39215, "2015": 165194, '2016': 21391, '2017': 227779, '2018': 195047, '2019': 192513, '2020': 157699, '2021': 21591}
selected_value = st.sidebar.selectbox('Select value to display', list(my_dict.keys()))
st.markdown('### Total (100 million Yen)')
col1, col2, col3= st.columns(3)

# Calculate the delta to the previous year
previous_year = str(int(selected_value) - 1)  
previous_value = my_dict.get(previous_year, 0) 
current_value = my_dict.get(selected_value, 0)
delta = current_value - previous_value if previous_value else 0

col1.metric(label=selected_value, value=current_value, delta= "{} 前年比".format(delta))
#col2.metric("2022 ", "49143", "1st quarter")
col2.metric("2022 (2st quarter)", "23779", delta=23779-49143)
col3.metric("2022 (3st quarter)", "23782", delta=23782-23779)

# for example
# col1.metric(label="{} (100 million Yen)".format(selected_value), value=current_value, delta= "{} 前年比".format(delta))


st.sidebar.subheader('Bar Chart parameter')
selected_column = st.sidebar.selectbox('Select a year', df.columns[1:])



c1, c2 = st.columns((7,3))
with c1:
    st.markdown('### Bar Chart')
    # fig = px.bar(df, y='2021', x='Continent', text_auto='.2s',
    #         title="大陸ごとの経常収支の指標")
    # st.plotly_chart(fig)

    fig = px.bar(df, x='Continent', y=selected_column, title=f"経常収支の大陸別推移({selected_column}) \n Japan's Balance of Payments")
    

    fig.update_layout(
    title='経常収支の大陸別推移 (by continent) - {}'.format(selected_column),
    xaxis_title='Continent', # set the x-axis title
    yaxis_title='100 million Yen' # set the y-axis title
)
    
    st.plotly_chart(fig)
# with c2:
#     st.markdown('### Donut chart')
#     plost.donut_chart(
#         data=stocks,
#         theta=donut_theta,
#         color='company',
#         legend='bottom', 
#         use_container_width=True)

#_____________________________

st.markdown('### Line Chart')
# reshape the data frame to long format
df2 = pd.melt(df2, id_vars=['Continent', 'Country'], var_name='year', value_name='value')

# create a dictionary of data frames, one for each continent
df_by_continent = {}
for continent in df2['Continent'].unique():
    df_by_continent[continent] = df2[df2['Continent'] == continent]

 # create a Streamlit selectbox for choosing the continent to display
st.sidebar.subheader('Line chart parameter')
selected_continent = st.sidebar.selectbox('Select continent:', list(df_by_continent.keys()))

# get the data frame for the selected continent
df_continent = df_by_continent[selected_continent]

# create a subplot with one row and one column
fig3 = make_subplots(rows=1, cols=1)

# add traces to the subplot for each country in the selected continent
for country in df_continent['Country'].unique():
    df_country = df_continent[df_continent['Country'] == country]
    fig3.add_trace(go.Line(
        x=df_country['year'], y=df_country['value'],
        name=country,
        line=dict(width=2)), row=1, col=1)
    

# update the layout of the subplot with the selected continent
fig3.update_layout(
    title='経常収支の地域別推移 (by country) - {}'.format(selected_continent),
    xaxis_title='Year', # set the x-axis title
    yaxis_title='100 million Yen' # set the y-axis title
)
# show the chart
st.plotly_chart(fig3)



string = "Created with ❤️ by [Yuliya (ゆりあ)]"
word = "[Yuliya (ゆりあ)]"
link = "https://www.linkedin.com/in/yuliya-azanovich-80a260175/"

# Replace the word with a clickable link
clickable_word = f'<a href="{link}">{word}</a>'
new_string = string.replace(word, clickable_word)

# Render the new string with a clickable link using st.markdown
st.sidebar.markdown(new_string, unsafe_allow_html=True)
