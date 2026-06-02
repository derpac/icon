from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import sympy as sp

from diff2sympy import diff2sympy
from symdiff2genform import symdiff2genform
from genform2controlsim import genform2controller

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*', async_mode='threading')

session_state = {
    'simulate_fn': None,
    'f_expr': None,
    'b_expr': None, 
    'n': None,
    'free_params': [],
    'control_type': None,
    'trajectory_type': None,
}

# app route

@app.route('/')
def index():
    return render_template('index.html') # justensure they are in same directory ofc

# web socket events

@socketio.on('parse_equation')
def handle_parse(data):
    # this recives the raw latex from user input
    # needs to emit parse_result {n, f, b, free_params} | e 
    try: 
        sym_expr, params = diff2sympy(data['equation'])
        xn_expr, f_expr, b_expr, n = symdiff2genform(sym_expr)

        session_state['f_expr'] = f_expr
        session_state['b_expr'] = b_expr
        session_state['n'] = n

        exclude = {'t', 'u', 'x', 'x_s', 'dx_s'}
        free = [str(s) for s in params if str(s) not in exclude] # could maybe be done with sympy.free_symbols ?
        session_state['free_params'] = free

        emit('parse_result', {
            'n': n,
            'f': str(f_expr),
            'b': str(b_expr),
            'free_params': free,
        })

    except Exception as e:
        emit('parse_result', {'error': str(e)})

# next socket to build controller
@socketio.on('build_controller')
def handle_build(data):
    # recives params, control_type, trajectroy type
    # emits build_result: true | e

    try:
        simulate_fn, _ = genform2controller(
            session_state['f_expr'],
            session_state['b_expr'],
            session_state['n'],
            data['control_type'],
            data['trajectory_type'],
            data['params'],
        )
        session_state['simulate_fn'] = simulate_fn
        session_state['control_type'] = data['control_type']
        session_state['trajectory_type'] = data['trajectory_type']

        emit('build_result', {'ok' : True})

    except Exception as e:
        emit('build_result', {'error': str(e)})


# finally simulate socket
@socketio.on('simulate')
def handle_simulate(data):
    # recives gains 
    # emits sim_result: t,x,dx,xd,tracking_error, u | e

    try:
        simulate_fn = session_state.get('simulate_fn')
        if simulate_fn is None:
            emit('sim_result', {'error': 'build controller first'})

            return
        
        result = simulate_fn(data['gains'])
        emit('sim_result', result)
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        emit('sim_result', {'error': str(e)})


# entry point 

if __name__ == '__main__':
    print('http://localhost:5000')
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)