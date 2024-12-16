from flask import Flask, render_template, request
from flask_socketio import SocketIO, send
import plotly.graph_objs as go  # Ensure this import is correct
import plotly.offline as pyo
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)

def create_graph():
    data = [go.Bar(
        x=['Category A', 'Category B', 'Category C'],
        y=[10, 20, 15]
    )]
    layout = go.Layout(
        title='Sample Bar Chart',
        height=500  # Set a specific height for the chart
    )
    fig = go.Figure(data=data, layout=layout)
    graph = pyo.plot(fig, output_type='div')
    return graph

@app.route('/', methods=['GET', 'POST'])
def index():
    graph = create_graph()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        return render_template('index.html', graph=graph, name=name, email=email)
    
    return render_template('index.html', graph=graph)

@app.route('/html.html')
def html_page():
    return render_template('html.html')

@app.route('/python.html')
def python_page():
    return render_template('python.html')

@app.route('/c#.html')
def c#_page():
    return render_template('c#.html')

@app.route('/c++.html')
def c++_page():
    return render_template('c++.html')

@app.route('/javascript.html')
def javascript_page():
    return render_template('javascript.html')
messages = []


@socketio.on('connect')
def handle_connect():
    # Send existing messages to the newly connected client
    for msg in messages:
        send(msg)

@socketio.on('message')
def handle_message(msg):
    print(f"Message: {msg}")
    # Add the new message to the global list
    messages.append(msg)
    # Keep only the last 10 messages
    if len(messages) > 10:
        messages.pop(0)
    # Broadcast the message to all clients
    send(msg, broadcast=True)
    
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Ensure the PORT environment variable is used
    socketio.run(app, host='0.0.0.0', port=port, debug=True, allow_unsafe_werkzeug=True)
