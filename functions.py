# Functions that can be imported for the other files

import numpy as np
import scipy as sci
import sympy as sym

# Parameters for the functions
# major radius
a = 1
# minor radius
b = 0.5

# Function that returns the vectors at each point
def MagneticVectorField(l_, mesh):
    # Unpack l_
    # The function that describes the loop
    l = l_[0]
    # The domain of the loop, from a to b
    a = l_[1][0]
    b = l_[1][1]
    # The parameter of the loop
    v = l_[2]

    # Unpack the meshgrid
    # Toroidal
    # r = mesh[0]
    # a_ = mesh[0][0][0]
    # b_ = mesh[0][-1][0]
    # phi = mesh[1]
    # theta = mesh[2]
    # Cartesian
    xp = mesh[0]
    yp = mesh[1]
    zp = mesh[2]

    # Create the xyz grid inside the toroid
    # xp = (a_ + r*np.sin(theta))*np.cos(phi)
    # yp = (a + r*np.sin(theta))*np.sin(phi)
    # zp = b_*np.cos(theta)

    # Initialize symbols and vectors
    # Use the same symbols when defining the loops
    x, y, z = sym.symbols('x, y, z')
    r = sym.Matrix([x, y, z])
    sep = r - l

    # Define integrand
    # v is the variable that is going to be integrated
    integrand = sym.diff(l, v).cross(sep)/sep.norm()**3

    # Separate integrand into the coordinates
    dBxdv = sym.lambdify([v, x, y, z], integrand[0])
    dBydv = sym.lambdify([v, x, y, z], integrand[1])
    dBzdv = sym.lambdify([v, x, y, z], integrand[2])

    # Function to integrate over the loop at a given point
    def B(x, y, z):
        # use scipy quad to integrate
        X = sci.integrate.quad(dBxdv, a, b, args=(x, y, z))[0]
        Y = sci.integrate.quad(dBydv, a, b, args=(x, y, z))[0]
        Z = sci.integrate.quad(dBzdv, a, b, args=(x, y, z))[0]
        return np.array([X, Y, Z])

    # Calculate the magnetic field at every point of the meshgrid
    B_grid = np.vectorize(B, signature='(),(),()->(n)')(xp, yp, zp)

    # Extract the components into separate arrays
    # 3D meshgrid
    Bx = B_grid[:, :, :, 0]
    By = B_grid[:, :, :, 1]
    Bz = B_grid[:, :, :, 2]
    # 2D meshgird
    # Bx = B_grid[:, :, 0]
    # By = B_grid[:, :, 1]
    # Bz = B_grid[:, :, 2]

    return np.array([Bx, By, Bz])


# Function that returns the vector at a point
def MagneticVector(l_, r_):
    # Unpack l_
    # The function that describes the loop
    l = l_[0]
    # The domain of the loop, from a to b
    a = l_[1][0]
    b = l_[1][1]
    # The parameter of the loop
    v = l_[2]

    # Unpack the point
    # r = mesh[0]
    # a_ = mesh[0][0][0]
    # b_ = mesh[0][-1][0]
    # phi = mesh[1]
    # theta = mesh[2]
    xp = r_[0]
    yp = r_[1]
    zp = r_[2]

    # Create the xyz grid inside the toroid
    # xp = (a_ + r*np.sin(theta))*np.cos(phi)
    # yp = (a + r*np.sin(theta))*np.sin(phi)
    # zp = b_*np.cos(theta)

    # Initialize symbols and vectors
    # Use the same symbols when defining the loops
    x, y, z = sym.symbols('x, y, z')
    r = sym.Matrix([x, y, z])
    sep = r - l

    # Define integrand
    # v is the variable that is going to be integrated
    integrand = sym.diff(l, v).cross(sep)/sep.norm()**3

    # Separate integrand into the coordinates
    dBxdv = sym.lambdify([v, x, y, z], integrand[0])
    dBydv = sym.lambdify([v, x, y, z], integrand[1])
    dBzdv = sym.lambdify([v, x, y, z], integrand[2])

    # Function to integrate over the loop at a given point
    def B(x, y, z):
        X = sci.integrate.quad(dBxdv, a, b, args=(x, y, z))[0]
        Y = sci.integrate.quad(dBydv, a, b, args=(x, y, z))[0]
        Z = sci.integrate.quad(dBzdv, a, b, args=(x, y, z))[0]
        return np.array([X, Y, Z])

    # Calculate the magnetic field at the point
    B_vec = B(xp, yp, zp)

    return B_vec


