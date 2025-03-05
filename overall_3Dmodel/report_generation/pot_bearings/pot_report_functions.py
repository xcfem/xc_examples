from misc_utils import log_messages as lmsg

def gen_longtable_head(headTitles,justif,caption,tit2ndLine=None):
    '''Generate the heading tex lines for a long table

    :param headTitles: list of titles for the table (first line e.g. ['tit1','tit2',...]
    :param justif: justification of columns (e.g. 'lcr')
    :param caption: caption text (e.g. 'Caption text')
    :param tit2ndLine:  list of titles, if any, for the second line of the head titles (defaults to None)
    
    '''
    retval='\\begin{center} \n \\begin{longtable}{|'
    retval+=justif + '|} \n'
    retval+='\\caption{'+caption+'} \\\\ \n'
    head='\\hline \n '
    for tit in headTitles:
        head+=tit+' & '
    head=head.removesuffix('& ')
    head+=' \\\\ \n'
    if tit2ndLine:
        for tit in tit2ndLine:
            head+=tit+' & '
    head=head.removesuffix('& ')
    head+=' \\\\ \n'
    #head+=' \\hline \n'
    retval+=head + '\\endfirsthead \n'
    retval+=head + '\\hline \\endhead \n \\\\ \\hline \n'
    retval+='\\multicolumn{'+str(len(headTitles))+'}{r}{\\emph{Continúa en la siguiente página}} \\\\ \n'
    retval+=' \\endfoot \n \\hline \n  \\endlastfoot  \n \\hline \n'
    return retval

def combs_diasggr(combDict):
    ''' Return a new dictionary of combinations with the keys 'combExpr': combination as usually expressed and 'combDisaggr'combination expressed as a list of [[factor,lcName],..] 
    '''
    retval=dict()
    for k in combDict.keys():
        retval[k]=dict()
        compExpr=combDict[k]
        retval[k]['combExpr']=compExpr
        disaggr=compExpr.split('+')
        for i in range(len(disaggr)):
            disaggr[i]=disaggr[i].split('*')
            disaggr[i][0]=eval(disaggr[i][0])
        retval[k]['combDisaggr']=disaggr
    return retval


            
def gen_dict_Rmaxmin(combs,potResdict):
    ''' Generates the dictionary with maximum and minimum reactions:
        {'PU-P1':
                {'potDescr': 'PU pila 1',
                 'RXmin': 76312.91687794843,
                 'combRXmin': '1.0*G1+1.0*G2+1.35*GNC2',
                 'RYmin': 36511.47961638082,
                 'combRYmin': '1.0*G1+1.0*G2+1.35*GNC2',
                 'RZmin': 746933.0538029419,
                 'combRZmin': '1.0*G1+1.0*G2+1.35*GNC2+1.5*Q3A2',
                 'RXmax': 189037.97450506716,
                 'combRXmax': '1.0*G1+1.0*G2+1.35*GNC2+1.5*Q3A2',
                 'RYmax': 476084.46920392604,
                 'combRYmax': '1.35*G1+1.35*G2+1.35*GNC2+1.50*Q1A1+1.50*Q1B1+1.50*Q1C1+0.9*Q1E+0.9*Q2A1+0.9*Q2B1+0.9*Q3A2',
                 'RZmax': 1455328.765352401,
                 'combRZmax': '1.35*G1+1.35*G2+1.35*GNC2+1.50*Q1A3+1.50*Q1B1+1.50*Q1C3+0.9*Q1E+0.9*Q2A1+0.9*Q2B1+0.9*Q3A2'},

    :param combs: dictionary of combinations
    :param potResdict: dictionary of POT results 
    '''
    resDict=dict()
    for potId in potResdict.keys():
        resDict[potId]=dict()
        resDict[potId]['potDescr']=potResdict[potId]['potDescr']
        RXmax=0; RXmin=1e15 ; RYmax=0; RYmin=1e15 ; RZmax=0; RZmin=1e15
        combRXmax=' '; combRXmin=' ' ; combRYmax=' '; combRYmin=' ' ; combRZmax=' '; combRZmin=' '
        for cmb in combs.keys():
            RX=0; RY=0; RZ=0
            for lcComp in combs[cmb]['combDisaggr']:
                lcFactor=lcComp[0]
                lcName=lcComp[1]
                RX+=lcFactor*potResdict[potId]['LCres'][lcName]['Rx']
                RY+=lcFactor*potResdict[potId]['LCres'][lcName]['Ry']
                RZ+=lcFactor*potResdict[potId]['LCres'][lcName]['Rz']
            if abs(RX)<RXmin:
                RXmin=abs(RX)
                combRXmin=combs[cmb]['combExpr']
            if abs(RY)<RYmin:
                RYmin=abs(RY)
                combRYmin=combs[cmb]['combExpr']
            if -RZ<RZmin:
                RZmin=-RZ
                combRZmin=combs[cmb]['combExpr']
                if -RZ<0:
                    lmsg.warning('En la combinación: '+combRZmin+' se produce despegue en el apoyo '+potResdict[potId]['potDescr'])
            if abs(RX)>RXmax:
                RXmax=abs(RX)
                combRXmax=combs[cmb]['combExpr']
            if abs(RY)>RYmax:
                RYmax=abs(RY)
                combRYmax=combs[cmb]['combExpr']
            if -RZ>RZmax:
                RZmax=-RZ
                combRZmax=combs[cmb]['combExpr']
        resDict[potId]['RXmin']=RXmin
        resDict[potId]['combRXmin']=combRXmin
        resDict[potId]['RYmin']=RYmin
        resDict[potId]['combRYmin']=combRYmin
        resDict[potId]['RZmin']=RZmin
        resDict[potId]['combRZmin']=combRZmin
        resDict[potId]['RXmax']=RXmax
        resDict[potId]['combRXmax']=combRXmax
        resDict[potId]['RYmax']=RYmax
        resDict[potId]['combRYmax']=combRYmax
        resDict[potId]['RZmax']=RZmax
        resDict[potId]['combRZmax']=combRZmax
    return resDict

