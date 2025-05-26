HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Even Numbers Generator</title>
    <style>
        :root {
            --primary: #667eea;
            --secondary: #764ba2;
            --background: #f4f7fa;
            --white: #fff;
            --text-dark: #2c3e50;
            --text-light: #7f8c8d;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: var(--background);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .container {
            background: var(--white);
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.07);
            max-width: 600px;
            width: 100%;
            text-align: center;
            border: 1px solid #e0e0e0;
        }

        h1 {
            font-size: 2.3em;
            font-weight: 600;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 25px;
        }

        label {
            font-size: 1.1em;
            font-weight: 500;
            color: var(--text-dark);
            display: block;
            margin-bottom: 10px;
        }

        input[type="number"] {
            width: 100%;
            max-width: 250px;
            padding: 12px 16px;
            font-size: 1.1em;
            border-radius: 10px;
            border: 2px solid #ccc;
            transition: 0.3s ease;
        }

        input[type="number"]:focus {
            border-color: var(--primary);
            box-shadow: 0 0 10px rgba(102, 126, 234, 0.2);
            outline: none;
        }

        .btn {
            display: inline-block;
            margin: 10px 8px;
            padding: 12px 25px;
            font-size: 1em;
            border-radius: 30px;
            border: none;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            cursor: pointer;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }

        .result {
            margin-top: 30px;
            padding: 20px;
            background: #eef2f7;
            border-radius: 12px;
            border-left: 4px solid var(--primary);
            display: none;
            text-align: left;
        }

        .result.show {
            display: block;
            animation: fadeInUp 0.4s ease-out;
        }

        .result h3 {
            color: var(--text-dark);
            margin-bottom: 15px;
        }

        .numbers-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(50px, 1fr));
            gap: 10px;
        }

        .number-item {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            font-weight: 600;
            border-radius: 8px;
            padding: 10px;
            text-align: center;
            transition: transform 0.3s ease;
        }

        .number-item:hover {
            transform: scale(1.1);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }

        .error {
            background: #ffe5e5;
            color: #c0392b;
            border-left: 4px solid #e74c3c;
        }

        .loading {
            margin-top: 15px;
            color: var(--primary);
            font-style: italic;
            display: none;
        }

        .loading.show {
            display: block;
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @media (max-width: 480px) {
            .container {
                padding: 25px;
            }

            h1 {
                font-size: 1.8em;
            }

            input[type="number"] {
                max-width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>✨ Even Numbers Generator</h1>
        <form id="evenForm">
            <label for="numberInput">Enter number of even numbers:</label>
            <input type="number" id="numberInput" name="n" min="1" max="1000" value="10" required>
            <div>
                <button type="submit" class="btn">Generate</button>
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
                    for (let i = 1; i <= n; i++) evenNumbers.push(2 * i);
                    displayResult(n, evenNumbers);
                } catch {
                    showError('An error occurred while generating numbers.');
                } finally {
                    loading.classList.remove('show');
                }
            }, 300);
        }

        function displayResult(n, numbers) {
            resultTitle.textContent = `First ${n} even numbers:`;
            numbersGrid.innerHTML = '';
            numbers.forEach((num, i) => {
                const el = document.createElement('div');
                el.className = 'number-item';
                el.textContent = num;
                el.style.animationDelay = `${i * 0.03}s`;
                numbersGrid.appendChild(el);
            });
            result.className = 'result show';
        }

        function showError(message) {
            resultTitle.textContent = 'Error';
            numbersGrid.innerHTML = `<div style="grid-column: 1 / -1;">${message}</div>`;
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

