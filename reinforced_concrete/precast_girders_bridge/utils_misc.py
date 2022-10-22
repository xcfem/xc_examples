artesaName= 'Artesa2'
count= 0
artesaGrp= document.getObjectsByLabel(artesaName)[0]
for obj in artesaGrp.OutList:
    label= artesaName+'.'+str(count)
    obj.Label= label
    count+= 1

