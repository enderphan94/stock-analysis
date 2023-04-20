from flask import Flask, render_template, request
import subprocess
import json

app = Flask(__name__)
app=Flask(__name__,template_folder='template')


@app.route('/')
def index():
    years_from = ["2013","2014","2015","2016","2017","2018","2019","2020","2021","2022"]
    years_to = ["2013","2014","2015","2016","2017","2018","2019","2020","2021","2022"]
    return render_template('index.html', years_from=years_from, years_to=years_to)

def remove_chars(values):
    if isinstance(values, list):
        for i, value in enumerate(values):
            if isinstance(value, str):
                values[i] = value.replace('[','').replace(']','').replace('{','').replace('}','').replace('"','')
    elif isinstance(values, str):
        data_dict[key] = values.replace('[','').replace(']','').replace('{','').replace('}','').replace('"','')

@app.route('/submit', methods=['POST'])
def submit():
    user_input = None
    user_input_simple = None

    if request.method == 'POST':
        if 'user_input' in request.form:
            user_input = request.form['user_input']
        elif 'user_input_simple' in request.form:
            user_input_simple = request.form['user_input_simple']

    fromYear = "2017" #request.form['years_from']
    toYear = "2022" #request.form['years_to']
    
    # Periods:
    
    growth_values = []
    types=""
    cmd =""
    if user_input is not None:
        types="advanced"
        for i in range(1, 11):
            print(i)
            year = request.form.get(f'year{i}')
            print(f'year{i}: {year}')
            if year:
                growth_values.append(year)

        growth_str = ','.join(growth_values)
        cmd = ['python3', 'getData.py','--code', user_input,'--type',types,'--fr',fromYear,'--to',toYear,'--growth',growth_str]

        print(growth_values)

    # Call the Python script with the user input as an argument
    
    # Display the result to the user
    
        data = subprocess.check_output(cmd).decode('utf-8')
        #print(data)
        data_dict = json.loads(data.replace("'", "\""))
        headers = list(data_dict.keys())
        rows = []

        # for key, value in data_dict.items():
        #     rows.append([key, value])
        for key, value in data_dict.items():
            if isinstance(value, list) and isinstance(value[0], list):
                # If the value is a nested list, flatten it and convert each element to a string
                flattened_value = [str(item) for sublist in value for item in sublist]
                value_str = ', '.join(flattened_value)
                value_str = str(value).strip('[{]}\'"')
                value_str = value_str.replace("'","")
            else:
            # If the value is not a nested list, convert it to a string and remove the brackets, braces, and quotes
                value_str = str(value).strip('[{]}\'"')

            # Append the key and the value string to the rows list
            rows.append([key, value_str])   
        return render_template('result.html', code=user_input, rows=rows)

    elif user_input_simple is not None:
        simpleYear = request.form['5years']

        types="simple"
        growth_values.append(simpleYear)
        growth_values.append(simpleYear)
        growth_values.append(simpleYear)
        growth_values.append(simpleYear)
        growth_values.append(simpleYear)
        growth_values.append(simpleYear)
        growth_values.append(simpleYear)
        growth_values.append(simpleYear)
        growth_values.append(simpleYear)
        growth_values.append(simpleYear)
        growth_str = ','.join(growth_values)
        cmd = ['python3', 'getData.py','--code', user_input_simple,'--type',types,'--fr',fromYear,'--to',toYear,'--growth',growth_str]

        data = subprocess.check_output(cmd).decode('utf-8')
        #print(data)
        data_dict = json.loads(data.replace("'", "\""))
        headers = list(data_dict.keys())
        rows = []

        # for key, value in data_dict.items():
        #     rows.append([key, value])
        for key, value in data_dict.items():
            if isinstance(value, list) and isinstance(value[0], list):
                # If the value is a nested list, flatten it and convert each element to a string
                flattened_value = [str(item) for sublist in value for item in sublist]
                value_str = ', '.join(flattened_value)
                value_str = str(value).strip('[{]}\'"')
                value_str = value_str.replace("'","")
            else:
            # If the value is not a nested list, convert it to a string and remove the brackets, braces, and quotes
                value_str = str(value).strip('[{]}\'"')

            # Append the key and the value string to the rows list
            rows.append([key, value_str])   
        return render_template('result.html', code=user_input_simple, rows=rows)

    


if __name__ == '__main__':
    app.run(debug=True)