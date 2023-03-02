from flask import Flask, request, abort
import os
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask('app')
ip_ban_list = []


@app.before_request
def block_method():
  ip = request.environ.get('REMOTE_ADDR')
  if ip in ip_ban_list:
    abort(403)


@app.route('/')
def hello_world():
  return 'Use the app to use chatrooms'


@app.route('/help')
def help():
  return 'Email me at ajeff9752@gmail.com for help'


@app.route('/create')
def create():
  with open(f"rooms/{request.args.get('name')}.txt", "w") as file:
    if request.args.get('password') != None:
      file.write(f"password:{request.args.get('password')}\n")
      file.write("ip:name: message")
    else:
      pass
    file.close()
  return "200"


@app.route('/rooms')
def rooms():
  list = ""
  for filename in os.listdir('rooms'):
    f = os.path.join('rooms', filename)
    if os.path.isfile(f):
      list += f[6:-4]
      list += "\n"
  return list


@app.route('/get')
def get():
  try:
    if request.args.get('room') == "home":
      return f"\n{'-'*10}\nROOMS:\n\n{rooms()}"
    else:
      try:
        with open(f"rooms/{request.args.get('room')}", "r") as file:
          contents = ""
          list = file.read().split('\n')
          for line in list:
            if line.strip() == "":
              contents += "\n"
            else:
              if line.split(":")[0] == "password":
                contents += f"password:{line.split(':')[1]}\n"
              else:
                name = line.split(":")[1]
                message = line.split(":")[2]
                contents += f"{name}: {message}\n"
          return contents
      except Exception as e:
        return str(e)
  except Exception as e:
    return str(e)


@app.route('/post')
def post():
  try:
    if request.args.get('room') == 'home.txt':
      pass
    else:

      with open(f"rooms/{request.args.get('room')}", "a") as file:
        file.write(f"\n{request.remote_addr}:{request.args.get('text')}")
        file.close()
        return "200"
  except:
    return ("404 room not found")


app.run(host='0.0.0.0', port=8080)
