from flask import Flask, request, render_template_string
app = Flask(__name__)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Matrix Multiplication</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body { 
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
            padding: 40px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            position: relative;
            overflow-x: hidden;
        }

        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 25% 25%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 75% 75%, rgba(255, 255, 255, 0.05) 0%, transparent 50%);
            pointer-events: none;
            z-index: 1;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 24px;
            padding: 50px;
            box-shadow: 
                0 32px 64px rgba(0, 0, 0, 0.15),
                inset 0 1px 0 rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            position: relative;
            z-index: 2;
        }

        h2 { 
            color: #2d3748; 
            text-align: center;
            font-size: 2.5em;
            font-weight: 700;
            margin-bottom: 40px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }

        form { 
            margin-bottom: 40px; 
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 30px;
        }

        .matrices-container {
            display: flex;
            gap: 60px;
            align-items: center;
            flex-wrap: wrap;
            justify-content: center;
        }

        .multiply-symbol {
            font-size: 3em;
            font-weight: 700;
            color: #667eea;
            text-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
            animation: pulse 2s ease-in-out infinite;
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 0.8; }
            50% { transform: scale(1.1); opacity: 1; }
        }

        input[type="number"] {
            width: 60px;
            height: 60px;
            padding: 8px;
            margin: 6px;
            text-align: center;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            font-size: 1.2em;
            font-weight: 600;
            background: rgba(255, 255, 255, 0.9);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }

        input[type="number"]:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 
                0 0 0 4px rgba(102, 126, 234, 0.1),
                0 4px 16px rgba(102, 126, 234, 0.2);
            transform: translateY(-2px);
            background: white;
        }

        input[type="number"]:hover {
            border-color: #764ba2;
            transform: translateY(-1px);
        }

        .matrix { 
            display: inline-block; 
            margin: 0 20px; 
            padding: 25px;
            background: rgba(255, 255, 255, 0.6);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            position: relative;
        }

        .matrix::before {
            content: '';
            position: absolute;
            top: -1px;
            left: -1px;
            right: -1px;
            bottom: -1px;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.3), rgba(118, 75, 162, 0.3));
            border-radius: 20px;
            z-index: -1;
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .matrix:hover::before {
            opacity: 1;
        }

        .matrix h4 {
            color: #4a5568;
            font-size: 1.3em;
            font-weight: 600;
            margin-bottom: 15px;
            text-align: center;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        table { 
            border-collapse: separate;
            border-spacing: 8px;
            margin: 0 auto;
        }

        td {
            border: 2px solid #667eea;
            padding: 15px;
            min-width: 60px;
            height: 60px;
            text-align: center;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.7));
            border-radius: 12px;
            font-size: 1.3em;
            font-weight: 700;
            color: #2d3748;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        td::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
            transition: left 0.5s ease;
        }

        td:hover::before {
            left: 100%;
        }

        td:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        }

        input[type="submit"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 18px 48px;
            font-size: 1.3em;
            font-weight: 600;
            border-radius: 50px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 12px 32px rgba(102, 126, 234, 0.3);
            position: relative;
            overflow: hidden;
        }

        input[type="submit"]::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        }

        input[type="submit"]:hover::before {
            left: 100%;
        }

        input[type="submit"]:hover {
            transform: translateY(-4px);
            box-shadow: 0 20px 48px rgba(102, 126, 234, 0.4);
        }

        input[type="submit"]:active {
            transform: translateY(-2px);
        }

        h3 {
            color: #2d3748;
            font-size: 1.8em;
            font-weight: 600;
            text-align: center;
            margin: 40px 0 20px 0;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .result-container {
            display: flex;
            justify-content: center;
            margin-top: 30px;
            animation: slideUp 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        }

        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(40px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .matrix-row {
            display: flex;
            justify-content: center;
            gap: 8px;
        }

        @media (max-width: 768px) {
            .container {
                padding: 30px 20px;
                margin: 20px;
            }
            
            .matrices-container {
                flex-direction: column;
                gap: 30px;
            }
            
            .multiply-symbol {
                font-size: 2em;
                transform: rotate(90deg);
            }
            
            h2 {
                font-size: 2em;
            }
            
            input[type="number"] {
                width: 50px;
                height: 50px;
                font-size: 1em;
            }
            
            td {
                min-width: 50px;
                height: 50px;
                font-size: 1.1em;
                padding: 10px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>2x2 Matrix Multiplication</h2>
        <form method="post">
            <div class="matrices-container">
                <div class="matrix">
                    <h4>Matrix A</h4>
                    {% for i in range(2) %}
                        <div class="matrix-row">
                            {% for j in range(2) %}
                                <input type="number" name="a{{i}}{{j}}" required>
                            {% endfor %}
                        </div>
                    {% endfor %}
                </div>
                
                <div class="multiply-symbol">×</div>
                
                <div class="matrix">
                    <h4>Matrix B</h4>
                    {% for i in range(2) %}
                        <div class="matrix-row">
                            {% for j in range(2) %}
                                <input type="number" name="b{{i}}{{j}}" required>
                            {% endfor %}
                        </div>
                    {% endfor %}
                </div>
            </div>
            <input type="submit" value="Multiply">
        </form>
        {% if result %}
            <h3>Result:</h3>
            <div class="result-container">
                <div class="matrix">
                    <h4>A × B</h4>
                    <table>
                        {% for row in result %}
                            <tr>
                                {% for val in row %}
                                    <td>{{ val }}</td>
                                {% endfor %}
                            </tr>
                        {% endfor %}
                    </table>
                </div>
            </div>
        {% endif %}
    </div>
</body>
</html>
'''
@app.route('/', methods=['GET', 'POST'])
def multiply_matrices():
    result = None
    if request.method == 'POST':
        try:
            # Read Matrix A
            matrix_a = [
                [int(request.form['a00']), int(request.form['a01'])],
                [int(request.form['a10']), int(request.form['a11'])]
            ]
            # Read Matrix B
            matrix_b = [
                [int(request.form['b00']), int(request.form['b01'])],
                [int(request.form['b10']), int(request.form['b11'])]
            ]
            # Matrix multiplication logic
            result = [[0, 0], [0, 0]]
            for i in range(2):
                for j in range(2):
                    result[i][j] = matrix_a[i][0] * matrix_b[0][j] + matrix_a[i][1] * matrix_b[1][j]
        except ValueError:
            result = [["Error", "in"], ["input", "!"]]
    return render_template_string(HTML_TEMPLATE, result=result)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
