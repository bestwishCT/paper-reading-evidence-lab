import json
value='8e681708-734e-4a8c-ae80-59a14c5f8eb8'
examples={'bare':value,'explanation':'The value is '+value,
 'json_extra':json.dumps({'value':value,'extra':True}),
 'code_no_value':'print(data[query])','json_contract':json.dumps({'value':value})}
def strict(s):
 try:
  d=json.loads(s)
  return type(d)==dict and set(d)=={'value'} and d['value']==value
 except (ValueError,TypeError):return False
print(json.dumps({'teaching_only_not_author_code':True,'cases':{
 k:{'contains':value in s,'exact':s==value,'json_contract':strict(s)} for k,s in examples.items()}},indent=2))
