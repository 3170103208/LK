import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math as mt
from sko.PSO import PSO
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import messagebox
from tkinter import filedialog


#B, g, mstar, alpha, Ef, broadening, A, c
def bp_fun(B, g, Ef, broadening, A, c, count):

    h = 6.63 * 10 ** (-34) / (2 * mt.pi)
    k = 1.38 * 10 ** (-23)
    q = 1.6 * 10 ** (-19)
    m = 9.1 * 10 ** (-31)
    u = h / (2 * m) * q
    T = 1.6
    ns = 4.5*10**(16)

    broadening = broadening*q*10**(-3)
    Ef = Ef*q*10**(-3)
    me = 0.42*m
    wc = q*B/me
    sigmaxx = 0



    '''
    Enup = h*wc*(1+0.5)+5*u*B
    Endown = h*wc*(1+0.5)-5*u*B
    sigmaxx = sigmaxx+(1+0.5)*np.exp(-np.square((Ef-Enup)/broadening))
    sigmaxx = sigmaxx+(1-0.5)*np.exp(-np.square((Ef-Endown)/broadening))

    Enup = h*wc*(2+0.5)+4*u*B
    Endown = h*wc*(2+0.5)-4*u*B
    sigmaxx = sigmaxx+(2+0.5)*np.exp(-np.square((Ef-Enup)/broadening))
    sigmaxx = sigmaxx+(2-0.5)*np.exp(-np.square((Ef-Endown)/broadening))

    Enup = h*wc*(3+0.5)+3*u*B
    Endown = h*wc*(3+0.5)-3*u*B
    sigmaxx = sigmaxx+(3+0.5)*np.exp(-np.square((Ef-Enup)/broadening))
    sigmaxx = sigmaxx+(3-0.5)*np.exp(-np.square((Ef-Endown)/broadening))

    Enup = h*wc*(4+0.5)+2*u*B
    Endown = h*wc*(4+0.5)-2*u*B
    sigmaxx = sigmaxx+(4+0.5)*np.exp(-np.square((Ef-Enup)/broadening))
    sigmaxx = sigmaxx+(4-0.5)*np.exp(-np.square((Ef-Endown)/broadening))
    '''

    for n in range(0, 200):
        Enup = h*wc*(n+0.5)+0.5*g*u*B
        sigmaxx = sigmaxx+(n+0.5)*np.exp(-np.square((Ef-Enup)/broadening))
        Endown = h*wc*(n+0.5)-0.5*g*u*B
        sigmaxx = sigmaxx+(n-0.5)*np.exp(-np.square((Ef-Endown)/broadening))
        if n==count:
            energy = Endown*1000/(q)

    rxx = A*sigmaxx*np.square(B/(q*ns))/10000000+c
    return rxx

def rashba_fun(B, g, mstar, alpha, Ef, broadening, A, c):

    h = 6.63 * 10 ** (-34) / (2 * mt.pi)
    k = 1.38 * 10 ** (-23)
    q = 1.6 * 10 ** (-19)
    m = 9.1 * 10 ** (-31)
    u = h / (2 * m) * q
    T = 1.6
    ns = 5*10**(16)

    broadening = broadening*q*10**(-3)
    Ef = Ef*q*10**(-3)
    Er = alpha*q*10**(-3)
    me = mstar*m
    wc = q*B/me
    lc = np.sqrt(h/(me*wc))
    delta = (1-g*me/(2*m))/2
    sigmaxx = 0
    ns = 4.5*10**(16)

    for n in range(0, 200):
        Enup = h*wc*(n+0.5*np.sqrt(np.square(1-g*me/(2*m))+n*np.square(Er)/(Ef*h*wc)))
        sigmaxx = sigmaxx+(n+0.5)*np.exp(-np.square((Ef-Enup)/broadening))
        Endown = h*wc*(n-0.5*np.sqrt(np.square(1-g*me/(2*m))+n*np.square(Er)/(Ef*h*wc)))
        sigmaxx = sigmaxx+(n-0.5)*np.exp(-np.square((Ef-Endown)/broadening))

    rxx = A*sigmaxx*np.square(B/(q*ns))/10000000+c
    return rxx

