from flask import Flask, render_template_string

app = Flask(__name__)

# HTML template as a string (Design Updated ONLY)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Even Numbers Generator</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(120deg, #74ebd5 0%, #ACB6E5 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .container {
            background: rgba(255, 255, 255, 0.2);
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.18);
            max-width: 600px;
            width: 100%;
            text-align: center;
        }

        h1 {
            color: #fff;
            margin-bottom: 25px;
            font-size: 2.5em;
            font-weight: 600;
        }

        label {
            display: block;
            margin-bottom: 10px;
            color: #fff;
            font-size: 1.1em;
        }

        input[type="number"] {
            padding: 12px 20px;
            border-radius: 10px;
            border: none;
            font-size: 1.2em;
            text-align: center;
            width: 100%;
            max-width: 200px;
            margin-bottom: 20px;
        }

        .btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 12px 25px;
            font-size: 1em;
            border-radius: 30px;
            cursor: pointer;
            transition: 0.3s ease;
            margin: 5px;
        }

        .btn:hover {
            background: #5a67d8;
            transform: translateY(-2px);
        }

        .result {
            margin-top: 30px;
            padding: 20px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            border-left: 5px solid #667eea;
            display: none;
        }

        .result.show {
            display: block;
            animation: fadeIn 0.5s ease-in-out;
        }

        .numbers-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(50px, 1fr));
            gap: 10px;
            margin-top: 15px;
        }

        .number-item {
            background: #667eea;
            color: white;
            padding: 10px;
            border-radius: 10px;
            font-weight: bold;
        }

        .loading {
            color: #333;
            font-style: italic;
            margin-top: 10px;
            display: none;
        }

        .loading.show {
            display: block;
        }

        .error {
            border-left-color: #e74c3c;
            background: rgba(231, 76, 60, 0.1);
            color: #e74c3c;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @media (max-width: 500px) {
            h1 {
                font-size: 2em;
            }

            input[type="number"] {
                max-width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Even Numbers Generator</h1>
        
        <form id="evenForm">
            <label for="numberInput">Enter the count of even numbers:</label>
            <input type="number" id="numberInput" name="n" min="1" max="1000" value="10" required>
            
            <div>
                <button type="submit" class="btn">Generate Numbers</button>
                <button type="button" class="btn" onclick="clearResult()">Clear</button>
            </div>
        </form>

        <div class="loading" id="loading">Generating numbers...</div>
        
        <div class="result" id="result">
            <h3 id="resultTitle"></h3>
            <div class="numbers-grid" id="numbersGrid"></div>
        </div>
    </div>

    <script>
        const form = document.getElementById('evenForm');
        const loading = document.getElementById('loading');
        const result = document.getElementById('result');
        const resultTitle = document.getElementById('resultTitle');
        const numbersGrid = document.getElementById('numbersGrid');

        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const n = parseInt(document.getElementById('numberInput').value);
            if (isNaN(n) || n < 1 || n > 1000) {
                showError('Please enter a valid number between 1 and 1000.');
                return;
            }
            generateEvenNumbers(n);
        });

        function generateEvenNumbers(n) {
            loading.classList.add('show');
            result.classList.remove('show');

            setTimeout(() => {
                try {
                    const evenNumbers = [];
                    for (let i = 1; i <= n; i++) {
                        evenNumbers.push(2 * i);
                    }

                    displayResult(n, evenNumbers);
                } catch (error) {
                    showError('An error occurred while generating numbers.');
                } finally {
                    loading.classList.remove('show');
                }
            }, 300);
        }

        function displayResult(n, numbers) {
            resultTitle.textContent = `The first ${n} even numbers are:`;
            numbersGrid.innerHTML = '';
            numbers.forEach((num, index) => {
                const numElement = document.createElement('div');
                numElement.className = 'number-item';
                numElement.textContent = num;
                numElement.style.animationDelay = `${index * 0.05}s`;
                numbersGrid.appendChild(numElement);
            });

            result.className = 'result show';
        }

        function showError(message) {
            resultTitle.textContent = 'Error';
            numbersGrid.innerHTML = `<div style="grid-column: 1 / -1; font-weight: 500;">${message}</div>`;
            result.className = 'result show error';
            loading.classList.remove('show');
        }

        function clearResult() {
            result.classList.remove('show');
            document.getElementById('numberInput').value = '10';
            document.getElementById('numberInput').focus();
        }

        document.getElementById('numberInput').focus();
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/health')
def health_check():
    return {"status": "healthy"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
