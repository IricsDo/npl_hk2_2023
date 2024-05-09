import os

def creat_answer_folder():
    paths = ['output/answer_question', 'output/grammatical_relations', 'output/logical_form', 'output/parsing_dependency_grammar', 'output/procedural_semantics']
    for path in paths:
        try: 
            os.makedirs(path, exist_ok = True) 
            print("Directory '%s' created successfully" % path) 
        except OSError as error: 
            print("Directory '%s' can not be created" % path) 
