import streamlit as st
import pandas as pd
import io



st.set_page_config(page_title="CSV Cleaner", page_icon=":smiley:")
st.title('CSV Cleaner :smiley:')
st.markdown('''
This app allows you to clean your CSV files by removing empty rows and columns, and filling missing values with a specified value.
''')

if 'cleaned_count' not in st.session_state:
    st.session_state.cleaned_count = 0
uploaded_file = st.file_uploader("Upload your file", type=["csv", "xlsx"])
if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
    st.subheader('Original Data')
    st.dataframe(df)
    col1, col2, col3 = st.columns(3)
    col1.metric("Empty Rows", df.isnull().all(axis=1).sum())
    col2.metric("Empty Columns", df.isnull().all(axis=0).sum())
    col3.metric("Total Missing Values", df.isnull().sum().sum())
    clean_missing = st.radio("Handle Missing Values", ("Fill with Mean", "Drop Rows/Columns", "Fill with Unknown"))
    if clean_missing == "Fill with Mean":
        df = df.fillna(df.mean(numeric_only=True))
    elif clean_missing == "Fill with Unknown":
        for col in df.columns:
            if df[col].dtype in ['int64', 'float64', 'int32', 'float32']:
                df[col] = df[col].fillna(0)
            else:
                df[col] = df[col].fillna("Unknown")
        df = df.fillna("Unknown")
    elif clean_missing == "Drop Rows/Columns":
        df = df.dropna(how='all')
        df = df.dropna(how='all', axis=1)
    else:
        st.warning("Please select a method to handle missing values.")

    st.subheader('Cleaned Data')
    st.dataframe(df)

    csv = df.to_csv(index=False).encode('utf-8')
    download_csv = st.download_button(
        label="Download Cleaned CSV",
        data=csv,
        file_name='cleaned_data.csv',
        mime='text/csv',
            )

    excel_buffer = io.BytesIO()

    df.to_excel(excel_buffer, index=False)
    download_excel = st.download_button(
            label="Download Cleaned Excel",
            data=excel_buffer.getvalue(),
            file_name='cleaned_data.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
    if download_csv or download_excel:
        st.session_state.cleaned_count += 1
        st.success("cleaned file downloded successfully")    
        st.balloons()
        st.rerun()
    
            
else:
    st.info('Please upload a CSV or Excel file to get started.')