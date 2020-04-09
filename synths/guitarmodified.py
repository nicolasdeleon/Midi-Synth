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
from scipy.io.wavfile import write
from . import base_synth
import os   
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write
from scipy.signal import argrelextrema
import IPython.display as ipd
import warnings
warnings.filterwarnings('ignore')

class guitarmodified(base_synth):

    def __init__(self,fo,fs,length,*args):
        self.fo=fo
        self.fs=fs
        self.len=length
        self.Ao=args[0]
        self.Io=args[1]
        n_samples=int(length*fs)-1        #para marcar el tiempo
        N=int(fs/fo)
        strechFactor=(fs/fo-N)
        #limites rigurosos ya que 0 < strechFactor < 1
        if (strechFactor < 0.1):
            strechFactor=0.1
        elif (strechFactor > 0.9):
            strechFactor = 0.9
        ro=self.getRO(length,fo,fs,N,strechFactor)
        wavetable = self.Ao * (((2 * np.random.randint(0, 2, N)) - 1).astype(np.float))
        wavetableAux = np.zeros(n_samples)
        previousValue=0
        wavetable=np.concatenate((wavetable,wavetableAux), axis=0)
        for i in range(n_samples):
            wavetable[i+N] = ro* ((1-strechFactor)*wavetable[i] + strechFactor*previousValue)
            previousValue=wavetable[i]
        aux=np.split(wavetable,[N,len(wavetable)])
        self.wavData=aux[1]    
        mx = 1.059*(max(abs(self.wavData))) # escalo para que el pico máximo sea de -.5 dB
        self.wavData = self.wavData/mx
        
    def getRO(self, time,fo,fs,N,strechFactor):
        gainWithStrechFactor = math.sqrt((1-strechFactor)**2 + strechFactor**2 + 2*strechFactor*(1-strechFactor)*np.cos(2*np.pi*(fo/fs)))
        attenuationWithoutStrechFactor = np.cos(np.pi*(fo/fs))**((time*fs)/(N+0.5))
        attenuationWithStrechFactor = gainWithStrechFactor**((time*fs)/(N+strechFactor))
        aux=(log(attenuationWithoutStrechFactor/attenuationWithStrechFactor))/((time*fs)/(N+strechFactor))
        ro=math.exp(aux)
        return ro
