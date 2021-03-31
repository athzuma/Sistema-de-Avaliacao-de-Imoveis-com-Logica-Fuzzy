import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


area = ctrl.Antecedent(np.arange(20, 351, 1), 'area')
padrao = ctrl.Antecedent(np.arange(0, 11, 1), 'padrao')
idade = ctrl.Antecedent(np.arange(0, 51, 1), 'idade')
zona = ctrl.Antecedent(np.arange(0, 11, 1), 'zona')
preco = ctrl.Consequent(np.arange(50000, 1000001, 1), 'preco')

area.automf(3)

padrao['simples'] = fuzz.trimf(padrao.universe, [0, 0, 5])
padrao['comum'] = fuzz.trimf(padrao.universe, [0, 5, 10])
padrao['alto'] = fuzz.trimf(padrao.universe, [5, 10, 10])

idade['muito_nova'] = fuzz.trimf(idade.universe, [0, 0, 1])
idade['nova'] = fuzz.trimf(idade.universe, [0, 5, 10])
idade['usada'] = fuzz.trimf(idade.universe, [5, 10, 20])
idade['velha'] = fuzz.trimf(idade.universe, [10, 30, 40])
idade['muito_velha'] = fuzz.trimf(idade.universe, [30, 50, 50])

zona['periferica'] = fuzz.trimf(zona.universe, [0, 0, 5])
zona['central'] = fuzz.trimf(zona.universe, [0, 5, 10])
zona['nobre'] = fuzz.trimf(zona.universe, [5, 10, 10])

preco.automf(7) # dismal poor mediocre average decent good excellent

#area.view()
#padrao.view()
#idade.view()
#zona.view()
#preco.view()


#Criterios de desvalorização
rule1 = ctrl.Rule(idade['muito_velha'], preco['dismal'])
rule2 = ctrl.Rule(zona['periferica'] & area['poor'], preco['dismal'])
rule3 = ctrl.Rule(padrao['simples'] & area['poor'], preco['dismal'])

#Criterios medianos
rule4 = ctrl.Rule(padrao['simples'] & area['poor'] & zona['central'] & idade['usada'], preco['poor'])
rule5 = ctrl.Rule(padrao['simples'] & area['average'] & zona['central'] & idade['usada'], preco['mediocre'])
rule6 = ctrl.Rule(padrao['comum'] & area['poor'] & zona['central'] & idade['usada'], preco['mediocre'])
rule7 = ctrl.Rule(padrao['comum'] & area['average'] & zona['central'] & idade['usada'], preco['mediocre'])
rule8 = ctrl.Rule(padrao['comum'] & area['good'] & zona['central'] & idade['usada'], preco['average'])

#criterios de valorização
rule9 = ctrl.Rule(padrao['alto'] & zona['nobre'] & idade['muito_nova'] & area['good'], preco['excellent'])
rule10 = ctrl.Rule(padrao['alto'] & zona['nobre'] & area['poor'], preco['decent'])
rule11 = ctrl.Rule(padrao['alto'] & zona['nobre'] & area['average'], preco['decent'])
rule12 = ctrl.Rule(padrao['alto'] & zona['nobre'] & area['good'], preco['good'])


tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12])


tipping = ctrl.ControlSystemSimulation(tipping_ctrl)

tipping.input['area'] = 20
tipping.input['padrao'] = 1
tipping.input['idade'] = 40
tipping.input['zona'] = 1


tipping.compute()

print(tipping.output['preco'])
preco.view(sim=tipping)
plt.show()
