from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/calculate", methods=["GET"])
def calculate():
    try:
        # Get query parameters
        num1 = float(request.args.get("num1"))
        num2 = float(request.args.get("num2"))
        operation = request.args.get("operation").lower()

        # Perform operation
        if operation == "add":
            result = num1 + num2
        elif operation == "subtract":
            result = num1 - num2
        elif operation == "multiply":
            result = num1 * num2
        elif operation == "divide":
            if num2 == 0:
                return jsonify({"error": "Division by zero is not allowed"}), 400
            result = num1 / num2
        else:
            return jsonify({"error": "Invalid operation. Use add, subtract, multiply, divide"}), 400

        return jsonify({
            "num1": num1,
            "num2": num2,
            "operation": operation,
            "result": result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
