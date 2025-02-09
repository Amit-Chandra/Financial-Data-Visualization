import pandas as pd
import plotly.express as px
from flask import Flask, request, render_template
import base64
from io import BytesIO
import openpyxl

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template('upload.html', error="No file selected!")

    file = request.files['file']
    if file.filename == '':
        return render_template('upload.html', error="No file uploaded!")

    try:
        df = pd.read_excel(file)
        df['Buy Date'] = pd.to_datetime(df['Buy Date'])
        df['Sell Date'] = pd.to_datetime(df['Sell Date'])
        df['Profit/Loss'] = df['Sell Value'] - df['Buy Value']
        df['Month'] = df['Buy Date'].dt.to_period('M')
        monthly_pl = df.groupby('Month')['Profit/Loss'].sum().reset_index()
        monthly_pl['Month'] = monthly_pl['Month'].astype(str)  # Convert Period to String for Plotly
        
        # Create interactive Plotly graph
        fig = px.bar(
            monthly_pl, 
            x='Month', 
            y='Profit/Loss', 
            color='Profit/Loss',
            color_continuous_scale=['red', 'green'],
            title='Realized Profit and Loss by Month',
            labels={'Profit/Loss': 'Profit or Loss (₹)', 'Month': 'Month'},
            template='plotly_dark'
        )
        fig.update_layout(xaxis_tickangle=-45)

        # Convert Plotly graph to HTML
        plot_html = fig.to_html(full_html=False)

        # Calculate summary statistics
        total_profit = df['Profit/Loss'].sum()
        best_month = monthly_pl.loc[monthly_pl['Profit/Loss'].idxmax()]
        worst_month = monthly_pl.loc[monthly_pl['Profit/Loss'].idxmin()]

        return render_template(
            'plot.html', 
            plot_html=plot_html,
            total_profit=total_profit,
            best_month=best_month['Month'],
            best_month_profit=best_month['Profit/Loss'],
            worst_month=worst_month['Month'],
            worst_month_loss=worst_month['Profit/Loss']
        )

    except Exception as e:
        return render_template('upload.html', error=f"Error processing file: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)






















































# ============================================ Last Working =================================================


# import pandas as pd
# import matplotlib.pyplot as plt
# from flask import Flask, request, render_template
# from io import BytesIO
# import base64
# import openpyxl


# app = Flask(__name__)

# @app.route('/', methods=['GET'])
# def index():
#     return render_template('upload.html')

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if request.method == 'POST':
#         file = request.files['file']
#         if file:
#             df = pd.read_excel(file)
#             print(df.columns)
#             plot = create_plot(df)
#             plot_bytes = BytesIO()
#             plt.savefig(plot_bytes, format='png')
#             plot_bytes.seek(0)
#             plot_base64 = base64.b64encode(plot_bytes.read()).decode('utf-8')
            
#             return render_template('plot.html', plot_base64=plot_base64)
#     return render_template('upload.html')

# def create_plot(df):
#     df['Buy Date'] = pd.to_datetime(df['Buy Date'])
#     df['Sell Date'] = pd.to_datetime(df['Sell Date'])
#     df['Profit/Loss'] = df['Sell Value'] - df['Buy Value']
#     df['Month'] = df['Buy Date'].dt.to_period('M')
#     monthly_pl = df.groupby('Month')['Profit/Loss'].sum()
#     colors = []
#     for pl in monthly_pl:
#         if pl >= 0:
#             colors.append('skyblue')
#         else:
#             colors.append('red')

#     plt.figure(figsize=(10, 6))
#     monthly_pl.plot(kind='bar', color=colors, width=0.2)
#     plt.title('Realized Profit and Loss by Month')
#     plt.xlabel('Month')
#     plt.ylabel('Profit/Loss')
#     plt.xticks(rotation=45)
#     plt.grid(axis='y', linestyle='--', alpha=0.7)
#     plt.tight_layout()

# if __name__ == '__main__':
#     app.run(debug=True)


# =================================================================================================================