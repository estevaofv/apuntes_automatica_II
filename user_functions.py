#Python no trae una función para conectar funciones de transferencia en serie o 
#retroalimentadas, asi que con ayuda del equipo de pybonacci creamos unas funciones.
#http://pybonacci.org/2013/10/10/teoria-de-control-en-python-con-scipy-i/
#http://pybonacci.org/2013/11/06/teoria-de-control-en-python-con-scipy-ii-control-pid/

from scipy import signal

import numpy as np

def series(sys1, sys2):


    """Series connection of two systems.
    """
    if not isinstance(sys1, signal.lti):
        sys1 = signal.lti(*sys1)
    if not isinstance(sys2, signal.lti):
        sys2 = signal.lti(*sys2)
    num = np.polymul(sys1.num, sys2.num)
    den = np.polymul(sys1.den, sys2.den)
    sys = signal.lti(num, den)
    return sys
def feedback(plant, sensor=None):
    """Negative feedback connection of plant and sensor.
    If sensor is None, then it is assumed to be 1.
    """
    if not isinstance(plant, signal.lti):
        plant = signal.lti(*plant)
    if sensor is None:
        sensor = signal.lti([1], [1])
    elif not isinstance(sensor, signal.lti):
        sensor = signal.lti(*sensor)
    num = np.polymul(plant.num, sensor.den)
    den = np.polyadd(np.polymul(plant.den, sensor.den),
                     np.polymul(plant.num, sensor.num))
    sys = signal.lti(num, den)
    return sys


def error(plant, sensor=None, entrada=None):
    """Negative feedback connection of plant and sensor.
    If sensor is None, then it is assumed to be 1.
    """
    if not isinstance(plant, signal.lti):
        plant = signal.lti(*plant)

    if sensor is None:
        sensor = signal.lti([1], [1])
    elif not isinstance(sensor, signal.lti):
        sensor = signal.lti(*sensor)
        

    if entrada is None:
        entrada = signal.lti([1], [1])
    elif not isinstance(entrada, signal.lti):
        entrada = signal.lti(*entrada) 
 
        
        
 #   aux = np.polymul(plant.den, sensor.den)
    num = np.polymul(np.polymul(plant.den, sensor.den),entrada.num)
    den = np.polyadd(np.polymul(np.polymul(plant.den, sensor.den),entrada.den),
                     np.polymul(np.polymul(plant.num, sensor.num),entrada.den))
    sys = signal.lti(num, den)
    return sys


# De la misma manera, construimos una función para que nos devuelva el tiempo de 
# respuesta y el sobredisparo.

def tr(t, y, ys=None, margins=(0.0, 1.0)):
    """Rise time.
    Other possible margins: (0.05, 0.95), (0.1, 0.9). If no ys is given,
    then last value of y is assumed as stationary.
    """
    if ys is None:
        ys = y[-1]
    # Values between margins[0] * ys and margins[1] * ys
    mask = (y > margins[0] * ys) & (y < margins[1] * ys)
    # If response oscillates, only interested in limits of first region
    idx_change = np.nonzero(np.diff(mask))[0]
    # Initial and final indexes
    idx = idx_change[0], idx_change[1]
    # Time difference
    return t[idx[1]] - t[idx[0]]
def Ms(y, ys=None):
    """Maximum overshoot.
    Other possible margins: (0.05, 0.95), (0.1, 0.9). If no ys is given,
    then last value of y is assumed as stationary.
    """
    if ys is None:
        ys = y[-1]
    ymax = np.max(y)
    Ms = (ymax - ys) / ys
    return Ms
