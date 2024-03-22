import streamlit as st  
import pandas as pd  
import plotly.express as px  
import base64  
from io import StringIO, BytesIO  
import plotly


def generate_excel_download_link(df):
    towrite = BytesIO()
    df.to_excel(towrite, encoding="utf-8", index=False, header=True)  
    towrite.seek(0) 
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="data_download.xlsx">Download Excel File</a>'
    return st.markdown(href, unsafe_allow_html=True)

def generate_html_download_link(fig):
    towrite = StringIO()
    fig.write_html(towrite, include_plotlyjs="cdn")
    towrite = BytesIO(towrite.getvalue().encode())
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:text/html;charset=utf-8;base64, {b64}" download="plot.html">Download Plot</a>'
    return st.markdown(href, unsafe_allow_html=True)


st.set_page_config(page_title='Data Analysis using python')
st.title('Data Analysis using python')
st.subheader('Upload your Excel file')

uploaded_file = st.file_uploader('Choose a XLSX file', type='xlsx')
if uploaded_file:
    st.markdown('---')
    df = pd.read_excel(uploaded_file, engine='openpyxl')
    df = pd.DataFrame(df)
    column_names = list(df)
    st.dataframe(df)


    Y_Axis = st.selectbox(
        'Choose the option for Y-axis?',
        (column_names),
        key = 11,
     )

    color_indication = st.selectbox(
        'Choose a option for color indication?',
        (column_names),
        key = 12,
     )

    groupby_column = st.selectbox(
        'What would you like to analyse?',
        (column_names),
    )


    output_columns = [Y_Axis,color_indication]
    df_grouped = df.groupby(by=[groupby_column], as_index=False)[output_columns].sum()

    fig = px.bar(
        df_grouped,
        x=groupby_column,
        y = Y_Axis,
        color = color_indication,
        color_continuous_scale=['red', 'yellow', 'green'],
        template='plotly_white',
        title=f'<b>{Y_Axis} & {color_indication} by {groupby_column}</b>'
    )
    st.plotly_chart(fig)
  

    

    st.subheader('Downloads:')
    generate_excel_download_link(df_grouped)
    generate_html_download_link(fig)
