#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from suruq.sur.backend.gp import GPSurrogate

#%% Define some model f(u, v)
def rosenbrock(x, y, a, b):
    return (a - x)**2 + b * (y - x**2)**2
def f(r, u, v):
    return rosenbrock((r - 0.5) + u - 5, 1 + 3 * (v - 0.6), a=1, b=3)/20
  

#%% Plot model at [u0, v0]
    
u0 = 5
v0 = 0.575
r = np.linspace(0,1,100)

plt.figure()
plt.plot(r, f(r, u0, v0))
plt.show()

#%% Plot behavior around [u0, v0]

u = np.linspace(4.7, 5.3, 20)
v = np.linspace(0.55, 0.6, 20)
y = np.fromiter((f(0.25, uk, vk) for vk in v for uk in u), float)
[U,V] = np.meshgrid(u, v)
Y = y.reshape(U.shape)

plt.figure()
plt.contour(U,V,Y)
plt.colorbar()
plt.show()

#%% Generate training data
nr = 5
nuv = 5
rtrain = np.linspace(0,1,nr)
sig_u = 0.01
sig_v = 0.001

uvtrain = np.random.multivariate_normal([u0,v0], np.diag([sig_u, sig_v])**2, 
                                        [nr,nuv])

xtrain = np.array([rtrain[kr] for kr in range(nr)
    for vk in uvtrain[kr,:,1] for uk in uvtrain[kr,:,0]])
ytrain = np.array([f(rtrain[kr], uk, vk) for kr in range(nr)
    for vk in uvtrain[kr,:,1] for uk in uvtrain[kr,:,0]])
ntrain = len(ytrain)

plt.figure()
plt.plot(uvtrain[:,:,0], uvtrain[:,:,1], 'x')
plt.show()

#%% Create and train surrogate
sur = GPSurrogate()
sur.train(xtrain, ytrain)

#%% Compute surrogate predictor for test input
xtest = r
ftest = sur.predict(xtest)

# reference for checking only:
ytest = f(r, u0, v0)

plt.figure()
plt.errorbar(xtrain, ytrain, sur.sigma*1.96, capsize=2, fmt='.')
plt.plot(xtest, ytest)
plt.plot(xtest, ftest)
plt.xlabel('r')
plt.ylabel('f(r)')
plt.show()
