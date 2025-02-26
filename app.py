from flask import Flask, render_template, request
import statistics
import re

app = Flask(__name__)

def calculate_statistics(numbers):
    try:
        numbers = [float(num.strip()) for num in numbers.split(',')]
        if not numbers:
            return None, "Error: Empty list."

        mean = statistics.mean(numbers)
        mode = statistics.mode(numbers)
        range_val = max(numbers) - min(numbers)
        stdev = statistics.stdev(numbers)

        return {
            'numbers': numbers,
            'mean': mean,
            'mode': mode,
            'range': range_val,
            'stdev': stdev
        }, None

    except (ValueError, statistics.StatisticsError) as e:
        return None, f"Error: Could not parse numbers. {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        numbers_str = request.form.get('numbers')
        if numbers_str:
            stats, error = calculate_statistics(numbers_str)
            if stats:
                return render_template('results.html', stats=stats)
            else:
                return render_template('index.html', error=error)
        else:
            return render_template('index.html', error="Error: Please enter numbers.")

    return render_template('index.html', error=None)

@app.route('/results')
def results():
    return "This page is only accessible after form submission."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)











