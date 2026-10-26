import json
q=' '.join('q'+str(i) for i in range(98))
a=' '.join('a'+str(i) for i in range(10))
clip=lambda s:' '.join(s.split()[:100])
first=clip(q+' '+a)
second=q+' '+clip(a)
print(json.dumps({'teaching_only_not_author_implementation':True,
 'concat_then_clip':{'total_words':len(first.split()),'answer_words':sum(w.startswith('a') for w in first.split())},
 'clip_answer_then_concat':{'total_words':len(second.split()),'answer_words':sum(w.startswith('a') for w in second.split())},
 'separate_first_line_example':('answer line\nunrelated continuation').splitlines()[0],
 'mauve_score':None},indent=2))
