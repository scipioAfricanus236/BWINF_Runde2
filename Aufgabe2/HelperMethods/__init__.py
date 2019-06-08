import sys 
sys.path.append("/Users/juliuside/Desktop/BWINF_Runde2/Aufgabe2/HelperMethods")

from textToPolygones import TextToPolygones
from draw import Draw
from polygonesToAngle import PolygonesToAngle
from sequenceToEdges import SequenceToEdges
from edgesToFile import EdgesToFile
from moveTogether import MoveTogether

import random


def textToTriangles(file):
    """
        This function converts an input textfile into a list of [smallest, angle, largest length]
    """
    text = TextToPolygones(file).getData()    
    toAngle = PolygonesToAngle(text)
    triangles = toAngle.triangles
    
    return triangles


def sequenceToEdges(sequences):
    sequenceToEdges = SequenceToEdges(sequences)
    edges = sequenceToEdges.edges
    
    return [edges, fitness(sequences)]


def moveTogether(edges):
    """ moves edges together and finds the difference in length to the first result """
    first = (edges[len(edges) - 1][len(edges[len(edges) - 1]) - 1][0][0])
    mv = MoveTogether(edges)
    mv.moveTogether()
    edges = mv.transformed_edges
    last = edges[len(edges) - 1][0][0]
    fitness = int(last - first)

    return [edges, fitness]


def fitness(sequences):
    """
        input: sequences of triangles with (angle, length, edges)
    """
    return SequenceToEdges(sequences).middleFitness


def completeFitness(sequences):
    return SequenceToEdges(sequences).fitness

def draw(edges, scale, filename):
    for edge in edges:
            for point in edge:
                point[0] = int(point[0] * scale)
                point[1] = int(point[1] * scale)

    drawing = Draw(None, filename)
    drawing.edges(edges)

def save(edges, distance, filename):
    saving = EdgesToFile(edges, distance, filename)
    saving.save()