def g_fun(B, g, mstar, alpha, Ef, broadening, A, c, ns):

    alpha = alpha*10**(21)
    broadening = broadening*q*10**(-3)
    Ef = Ef*q*10**(-3)
    me = mstar*m
    wc = q*B/me
    lc = np.sqrt(h/(me*wc))
    delta = (1-g*me/(2*m))/2
    gama = np.sqrt(2*me*alpha**2/wc)
    Ezero = h*wc*delta
    sigmaxx = 0

    for n in range(1, 200):
        Enup = h*wc*(n+np.sqrt(delta**2+np.square(gama)*n))
        Endown = h*wc*(n-np.sqrt(delta**2+np.square(gama)*n))
        sigmaxx = sigmaxx+(n+0.5)*(q**2/(mt.pi**2*h))*np.exp(-np.square((Ef-Enup)/broadening))+(n-0.5)*(q**2/(mt.pi**2*h))*np.exp(-np.square((Ef-Endown)/broadening))

    ns = ns*10**(16)
    rxx = A*sigmaxx/(np.square((q*ns)/B)+np.square(sigmaxx))/1+c
    return rxx

def df_rashba_fun(B, g, mstar, Er, Ef, broadening, A, c, num):
    h = 6.63 * 10 ** (-34) / (2 * mt.pi)
    k = 1.38 * 10 ** (-23)
    q = 1.6 * 10 ** (-19)
    m = 9.1 * 10 ** (-31)
    u = h / (2 * m) * q
    T = 1.6

    broadening = broadening*q*10**(-3)
    Ef = Ef*q*10**(-3)
    Er = Er*q*10**(-3)
    me = mstar*m
    wc = q*B/me
    lc = np.sqrt(h/(me*wc))
    delta = (1-g*me/(2*m))/2
    ns = num*10**(16)

    Ezero = h*wc*0.5

    sigmaxx = 0
    dsigmaxx = 0
    #NtwoD = 1/(2*mt.pi*np.square(lc))*(1/broadening)*np.sqrt(2/mt.pi)*np.exp(-2*np.square(Ef-Ezero)/broadening**2)
    #ns = NtwoD*(1/(1+np.exp((Ef-Ezero)/(k*T))))


    for n in range(1, 200):
        Enup = h*wc*(n+0.5*np.sqrt(np.square(1-g*me/2)+n*np.square(Er)/(Ef*h*wc)))+g*u*B
        #Enup = h*wc*(n+0.5)+g*u*B
        sigmaxx = sigmaxx+(n+0.5)*np.exp(-np.square((Ef-Enup)/broadening))+Ezero
        Endown = h*wc*(n-0.5*np.sqrt(np.square(1-g*me/2)+n*np.square(Er)/(Ef*h*wc)))-g*u*B
        #Endown = h*wc*(n+0.5)-g*u*B
        sigmaxx = sigmaxx+(n-0.5)*np.exp(-np.square((Ef-Endown)/broadening))

        dEnup = h*q/me*(n+0.5*np.sqrt(np.square(1-g*me/2)+n*np.square(Er)/(Ef*h*wc)))-h*wc*0.25*n*np.square(Er)*me/(np.sqrt(np.square(1-g*me/2)+n*np.square(Er)/(Ef*h*wc))*Ef*h*q*np.square(B))+g*u

        dEndown = h*q/me*(n-0.5*np.sqrt(np.square(1-g*me/2)+n*np.square(Er)/(Ef*h*wc)))+h*wc*0.25*n*np.square(Er)*me/(np.sqrt(np.square(1-g*me/2)+n*np.square(Er)/(Ef*h*wc))*Ef*h*q*np.square(B))-g*u

        dsigmaxx = dsigmaxx+(n+0.5)*2*np.exp(-np.square((Ef-Enup)/broadening))*(Ef-Enup)/broadening**2*dEnup+(n-0.5)*2*np.exp(-np.square((Ef-Endown)/broadening))*(Ef-Endown)/broadening**2*dEndown+0.5*h*q/me


        #NtwoD = NtwoD+1/(2*mt.pi*np.square(lc))*(1/broadening)*np.sqrt(2/mt.pi)*np.exp(-2*np.square(Ef-Enup)/broadening**2)
        #NtwoD = NtwoD+1/(2*mt.pi*np.square(lc))*(1/broadening)*np.sqrt(2/mt.pi)*np.exp(-2*np.square(Ef-Endown)/broadening**2)

        #ns = ns+NtwoD*(1/(1+np.exp((Ef-Enup)/(k*T))))
        #ns = ns+NtwoD*(1/(1+np.exp((Ef-Endown)/(k*T))))






    drxx = A*(sigmaxx*2*B/(q*ns)+np.square(B/(q*ns))*dsigmaxx)/1000000+c
    return drxx

