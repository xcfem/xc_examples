 #Geometry data
spansL=[30,43.5,30] # length spans
Lbeam=sum(spansL)
yBearings=[0,30,73.5,Lbeam]

deckW=10 # deck width
#beamsDist=5 # distance between beams 
beamH=1.9 # height of beams
slabTh=0.25 # slab thickness
slabW=5 # slab width (over each beam)
# steel-beam sections
# 'yCoord': list of Ycoordinates [start,end] to place the section inside
# 'bf_w': bottom flange width
# 'bf_t': bottom flange thickness
# 'w_t': web thickness
# 'w_h': web height
# 'tf_w': top flange width
# 'tf_h': top flange thickness
# Section type 1 (piers)
sbeam_st1={
    'yCoord':[[yBearings[1]-5,yBearings[1]+5],
              [yBearings[2]-5,yBearings[2]+5]],
    'bf_w':600e-3,
    'bf_t':60e-3,
    'w_t':15e-3,
    'w_h':1815e-3,
    'tf_w':450e-3,
    'tf_t':25e-3,
    }
# Section type 2 (abutments)
sbeam_st2={
    'yCoord':[[0,5],[Lbeam-5,Lbeam]],
    'bf_w':600e-3,
    'bf_t':25e-3,
    'w_t':12e-3,
    'w_h':1850e-3,
    'tf_w':450e-3,
    'tf_t':25e-3,
    }
# Section type 3 (mid-span)
sbeam_st3={
    'yCoord':[[5,yBearings[1]-5],
              [yBearings[1]+5,yBearings[2]-5],
              [yBearings[2]+5,Lbeam-5]],
    'bf_w':600e-3,
    'bf_t':40e-3,
    'w_t':12e-3,
    'w_h':1835e-3,
    'tf_w':450e-3,
    'tf_t':25e-3,
    }

# transverse stiffeners (Y-coord)
yTS=list()
# intermediate diaphragms (Y-coord)
yID=list()

yTS+=[2.0833]
yTS.append(yTS[-1]+2.0833)
yID.append(yTS[-1]+2.0833)
yTS.append(yID[-1]+3.125)
yID.append(yTS[-1]+3.125)
yTS.append(yID[-1]+3.125)
yID.append(yTS[-1]+3.125)
yTS.append(yID[-1]+3.125)
yID.append(yTS[-1]+3.125)
yTS.append(yID[-1]+2.5)
yTS.append(yTS[-1]+2.5+2.5)
yID.append(yTS[-1]+2.5)
yTS.append(yID[-1]+3.35)
yID.append(yTS[-1]+3.35)
yTS.append(yID[-1]+3.35)
yID.append(yTS[-1]+3.35)

yTSaux=list()
for y in yTS:
    yTSaux.append(Lbeam-y)
yTSaux.sort()
yTS+=[Lbeam/2]+yTSaux

yIDaux=list()
for y in yID:
    yIDaux.append(Lbeam-y)
yIDaux.sort()
yID+=yIDaux
# z coordinate of the diaphragms flanges
zBF_ID=1
zTF_ID=zBF_ID+0.5
# Transverse stiffness geometry
TSw=600e-3 #width 
TSth=12e-3 #thickness
# 
eSize= 0.30     #length of elements

# Effective width calculation EC4-2 art. 5.4.1.2
b_0=0.20 # [m] distance between the centres of the outstand shear connectors
# Y-interval width shear connections each 150 mm
SCdisY=0.20
'''

### NOT USED IN THIS MODEL
# equivalent spans= approximate distance between points of zero bending n10ment.: EC4-2, fig. 5.1
b_i_real=[beamsDist/2-b_0/2, beamsDist/2-b_0/2] # real slab flange width (at each side of the beam)
 # equivalent span length for the calculation of the equivalent widh at mid-span (beff,1) (fig. 5.1 EC4-2):
Le_mid_span=[0.85*spansL[0], 0.7*spansL[1], 0.85*spansL[2]]
b_ei_mid_span=[[min(Le/8,b_i_real[0]),min(Le/8,b_i_real[1])] for Le in Le_mid_span]
b_eff_mid_span=[b_0+sum(b_ei) for b_ei in b_ei_mid_span]
#  equivalent span length for the calculation of the equivalent widh at internal support (beff,2) (fig. 5.1 EC4-2):
Le_internal_support=[0.25*(spansL[i]+spansL[i+1]) for i in range(len(spansL)-1)]
b_ei_internal_support=[[min(Le/8,b_i_real[0]),min(Le/8,b_i_real[1])] for Le in Le_internal_support]
b_eff_internal_support=[b_0+sum(b_ei) for b_ei in b_ei_internal_support]
## Effective width at mid-span or internal support
# Effective width at an end supports
beta_i_start_support=0.55+0.025*Le_mid_span[0]/b_ei_mid_span[0][0]
beta_i_end_support=0.55+0.025*Le_mid_span[-1]/b_ei_mid_span[-1][0]
b_eff_end_supports=[b_0+beta_i_start_support*sum(b_ei_mid_span[0]),
                    b_0+beta_i_end_support*sum(b_ei_mid_span[-1])]
'''
