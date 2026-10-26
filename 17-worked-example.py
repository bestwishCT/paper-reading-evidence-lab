from fractions import Fraction
import json
n,a,b=120,112,96
low,high=max(0,a+b-n),min(a,b)
# Hypothetical aligned population only; not paper end-to-end measurements.
out={'paper_claim_quality':str(Fraction(112,120)),'failed_claims':120-112,
     'hypothetical_joint_count_bounds':[low,high],
     'hypothetical_independent_expected_count':float(Fraction(a*b,n)),
     'joint_rates_percent':[float(Fraction(x,n)*100) for x in [low,high]],
     'paper_end_to_end_rate':None}
print(json.dumps(out,indent=2))