def h_fun(B, ll, es, ef, g, A, c, theta):
    h = 6.63*10**(-34)/(2*mt.pi)
    ne = 10**14
    k = 1.38*10**(-23)
    T = 0.26
    e = 1.6*10**(-19)
    m = 9.1*10**(-31)
    me = 0.58*m
    b_vertical = real_b*mt.cos(theta*mt.pi/180)
    u = e*h/me
    j = np.sqrt(h/(e*B))
    wc = e*b_vertical/me
    ezero = 0.5*h*wc
    sigmaxx = 0




    for n in range(1,200):
        eone = h*wc*(n+0.5*np.sqrt(np.square(1-g*me/(2*m)/mt.cos(theta*mt.pi/180))+n*es*es/(ef*h*wc*1000/e)))
        etwo = h*wc*(n-0.5*np.sqrt(np.square(1-g*me/(2*m)/mt.cos(theta*mt.pi/180))+n*es*es/(ef*h*wc*1000/e)))
        sigmaxx = sigmaxx+(n+0.5)*np.exp(-np.square((ef-eone*1000/e)/ll))+(n-0.5)*np.exp(-np.square((ef-etwo*1000/e)/ll))


    r = c+A*10**(-4)*(e*e*np.square(B)/(ne**2*e**2))/(mt.pi**2*h*1000/(2*mt.pi))*sigmaxx
    return r

def heavydirac_fun(B, ll, lamda, ef, delta, A, c, count):
    h = 6.63*10**(-34)/(2*mt.pi)
    ne = 10**14
    k = 1.38*10**(-23)
    T = 0.26
    e = 1.6*10**(-19)
    m = 9.1*10**(-31)
    me = 0.58*m
    u = e*h/(2*m)
    j = np.sqrt(h/(e*B))
    v = 0.53*10**(6)
    wc = (e*B/me)*1000/e
    sigmaxx = 0
    energy = 0

    for n in range(1,200):

        eone = lamda+np.sqrt(n*np.square(h*wc)+np.square(delta-lamda))
        etwo = -lamda+np.sqrt(n*np.square(h*wc)+np.square(delta+lamda))


        sigmaxx = sigmaxx+(n+0.5)*np.exp(-np.square((ef-eone)/ll))+(n-0.5)*np.exp(-np.square((ef-etwo)/ll))
        if n==count:
            energy = etwo

    r = c+A*10**(-4)*(e*e*np.square(B)/(ne**2*e**2))/(mt.pi**2*h*1000/(2*mt.pi))*sigmaxx
    return r

def heavydiracExpansion_fun(B, ll, lamdaone, lamdatwo, ef, delta, A, c, v, count):
    h = 6.63*10**(-34)/(2*mt.pi)
    ne = 10**14
    k = 1.38*10**(-23)
    T = 0.26
    e = 1.6*10**(-19)
    m = 9.1*10**(-31)
    me = 0.58*m
    u = e*h/(2*m)
    j = np.sqrt(h/(e*B))
    wc = (e*B/me)*1000/e
    sigmaxx = 0
    energy = 0
    v = v*10**(6)

    for n in range(1,200):

        eone = delta+(lamdaone-lamdatwo)+e*h*v*v*n*B*(1000/e)**2/(delta-lamdatwo)
        etwo = delta-(lamdaone-lamdatwo)+e*h*v*v*n*B*(1000/e)**2/(delta+lamdatwo)


        sigmaxx = sigmaxx+(n+0.5)*np.exp(-np.square((ef-eone)/ll))+(n-0.5)*np.exp(-np.square((ef-etwo)/ll))
        if n==count:
            energy = etwo

    eone = delta+(lamdaone-lamdatwo)
    etwo = delta-(lamdaone-lamdatwo)
    sigmaxx=sigmaxx+(0.5)*np.exp(-np.square((ef-eone)/ll))-(0.5)*np.exp(-np.square((ef-etwo)/ll)) #n=0
    r = c+A*10**(-4)*(e*e*np.square(B)/(ne**2*e**2))/(mt.pi**2*h*1000/(2*mt.pi))*sigmaxx
    return r

