import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide',page_title="Startup Analysis")
df=pd.read_csv('startup_cleaned1.csv')
df['Date']=pd.to_datetime(df['Date'])
df['Month']=df['Date'].dt.month
df['Year'] = df['Date'].dt.year

def load_overall_analysis():
    st.title("Overall Analysis")

    # Total Invested Amount
    total= round(df['Amount'].sum())

    #Maximum Funding taken Startup
    max_funding=df.groupby('Startup')['Amount'].max().sort_values(ascending=False).head(1).values[0]

    #Average Funding to Startup
    avg_funding=round(df.groupby('Startup')['Amount'].sum().mean())

    #Total  Startup
    total_startup=df['Startup'].nunique()


    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.metric('Total Funding',str(total)+' Cr')
    with col2:
        st.metric('Max Funding Taken By Startup', str(max_funding) + ' Cr')
    with col3:
        st.metric('Average Funding To Startup',str(avg_funding)+' Cr')
    with col4:
        st.metric('Total Startups',str(total_startup)+' Cr')

    #MoM Analysis
    st.header('MoM graph')
    selected_option = st.selectbox('Select Type', ['Total', 'Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['Year', 'Month'])['Amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['Year', 'Month'])['Amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['Month'].astype('str') + '-' + temp_df['Year'].astype('str')
    fig3, ax3 = plt.subplots()
    ax3.plot(temp_df['x_axis'], temp_df['Amount'])
    st.pyplot(fig3)


def load_investor_details(investor):
    st.title(investor)
    # Load recent 5 investment
    last5_df=df[df['Investors'].str.contains(investor)].head()[['Date','Startup','Vertical','City','Round','Amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)


    col1,col2=st.columns(2)
    with col1:
        big_series=df[df['Investors'].str.contains(investor)].groupby('Startup')['Amount'].sum().sort_values(ascending=False).head()

        #st.dataframe(big_series)
        st.subheader('Biggest  Investments')
        fig,ax=plt.subplots()
        ax.bar(big_series.index,big_series.values)
        st.pyplot(fig)

    with col2:
        vertical_series=df[df['Investors'].str.contains(investor)].groupby('Vertical')['Amount'].sum()
        st.subheader('Sector Invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series,labels=vertical_series.index,autopct="%0.01f%%")
        st.pyplot(fig1)

   # with col3:
    col1,col2=st.columns(2)
    with col1:
        vertical_series=df[df['Investors'].str.contains(investor)].groupby('Round')['Amount'].sum()
        st.subheader('Round in')
        fig2, ax2 = plt.subplots()
        ax2.pie(vertical_series,labels=vertical_series.index,autopct="%0.01f%%")
        st.pyplot(fig2)

    with col2:
        vertical_series = df[df['Investors'].str.contains(investor)].groupby('City')['Amount'].sum()
        st.subheader('In City')
        fig3, ax3 = plt.subplots()
        ax3.pie(vertical_series, labels=vertical_series.index, autopct="%0.01f%%")
        st.pyplot(fig3)

    #For Year on Year Basis
    #df['Year'] = df['Date'].dt.year
    year_series = df[df['Investors'].str.contains(investor)].groupby('Year')['Amount'].sum()
    st.subheader('Y-O-Y')
    fig4, ax4 = plt.subplots()
    ax4.plot(year_series.index,year_series.values)
    st.pyplot(fig4)

st.sidebar.title('Startup Funding Analysis')

option= st.sidebar.selectbox('Select One 0',['Overall Analysis','Startup','Investor'])

if option=='Overall Analysis':
   # btn0=st.sidebar.button('Show Overall Analysis')
   # if btn0:
        load_overall_analysis()

elif option =='Startup':
    st.sidebar.selectbox('Select Startup',sorted(df['Startup'].unique().tolist()))
    btn1=st.sidebar.button('Find Startup Details')
    st.title('Startup Analysis')
else:
    selected_incestor= st.sidebar.selectbox('Select Startup',sorted(set(df['Investors'].str.split(',').sum())))
    btn2=st.sidebar.button('Find Startup Details')
    if btn2:
        load_investor_details(selected_incestor)
