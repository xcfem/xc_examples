
import BOPTools.SplitFeatures
import CompoundTools.Explode

document= App.ActiveDocument

def cutSurfaces(document, surfaces, baseName, tools):
    ''' Cut the surfaces argument.
   
    :param document: document containing the surfaces to cut. 
    :param surfaces: surfaces to cut.
    :param baseName: base name for the resulting object.
    :param tools: cutting tools.
    '''
    for name in surfaces:
        surf= document.getObjectsByLabel(name)[0]
        f = BOPTools.SplitFeatures.makeSlice(name= baseName)
        f.Base = surf
        f.Tools = tools
        f.Mode= 'Split'
        f.Proxy.execute(f)
        f.purgeTouched()
        for obj in f.ViewObject.Proxy.claimChildren():
            obj.ViewObject.hide()
        CompoundTools.Explode.explodeCompound(f)
        f.ViewObject.hide()
        document.recompute()
    

deckSurfLabels= ['Deck1A', 'Deck1B', 'Deck1C', 'Deck2A', 'Deck2B', 'Deck2C']
linkLabels= ['LinkA', 'LinkB', 'LinkC', 'LinkD']
girder1Labels= ['Artesa1.0', 'Artesa1.1', 'Artesa1.2', 'Artesa1.3', 'Artesa1.4', 'Artesa1.5', 'Artesa1.6']
girder2Labels= ['Artesa2.0', 'Artesa2.1', 'Artesa2.2', 'Artesa2.3', 'Artesa2.4', 'Artesa2.5', 'Artesa2.6']

# Cut surfaces by bearing lines.
cutPlane1= document.getObjectsByLabel("Apoyos1")[0]
cutPlane2= document.getObjectsByLabel("Apoyos2")[0]

cutSurfaces(document, girder1Labels, baseName= 'Girder1Slc', tools= [cutPlane1, cutPlane2])
cutSurfaces(document, girder2Labels, baseName= 'Girder2Slc', tools= [cutPlane1, cutPlane2])
cutSurfaces(document, deckSurfLabels, baseName= 'DeckSlc', tools= [cutPlane1, cutPlane2])

cutSurfaces(document, linkLabels, baseName= 'LinkSlc', tools= [cutPlane1, cutPlane2])


# surf= document.getObjectsByLabel('Deck2A')[0]
# surf.addProperty("App::PropertyFloat", "thickness")
# surf.thickness= 0.28
    
