"""
v.1.003

Observer to make sidebearings magnetic to outline modifications.  
Its aim to be used as a startup script so it can be activated and deactivated whenever you need.

Version history:
    v1.002: first private release
    v1.003: fix magnet multiple drawing

"""

from defconAppKit.windows.baseWindow import BaseWindowController
from mojo.events import addObserver, removeObserver, clearObservers, extractNSEvent
from mojo.roboFont import CurrentGlyph
from mojo.UI import CurrentGlyphWindow, UpdateCurrentGlyphView
import mojo.drawingTools as ctx
import AppKit


pressed_key = "M"

class magneticMetrics():
    
    clearObservers()

    def __init__(self):
        self.leftMargin = None
        self.rightMargin = None
        self.status = 1
        self.updateGlyph()

        addObserver(self, "keyWasPressed", "keyDown")
        addObserver(self, "glyphWindowOpened", "glyphWindowDidOpen")

    def keyWasPressed(self, info):
        glyph = self.glyph
        
        if CurrentGlyph():
            glyph = CurrentGlyph()
            self.glyph = glyph

        
        if glyph is not None:

            event = info["event"]
            characters = event.characters()
            shiftDown = extractNSEvent(info)['shiftDown']
        
        
            if shiftDown and characters == pressed_key :
                if self.status == 0:
                    addObserver(self, "viewDidChangeGlyph", "viewDidChangeGlyph")
                    addObserver(self, "glyphChanged", "draw")
                    addObserver(self, "drawText", "draw")
                    
                    self.updateGlyph()
                    self.updateGlyphView()
                    self.status = 1
                    self.updateGlyph()
                

                else:
                    self.status = 0
                
                    removeObserver(self, "draw")

                    self.updateGlyph()
                    self.updateGlyphView()

                    addObserver(self, "viewDidChangeGlyph", "viewDidChangeGlyph")
                    addObserver(self, "glyphChanged", "draw")
                
                


    def viewDidChangeGlyph(self, notification):
        # notification when the glyph changes in the glyph view
        glyph = CurrentGlyph()
        self.leftMargin = glyph.leftMargin
        self.rightMargin = glyph.rightMargin
        
        removeObserver(self, "draw")

        self.unsubscribeGlyph()
        self.subscribeGlyph(glyph)
        self.updateGlyph()
        self.updateGlyphView()

    def glyphChanged(self, notification):
        glyph = self.glyph
        
        if CurrentGlyph():
            glyph = CurrentGlyph()
            self.glyph = glyph

        
        if glyph is not None:
        
            if self.status == 0:
                glyph.leftMargin = self.leftMargin
                glyph.rightMargin = self.rightMargin
            # Sends the glyph margins when tool isn’t active
            # so when you activate it the good margins will be used
            if self.status == 1:
                self.leftMargin = glyph.leftMargin
                self.rightMargin = glyph.rightMargin
            
            
    def a_magnet(self):
        ctx.newPath()
        ctx.fill(0, 0, 0, .75)
        ctx.moveTo((25, 15))
        ctx.curveTo((20.0, 15.0), (17, 16), (17, 20))
        ctx.lineTo((17, 45))
        ctx.curveTo((17.0, 48.0), (15, 50), (9, 50))
        ctx.curveTo((2, 50), (0, 48.0), (0, 45))
        ctx.lineTo((0, 22))
        ctx.curveTo((0, 6), (9, 0), (25, 0))
        ctx.curveTo((41.0, 0.0), (50, 6), (50, 22))
        ctx.lineTo((50, 45))
        ctx.curveTo((50, 48), (48, 50), (41, 50))
        ctx.curveTo((35, 50), (33, 48), (33, 45))
        ctx.lineTo((33, 20))
        ctx.curveTo((33, 16), (30, 15), (25, 15))
        ctx.closePath()
        ctx.drawPath()

        ctx.newPath()
        ctx.fill(1)
        ctx.moveTo((25, 3))
        ctx.curveTo((11.0, 3), (3, 8), (3, 22))
        ctx.lineTo((3, 34))
        ctx.lineTo((14, 34))
        ctx.lineTo((14, 20))
        ctx.curveTo((14.0, 14.0), (18, 12), (25, 12))
        ctx.curveTo((32.0, 12.0), (36.0, 14.0), (36, 20))
        ctx.lineTo((36, 34))
        ctx.lineTo((47, 34))
        ctx.lineTo((47, 22))
        ctx.curveTo((47, 8), (39, 3), (25, 3))
        ctx.closePath()
        ctx.drawPath()

    def drawText(self, scale):
        glyph = self.glyph
        scaleValue = scale["scale"]
        
        magnet_scale = 3 # The original magnet drawing is too big, this value reduce it
        
        ctx.save()
        ctx.translate(-25*(scaleValue/magnet_scale), CurrentFont().info.capHeight/magnet_scale)
        ctx.scale(scaleValue/magnet_scale)
        self.a_magnet()        
        ctx.restore()


        ctx.save()
        ctx.translate(-25*(scaleValue/magnet_scale) + glyph.width, CurrentFont().info.capHeight/magnet_scale)
        ctx.scale(scaleValue/magnet_scale)
        self.a_magnet()        
        ctx.restore()
        

    def glyphWindowOpened(self, notification):
        self.glyph = CurrentGlyph()
        self.leftMargin = self.glyph.leftMargin
        self.rightMargin = self.glyph.rightMargin
        
        self.updateGlyph()

        

    def updateGlyphView(self):
        # update the current glyph view
        UpdateCurrentGlyphView()


    def updateGlyph(self):
        if CurrentGlyph():
            self.glyph = CurrentGlyph()
            self.leftMargin = self.glyph.leftMargin
            if self.status == 1:
                removeObserver(self, "draw")
                self.updateGlyphView()
            if self.status == 0:
                addObserver(self, "drawText", "draw")
                self.updateGlyphView()
            
        

    def subscribeGlyph(self, glyph):
        # subscribe to glyph
        self.glyph = glyph
        # add an observer to glyph data changes
        self.glyph.addObserver(self, "glyphChanged", "Glyph.Changed")
        self.updateGlyphView()

    def unsubscribeGlyph(self):
        # unsubscribe from glyph
        if self.glyph is None:
            return
        # remove observer from the glyph
        self.glyph.removeObserver(self, "Glyph.Changed")
        self.glyph.removeObserver(self, "Glyph.draw")
        self.updateGlyphView()


magneticMetrics()
