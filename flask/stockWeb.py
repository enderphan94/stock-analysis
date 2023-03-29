from flask import Flask, render_template, request
import subprocess
import json

app = Flask(__name__)
app=Flask(__name__,template_folder='template')

@app.route('/')
def index():
    return render_template('form.html')

def remove_chars(values):
    if isinstance(values, list):
        for i, value in enumerate(values):
            if isinstance(value, str):
                values[i] = value.replace('[','').replace(']','').replace('{','').replace('}','').replace('"','')
    elif isinstance(values, str):
        data_dict[key] = values.replace('[','').replace(']','').replace('{','').replace('}','').replace('"','')

@app.route('/submit', methods=['POST'])
def submit():
    # Get the user input from the form
    user_input = request.form['user_input']
    
    # Call the Python script with the user input as an argument
    cmd = ['python3', 'smain.py','--code', user_input]
    #result = subprocess.check_output(command)
    
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


if __name__ == '__main__':
    app.run(debug=True)