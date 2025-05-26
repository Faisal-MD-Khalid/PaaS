from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nth Largest Number Finder</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #0a0b0d;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
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
                radial-gradient(circle at 20% 20%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 40% 60%, rgba(30, 144, 255, 0.2) 0%, transparent 50%);
            animation: float 8s ease-in-out infinite;
            z-index: -1;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(1deg); }
        }

        .container {
            background: rgba(18, 20, 23, 0.95);
            padding: 60px;
            border-radius: 32px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 
                0 32px 64px rgba(0, 0, 0, 0.4),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px) saturate(180%);
            max-width: 800px;
            width: 100%;
            text-align: center;
            position: relative;
        }

        .container::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            border-radius: 32px;
            padding: 1px;
            background: linear-gradient(135deg, 
                rgba(120, 119, 198, 0.4) 0%, 
                rgba(255, 119, 198, 0.4) 50%, 
                rgba(30, 144, 255, 0.4) 100%);
            mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            mask-composite: exclude;
            z-index: -1;
        }

        h1 {
            color: #ffffff;
            margin-bottom: 12px;
            font-size: 3.5em;
            font-weight: 700;
            background: linear-gradient(135deg, #7877c6, #ff77c6, #1e90ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -0.02em;
            text-shadow: 0 0 40px rgba(120, 119, 198, 0.5);
        }

        .subtitle {
            color: #a1a1aa;
            font-size: 1.2em;
            margin-bottom: 50px;
            font-weight: 400;
            opacity: 0.9;
        }

        form {
            position: relative;
        }

        .input-group {
            margin-bottom: 32px;
            text-align: left;
        }

        label {
            display: block;
            margin-bottom: 12px;
            color: #e4e4e7;
            font-size: 1.1em;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-size: 0.9em;
        }

        input[type="text"], input[type="number"] {
            width: 100%;
            padding: 20px 24px;
            font-size: 1.1em;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            background: rgba(255, 255, 255, 0.05);
            color: #ffffff;
            backdrop-filter: blur(10px);
        }

        input[type="text"]::placeholder, input[type="number"]::placeholder {
            color: #71717a;
        }

        input[type="text"]:focus, input[type="number"]:focus {
            outline: none;
            border-color: rgba(120, 119, 198, 0.8);
            background: rgba(255, 255, 255, 0.08);
            box-shadow: 
                0 0 0 4px rgba(120, 119, 198, 0.1),
                0 8px 32px rgba(120, 119, 198, 0.2);
            transform: translateY(-2px);
        }

        .form-row {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 24px;
            align-items: end;
        }

        .btn {
            background: linear-gradient(135deg, #7877c6 0%, #ff77c6 50%, #1e90ff 100%);
            color: white;
            border: none;
            padding: 20px 48px;
            font-size: 1.2em;
            border-radius: 16px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 
                0 12px 32px rgba(120, 119, 198, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.2);
            position: relative;
            overflow: hidden;
        }

        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, 
                transparent, 
                rgba(255, 255, 255, 0.2), 
                transparent);
            transition: left 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .btn:hover::before {
            left: 100%;
        }

        .btn:hover {
            transform: translateY(-4px);
            box-shadow: 
                0 20px 48px rgba(120, 119, 198, 0.4),
                inset 0 1px 0 rgba(255, 255, 255, 0.3);
        }

        .btn:active {
            transform: translateY(-2px);
        }

        .result {
            margin-top: 48px;
            padding: 32px;
            border-radius: 20px;
            position: relative;
            animation: slideUp 0.6s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
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

        .result.success {
            background: rgba(34, 197, 94, 0.1);
            border-color: rgba(34, 197, 94, 0.3);
            color: #bbf7d0;
        }

        .result.error {
            background: rgba(239, 68, 68, 0.1);
            border-color: rgba(239, 68, 68, 0.3);
            color: #fecaca;
        }

        .result h3 {
            font-size: 1.6em;
            margin-bottom: 16px;
            font-weight: 700;
        }

        .result-value {
            font-size: 3.2em;
            font-weight: 800;
            text-shadow: 0 0 20px currentColor;
            margin: 16px 0;
        }

        .numbers-display {
            margin-top: 24px;
            padding: 20px;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 16px;
            font-size: 0.95em;
            color: #a1a1aa;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }

        .sorted-numbers {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            justify-content: center;
            margin-top: 16px;
        }

        .number-item {
            background: rgba(120, 119, 198, 0.2);
            color: #e4e4e7;
            padding: 8px 16px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 0.95em;
            border: 1px solid rgba(120, 119, 198, 0.3);
            backdrop-filter: blur(5px);
        }

        .number-item.highlight {
            background: rgba(34, 197, 94, 0.3);
            border-color: rgba(34, 197, 94, 0.5);
            color: #bbf7d0;
            transform: scale(1.1);
            animation: pulse 0.6s ease;
            box-shadow: 0 4px 20px rgba(34, 197, 94, 0.3);
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1.1); }
            50% { transform: scale(1.15); }
        }

        .placeholder-text {
            color: #71717a;
            font-style: italic;
        }

        @media (max-width: 600px) {
            .container {
                padding: 40px 24px;
                margin: 10px;
            }
            
            h1 {
                font-size: 2.8em;
            }
            
            .form-row {
                grid-template-columns: 1fr;
                gap: 24px;
            }
            
            .result-value {
                font-size: 2.4em;
            }
        }

        .info-box {
            background: rgba(30, 144, 255, 0.1);
            border-left: 4px solid #1e90ff;
            border-radius: 12px;
            padding: 20px;
            margin: 24px 0;
            color: #93c5fd;
            font-size: 0.95em;
            text-align: left;
            backdrop-filter: blur(5px);
            border: 1px solid rgba(30, 144, 255, 0.2);
        }

        .info-box strong {
            color: #dbeafe;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Nth Largest Finder</h1>
        <p class="subtitle">Discover the Nth largest number from your dataset</p>
        
        <div class="info-box">
            <strong>How it works:</strong> Enter numbers separated by commas, specify which largest number you want (1st, 2nd, 3rd, etc.), and we'll find it for you!
        </div>
        
        <form method="POST">
            <div class="form-row">
                <div class="input-group">
                    <label for="numbers">📊 Enter Numbers:</label>
                    <input type="text" 
                           id="numbers" 
                           name="numbers" 
                           placeholder="e.g., 45, 23, 78, 12, 89, 34, 67" 
                           value="{{ request.form.numbers if request.form.numbers else '' }}"
                           required>
                </div>
                
                <div class="input-group">
                    <label for="n">🎯 Find Nth Largest:</label>
                    <input type="number" 
                           id="n" 
                           name="n" 
                           min="1" 
                           placeholder="e.g., 3"
                           value="{{ request.form.n if request.form.n else '' }}"
                           required>
                </div>
            </div>
            
            <button type="submit" class="btn">Find Number</button>
        </form>

        {% if result is not none %}
            <div class="result {{ 'success' if result != 'Error' and 'Error' not in result|string else 'error' }}">
                {% if 'Error' in result|string %}
                    <h3>❌ Error Occurred</h3>
                    <p>{{ result }}</p>
                {% elif result == "N is too large" %}
                    <h3>⚠️ Invalid Input</h3>
                    <p>The value of N ({{ n }}) is larger than the number of elements provided.</p>
                {% else %}
                    <h3>✅ Result Found!</h3>
                    <p>The <strong>{{ n }}{{ 'st' if n == 1 else 'nd' if n == 2 else 'rd' if n == 3 else 'th' }}</strong> largest number is:</p>
                    <div class="result-value">{{ result }}</div>
                    
                    {% if sorted_numbers %}
                        <div class="numbers-display">
                            <p><strong>Numbers sorted in descending order:</strong></p>
                            <div class="sorted-numbers">
                                {% for num in sorted_numbers %}
                                    <span class="number-item {{ 'highlight' if loop.index == n else '' }}">{{ num }}</span>
                                {% endfor %}
                            </div>
                        </div>
                    {% endif %}
                {% endif %}
            </div>
        {% endif %}
    </div>

    <script>
        // Add some interactive effects
        document.addEventListener('DOMContentLoaded', function() {
            const inputs = document.querySelectorAll('input');
            inputs.forEach(input => {
                input.addEventListener('focus', function() {
                    this.parentElement.style.transform = 'scale(1.02)';
                });
                
                input.addEventListener('blur', function() {
                    this.parentElement.style.transform = 'scale(1)';
                });
            });

            // Auto-focus on first input
            document.getElementById('numbers').focus();
        });
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    n = None
    sorted_numbers = None
    
    if request.method == 'POST':
        numbers = request.form['numbers']
        n = int(request.form['n'])
        
        try:
            # Parse and validate numbers
            num_list = [int(x.strip()) for x in numbers.split(',') if x.strip()]
            
            if not num_list:
                result = "Error: Please enter at least one valid number"
            elif n > len(num_list):
                result = "N is too large"
            else:
                # Sort in descending order and find nth largest
                sorted_list = sorted(num_list, reverse=True)
                result = sorted_list[n-1]
                sorted_numbers = sorted_list
                
        except ValueError:
            result = "Error: Please enter valid numbers separated by commas"
        except Exception as e:
            result = f"Error: {str(e)}"
    
    return render_template_string(HTML_TEMPLATE, 
                                result=result, 
                                n=n, 
                                sorted_numbers=sorted_numbers,
                                request=request)

@app.route('/health')
def health_check():
    return {"status": "healthy"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
