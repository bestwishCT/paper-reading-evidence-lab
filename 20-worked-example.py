from decimal import Decimal as D
import json
rows=[('LongChat13B16K','35.0','83.4'),('MPT30BInstruct','31.5','81.9'),
 ('GPT3.5','56.1','88.3'),('GPT3.5-16K','56.0','88.6'),
 ('Claude1.3','48.3','76.1'),('Claude1.3-100K','48.2','76.4')]
print(json.dumps({'paper_table1_differences_pp':{k:str(D(o)-D(c)) for k,c,o in rows},
 'regimes':{'closed_book':'no documents','oracle':'one answer document given',
 'controlled_multi_document':'one annotated answer document plus distractors'},
 'online_retriever_gain_measured':False},indent=2))