def gen_Rmaxmin_table(reportFile,dictRmaxmin,caption):
    longtableHead= gen_longtable_head(headTitles=['Tipo carga ','Valor (kN)','Combinación'],justif='lrl',caption=caption)
    reportFile.write(longtableHead)
    for pot in dictRmaxmin.keys():
        reportFile.write('\\hline \\multicolumn{3}{c}{'+ str(dictRmaxmin[pot]['potDescr']) +'} \\\\ \\hline \n')
        reportFile.write('$F_{VERT., MINIMO}$ & '+ str(round(dictRmaxmin[pot]['RZmin']*1e-3,2)) +' & '+ str(dictRmaxmin[pot]['combRZmin']) + '\\\\  \n')
        reportFile.write('$F_{VERT., MAXIMO}$ & '+ str(round(dictRmaxmin[pot]['RZmax']*1e-3,2)) +' & '+ str(dictRmaxmin[pot]['combRZmax']) + '\\\\  \n')
        reportFile.write('$F_{LONG., MINIMO}$ & '+ str(round(dictRmaxmin[pot]['RXmin']*1e-3,2)) +' & '+ str(dictRmaxmin[pot]['combRXmin']) + '\\\\  \n')
        reportFile.write('$F_{LONG., MAXIMO}$ & '+ str(round(dictRmaxmin[pot]['RXmax']*1e-3,2)) +' & '+ str(dictRmaxmin[pot]['combRXmax']) + '\\\\  \n')
        reportFile.write('$F_{TRASNV., MINIMO}$ & '+ str(round(dictRmaxmin[pot]['RYmin']*1e-3,2)) +' & '+ str(dictRmaxmin[pot]['combRYmin']) + '\\\\  \n')
        reportFile.write('$F_{TRASNV., MAXIMO}$ & '+ str(round(dictRmaxmin[pot]['RYmax']*1e-3,2)) +' & '+ str(dictRmaxmin[pot]['combRYmax']) + '\\\\  \n')
    reportFile.write('\\end{longtable} \n \\end{center} \n')
        
