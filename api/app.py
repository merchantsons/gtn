from flask import Flask, render_template, request, jsonify, session
import random
import os

app = Flask(__name__,
            static_folder='../static',  # Relative to api/
            template_folder='../templates')  # Relative to api/
app.secret_key = os.urandom(24)

@app.route('/', methods=['GET'])
def index():
    session['number'] = random.randint(1, 100)
    session['attempts'] = 0
    return render_template('index.html')

@app.route('/guess', methods=['POST'])
def guess():
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

@app.route('/reset', methods=['POST'])
def reset():
    session['number'] = random.randint(1, 100)
    session['attempts'] = 0
    return jsonify({'message': 'Game reset successfully!'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

# Create HTML template
with open('templates/index.html', 'w') as f:
    f.write('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Guess the Number Game</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <link rel="icon" type="image/x-icon" href="{{ url_for('static', filename='favicon.ico') }}">
 <style>
        :root {
            --primary-color: #384155;
            --secondary-color: #384155;
            --background-color: #384155;
            --text-color: #384155;
            --accent-color: #2e502e;
            --error-color: #884147;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Poppins', sans-serif;
        }
        
        body {
            background-color: var(--background-color);
            color: var(--text-color);
            height: 85vh;
            display: flex;
            justify-content: center;
            align-items: center;
            transition: background-color 0.3s ease;
        }
        
        .container {
            background-color: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            padding: 2rem;
            width: 90%;
            justify-self: center;
            max-width: 600px;
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .container:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
        }
        
        h1 {
            color: var(--primary-color);
            margin-bottom: 1rem;
            font-weight: 600;
        }
            
        .head1 {
            color: #fff;            
            font-weight: 600;
            text-align: center;
            font-size: 3vmin;
            text-decoration: underline;
            text-decoration-thickness: .5px;
        }
            
        .head2 {
            color: #fff;
            margin-top: -.6vmin;
            text-align: center;
            margin-bottom: 1rem;
            font-weight: 300;
            font-size: 2vmin;
        }
            
        .footer {
            color: #fff;
            text-align: center;
            font-size: 1.5vmin;
            margin-top: 2rem;
        }
        
        .instructions {
            margin-top: -1.6rem;
            margin-bottom: 1rem;
            color: #666;
            font-size: 1.8vmin;
        }
        
        #gameSection {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        .input-group {
            display: flex;
            margin-bottom: 1.5rem;
            width: 100%;
        }
        
        input {
            flex: 1;
            padding: 0.75rem;
            border: 2px solid #ddd;
            border-radius: 8px 0 0 8px;
            font-size: 1rem;
            transition: border-color 0.3s ease;
        }
        
        input:focus {
            outline: none;
            border-color: var(--primary-color);
        }
        
        button {
            background-color: var(--primary-color);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 600;
            transition: background-color 0.3s ease, transform 0.2s ease;
        }
        
        .input-group button {
            border-radius: 0 8px 8px 0;
        }
        
        button:hover {
            background-color: #445538;
            transform: scale(1.05);
        }
        
        button:active {
            transform: scale(0.95);
        }
        
        #reset {
            background-color: var(--secondary-color);
            margin-top: 1rem;
        }
        
        #reset:hover {
            background-color: #445538;
        }
        
        #message {
            margin: 1.5rem 0;
            padding: 1rem;
            border-radius: 8px;
            background-color: #f0f0f0;
            display: none;
            animation: fadeIn 0.5s ease;
        }
        
        #message.correct {
            background-color: rgba(50, 205, 50, 0.2);
            color: var(--accent-color);
        }
        
        #message.too_high {
            background-color: rgba(255, 71, 87, 0.2);
            color: var(--error-color);
        }
        
        #message.too_low {
            background-color: rgba(255, 165, 0, 0.2);
            color: #ffa500;
        }
        
        .attempts {
            margin-top: 1rem;
            font-weight: 600;
            color: var(--primary-color);
        }
        
        .progress-container {
            width: 100%;
            background-color: #ddd;
            border-radius: 10px;
            margin: 1.5rem 0;
            height: 10px;
            overflow: hidden;
        }
        
        .progress-bar {
            height: 100%;
            background-color: var(--primary-color);
            width: 0;
            transition: width 0.5s ease;
            border-radius: 10px;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes celebrate {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }
        
        .celebrate {
            animation: celebrate 0.5s ease-in-out;
        }
        
        @media (max-width: 480px) {
            .container {
                padding: 1.5rem;
            }
            
            h1 {
                font-size: 1.5rem;
            }
            
            .instructions {
                font-size: 0.9rem;
            }
            
            input, button {
                font-size: 0.9rem;
                padding: 0.6rem;
            }
        }
    </style>
</head>
<body>
 <div>
    <div style="display: flex; justify-content: center;"><img src="/static/logo.gif" width="200v" height="210" alt="GIAIC LOGO" style="display: block;"></div>
    <div class="head1">PROJECT 2: GUESS THE NUMBER GAME PYTHON PROJECT</div>
    <div class="head2">FOR GIAIC Q3 - ROLL # 00037391 BY MERCHANTSONS</div>
    <div class="container">
        <h1>Guess the Number</h1>
        <p class="instructions">I'm thinking of a number between 1 and 100. Can you guess it?</p>
        
        <div id="gameSection">
            <div class="progress-container">
                <div class="progress-bar" id="progressBar"></div>
            </div>
            
            <div class="input-group">
                <input type="number" id="guessInput" min="1" max="100" placeholder="Enter your guess">
                <button id="guessButton">Guess</button>
            </div>
            
            <div id="message"></div>
            
            <div class="attempts" id="attemptsCounter">Attempts: 0</div>
            
            <button id="reset">Start New Game</button>
        </div>
    </div>
    <div class='footer'>(C) Copyright 2025 Merchantsons. All rights reserved.</div>
</div>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const guessInput = document.getElementById('guessInput');
            const guessButton = document.getElementById('guessButton');
            const resetButton = document.getElementById('reset');
            const messageEl = document.getElementById('message');
            const attemptsEl = document.getElementById('attemptsCounter');
            const progressBar = document.getElementById('progressBar');
            const container = document.querySelector('.container');
            
            let attempts = 0;
            
            function updateProgressBar() {
                const progress = Math.min(attempts * 10, 100);
                progressBar.style.width = `${progress}%`;
            }
            
            function displayMessage(message, type) {
                messageEl.textContent = message;
                messageEl.style.display = 'block';
                
                messageEl.className = '';
                messageEl.classList.add(type);
                
                if (type === 'correct') {
                    container.classList.add('celebrate');
                    setTimeout(() => {
                        container.classList.remove('celebrate');
                    }, 500);
                }
            }
            
            function handleGuess() {
                const guess = parseInt(guessInput.value);
                
                if (isNaN(guess) || guess < 1 || guess > 100) {
                    displayMessage('Please enter a valid number between 1 and 100!', 'too_high');
                    return;
                }
                
                fetch('/guess', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: `guess=${guess}`
                })
                .then(response => response.json())
                .then(data => {
                    attempts = data.attempts;
                    attemptsEl.textContent = `Attempts: ${attempts}`;
                    updateProgressBar();
                    displayMessage(data.message, data.result);
                    
                    if (data.result === 'correct') {
                        guessButton.disabled = true;
                        guessInput.disabled = true;
                    }
                })
                .catch(error => console.error('Error:', error));
                
                guessInput.value = '';
                guessInput.focus();
            }
            
            function resetGame() {
                fetch('/reset', {
                    method: 'POST'
                })
                .then(response => response.json())
                .then(() => {
                    attempts = 0;
                    attemptsEl.textContent = `Attempts: ${attempts}`;
                    messageEl.style.display = 'none';
                    guessButton.disabled = false;
                    guessInput.disabled = false;
                    guessInput.value = '';
                    guessInput.focus();
                    progressBar.style.width = '0%';
                })
                .catch(error => console.error('Error:', error));
            }
            
            guessButton.addEventListener('click', handleGuess);
            
            guessInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    handleGuess();
                }
            });
            
            resetButton.addEventListener('click', resetGame);
            
            guessInput.focus();
        });
    </script>
</body>
</html>
    ''')

if __name__ == '__main__':
    # Suppress the development server warning and run locally
    os.environ['FLASK_ENV'] = 'development'
    app.run(host='localhost', port=5000, debug=True, use_reloader=True)