def cubic_fun(x,a,b,c):
    r = a*x**3+b*x**2+c*x
    return r

def heavydiracandzeeman_fun(B, ll, lamdaone, lamdatwo, ef, delta, A, c, v, count):
    h = 6.63*10**(-34)/(2*mt.pi)
    ne = 10**14
    k = 1.38*10**(-23)
    T = 0.26
    e = 1.6*10**(-19)
    m = 9.1*10**(-31)
    me = 0.58*m
    u = e*h/(2*m)
    j = np.sqrt(h/(e*B))
    wc = (e*B/me)*1000/e
    g = 2.4
    sigmaxx = 0
    energy = 0
    v = v*10**(6)
    deltaone = delta+g*u*B*1000/e
    deltatwo = delta-g*u*B*1000/e

    eone = deltaone+(lamdaone-lamdatwo)
    etwo = deltatwo-(lamdaone-lamdatwo)
    ethree = deltatwo+(lamdaone-lamdatwo)
    efour = deltaone-(lamdaone-lamdatwo)
    sigmaxx=(0.5)*np.exp(-np.square((ef-eone)/ll))-(0.5)*np.exp(-np.square((ef-etwo)/ll))+(0.5)*np.exp(-np.square((ef-efour)/ll))-(0.5)*np.exp(-np.square((ef-ethree)/ll))

    for n in range(1,200):

        eone = deltaone+(lamdaone-lamdatwo)+e*h*v*v*n*B*(1000/e)**2/(deltaone-lamdatwo)
        etwo = deltatwo-(lamdaone-lamdatwo)+e*h*v*v*n*B*(1000/e)**2/(deltatwo+lamdatwo)
        ethree = deltatwo+(lamdaone-lamdatwo)+e*h*v*v*n*B*(1000/e)**2/(deltatwo-lamdatwo)
        efour = deltaone-(lamdaone-lamdatwo)+e*h*v*v*n*B*(1000/e)**2/(deltaone+lamdatwo)


        sigmaxx = sigmaxx+(n+0.5)*np.exp(-np.square((ef-eone)/ll))+(n-0.5)*np.exp(-np.square((ef-etwo)/ll))+(n+0.5)*np.exp(-np.square((ef-efour)/ll))+(n-0.5)*np.exp(-np.square((ef-ethree)/ll))
        if n==count:
            energy = eone

    r = c+A*10**(-4)*(e*e*np.square(B)/(ne**2*e**2))/(mt.pi**2*h*1000/(2*mt.pi))*sigmaxx
    return r

def lk_fun(B, mone, mtwo, bf, d, fone, ftwo, tone, ttwo, A, c):
    h = 6.63 * 10 ** (-34)
    k = 1.38 * 10 ** (-23)
    q = 1.6 * 10 ** (-19)
    m = 9.1 * 10 ** (-31)
    u = h / (2 * m) * q
    T = 0.3
    ns = 5*10**(16)
    sigmaxx = 0

    for n in range(1,4):
        sigmaxx = sigmaxx+(n*4*mt.pi**3*k*T*mone*m*B/(h*q))/np.sinh(n*4*mt.pi**3*k*T*mone*m*B/(h*q))*np.exp(-n*tone*B)*np.cos(n*(2*mt.pi*(bf+d)*B-mt.pi+(fone+ftwo)/2))
        sigmaxx = sigmaxx+(n*4*mt.pi**3*k*T*mtwo*m*B/(h*q))/np.sinh(n*4*mt.pi**3*k*T*mtwo*m*B/(h*q))*np.exp(-n*ttwo*B)*np.cos(n*(2*mt.pi*1*(bf-d)*B-mt.pi+(fone-ftwo)/2))

    rxx = 2*A*np.exp(16*B)*sigmaxx+c
    return rxx

