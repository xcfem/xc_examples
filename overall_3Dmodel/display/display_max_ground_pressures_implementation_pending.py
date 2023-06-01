# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from misc_utils import log_messages as lmsg

lmsg.warning('Implementation pending. Do not use.')
quit()

exec(open("../env_config_deck.py").read())
exec(open("../model_gen.py").read()) #FE model generation
exec(open(path_loads_def+"loadComb_deck.py").read())

combs=combContainer.SLS.rare

found_wink.displayMaxPressures(FEcase=FEcase,combs=combs,caption="Zapata estribo. Presiones máximas en el terreno",fUnitConv=1e-6,unitDescription='[MPa]',rgMinMax=None,fileName='pp')


