from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """<your HTML code from earlier here>"""

@app.route('/', methods=['GET', 'POST'])
def index():
    size = int(request.values.get('size', 2))
    matrix_a = [[0 for _ in range(size)] for _ in range(size)]
    matrix_b = [[0 for _ in range(size)] for _ in range(size)]
    result = None
    error = None

    if request.method == 'POST':
        try:
            # Populate matrices from form
            for i in range(size):
                for j in range(size):
                    matrix_a[i][j] = int(request.form.get(f'a{i}{j}', 0))
                    matrix_b[i][j] = int(request.form.get(f'b{i}{j}', 0))

            # Perform matrix multiplication
            result = [[sum(matrix_a[i][k] * matrix_b[k][j] for k in range(size)) for j in range(size)] for i in range(size)]

        except ValueError:
            error = "Please enter valid integer values only."

    return render_template_string(HTML_TEMPLATE, size=size, matrix_a=matrix_a, matrix_b=matrix_b, result=result, error=error)

if __name__ == '__main__':
    app.run(debug=True)