# Create loop function
# Poloidal loop
def PoloidalLoop (r, h):
    # Parameter of the loop
    phi = sym.symbols('\\phi')

    # Create sympy loop, domain and pack
    x_ = r*sym.sin(phi)
    y_ = -r*sym.cos(phi)
    z_ = h
    loop = sym.Matrix([x_, y_, z_])
    domain = np.array([0, 2*np.pi])
    sym_pack = [loop, domain, phi]

    # Create loop coordiantes to plot
    phi_ = np.linspace(domain[0], domain[-1], 100)
    X = r*np.sin(phi_)
    Y = -r*np.cos(phi_)
    Z = np.full(len(phi_), h)
    ploop = np.array([X, Y, Z])

    # return both loops
    return [sym_pack, ploop]


def PoloidalLoopCoil (r, h):
    # Parameter of the loop
    phi = sym.symbols('\\phi')

    # Create sympy loop, domain and pack
    x_ = r*sym.sin(phi)
    y_ = -r*sym.cos(phi)
    z_ = h
    loop = sym.Matrix([x_, y_, z_])
    domain = np.array([2*np.pi, 0])
    sym_pack = [loop, domain, phi]

    # Create loop coordiantes to plot
    phi_ = np.linspace(domain[0], domain[-1], 100)
    X = r*np.sin(phi_)
    Y = -r*np.cos(phi_)
    Z = np.full(len(phi_), h)
    ploop = np.array([X, Y, Z])

    return [sym_pack, ploop]



# Central solenoid
def CentralSolenoid (n): 
    a = 1
    b = 0.5
    # Parameter of the coil
    zs = sym.symbols('zs')

    # Create sympy loop, domain and pack
    r = a - b - 0.3
    x_ = r*sym.sin((n*2*np.pi*(b+zs))/(2*b))
    y_ = -r*sym.cos((n*2*np.pi*(b+zs))/(2*b))
    z_ = zs
    loop = sym.Matrix([x_, y_, z_])
    domain = np.array([-(b + 0.2), (b + 0.2)])
    sym_pack = [loop, domain, zs]

    # Create plot loop coordinates to plot
    zl = np.linspace(domain[0], domain[-1], 200)
    X = r*np.sin((n*2*np.pi*(b+zl))/(2*b))
    Y = -r*np.cos((n*2*np.pi*(b+zl))/(2*b))
    Z = zl
    ploop = np.array([X, Y, Z])

    return [sym_pack, ploop]

# Toroidal field coil
def ToroidalCoil (n):
    # Parameter of the coil
    phi = sym.symbols('\\phi')

    # Create sympy loop, domain and pack
    radius = b + 0.2
    x_ = (a + radius*sym.sin(n*phi))*sym.sin(phi)
    y_ = -(a + radius*sym.sin(n*phi))*sym.cos(phi)
    z_ = (radius + 0.3)*sym.cos(n*phi)
    loop = sym.Matrix([x_, y_, z_])
    domain = np.array([0, 2*np.pi])
    sym_pack = [loop, domain, phi]

    # Create plot loop coordinates to plot
    phi_ = np.linspace(domain[0], domain[-1], 400)
    X = (a + radius*np.sin(n*phi_))*np.sin(phi_)
    Y = -(a + radius*np.sin(n*phi_))*np.cos(phi_)
    Z = (radius + 0.3)*np.cos(n*phi_)
    ploop = np.array([X, Y, Z])

    return [sym_pack, ploop]


# runge-kutta 4 calculator
def RK4(f, tf, dt, init):

    # Discretize time
    tn = int(tf/dt)
    t = np.linspace(0, tf, tn)

    # Create solution array
    sol = np.zeros((tn, np.shape(init)[0]))
    sol[0, :] = init

    # Loop to solve
    for i in range(0, tn-1):
        # Create method steps
        k1 = f(t[i], sol[i, :])
        k2 = f(t[i] + dt/2, sol[i, :] + dt/2*k1)
        k3 = f(t[i] + dt/2, sol[i, :] + dt/2*k2)
        k4 = f(t[i + 1], sol[i, :] + dt*k3)

        # Make next value 
        sol[i + 1, :] = sol[i, :] + dt*(k1/6 + k2/3 + k3/3 + k4/6)

    return sol



# modified runge-kutta 4 calculator for the collision sim
def RK4mod(f, dt, init):

    # Solve for next point
    k1 = f(0, init)
    k2 = f(0, init + dt/2*k1)
    k3 = f(0, init + dt/2*k2)
    k4 = f(0, init + dt*k3)

    # Make slope for next value
    slope = (k1/6 + k2/3 + k3/3 + k4/6)

    return slope
