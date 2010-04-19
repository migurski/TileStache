"""

<stack> 
	<layer src="road-names" /> 
	<layer src="road-inlines" /> 
	<layer src="road-outlines"> 
		<mask src="road-name-halos" /> 
	</layer> 
	<layer color="#ccc"/> 
</stack>
"""

import sys

from os.path import join as pathjoin
from xml.dom.minidom import parse as parseXML
from StringIO import StringIO

import PIL.Image
import TileStache

class Layer:

    def __init__(self):
        pass

    def render(self):
        pass

class Stack:

    def __init__(self, layers):
        self.layers = layers

    def render(self):
        pass

def makeLayer(node):
    """
    """
    print >> sys.stderr, 'Making a layer.'

    return Layer()

def makeStack(node):
    """
    """
    layers = []
    
    for child in node.childNodes:
        if child.nodeType == child.ELEMENT_NODE:
            if child.tagName == 'stack':
                stack = makeStack(child)
                layers.append(stack)
            
            elif child.tagName == 'layer':
                layer = makeLayer(child)
                layers.append(layer)

            else:
                raise Exception('Unknown element "%s"' % child.tagName)

    print >> sys.stderr, 'Making a stack with %d layers' % len(layers)

    return Stack(layers)

class Composite:

    metatileOK = False

    def __init__(self, layer, stackfile=None):
        self.layer = layer
        
        stackfile = pathjoin(self.layer.config.dirpath, stackfile)
        stack = parseXML(stackfile).firstChild
        
        assert stack.tagName == 'stack', \
               'Expecting root element "stack" but got "%s"' % stack.tagName

        self.stack = stack

    def renderTile(self, width, height, srs, coord):
    
        makeStack(self.stack)
    
        layer = self.layer.config.layers['base']
        mime, body = TileStache.handleRequest(layer, coord, 'png')
        img_base = PIL.Image.open(StringIO(body))

        layer = self.layer.config.layers['outlines']
        mime, body = TileStache.handleRequest(layer, coord, 'png')
        img_outlines = PIL.Image.open(StringIO(body))
        
        layer = self.layer.config.layers['halos']
        mime, body = TileStache.handleRequest(layer, coord, 'png')
        img_halos = PIL.Image.open(StringIO(body))
        
        img_outlinesmask = PIL.Image.new('RGBA', img_outlines.size, (0, 0, 0, 0))
        img_outlinesmask.paste(img_outlines, None, img_halos.convert('L'))

        layer = self.layer.config.layers['streets']
        mime, body = TileStache.handleRequest(layer, coord, 'png')
        img_streets = PIL.Image.open(StringIO(body))
        
        img = PIL.Image.new('RGBA', (256, 256))
        
        img.paste(img_base, (0, 0), img_base)
        img.paste(img_outlines, None, img_outlinesmask)
        img.paste(img_streets, (0, 0), img_streets)
        
        return img
    
        pass

    def renderArea(self, width, height, srs, xmin, ymin, xmax, ymax):
        pass
