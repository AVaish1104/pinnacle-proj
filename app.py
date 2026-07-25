from flask import Flask, request, render_template_string

app = Flask(__name__)

CALCULATOR_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Basic Calculator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f4f7fb;
            color: #333;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
        }
        .calculator {
            width: 360px;
            padding: 24px;
            border-radius: 16px;
            background: white;
            box-shadow: 0 20px 35px rgba(0, 0, 0, 0.08);
        }
        h1 {
            margin: 0 0 16px;
            font-size: 1.8rem;
            text-align: center;
        }
        label {
            display: block;
            margin: 12px 0 6px;
            font-weight: 600;
        }
        input, select {
            width: 100%;
            padding: 12px 14px;
            border: 1px solid #ccd6dd;
            border-radius: 10px;
            font-size: 1rem;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            margin-top: 18px;
            padding: 12px 14px;
            border: none;
            border-radius: 10px;
            font-size: 1rem;
            cursor: pointer;
            background: #4b82ff;
            color: white;
        }
        .result {
            margin-top: 18px;
            padding: 14px;
            background: #eef3ff;
            border-radius: 10px;
            font-size: 1.1rem;
            text-align: center;
        }
        .error {
            color: #b00020;
        }I
    </style>
</head>
<body>
    <div class="calculator">
        <h1>Basic Calculator</h1>
        <form method="post">
            <label for="first">First number</label>
            <input id="first" name="first" type="text" value="{{ first }}" placeholder="Enter a number" required>

            <label for="second">Second number</label>
            <input id="second" name="second" type="text" value="{{ second }}" placeholder="Enter a number" required>

            <label for="operation">Operation</label>
            <select id="operation" name="operation">
                <option value="add"{{ ' selected' if operation == 'add' else '' }}>Add (+)</option>
                <option value="subtract"{{ ' selected' if operation == 'subtract' else '' }}>Subtract (-)</option>
                <option value="multiply"{{ ' selected' if operation == 'multiply' else '' }}>Multiply (&times;)</option>
                <option value="divide"{{ ' selected' if operation == 'divide' else '' }}>Divide (&divide;)</option>
            </select>

            <button type="submit">Calculate</button>
        </form>
        {{ message_block|safe }}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    first = ''
    second = ''
    operation = 'add'
    message_block = ''

    if request.method == 'POST':
        first = request.form.get('first', '').strip()
        second = request.form.get('second', '').strip()
        operation = request.form.get('operation', 'add')

        try:
            value1 = float(first)
            value2 = float(second)

            if operation == 'add':
                result = value1 + value2
                symbol = '+'
            elif operation == 'subtract':
                result = value1 - value2
                symbol = '-'
            elif operation == 'multiply':
                result = value1 * value2
                symbol = '×'
            elif operation == 'divide':
                if value2 == 0:
                    raise ZeroDivisionError('Cannot divide by zero')
                result = value1 / value2
                symbol = '÷'
            else:
                raise ValueError('Unknown operation')

            message_block = f"<div class='result'>Result: {value1} {symbol} {value2} = {result}</div>"
        except ValueError:
            message_block = "<div class='result error'>Please enter valid numbers and select an operation.</div>"
        except ZeroDivisionError:
            message_block = "<div class='result error'>Cannot divide by zero. Please enter a different second number.</div>"

    return render_template_string(
        CALCULATOR_PAGE,
        first=first,
        second=second,
        operation=operation,
        message_block=message_block,
    )

if __name__ == '__main__':
    app.run(debug=True)
