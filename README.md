# robotics
Utils for design and control robots

![image](https://github.com/user-attachments/assets/a1d195f3-c6ff-47f8-8488-a0fe0371be54)


# Run

python3 server.py

Now you can control the robot with cursors and A,S,W,D

Or send commands:

curl -X POST http://localhost:5000/mover -H "Content-Type: application/json" -d "{\"hombro_angle\": 45}"
curl -X POST http://localhost:5000/mover -H "Content-Type: application/json" -d "{\"hombro_angle\": 30, \"codo_updown\": 15}"
curl http://localhost:5000/estado
