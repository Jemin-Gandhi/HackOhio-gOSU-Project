from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return f'Hello, {app.config["NAME"]}!'

if __name__ == '__main__':
    app.config['NAME'] = 'Docker'
    app.run(host='0.0.0.0', port=80)