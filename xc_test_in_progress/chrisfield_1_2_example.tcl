# Mi-grammiki analysi - 1i Askisi 
# 
# download the program from: 
# http://opensees.berkeley.edu/OpenSees/user/download.php 
# 
# online manual: 
# http://opensees.berkeley.edu/wiki/index.php/OpenSees_User 
 
# Create ModelBuilder (with two-dimensions and 3 DOF/node) 
model BasicBuilder -ndm 2 -ndf 2 
 
set L0 3.; 
set z  0.04;  
 
set x2 [expr sqrt($L0*$L0 - $z*$z)] 
 
# Create nodes 
#    tag        X       Y 
node  1       0.0     0.0 
node  2       $x2     $z 
 
# Fix supports at base of columns 
#    tag   DX   DY  
fix   1     1    1  
fix   2     1    0 
 
set E 50000000 
 
puts " 
the Young modulus is: E= $E 
" 
 
#uniaxialMaterial Elastic $matTag $E 
uniaxialMaterial  Elastic     10   $E 
 
##element truss $eleTag $iNode $jNode $A $matTag 
#element truss 1 1 2 1 10 
 
#element corotTruss $eleTag $iNode $jNode $A  $matTag 
element corotTruss   1        1      2    1.0    10 
 
# Define loads 
set P [expr -100]; 
 
# Create a Plain load pattern with a Linear TimeSeries 
pattern Plain 1 "Linear" { 
      # Create nodal loads at node 2 
        #    nd    FX  Y 
    load 2   0.0  $P
} 
 
# Create a recorder to monitor nodal displacements 
recorder Node -file plotCRV.txt -time -node 2 -dof 2 disp 
recorder Element -file eleGlobal.txt -time -ele 1 forces 
recorder Element -file eleLocal.txt  -time -ele 1 basicForces

############################################## 
# start the solution 
############################################## 
 
initialize 
system BandGeneral 
constraints Plain 
numberer RCM 
 
# Create the convergence test, the norm of the residual with a tolerance of 
# 1e-12 and a max number of iterations of 10 
#test NormDispIncr 1.0e-4  10 3 
test NormUnbalance 1.0e-4  10 
 
# Create the solution algorithm, a Newton-Raphson algorithm 
algorithm Newton 
 
# Create the integration scheme, the LoadControl scheme using steps of 1% 
integrator LoadControl 0.01 
 
# Create the analysis object 
analysis Static 
 
# perform analysis 
analyze 100 
 
 
############################################## 
# telos tis analysis 
############################################## 
 
# ektypwsi stin othoni kapoiwn apotelesmatwn 
print -node 2 
print -ele 1
