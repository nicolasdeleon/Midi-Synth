import matplotlib.pyplot as plt
import mido as mido
import numpy as np
from scipy import signal

import synths


class Parametros:
  """ Voy a guardar mis parametros y sus caracteristicas en objetos Parametros """
  velocidad = None
  channel = None
  t = None
  def __init__(self, velocidad, channel, t):
      self.velocidad = velocidad
      self.channel = channel
      self.t = t

def note2Frec(n):
    """ 
      Suppose that two notes have frequencies f1 and f2, and a frequency ratio of f2/f1.
      An octave is a ratio of 2:1, so the number of octaves between f2 and f1 is
      no  =  log2(f2/f1).
      Now to divide the octave into smaller units. 
      In equal temperament, where all semitones have the same frequency ratio of 21/12, conversion between note name and frequency is simple. 
      First, one needs a reference note and frequency.
      This is usually A4, which is often set at 440 Hz.
      For a note that lies n semitones higher (or −n semitones lower), the frequency is then
      fn  =  2n/12*440 Hz.
    """ 
    f=((2**((n-69)/12)))*440
    return f


def specto_patronum(senal, frec_sampleo, overlap=None, ventana=None, largo_ventana=None):
    if ventana is None:
      f, t, Sxx=signal.spectrogram(senal, frec_sampleo, noverlap=overlap)
    else:
      new_ventana=ventana(largo_ventana)          # para crear una ventana nueva y pasarsela como arreglo al espectograma
      f,t, Sxx=signal.spectrogram(senal, frec_sampleo, new_ventana, noverlap=overlap)
    
    # dibujo el espectro 
    colores=plt.get_cmap('jet')
    plt.figure('Espectrograma')
    im = plt.pcolormesh(t, f, Sxx,cmap=colores)
    plt.ylabel('Frecuencia [Hz]')
    plt.xlabel('Tiempo [sec]')
    plt.title('Espectrograma Violin')
    plt.colorbar(im)
    plt.show()


def MidParser(MiFile):

  ticks = MiFile.ticks_per_beat
  arregloDeTracks = []
  variabledetracks=0
  tempoind=0
  arreglotempos = []
  FlagDePrimerTrack=1

  for track in MiFile.tracks:
      #itero por todos los elementos o mensajes de mi archivo midi
      #itero primero para ver de buscar mi tempo: saco del arreglo de tempos ó de mi track 
      #Guardo por cada iteracion para cada nota los tiempos y los parametros en NoteDictionary
      #Estructura: Diccionario de arreglos en los que cada key es la nota y cada arreglo contiene Objeto Paramtetro con tiempo channel y velocidad     
    print('Parsing... ', track)
    NoteDictionary  = {}
    CurrentTime = 0
    CurrentTimeTempos = 0
    tempoanterior = 0
    if(FlagDePrimerTrack):
      #Parseo el primer track para ver si tiene estipulados todos los tempos de la cancion.
      #De ser asi creo mi vector de tempos en donde coloco el valor del tempo y el tiempo en s en el que ocurre
      for message in track:
        tempoanterior=message.time
        CurrentTimeTempos + mido.tick2second(message.time,ticks,tempoanterior)
        if(message.type=='set_tempo'):
          arreglotempos.append([message.tempo,CurrentTimeTempos])  
      FlagDePrimerTrack=0

    for message in track:
        if(len(arreglotempos) > 1): ##si hay arreglo de tempos entonces me muevo con esto para fijar mi tempo
          tempoind=arreglotempos[0][0] ##a medida que avanzo guardo 
        else:
          if(message.type=='set_tempo'): 
            tempoind=message.tempo
            
        CurrentTime = CurrentTime + mido.tick2second(message.time,ticks,tempoind)
        if(message.type=='note_on' or message.type == 'note_off'):
            if not message.note in NoteDictionary:
              NoteDictionary[message.note] = []
              NoteDictionary[message.note].append(Parametros(message.velocity,message.channel,CurrentTime))
            else:   
              NoteDictionary[message.note].append(Parametros(message.velocity,message.channel,CurrentTime))
    
    #Armo un arreglo con todos los tracks y sus nombres (si no tiene se lo asigno)
    #Esto me sirve para despues asignar instrumentos a cada track
    if(len(NoteDictionary)!=0):      
        if (track.name==''):
            arregloDeTracks.append(['track'+ str(variabledetracks) ,NoteDictionary])
            variabledetracks=variabledetracks+1
        else:    
            arregloDeTracks.append([track.name,NoteDictionary])

  return arregloDeTracks


def sinthesize(fs, Time, nombreDeInstrumentos, arregloDeTracks, nombreDeTracks):
  
  #Creo vectores
  CancionTrack = np.arange(0, Time, 1/fs)
  CancionTrack = np.asarray(CancionTrack)
  Cancion = CancionTrack
  #Inicializando vectores en 0
  for index in range(len(CancionTrack)):
    Cancion[index] = 0
    CancionTrack[index] = 0
  print("Longitud Vector: " , len(Cancion))

  contadorDeInstrumentos = 0
  for track in arregloDeTracks:

    print('Sintetizando: ' , track[0])
    y = [] 
    print('Con Instrumento: ', nombreDeInstrumentos[contadorDeInstrumentos])

    for nota in track[1] :
      print('Nota: ',nota)
      for i in range(len(track[1].get(nota))-1):
        if i%2 == 0 : #Asumo que todas las notas impares son Velocity=0
          deltaT = track[1].get(nota)[i+1].t-track[1].get(nota)[i].t
          Fo = note2Frec(nota)
          tiempoinicial= track[1].get(nota)[i].t
          if(deltaT!=0 and nombreDeInstrumentos[contadorDeInstrumentos]!=''):   
            y=synths.create(
              nombreDeInstrumentos[contadorDeInstrumentos], 
              Fo, 
              fs,
              deltaT,
              track[1].get(nota)[i].velocidad,
              2
              ).getVector()    
            
            for j in range(len(y)):
              try :
                Cancion[int(tiempoinicial*fs)+j]= Cancion[int(tiempoinicial*fs)+j]+y[j]
              except IndexError:
                {}   
    contadorDeInstrumentos=contadorDeInstrumentos+1         
  
  return Cancion/(len(nombreDeTracks)+2)
