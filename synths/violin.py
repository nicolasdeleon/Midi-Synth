from . import base_synth
import numpy as np
import matplotlib.pyplot as plt
from math import *
from IPython.display import (
    Audio, display, clear_output)
from functools import partial

from scipy.signal import find_peaks
from scipy.io import wavfile
from scipy.fftpack import fft
from scipy import signal

from scipy.interpolate import pchip



class violin(base_synth):

    def __init__(self,f0,fs,duration,*args):
        
        MAXFREC=20000
        BASEFREC=220
        harmheight=0.01
        MDIST=50
        
        rate,note=wavfile.read("synths\Audios\A3violin.wav")
        L=len(note)/rate
        
        yf=fft(note,rate)[0:MAXFREC]
        normyf=abs(yf)/np.amax(abs(yf))
        
        peaks,values=find_peaks(normyf,height=harmheight,distance=BASEFREC/10)
        
        f,t,Sxx=signal.spectrogram(note,fs=rate,window="hamming",scaling='spectrum',nperseg=int(rate/BASEFREC))
        
        t2=np.linspace(0,duration,int(fs * duration))
        out=np.zeros(int(fs*duration))

        nSxx=np.zeros((len(Sxx)+1,len(t)+1))
        nt=np.concatenate(([0],t))
        
        for i in range(0,len(Sxx)):
            Sxx[i]=Sxx[i]/np.amax(Sxx[i])    
            nSxx[i]=np.concatenate(([0],Sxx[i]))
            
        for i in range(0,len(peaks)):
    
            npe,nva=find_peaks(Sxx[int(peaks[i]/BASEFREC)],distance=MDIST/nt[-1])    
            test1=Sxx[int(peaks[i]/BASEFREC)][npe]
            test2=nt[npe]
            env=pchip(test2*duration/L,test1*duration/L)
            out+=np.sin(peaks[i]*2*np.pi*t2*f0/BASEFREC)*abs(normyf[peaks[i]])*abs(env(t2))
    
        
        self.wavData = out
        #mx = 1.059*(max(abs(self.wavData)))
       # self.wavData = self.wavData/mx

    
  
