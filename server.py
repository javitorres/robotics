from flask import Flask, request, jsonify
import threading
import robot  # Importamos tu robot.py

app = Flask(__name__)

# API para mover articulaciones
@app.route('/mover', methods=['POST'])
def mover():
    data = request.get_json()

    if 'hombro_angle' in data:
        robot.hombro_angle = data['hombro_angle']
    if 'hombro_updown' in data:
        robot.hombro_updown = data['hombro_updown']
    if 'codo_angle' in data:
        robot.codo_angle = data['codo_angle']
    if 'codo_updown' in data:
        robot.codo_updown = data['codo_updown']
    if 'muñeca_angle' in data:
        robot.muñeca_angle = data['muñeca_angle']
    if 'muñeca_updown' in data:
        robot.muñeca_updown = data['muñeca_updown']

    return jsonify({"status": "ok"})

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

def lanzar_api():
    app.run(port=5000, threaded=True)

if __name__ == "__main__":
    # Lanzar servidor API en un hilo
    api_thread = threading.Thread(target=lanzar_api)
    api_thread.daemon = True  # Hilo de servidor como demonio
    api_thread.start()

    # Lanzar simulador en el hilo principal
    robot.main()
