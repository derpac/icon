# --------------------------------------------------------------------------
# enter sysmtem and click start 

# code generates states and parameters

# user need to identify classification of each param
# known, unknown_bounded, unknown_constant

# user then defines setpoint / set trajectory

# code can then find the derivatives of these for \dot{xd}...

# code then works out the appropriate controller
# feedback linearisation, SMC or adaptive

# user is then presented with controller gains to adjust
# code then outputs live system response data based on gains live

# front end on html, js, css is used to plot results live with python backend
# the response needs to update live when the user changes the gains or setpoints
# --------------------------------------------------------------------------

import sympy as sp
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

compiled_sys = {}

@socketio.on('init_system')
def handle_init(data):
    try:
        latin_str = data['equation']
        # diff2sympy returns sympy and params
        # symdiff2genform returns genform,f,b
    except Exception as e:
        emit('error',{'message': f"symbolic parse to backend failed: {str(e)}"})
    
@socketio.on('generate_controller')
def handle_controller(data):
    global compiled_sys

    f_func = sp.parse_expr(data['f_str'])
    b_coeff = sp.parse_expr(data['b_str'])