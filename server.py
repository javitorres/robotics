from flask import Flask, request, jsonify
import threading
import robot  # << Importamos tu robot.py

app = Flask(__name__)

# API para mover articulaciones
@app.route('/mover', methods=['POST'])
def mover():
    data = request.get_json()

    # Controlar hombro
    if 'hombro_angle' in data:
        robot.hombro_angle = data['hombro_angle']
    if 'hombro_updown' in data:
        robot.hombro_updown = data['hombro_updown']

    # Controlar codo
    if 'codo_angle' in data:
        robot.codo_angle = data['codo_angle']
    if 'codo_updown' in data:
        robot.codo_updown = data['codo_updown']

    # Controlar muñeca
    if 'muñeca_angle' in data:
        robot.muñeca_angle = data['muñeca_angle']
    if 'muñeca_updown' in data:
        robot.muñeca_updown = data['muñeca_updown']

    return jsonify({"status": "ok"})

# API para leer estado actual
@app.route('/estado', methods=['GET'])
def estado():
    return jsonify({
        "hombro_angle": robot.hombro_angle,
        "hombro_updown": robot.hombro_updown,
        "codo_angle": robot.codo_angle,
        "codo_updown": robot.codo_updown,
        "muñeca_angle": robot.muñeca_angle,
        "muñeca_updown": robot.muñeca_updown
    })

def lanzar_simulador():
    robot.main()

if __name__ == "__main__":
    # Lanzar simulador en un hilo
    simulador_thread = threading.Thread(target=lanzar_simulador)
    simulador_thread.start()

    # Lanzar servidor API
    app.run(port=5000)
