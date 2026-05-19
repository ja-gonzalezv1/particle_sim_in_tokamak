# Calculate and visualize the fields of the tokamak
# Uncomment the desired section before running, although probably better to just pass it to a notebook
# Import libaries
import matplotlib
import numpy as np
import scipy as sci
import sympy as sym
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio
# Import functions
from functions import MagneticVectorField
from functions import PoloidalLoop
from functions import CentralSolenoid
from functions import ToroidalCoil


# Create meshgrid and pack
a = 1
b = 0.5
# Rectanguar meshgrid
n_points = 20
points = np.linspace(-1.5, 1.5, n_points)
xp, yp, zp = np.meshgrid(points, points, points)
## for 3d calculation
# mesh = np.array([xp, yp, zp])
## for vertical cross section 2d calculation
mesh = np.array([xp[int(len(xp)/2)], yp[int(len(xp)/2)], zp[int(len(xp)/2)]])
## For toroidal cross section (2d calculation)
# mesh = np.array([xp[:, :, int(len(xp)/2)], yp[:, :, int(len(xp)/2)], zp[:, :, int(len(xp)/2)]])
# Toroidal meshgrid
# theta = np.linspace(0, 2*np.pi, 15)
# theta = theta[0: -1]
# r = np.linspace(0, b, 5)
# phi = np.linspace(0, 2*np.pi, 15)
# phi = phi[0:-1]
# R, Theta, Phi = np.meshgrid(r, theta, phi)
# xp = (a + b*np.sin(Theta))*np.sin(Phi)
# yp = -(a + b*np.sin(Theta))*np.cos(Phi)
# zp = (b + 0.3)*np.cos(Theta)
# mesh = np.array([xp, yp, zp])



### Calculation of the central solenoid field
# Get loops
loop_cs = CentralSolenoid(15)
# Unpack the sym and plot loops
sym_loop_cs = loop_cs[0]
ploop_cs = loop_cs[1]
# calculate the field with the sym loop
field_cs = MagneticVectorField(sym_loop_cs, mesh)

# make the total field equal to this calculated field
field = field_cs
###

### Calculation for the plasma current
# loop_plasma = PoloidalLoop(a, 0)
# sym_loop_plasma = loop_plasma[0]
# ploop_plasma = loop_plasma[1]
# field_plasma = MagneticVectorField(sym_loop_plasma, mesh)
#
# field = field_plasma
###


# Mock calculation of the induced current into the plasma
# Calculate 1D magnetic flux for the central solenoid and plasma current
# Central solenoid flux, just adding the vertical components of the field
# flux_cs = 0
# for i in range(len(xp[int(len(xp)/2)][:, int(len(xp)/2)])):
#     if abs(xp[int(len(xp)/2)][:, int(len(xp)/2)][i]) < a:
#         flux_cs += 2*field_cs[2][:, int(len(xp)/2)][i]
# print(flux_cs)
# # Plasma current flux, same thing
# flux_plasma = 0
# for i in range(len(xp[int(len(xp)/2)][:, int(len(xp)/2)])):
#     if abs(xp[int(len(xp)/2)][:, int(len(xp)/2)][i]) < a:
#         flux_plasma += 2*field_plasma[2][:, int(len(xp)/2)][i]
# print(flux_plasma)
# flux_ratio = abs(flux_cs/flux_plasma)
# print('---')
# print(flux_ratio)



### Calculation of the toroidal coil field
# loop_tor = ToroidalCoil(20)
# sym_loop_tor = loop_tor[0]
# ploop_tor = loop_tor[1]
# field_tor = MagneticVectorField(sym_loop_tor, mesh)
#
# field = field_tor
###


### Calculation for the poloidal loops
## Calculate the field of each coil separately
# loop_1 = PoloidalLoop(a + 0.5, b + 0.3)
# sym_loop_1 = loop_1[0]
# ploop_1 = loop_1[1]
# field_1 = MagneticVectorField(sym_loop_1, mesh)
#
# loop_2 = PoloidalLoop(a + 0.5, -b - 0.3)
# sym_loop_2 = loop_2[0]
# ploop_2 = loop_2[1]
# field_2 = MagneticVectorField(sym_loop_2, mesh)
#
# loop_3 = PoloidalLoop(a + b + 0.1, b/2)
# sym_loop_3 = loop_3[0]
# ploop_3 = loop_3[1]
# field_3 = MagneticVectorField(sym_loop_3, mesh)
#
# loop_4 = PoloidalLoop(a + b + 0.1, -b/2)
# sym_loop_4 = loop_4[0]
# ploop_4 = loop_4[1]
# field_4 = MagneticVectorField(sym_loop_4, mesh)
#
## the total field is equal to the sum of all
# field = field_1 + field_2 + field_3 + field_4
###


