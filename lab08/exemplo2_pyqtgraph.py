#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
import serial
import atexit
import time
interval = 0

def inicia_coleta():
    conexaoSerial.write(b'i')

def para_coleta():
    conexaoSerial.write(b'p')

def saindo():
    conexaoSerial.write(b'p')
    print('Saindo')

def intervalo():
    global interval
    conexaoSerial.write(b'p')
    #time.sleep(0.2)
    #ndados = conexaoSerial.inWaiting()
    #print(f'Temos {ndados} bytes esperando...')
    #for i in range(ndados):
    #    print(f'lendo byte {i}')
    #    dado4 = conexaoSerial.read()
    #    interval = dado4
    
    time.sleep(0.2)
        
    #time.sleep(0.2)
    #conexaoSerial.flush()
    #time.sleep(0.2)
    
    while conexaoSerial.inWaiting() > 0:
        conexaoSerial.read()
        time.sleep(0.02)
    
    print(f'enviando a')
    conexaoSerial.write(b'a')
    time.sleep(0.1)
    print(f'lendo')
    while conexaoSerial.inWaiting() == 0:
        print('esperando')
        #conexaoSerial.write(b'a')
        time.sleep(0.1)
        
    if conexaoSerial.inWaiting() > 0:
        interval = conexaoSerial.read()
        print(f'atraso = {ord(interval)}')
        texto1.setText(f"Intervalo: {ord(interval)} ms")
    else:
        print('nao deu tempo')
    
    conexaoSerial.write(b'i')   
    
def aumentar():
    conexaoSerial.write(b'm')
    print('Aumentou')
    
def diminuir():
    conexaoSerial.write(b'u')
    print('Diminuiu')


def update():
    global data1, curve1, ptr1, conexaoSerial, x_atual, npontos, previousTime
    esperando = conexaoSerial.inWaiting()
    if esperando > 1:
        dado1 = conexaoSerial.read()
        dado2 = conexaoSerial.read()
        novodado = float( (ord(dado1) + ord(dado2)*256.0)*5.0/1023.0 )
        
        data1[x_atual] = novodado
        data1[(x_atual+1)%npontos] = np.nan
        x_atual = x_atual+1
        if x_atual >= npontos:
            x_atual = 0
        
        curve1.setData(data1, connect="finite")
        actualTime = time.time()*1000
        taxa = str(round(actualTime-previousTime))
        previousTime = actualTime
        texto.setText("taxa: "+taxa.zfill(3)+"ms" )
        
        texto2.setText("waiting: "+str(esperando-2)+"bytes")


win = pg.GraphicsWindow()
win.setWindowTitle('Coletando dados do Arduino via Porta Serial')

npontos = 800
x_atual = 0
p1 = win.addPlot()
p1.setYRange(0,5,padding=0)
data1 = np.zeros(npontos)
curve1 = p1.plot(data1)
ptr1 = 0

previousTime = time.time()*1000 # pega a hora atual, em milissegundos
texto = pg.TextItem(text="", color=(255,255,0), anchor=(0,1))
texto1 = pg.TextItem(text="Interval: ", color=(255,255,0), anchor=(1,0))
texto2 = pg.TextItem(text="Trafego: ", color=(255,255,0), anchor=(0,0))


p1.addItem(texto)
p1.addItem(texto1)
p1.addItem(texto2)
texto.setPos(0,0) # adiciona o texto na posicao (0,0) do grafico
texto1.setPos(npontos,5)
texto2.setPos(0,5)

proxy1 = QtGui.QGraphicsProxyWidget()
botao1 = QtGui.QPushButton('Inicia')
proxy1.setWidget(botao1)
botao1.clicked.connect(inicia_coleta)

proxy2 = QtGui.QGraphicsProxyWidget()
botao2 = QtGui.QPushButton('Para')
proxy2.setWidget(botao2)
botao2.clicked.connect(para_coleta)

proxy3 = QtGui.QGraphicsProxyWidget()
botao3 = QtGui.QPushButton('Intervalo')
proxy3.setWidget(botao3)
botao3.clicked.connect(intervalo)

proxy4 = QtGui.QGraphicsProxyWidget()
botao4 = QtGui.QPushButton('Aumentar')
proxy4.setWidget(botao4)
botao4.clicked.connect(aumentar)

proxy5 = QtGui.QGraphicsProxyWidget()
botao5 = QtGui.QPushButton('Diminuir')
proxy5.setWidget(botao5)
botao5.clicked.connect(diminuir)


p2 = win.addLayout(row=1, col=0)
p2.addItem(proxy1,row=0,col=0)
p2.addItem(proxy2,row=1,col=0)
p2.addItem(proxy3,row=2,col=0)


p3 = win.addLayout(row=2, col=0)
p3.addItem(proxy4,row=3,col=0)
p3.addItem(proxy5,row=3,col=1)


conexaoSerial = serial.Serial('/dev/ttyACM0',115200)
conexaoSerial.write(b'i')
        
# inicia timer rodando o mais rápido possível
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)

atexit.register(saindo)

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    QtGui.QApplication.instance().exec_()
