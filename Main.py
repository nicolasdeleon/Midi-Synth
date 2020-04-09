import mido as mido
import numpy as np
import scipy.io.wavfile
from scipy.io.wavfile import write

from customio.userInteraction import RequestUserInfo
from custommidi.handleMidi import (MidParser, Parametros, note2Frec,
                                   sinthesize, specto_patronum)


def Main():

  """                                     --- USER INTERFACE ---                                          
        Le pido el archivo mid a procesar al usuario y  si va a querer generar un espectograma del audio generado
  """
  nombredeArchivo, BooleanEspectograma = RequestUserInfo()

  """                                   ---     MIDI PARSING   ---
          In this module we will parse the mid file, to the point that we can then sintheize the
          notes that correspond to the mid parameters
  """
  mid = mido.MidiFile(str(nombredeArchivo))
  print('Parsing Midi...')
  arregloDeTracks = MidParser(mid)
  print('Midi Parsed')
  print('Total Midi Time =', mid.length)

  Time = mid.length
  print('Total Midi Time =', Time)  
  
  """                           ---     REQUEST INSTRUMENTS TO SINTH  ---
        Request the instrument for the respective tracks
  """

  # PRINT ALL TRACKS
  nombreDeTracks = []
  for tracka in arregloDeTracks:
    nombreDeTracks.append(tracka[0])
  print(nombreDeTracks)

  # REQUEST INSTRUMENT
  print("Elegir en orden los instrumentos: \n'violin' \n'dbass' \n'drum'Conc \n'guitar'  \n'harp' \n'bell' \n'clarinet' \n'trumpet' \npara cada uno de los siguientes tracks:")
  nombreDeInstrumentos = []
  while (len(nombreDeInstrumentos)!=len(nombreDeTracks)):
    instr= input()
    if(instr=='bell' or instr=='clarinet' or instr=='violin' or instr=='dbass' or instr=='trumpet' or instr=='drum' or instr=='guitar' or instr=='harp' or instr==''):
      nombreDeInstrumentos.append(instr)
    else:
      print("Error input")
      exit()

  # SHOW CHOSEN
  print(nombreDeInstrumentos)

  """                                      ---     SINTHESIZE  ---                    
        Perform sinthezise for each respective track with the intrument selected
  """

  print("Sintetizando....")
  fs = 44100
  Cancion = sinthesize(fs, Time, nombreDeInstrumentos, arregloDeTracks, nombreDeTracks)
  print("Fin de Sintetización")

  """                                      ---     EXPORT FILE  ---                       
  """

  FileName = f'{nombredeArchivo[:len(nombredeArchivo)-4]}.wav'
  print('Exporting 2 wav', FileName)
  wavData = np.asarray(30000*Cancion, dtype=np.int16)       
  write(FileName, fs, wavData)

  """                                      ---     SHOW EXPECTOGRAM   ---                       
  """

  if(BooleanEspectograma):
    print("Expectograma: ")
    specto_patronum(Cancion, fs)

if __name__ == "__main__":
    Main()
