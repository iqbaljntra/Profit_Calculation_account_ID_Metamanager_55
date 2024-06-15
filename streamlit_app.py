import pandas as pd
import streamlit as st

def calculate_profit_from_csv(data):
    try:
        # Clean 'Profit' column (remove spaces and commas)
        data['Profit'] = data['Profit'].str.replace(' ', '').str.replace(',', '').astype(float)
        
        # Extract deposits and withdrawals based on 'Comment' column
        deposits = data[(data['Type'] == 'balance') & (data['Comment'].str.contains('Deposit', na=False))]
        withdrawals = data[(data['Type'] == 'balance') & (data['Comment'].str.contains('Withdrawal', na=False))]

        if deposits.empty or withdrawals.empty():
            return {'error': 'No deposits or withdrawals found in the data'}

        # Summing up the 'Profit' column for deposits and withdrawals
        initial_balance = deposits['Profit'].sum()
        total_withdrawals = withdrawals['Profit'].sum()

        # Calculate the profit
        profit = total_withdrawals - initial_balance

        # Calculate the profit percentage
        if initial_balance != 0:
            profit_percentage = (profit / initial_balance) * 100
        else:
            profit_percentage = 0.0

        return {
            'initial_balance': initial_balance,
            'total_withdrawals': total_withdrawals,
            'profit': profit,
            'profit_percentage': profit_percentage
        }
    except KeyError:
        return {'error': 'Could not find expected columns (e.g., "Profit") in the data'}
    except Exception as e:
        return {'error': f'Error processing data: {str(e)}'}

# Streamlit app
st.title('Profit Calculation from CSV')
st.write("Upload your CSV file to calculate the profit")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file)
        
        # Ensure 'Profit' column is numeric and clean it
        data['Profit'] = data['Profit'].str.replace(' ', '').str.replace(',', '').astype(float)
        
        result = calculate_profit_from_csv(data)
        
        if 'error' in result:
            st.error(result['error'])
        else:
            st.success('Calculation successful')
            st.write(f"Initial Balance: {result['initial_balance']}")
            st.write(f"Total Withdrawals: {result['total_withdrawals']}")
            st.write(f"Profit: {result['profit']}")
            st.write(f"Profit Percentage: {result['profit_percentage']}%")
    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.info('Please upload a CSV file')
