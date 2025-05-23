# run.py - Execute a aplicação Flask
from app import app

if __name__ == "__main__":
    # O host "0.0.0.0" permite acessar de qualquer lugar, incluindo fora do Codespaces
    app.run(debug=True, host="0.0.0.0", port=5000)
