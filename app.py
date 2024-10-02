from flask import Flask, jsonify, render_template
from flask_cors import CORS
import threading
import time
import random

app = Flask(__name__)
CORS(app)

NUM_FILOSOFOS = 5
tenedores = [threading.Semaphore(1) for _ in range(NUM_FILOSOFOS)]
filosofo_estado = ["Pensando" for _ in range(NUM_FILOSOFOS)]

# Función que simula a cada filósofo
def filosofo(num):
    while True:
        # Estado de pensando
        filosofo_estado[num] = "Pensando"
        time.sleep(random.uniform(1, 3))  # Simula pensar

        # Estado de hambriento
        filosofo_estado[num] = "Hambriento"

        # Tomar tenedores (derecho e izquierdo)
        if num % 2 == 0:
            tenedores[num].acquire()
            tenedores[(num + 1) % NUM_FILOSOFOS].acquire()
        else:
            tenedores[(num + 1) % NUM_FILOSOFOS].acquire()
            tenedores[num].acquire()

        # Estado de comiendo
        filosofo_estado[num] = "Comiendo"
        time.sleep(random.uniform(1, 2))  # Simula comer

        # Soltar los tenedores
        tenedores[num].release()
        tenedores[(num + 1) % NUM_FILOSOFOS].release()

# Ruta para obtener el estado de los filósofos
@app.route('/estado_filosofos')
def estado_filosofos():
    return jsonify(filosofo_estado)

# Ruta principal para servir la página HTML
@app.route('/')
def index():
    return render_template('index.html')

# Iniciar los hilos de los filósofos
def iniciar_filosofos():
    for i in range(NUM_FILOSOFOS):
        t = threading.Thread(target=filosofo, args=(i,))
        t.start()

if __name__ == '__main__':
    iniciar_filosofos()
    app.run(debug=True)