## Add the fields of all the coils
## add weights to each field as if it was the current of each coil
# field = 10*field_1 + 10*field_2 + 7*field_cs + field_tor
# field =  7*field_plasma + field_tor
## Normalize lenght
# field = field/(np.sqrt(field[0]**2 + field[1]**2 + field[2]**2))



# Plot the results

## for 3d plot
# fig_1 = plt.figure()
# ax_1 = fig_1.add_subplot(111, projection='3d')

# for 2d plot
fig_2 = plt.figure()
ax_2 = fig_2.add_subplot(111)


## plot to see the points that make up the toroid
# ax_1.scatter(xp, yp, zp)


### 3d plots
### Central solenoid 3D plot
# ax_1.plot(ploop_cs[0], ploop_cs[1], ploop_cs[2], color='green', label='Central solenoid')
# ax_1.quiver(xp, yp, zp, field[0], field[1], field[2], length=0.3, normalize=True)
###

### Plasma current 3D plot
# ax_1.plot(ploop_plasma[0], ploop_plasma[1], ploop_plasma[2], color='red', label='Plasma current')
# ax_1.quiver(xp, yp, zp, field[0], field[1], field[2], length=0.3, normalize=True)
###

### Toroidal field 3D plot
# ax_1.plot(ploop_tor[0], ploop_tor[1], ploop_tor[2], color='black', label='Toroidal coil')
# ax_1.quiver(xp, yp, zp, field[0], field[1], field[2], length=0.3, normalize=True)
###

### Poloidal field 3D plot
# Plot the loops and the field they generate
# ax_1.plot(ploop_1[0], ploop_1[1], ploop_1[2], color='blue', label='Poloidal coils')
# ax_1.plot(ploop_2[0], ploop_2[1], ploop_2[2], color='blue')
# ax_1.plot(ploop_3[0], ploop_3[1], ploop_3[2], color='blue')
# ax_1.plot(ploop_4[0], ploop_4[1], ploop_4[2], color='blue')
# ax_1.quiver(xp, yp, zp, field[0], field[1], field[2], length=0.3, normalize=True)
###

### All fields 3D plot
# Theta_ = np.linspace(0, 2*np.pi, 15)
# # Theta_ = Theta_[0: -1]
# Phi_ = np.linspace(0, 2*np.pi, 15)
# # Phi_ = Phi_[0: -1]
# theta_, phi_ = np.meshgrid(Theta_, Phi_)
#
# xs = (a + b*np.sin(theta_))*np.sin(phi_)
# ys = -(a + b*np.sin(theta_))*np.cos(phi_)
# zs = (b + 0.3)*np.cos(theta_)
#
## For neater results, use plotly
# pio.renderers.default = 'firefox'
#
# fig = go.Figure()
# fig.add_trace(go.Surface(x=xs, y=ys, z=zs, colorscale='Gray'))
#
# fig.add_trace(go.Cone(x=xp.flatten(), y=yp.flatten(), z=zp.flatten(),
#                        u=field[0].flatten(), v=field[1].flatten(), w=field[2].flatten(),
#                        sizemode="absolute", sizeref=2, colorscale=[[0, 'rgb(0,0,0)'], [1, 'rgb(0,0,0)']], anchor="tail"))
#
# fig.update_traces(showscale=False)
# fig.show()
###


# Changes to make the plot look as expected
# ax_1.set_xlim(-b-a,b+a) 
# ax_1.set_ylim(-b-a,b+a)
# ax_1.set_zlim(-b-a,b+a) 
# plt.legend()
# plt.show()


