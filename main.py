from os import close
from tkinter import font
from tkinter.constants import E
from typing import final
import PySimpleGUI as sg
from time import sleep

sg.LOOK_AND_FEEL_TABLE['MyNewTheme'] = {'BACKGROUND': '#CDCDCD',
                                            'TEXT': 'black',
                                            'INPUT': 'black',
                                            'TEXT_INPUT': '#cccccc',
                                            'SCROLL': '#c7e78b',
                                            'BUTTON': ('#eeeeee', '#222222'),
                                            'PROGRESS': ('#01826B', '#D0D0D0'),
                                            'BORDER': 1, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0,
                                            }
sg.theme('MyNewTheme')
startingPoint, finishPoint = [], []

buttons = sg.Column([
                     [sg.Button('✏️', disabled=True), sg.Text('Start from: ', background_color='green'), sg.Text(startingPoint, key='start')],
                     [sg.Button('✏️', key='finishEdit'), sg.Text('Finish: ', background_color='#FF5733'), sg.Text(finishPoint, key='finish')],
                     [sg.Button('Show Points', key='show')],
                     [sg.Button('Calculate', size=(12, 1))],
                     [sg.Text("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")],
                     [sg.Button('Clear', key='clear', size=(8, 1))]
                     ])

mainWindowLayout = [[sg.Graph((500, 500), (-100, -100), (100, 100), background_color=('#eeeeee'), key='graph', enable_events=True), buttons],
                     [sg.Button('Exit', key='EXIT')]]

window = sg.Window('dijkstrasAlgorithm', mainWindowLayout, finalize=True)
graph = window['graph']

def drawAxis():
    # X axis
    graph.draw_line((-100, 0), (100, 0))
    graph.draw_text('1', (10, 10))
    for x in range(-100, 101, 10):    
        graph.DrawLine((x, -2), (x, 2))    
    # Y axis
    graph.draw_line((0, -100), (0, 100))
    for y in range(-100, 101, 10):    
        graph.DrawLine((-2, y), (2, y))    

pointIterator = 0
pointsDict = {}
while True:
    drawAxis()
    event, value = window.read()

    if event == sg.WIN_CLOSED or event == 'EXIT':
        window.Close()
        break

    elif event == 'graph':
        x = int(round(value['graph'][0]/10))*10
        y = int(round(value['graph'][1]/10))*10
        pointsDict[pointIterator] = (int(x/10), int(y/10))

        if pointIterator == 0:
            startingPoint = [int(x/10), int(y/10)]
            window['start'].update(startingPoint)
            graph.draw_point((x, y), color='green', size=4)
        else:
            graph.draw_point((x, y), color='blue', size=3)

        pointIterator +=1
        
    elif event == 'clear':
        graph.erase()
        pointsDict.clear()
        pointIterator = 0
        window['start'].update([])
    
    elif event == 'show':
        print(pointsDict)

    elif event == 'Calculate':
        print(pointsDict)
        actualPoint = pointsDict.get(0)
        x1, y1 = actualPoint[0], actualPoint[1]
        del pointsDict[0]
        
        for i in range(len(pointsDict)):
            distanceDict = {}
            for e in pointsDict:
                x2, y2 = pointsDict.get(e)[0], pointsDict.get(e)[1]
                distanceDict[e] = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
            try:
                closestPoint = min(distanceDict.values())
            except:
                pass

            for e in distanceDict:
                if distanceDict.get(e) == closestPoint:
                    x2, y2 = pointsDict.get(e)[0], pointsDict.get(e)[1]
                    graph.draw_line((x1*10, y1*10), (x2*10, y2*10))
                    x1, y1 = x2, y2
                    del pointsDict[e]
            distanceDict.clear()
        
        print(pointsDict)
    elif event == 'finishEdit':
        window.Hide()

        inputColumn = [[sg.Text('X: '), sg.Input(key='inputX', size=(4, 1))],
                             [sg.Text('Y: '), sg.Input(key='inputY', size=(4, 1))]]

        finishInputLayout = [[sg.Column(inputColumn), sg.Button('OK')]]
        finishInput = sg.Window('Input', finishInputLayout)

        while True:
            event, value = finishInput.read()

            if event == 'OK':
                finishPoint = [int(value['inputX'])*10, int(value['inputY'])*10]
                pointsDict[pointIterator] = (int(value['inputX']), int(value['inputY']))
                finishInput.Close()
                window.UnHide()
                window['finish'].update(finishPoint)
                graph.draw_point(finishPoint, color='#FF5733', size=4)
                break