def gen_dict_DispMaxPosNeg(combs,potResdict):
    ''' Generates the dictionary with maximum and minimum displacements:
   'PU-P1':
     {'potDescr': 'PU pila 1',
      'UXmaxNeg': -0.005180726593436836,
      'combUXmaxNeg': '1.00*G1+1.00*G2+0.80*Q1A1+0.80*Q1B1+0.80*Q1C1
      'UYmaxNeg': -5.010118623972171e-07,
      'combUYmaxNeg': '1.00*G1+1.00*G2+0.80*Q1A1+0.80*Q1B1+0.80*Q1C1
      'UXmaxPos': 0.022992721336138562,
      'combUXmaxPos': '1.0*G1+1.0*G2+1.00*GNC2+0.6*Q3A2',
      'UYmaxPos': 2.8365972571627377e-07,
      'combUYmaxPos': '1.00*G1+1.00*G2+1.00*GNC2+0.80*Q1A3+0.80*Q1B1
    '''
    resDict=dict()
    for potId in potResdict.keys():
        resDict[potId]=dict()
        resDict[potId]['potDescr']=potResdict[potId]['potDescr']
        UXmaxPos=0; UXmaxNeg=0 ; UYmaxPos=0; UYmaxNeg=0 
        combUXmaxPos=' '; combUXmaxNeg=' ' ; combUYmaxPos=' '; combUYmaxNeg=' ' 
        for cmb in combs.keys():
            UX=0; UY=0 
            for lcComp in combs[cmb]['combDisaggr']:
                lcFactor=lcComp[0]
                lcName=lcComp[1]
                UX+=lcFactor*potResdict[potId]['LCres'][lcName]['dispX']
                UY+=lcFactor*potResdict[potId]['LCres'][lcName]['dispY']
            if UX<UXmaxNeg:
                UXmaxNeg=UX
                combUXmaxNeg=combs[cmb]['combExpr']
            if UY<UYmaxNeg:
                UYmaxNeg=UY
                combUYmaxNeg=combs[cmb]['combExpr']
            if UX>UXmaxPos:
                UXmaxPos=UX
                combUXmaxPos=combs[cmb]['combExpr']
            if UY>UYmaxPos:
                UYmaxPos=UY
                combUYmaxPos=combs[cmb]['combExpr']
        resDict[potId]['UXmaxNeg']=UXmaxNeg
        resDict[potId]['combUXmaxNeg']=combUXmaxNeg
        resDict[potId]['UYmaxNeg']=UYmaxNeg
        resDict[potId]['combUYmaxNeg']=combUYmaxNeg
        resDict[potId]['UXmaxPos']=UXmaxPos
        resDict[potId]['combUXmaxPos']=combUXmaxPos
        resDict[potId]['UYmaxPos']=UYmaxPos
        resDict[potId]['combUYmaxPos']=combUYmaxPos
    return resDict
       
def gen_DispMaxPosNeg_table(reportFile,dictDispMaxPosNeg,caption):
    longtableHead= gen_longtable_head(headTitles=['Tipo desplazamiento ','Valor (mm)','Combinación'],justif='lrl',caption=caption)
    reportFile.write(longtableHead)
    for pot in dictDispMaxPosNeg.keys():
        reportFile.write('\\hline \\multicolumn{3}{c}{'+ str(dictDispMaxPosNeg[pot]['potDescr']) +'} \\\\ \\hline \n')
        reportFile.write('$U_{LONG., MAXIMO(+)}$ & '+ str(round(dictDispMaxPosNeg[pot]['UXmaxPos']*1e3,1)) +' & '+ str(dictDispMaxPosNeg[pot]['combUXmaxPos']) + '\\\\  \n')
        reportFile.write('$U_{LONG., MAXIMO(-)}$ & '+ str(round(dictDispMaxPosNeg[pot]['UXmaxNeg']*1e3,1)) +' & '+ str(dictDispMaxPosNeg[pot]['combUXmaxNeg']) + '\\\\  \n')
        reportFile.write('$U_{TRASNV., MAXIMO(+)}$ & '+ str(round(dictDispMaxPosNeg[pot]['UYmaxPos']*1e3,1)) +' & '+ str(dictDispMaxPosNeg[pot]['combUYmaxPos']) + '\\\\  \n')
        reportFile.write('$U_{TRASNV., MAXIMO(-)}$ & '+ str(round(dictDispMaxPosNeg[pot]['UYmaxNeg']*1e3,1)) +' & '+ str(dictDispMaxPosNeg[pot]['combUYmaxNeg']) + '\\\\  \n')
    reportFile.write('\\end{longtable} \n \\end{center} \n')
        