def lk_hcq_fun(B, mone, mtwo, bf, d, fone, ftwo, tone, ttwo, fbplus, fbdecr, A, c):
    h = 6.63 * 10 ** (-34)
    k = 1.38 * 10 ** (-23)
    q = 1.6 * 10 ** (-19)
    m = 9.1 * 10 ** (-31)
    u = h / (2 * m) * q
    T = 0.3
    ns = 5*10**(16)
    sigmaxx = 0
    fone = fone*mt.pi
    ftwo = ftwo*mt.pi
    fbplus = fbplus*mt.pi
    fbdecr = fbdecr*mt.pi

    for n in range(1,11):
        sigmaxx = sigmaxx+(n*4*mt.pi**3*k*T*mone*m*B/(h*q))/np.sinh(n*4*mt.pi**3*k*T*mone*m*B/(h*q))*np.exp(-n*tone*B)*np.cos(n*(2*mt.pi*(bf+d)*B-mt.pi+fone+fbplus))
        sigmaxx = sigmaxx+(n*4*mt.pi**3*k*T*mtwo*m*B/(h*q))/np.sinh(n*4*mt.pi**3*k*T*mtwo*m*B/(h*q))*np.exp(-n*ttwo*B)*np.cos(n*(2*mt.pi*(bf-d)*B-mt.pi+ftwo+fbdecr))

    rxx = 2*A*np.exp(16*B)*sigmaxx+c
    return rxx

def lk_upLLE_hcq_fun(B, mone, mtwo, bf, d, fone, ftwo, tone, ttwo, fbplus, fbdecr, A, c, count):
    h = 6.63 * 10 ** (-34)
    k = 1.38 * 10 ** (-23)
    q = 1.6 * 10 ** (-19)
    m = 9.1 * 10 ** (-31)
    u = h / (2 * m) * q
    T = 0.3
    ns = 5*10**(16)
    sigmaxx = 0
    fone = fone*mt.pi
    ftwo = ftwo*mt.pi
    fbplus = fbplus*mt.pi
    fbdecr = fbdecr*mt.pi

    for n in range(1,4):
        sigmaxx = sigmaxx+(n*4*mt.pi**3*k*T*mone*m*B/(h*q))/np.sinh(n*4*mt.pi**3*k*T*mone*m*B/(h*q))*np.exp(-n*tone*B)*np.cos(n*(2*mt.pi*(bf+d)*B-mt.pi+fone+fbplus))
        sigmaxx = sigmaxx+(n*4*mt.pi**3*k*T*mtwo*m*B/(h*q))/np.sinh(n*4*mt.pi**3*k*T*mtwo*m*B/(h*q))*np.exp(-n*ttwo*B)*np.cos(n*(2*mt.pi*(bf-d)*B-mt.pi+ftwo+fbdecr))
        if n == count:
            energy = sigmaxx
        elif count == 0:
            energy = sigmaxx
    return energy

def lk_downLLE_hcq_fun(B, mone, mtwo, bf, d, fone, ftwo, tone, ttwo, fbplus, fbdecr, A, c, count):
    h = 6.63 * 10 ** (-34)
    k = 1.38 * 10 ** (-23)
    q = 1.6 * 10 ** (-19)
    m = 9.1 * 10 ** (-31)
    u = h / (2 * m) * q
    T = 0.3
    ns = 5*10**(16)
    sigmaxx = 0
    fone = fone*mt.pi
    ftwo = ftwo*mt.pi
    fbplus = fbplus*mt.pi
    fbdecr = fbdecr*mt.pi

    for n in range(1,4):
        sigmaxx = sigmaxx+(n*4*mt.pi**3*k*T*mone*m*B/(h*q))/np.sinh(n*4*mt.pi**3*k*T*mone*m*B/(h*q))*np.exp(-n*tone*B)*np.cos(n*(2*mt.pi*(bf+d)*B-mt.pi+fone+fbplus))
        sigmaxx = sigmaxx+(n*4*mt.pi**3*k*T*mtwo*m*B/(h*q))/np.sinh(n*4*mt.pi**3*k*T*mtwo*m*B/(h*q))*np.exp(-n*ttwo*B)*np.cos(n*(2*mt.pi*(bf-d)*B-mt.pi+ftwo+fbdecr))
        if n == count:
            energy = sigmaxx
        elif count == 0:
            energy = sigmaxx
    return energy
