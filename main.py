import  c4d, time
from c4d import Vector, Document
myObjects= doc.GetObjects() # lista de objetos usados.


def main():
    
    doc.StartUndo() 
    #c4d.CallCommand(12501) # Ir al Inicio Fotograma 0
    
    print "inicio.."
    def obj_sel(obj):
        for _obj in myObjects:
            doc.SetActiveObject(_obj,0)
        doc.SetActiveObject(obj,0)
    def obj(nombre):
        return doc.SearchObject(nombre)
    
    
        
    ## aqui colocar el objeto para signar coordenadas en este caso es Cono
    objeto_a_copiar=obj("Cono")

    ## este es el objeto de donde se realiza la extracion de coordenadas por fotograma
    esfera=obj("Esfera1")
    cubo1=objeto_a_copiar
    
    print "Iniciando ejecucion"
    
    Fclave=0;
    xyz="";
    obj_sel(esfera)
    
    obj_sel(cubo1)
    for i in range(0,61):
        
        doc.SetTime(c4d.BaseTime(i,  doc.GetFps()))
        doc.ExecutePasses (None, True, True, True, c4d.BUILDFLAGS_INTERNALRENDERER)
        curFrame = doc.GetTime().GetFrame(doc.GetFps())

        axi=esfera.GetAbsPos()
        x=axi.x
        y=axi.y
        z=axi.z
        #print(axi)    
        x+=300
        z+=300
        y+=600

        rot=esfera.GetAbsRot()
        h=rot.x
        p=rot.y
        b=rot.z

        escala=esfera.GetAbsScale()
        ex=escala.x
        ey=escala.y
        ez=escala.z

        xyz+="curFrame: "+ str(curFrame)+" Axi " +str(x) + ","+ str(y) + "," + str(z) +"\n\r"
        cubo1.SetAbsPos(c4d.Vector(x,y,z))
        cubo1.SetAbsRot(c4d.Vector(h,p,b))
        cubo1.SetAbsScale(escala)
        
        
        cubo1.Message(c4d.MSG_UPDATE)
        c4d.EventAdd()
        
        track = cubo1.GetFirstCTrack() #Get it's first animation track
        if not track: 
            print "no hay GetFirstCTrack."
            track=c4d.CTrack(cubo1, c4d.DescID(c4d.DescLevel(c4d.ID_BASEOBJECT_POSITION, c4d.DTYPE_VECTOR, 0), c4d.DescLevel(c4d.VECTOR_X, c4d.DTYPE_REAL, 0)))
            #trackRender = c4d.CTrack(o, c4d.DescID( c4d.DescLevel(c4d.ID_BASEOBJECT_VISIBILITY_RENDER,c4d.DTYPE_LONG,0,)))
            cubo1.InsertTrackSorted(track)
            trackEditor = c4d.CTrack(cubo1, c4d.DescID( c4d.DescLevel(c4d.ID_BASEOBJECT_VISIBILITY_EDITOR,c4d.DTYPE_LONG,0,)))
            cubo1.InsertTrackSorted(trackEditor)
            trackEditor.SetAfter(c4d.CLOOP_CONSTANT)
            #return # if it doesn't have any tracks. End the script
        curve = track.GetCurve()
        count = curve.GetKeyCount() #Count how many keys are on it
        time = doc.GetTime() #Get the time
        frame = time.GetFrame(doc.GetFps()) #Get the FPS
        if i == Fclave :
            c4d.CallCommand(12410) # Grabar Objetos Activos
            added = curve.AddKey(time)
            key=added["key"]
            Fclave+=10
            c4d.CallCommand(12410) # Grabar Objetos Activos
            
        
    print "Fin del Proceso."
    print xyz # salida del log
    doc.EndUndo()
    
# evento maestro que la funcion    
if __name__=='__main__':
    main()
    c4d.EventAdd()