def gen_dict_RotMaxPosNeg(combs,potResdict):
    ''' Generates the dictionary with maximum and minimum rotations:
    '''
    resDict=dict()
    for potId in potResdict.keys():
        resDict[potId]=dict()
        resDict[potId]['potDescr']=potResdict[potId]['potDescr']
        RotXmaxPos=0; RotXmaxNeg=0 ; RotYmaxPos=0; RotYmaxNeg=0
        combRotXmaxPos=' '; combRotXmaxNeg=' ' ; combRotYmaxPos=' '; combRotYmaxNeg=' '
        for cmb in combs.keys():
            RotX=0; RotY=0 
            for lcComp in combs[cmb]['combDisaggr']:
                lcFactor=lcComp[0]
                lcName=lcComp[1]
                RotX+=lcFactor*potResdict[potId]['LCres'][lcName]['rotX']
                RotY+=lcFactor*potResdict[potId]['LCres'][lcName]['rotY']
            if RotX<RotXmaxNeg:
                RotXmaxNeg=RotX
                combRotXmaxNeg=combs[cmb]['combExpr']
            if RotY<RotYmaxNeg:
                RotYmaxNeg=RotY
                combRotYmaxNeg=combs[cmb]['combExpr']
            if RotX>RotXmaxPos:
                RotXmaxPos=RotX
                combRotXmaxPos=combs[cmb]['combExpr']
            if RotY>RotYmaxPos:
                RotYmaxPos=RotY
                combRotYmaxPos=combs[cmb]['combExpr']
        resDict[potId]['RotXmaxNeg']=RotXmaxNeg
        resDict[potId]['combRotXmaxNeg']=combRotXmaxNeg
        resDict[potId]['RotYmaxNeg']=RotYmaxNeg
        resDict[potId]['combRotYmaxNeg']=combRotYmaxNeg
        resDict[potId]['RotXmaxPos']=RotXmaxPos
        resDict[potId]['combRotXmaxPos']=combRotXmaxPos
        resDict[potId]['RotYmaxPos']=RotYmaxPos
        resDict[potId]['combRotYmaxPos']=combRotYmaxPos
    return resDict
       
def gen_RotMaxPosNeg_table(reportFile,dictRotMaxPosNeg,caption):
    longtableHead= gen_longtable_head(headTitles=['Tipo rotación ','Valor ($\\times 10^2$ rad)','Combinación'],justif='lrl',caption=caption)
    reportFile.write(longtableHead)
    for pot in dictRotMaxPosNeg.keys():
        reportFile.write('\\hline \\multicolumn{3}{c}{'+ str(dictRotMaxPosNeg[pot]['potDescr']) +'} \\\\ \\hline \n')
        reportFile.write('$\\alpha_{LONG., MAXIMO(+)}$ & '+ str(round(dictRotMaxPosNeg[pot]['RotXmaxPos']*1e3,1)) +' & '+ str(dictRotMaxPosNeg[pot]['combRotXmaxPos']) + '\\\\  \n')
        reportFile.write('$\\alpha_{LONG., MAXIMO(-)}$ & '+ str(round(dictRotMaxPosNeg[pot]['RotXmaxNeg']*1e3,1)) +' & '+ str(dictRotMaxPosNeg[pot]['combRotXmaxNeg']) + '\\\\  \n')
        reportFile.write('$\\alpha_{TRASNV., MAXIMO(+)}$ & '+ str(round(dictRotMaxPosNeg[pot]['RotYmaxPos']*1e3,1)) +' & '+ str(dictRotMaxPosNeg[pot]['combRotYmaxPos']) + '\\\\  \n')
        reportFile.write('$\\alpha_{TRASNV., MAXIMO(-)}$ & '+ str(round(dictRotMaxPosNeg[pot]['RotYmaxNeg']*1e3,1)) +' & '+ str(dictRotMaxPosNeg[pot]['combRotYmaxNeg']) + '\\\\  \n')
    reportFile.write('\\end{longtable} \n \\end{center} \n')
        

    



    
                       
