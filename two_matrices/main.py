from flask import Flask, render_template_string, request
import numpy as np

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<title>Matrix Multiplication</title>
<h2>Matrix Multiplication App</h2>
<form method="POST">
  <label for="matrix1">Matrix 1 (rows separated by newline, elements by space):</label><br>
  <textarea name="matrix1" rows="5" cols="40">{{ matrix1 }}</textarea><br><br>

  <label for="matrix2">Matrix 2 (rows separated by newline, elements by space):</label><br>
  <textarea name="matrix2" rows="5" cols="40">{{ matrix2 }}</textarea><br><br>

  <input type="submit" value="Multiply">
</form>

{% if result %}
<h3>Result:</h3>
<pre>{{ result }}</pre>
{% elif error %}
<h3 style="color:red;">Error:</h3>
<pre>{{ error }}</pre>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def multiply():
    result = ""
    error = ""
    matrix1 = ""
    matrix2 = ""

    if request.method == "POST":
        matrix1 = request.form["matrix1"]
        matrix2 = request.form["matrix2"]

        try:
            mat1 = np.array([[float(num) for num in row.split()] for row in matrix1.strip().split('\n')])
            mat2 = np.array([[float(num) for num in row.split()] for row in matrix2.strip().split('\n')])

            if mat1.shape[1] != mat2.shape[0]:
                raise ValueError("Number of columns in Matrix 1 must equal number of rows in Matrix 2.")

            product = np.dot(mat1, mat2)
            result = "\n".join(" ".join(f"{num:.2f}" for num in row) for row in product)

        except Exception as e:
            error = str(e)

    return render_template_string(HTML_TEMPLATE, result=result, error=error, matrix1=matrix1, matrix2=matrix2)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
