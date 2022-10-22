for obj in App.ActiveDocument.Objects:
    label= obj.Label
    if(label.startswith('IFCTendon')):
        tendonNumber= label[-3:-1]
        tendonLetter= label[-1]
        bondedLength= 0.0
        if(tendonLetter in ['C','D']):
            if(tendonNumber=='02'):
                bondedLength= 2.0
            else:
                bondedLength= 6.0
        else:
            if(tendonNumber in ['05','12']):
                bondedLength= 2.0
            elif(tendonNumber in ['08','15']):
                bondedLength= 4.0
            elif(tendonNumber=='02'):
                bondedLength= 6.0
        obj.IfcProperties= {'Bonded length': 'Tendon Common;;IfcLengthMeasure;;'+str(bondedLength), 'Transference length': 'Tendon Common;;IfcLengthMeasure;;1.4'}        
