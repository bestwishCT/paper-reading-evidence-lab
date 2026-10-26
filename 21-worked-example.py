from decimal import Decimal as D
import json
s=list(map(D,['64.1','39.5','69.6','73.2']))
f=list(map(D,['66.6','40.4','73.6','72.5']))
dominates=lambda a,b:all(x>=y for x,y in zip(a,b)) and any(x>y for x,y in zip(a,b))
print(json.dumps({'metrics':['MAUVE score','EM recall pp','citation recall pp','citation precision pp'],
 'full_minus_short':[str(x-y) for x,y in zip(f,s)],
 'full_pareto_dominates_short':dominates(f,s),
 'short_pareto_dominates_full':dominates(s,f),'statistical_significance':None},indent=2))
