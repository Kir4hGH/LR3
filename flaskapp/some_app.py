print("Hello world") 
import datetime
import requests
from flask import Flask
app = Flask(__name__) 
#декоратор для вывода страницы по умолчанию 
@app.route("/")
def hello(): 
    return " <html><head></head> <body> <h1>Hello World!</h1><br>Hello World!</body></html>"
if __name__ == "__main__": 
    app.run(host='127.0.0.1',port=5000)
