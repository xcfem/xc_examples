import xc
from postprocess import limit_state_data as lsd
from postprocess.config import default_config

import sys
workingDirectory= default_config.findWorkingDirectory()+'/' #search env_config.py
sys.path.append(workingDirectory)
import env_config as env
import mesh_gen as msh
import limit_states_def as lstts

msh.modelSpace.addNewLoadCaseToDomain('BuckLC','1.0*D')

solu= msh.FEcase.getSoluProc
solCtrl= solu.getSoluControl
solModels= solCtrl.getModelWrapperContainer
sm= solModels.newModelWrapper("sm")
# cHandler= sm.newConstraintHandler("penalty_constraint_handler")
# cHandler.alphaSP= 1.0e15
# cHandler.alphaMP= 1.0e15
cHandler= sm.newConstraintHandler("transformation_constraint_handler")

numberer= sm.newNumberer("default_numberer")
numberer.useAlgorithm("rcm")
solutionStrategies= solCtrl.getSolutionStrategyContainer

solutionStrategy= solutionStrategies.newSolutionStrategy("solutionStrategy","sm")
#solAlgo= solutionStrategy.newSolutionAlgorithm("newton_raphson_soln_algo")
solAlgo= solutionStrategy.newSolutionAlgorithm("krylov_newton_soln_algo")
ctest= solutionStrategy.newConvergenceTest("norm_disp_incr_conv_test")
ctest.printFlag= 0
ctest.tol= 1e-8
ctest.maxNumIter= 1000
integ= solutionStrategy.newIntegrator("load_control_integrator",xc.Vector([]))
#soe= solutionStrategy.newSystemOfEqn("band_spd_lin_soe")
#solver= soe.newSolver("band_spd_lin_lapack_solver")
soe= solutionStrategy.newSystemOfEqn("band_gen_lin_soe")
solver= soe.newSolver("band_gen_lin_lapack_solver")

buck= solutionStrategies.newSolutionStrategy("buck","sm")
buckSolAlgo= buck.newSolutionAlgorithm("linear_buckling_soln_algo")
buckInteg= buck.newIntegrator("linear_buckling_integrator",xc.Vector([]))
buckSoe= buck.newSystemOfEqn("band_arpackpp_soe")
#buckSoe= buck.newSystemOfEqn("band_arpack_soe")
buckSoe.shift= 0.0
buckSolver= buckSoe.newSolver("band_arpackpp_solver")
#buckSolver= buckSoe.newSolver("band_arpack_solver")

msh.FEcase.setVerbosityLevel(10) # print warning messages
analysis= solu.newAnalysis("linear_buckling_analysis","solutionStrategy","buck")
analysis.numModes= 2
analOk= analysis.analyze(2)

out.displayEigenvectors(1)
out.displayEigenResult(1)

'''
# Shape
shape= list()
wMax= 0.0
for n in tank.nodes:
    pt= n.getInitialPos3d
    x= pt.x; y= pt.y ; z=pt.z
    wRef= math.cos(math.pi*x/b)*math.cos(math.pi*y/b)
    ev= n.getEigenvector(1)
    wCalc= abs(ev[2])
    wMax= max(wMax, wCalc)
    if(abs(wCalc)>0.0 and abs(wRef)>0.0):
        shape.append([wRef, wCalc])
'''
