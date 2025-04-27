from flask import Flask, request, jsonify
import threading
import robot

app = Flask(__name__)

# Creamos el estado global
estado = robot.EstadoRobot()

@app.route('/mover', methods=['POST'])
def mover():
    data = request.get_json()
    print("Recibido en mover():", data)

    if 'hombro_angle' in data:
        estado.hombro_angle = data['hombro_angle']
    if 'hombro_updown' in data:
        estado.hombro_updown = data['hombro_updown']
    if 'codo_angle' in data:
        estado.codo_angle = data['codo_angle']
    if 'codo_updown' in data:
        estado.codo_updown = data['codo_updown']
    if 'muneca_angle' in data:
        estado.muneca_angle = data['muneca_angle']
    if 'muneca_updown' in data:
        estado.muneca_updown = data['muneca_updown']

    return jsonify({"status": "ok"})

@app.route('/estado', methods=['GET'])
def get_estado():
    return jsonify({
        "hombro_angle": estado.hombro_angle,
        "hombro_updown": estado.hombro_updown,
        "codo_angle": estado.codo_angle,
        "codo_updown": estado.codo_updown,
        "muneca_angle": estado.muneca_angle,
        "muneca_updown": estado.muneca_updown
    })

def lanzar_api():
    app.run(port=8080, threaded=True)

if __name__ == "__main__":
    api_thread = threading.Thread(target=lanzar_api)
    api_thread.daemon = True
    api_thread.start()

    robot.main(estado)