### 2d plots
### Poloidal field cross section
### For a mesh, send the p[int(len(xp)/2)] components, to the field calculator
### Also use the 2D field option of the calculator. Then just plot. Streamplot look very ugly
# # Plot the field
# rn = (np.sqrt(field[0]**2 + field[2]**2))**(1)
# ax_2.quiver(xp[int(len(xp)/2)], zp[int(len(xp)/2)], field[0]/rn, field[2]/rn, color='purple')
#
# # Circle patch for the torus walls
# circ_1 = matplotlib.patches.Ellipse((1, 0), 1, 1.6, color=None, fill=False, label='Torus walls')
# circ_2 = matplotlib.patches.Ellipse((-1, 0), 1, 1.6, color=None, fill=False)
# ax_2.add_patch(circ_1)
# ax_2.add_patch(circ_2)
#
# # Lines to represent the coils
# ax_2.plot(ploop_1[0], ploop_1[2], color='blue', label='Poloidal coils')
# ax_2.plot(ploop_2[0], ploop_2[2], color='blue')
# ax_2.scatter(-a - b - 0.1, b/2, color='blue')
# ax_2.scatter(a + b + 0.1, b/2, color='blue')
# ax_2.scatter(-a - b - 0.1, -b/2, color='blue')
# ax_2.scatter(a + b + 0.1, -b/2, color='blue')
#
# ax_2.set_aspect('equal')
# plt.legend()
# plt.show()
###

### Central solenoid cross section
### Same thing as for the poloidal coils
# Plot the field
rn = 0.5*np.sqrt(field[0]**2 + field[2]**2)
ax_2.quiver(xp[int(len(xp)/2)], zp[int(len(xp)/2)], field[0]/rn, field[2]/rn, color='purple')

# Circle patch for the torus walls
circ_1 = matplotlib.patches.Ellipse((1, 0), 1, 1.6, color=None, fill=False, label='Torus walls')
circ_2 = matplotlib.patches.Ellipse((-1, 0), 1, 1.6, color=None, fill=False)
ax_2.add_patch(circ_1)
ax_2.add_patch(circ_2)
#
# Coil
ax_2.plot(ploop_cs[0], ploop_cs[2], color='green', label='Central solenoid', alpha=0.5)
# Plasma
ax_2.scatter(-1, 0, color='red', label='Plasma loop')
ax_2.scatter(1, 0, color='red')

ax_2.set_aspect('equal')
plt.legend()
plt.show()
###


### Plasma current cross section
### Same thing as for the poloidal coils
# # Plot the field
# rn = 0.5*np.sqrt(field[0]**2 + field[2]**2)
# ax_2.quiver(xp[int(len(xp)/2)], zp[int(len(xp)/2)], field[0]/rn, field[2]/rn, color='purple')
#
# # Circle patch for the torus walls
# circ_1 = matplotlib.patches.Ellipse((1, 0), 1, 1.6, color=None, fill=False, label='Torus walls')
# circ_2 = matplotlib.patches.Ellipse((-1, 0), 1, 1.6, color=None, fill=False)
# ax_2.add_patch(circ_1)
# ax_2.add_patch(circ_2)
# #
# # Plasma
# ax_2.scatter(-1, 0, color='red', label='Plasma current')
# ax_2.scatter(1, 0, color='red')
#
# ax_2.set_aspect('equal')
# plt.legend()
# plt.show()
###

### Toroidal coild cross section
### Take slices like xp[:, :, :], yp[:, :, :], zp[:, :, int(len(zp)/2)]
## Plot the field
# rn = 0.5*np.sqrt(field[0]**2 + field[1]**2)
# ax_2.quiver(xp[:, :, int(len(zp)/2)], yp[:, :, int(len(yp)/2)], field[0]/rn, field[1]/rn, color='purple')
#
# # Circle patch for the torus walls
# circ_1 = matplotlib.patches.Circle((0, 0), (a + b), color=None, fill=False, label='Torus walls')
# circ_2 = matplotlib.patches.Circle((0, 0), (b - a), color=None, fill=False)
# ax_2.add_patch(circ_1)
# ax_2.add_patch(circ_2)
#
# # Coil
# ax_2.plot(ploop_tor[0], ploop_tor[1], color='black', label='Toroidal coil', alpha=0.5)
#
# ax_2.set_aspect('equal')
# plt.legend()
# plt.show()
###
