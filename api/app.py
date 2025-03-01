from flask import Flask, render_template, request, jsonify, session
import random
import os
from werkzeug.middleware.proxy_fix import ProxyFix

# Initialize Flask app with correct static and template folder paths
app = Flask(__name__, 
           static_folder='../static',
           template_folder='../templates')

# Required for Vercel serverless environment
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

@app.route('/', methods=['GET'])
def index():
    try:
        session['number'] = random.randint(1, 100)
        session['attempts'] = 0
        return render_template('index.html')
    except Exception as e:
        return str(e), 500

@app.route('/guess', methods=['POST'])
def guess():
    try:
        user_guess = int(request.form['guess'])
        target_number = session.get('number', random.randint(1, 100))
        session['attempts'] = session.get('attempts', 0) + 1
        
        if user_guess < target_number:
            result = "too_low"
            message = "Too low! Try a higher number."
        elif user_guess > target_number:
            result = "too_high"
            message = "Too high! Try a lower number."
        else:
            result = "correct"
            message = f"Congratulations! You guessed the number in {session['attempts']} attempts!"
        
        return jsonify({
            'result': result,
            'message': message,
            'attempts': session['attempts']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/reset', methods=['POST'])
def reset():
    try:
        session['number'] = random.randint(1, 100)
        session['attempts'] = 0
        return jsonify({'message': 'Game reset successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Catch-all route to handle other paths
@app.route('/<path:path>')
def catch_all(path):
    return render_template('index.html')

# For local development
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)