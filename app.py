import streamlit as st
import pandas as pd

st.set_page_config(page_title='Intelligent Text-to-SQL Agent | Demo', page_icon='🗄️', layout='wide')
st.title('🗄️ Intelligent Text-to-SQL Agent')
st.caption('Interactive concept demo • HR database • Simulated SQL and results (not connected to a real LLM or database)')

examples = {
    'How many employees work in each department?': (
        '''SELECT d.department_name, COUNT(e.employee_id) AS employee_count\nFROM departments d\nLEFT JOIN employees e ON e.department_id = d.department_id\nGROUP BY d.department_id, d.department_name;''',
        pd.DataFrame({'Department': ['IT', 'Human Resources', 'Finance', 'Operations'], 'Employee count': [18, 12, 9, 26]}),
        'bar',
    ),
    'Which employees earn more than SAR 10,000?': (
        '''SELECT employee_name, salary\nFROM employees\nWHERE salary > 10000\nORDER BY salary DESC;''',
        pd.DataFrame({'Employee': ['Ahmed', 'Khalid', 'Mohammed'], 'Salary (SAR)': [15000, 13500, 11000]}),
        'table',
    ),
    'How many employees have approved leave?': (
        '''SELECT COUNT(DISTINCT employee_id) AS approved_employees\nFROM leaves\nWHERE status = 'Approved';''',
        pd.DataFrame({'Approved employees': [8]}),
        'metric',
    ),
}

with st.sidebar:
    st.header('Demo database')
    st.success('HR_Database.db (simulated)')
    st.write('**Discovered tables**')
    st.code('employees\ndepartments\nsalaries\nleaves', language='text')
    st.info('This prototype uses fixed example responses. Schema discovery, fine-tuning, safe SQL execution and evaluation are planned for the final project.')

st.subheader('Ask your database')
selected = st.selectbox('Choose a sample question', list(examples))
question = st.text_input('Natural-language question', value=selected)

if st.button('Generate SQL & show results', type='primary', use_container_width=True):
    if question.strip() not in examples:
        st.warning('This concept demo supports the three sample questions above. The finished agent will handle new questions.')
    else:
        sql, df, kind = examples[question.strip()]
        st.success('Simulated read-only query completed')
        result_tab, sql_tab, chart_tab = st.tabs(['📋 Results', '🧾 Generated SQL', '📊 Chart'])
        with result_tab:
            st.dataframe(df, hide_index=True, use_container_width=True)
        with sql_tab:
            st.code(sql, language='sql')
        with chart_tab:
            if kind == 'bar':
                st.bar_chart(df.set_index('Department'))
            elif kind == 'metric':
                st.metric('Employees with approved leave', int(df.iloc[0, 0]))
            else:
                st.info('A table is more suitable for this result.')
        st.caption('All data, SQL responses and counts are illustrative. No real database queries are executed.')

st.divider()
st.subheader('Planned full system')
st.markdown('**Question → Schema discovery → Fine-tuned LLM → SQL validation (SELECT only) → SQLite execution → Results / chart**')
st.caption('Academic project proposal discussion demo — not a trained or deployed AI system.')
