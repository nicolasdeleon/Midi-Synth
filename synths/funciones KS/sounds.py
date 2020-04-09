#!/usr/bin/python

from scipy import*
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib.pyplot import plot,xscale,show
import matplotlib.patches as patches
import numpy as np
import matplotlib.pyplot as plt
import matplotlib, sys
import matplotlib.path as mpath
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from scipy import signal
matplotlib.use('TkAgg')
import math
import IPython.display as ipd
import sounddevice as sd
import librosa
from scipy.io.wavfile import write
from sympy.solvers import solve
from sympy import Symbol
import simpleaudio as sa

def guitar_modified(fs, fo, time, amplitud):
  n_samples=time*fs
  N=int(fs/fo)
  strechFactor=(fs/fo-N)
  #limites rigurosos ya que 0 < strechFactor < 1
  if (strechFactor < 0.1):
    strechFactor=0.1
  elif (strechFactor > 0.9):
    strechFactor = 0.9
  ro=getRO(time,fo,fs,N,strechFactor)
  wavetable = amplitud * (((2 * np.random.randint(0, 2, N)) - 1).astype(np.float))
  wavetableAux = np.zeros(n_samples)
  previousValue=0
  wavetable=np.concatenate((wavetable,wavetableAux), axis=0)
  for i in range(n_samples):
    wavetable[i+N] = ro* ((1-strechFactor)*wavetable[i] + strechFactor*previousValue)
    previousValue=wavetable[i]
  return wavetable

def drum(fs, fo, time, amplitud):
  n_samples=time*fs
  N=int(fs/fo)
  wavetable = amplitud * np.ones(N)
  wavetableAux = np.zeros(n_samples)
  previousValue=0
  wavetable=np.concatenate((wavetable,wavetableAux), axis=0)
  for i in range(n_samples):
    r = np.random.binomial(1, 0.5)
    sign = float(r == 1) * 2 - 1
    wavetable[i+N] = sign*(0.5*wavetable[i] + 0.5*previousValue)
    previousValue=wavetable[i]
  return wavetable

def guitar(fs, fo, time, amplitud, ro = 1):
  n_samples=time*fs
  N=int(fs/fo)
  wavetable = amplitud * (((2 * np.random.randint(0, 2, N)) - 1).astype(np.float))
  wavetableAux = np.zeros(n_samples)
  previousValue=0
  wavetable=np.concatenate((wavetable,wavetableAux), axis=0)
  for i in range(n_samples):
    wavetable[i+N] = ro * (0.5*wavetable[i] + 0.5*previousValue)
    previousValue=wavetable[i]
  return wavetable

def harp(fs, fo, time, amplitud):
  n_samples=time*fs
  N=int(fs/fo)
  wavetable = amplitud * (((2 * np.random.randint(0, 2, N)) - 1).astype(np.float))
  wavetableAux = np.zeros(n_samples)
  previousValue=0
  wavetable=np.concatenate((wavetable,wavetableAux), axis=0)
  for i in range(n_samples):
    wavetable[i+N] = -(0.5*wavetable[i] + 0.5*previousValue)
    previousValue=wavetable[i]
  return wavetable

def electric_guitar(fs, fo, time, amplitud):
  x = guitar(fs, fo, time, amplitud, 0.997)
  for i in range(len(x)):
    if (x[i]>1):
      x[i]=2/3
    elif (x[i]<-1):
      x[i]=-2/3
    else:
      a=x[i]
      x[i]= (a-(a**3)/3)
  return x

def getRO(time,fo,fs,N,strechFactor):
  gainWithStrechFactor = math.sqrt((1-strechFactor)**2 + strechFactor**2 + 2*strechFactor*(1-strechFactor)*np.cos(2*np.pi*(fo/fs)))
  attenuationWithoutStrechFactor = np.cos(np.pi*(fo/fs))**((time*fs)/(N+0.5))
  attenuationWithStrechFactor = gainWithStrechFactor**((time*fs)/(N+strechFactor))
  aux=(log(attenuationWithoutStrechFactor/attenuationWithStrechFactor))/((time*fs)/(N+strechFactor))
  ro=math.exp(aux)
  return ro

def playSound(arr, fs=44100):
    arr *= 32767 / max(abs(arr))
    arr = arr.astype(np.int16)
    play_obj = sa.play_buffer(arr, 1, 2, fs)
    play_obj.wait_done()

fs = 44100 # sample rate
#e=basic_karplus_strong(fs,200,2,3,1)
#q=guitar(fs,440,2,20)
w=guitar_modified(fs,550,2,20)
s=electric_guitar(fs,550,4,20)
#e=drum(fs,50,2,20)
#r=harp(fs,380,2,20)

#playSound(q, fs=fs)  
playSound(w, fs=fs)  
playSound(s, fs=fs)
#playSound(e, fs=fs)  
#playSound(r, fs=fs)  