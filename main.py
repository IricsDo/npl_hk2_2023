import models.nlp as XLNNTN
import models.make_folder as mf

if __name__ == '__main__':
    mf.creat_answer_folder()
    print("\nCreated folder finished\n")

    nlp = XLNNTN.NLP()
    list_questions = nlp.read_questions()
    for i, s in enumerate(list_questions):
        print(s)
        sentence = nlp.sentence_segment(s)
        relation_sentences = nlp.parsing_dependency_grammar(sentence, i)
        pre_logical_form = nlp.grammatical_relations(relation_sentences, i)
        logical_form = nlp.logical_form(pre_logical_form, i)
        procedural_semantics = nlp.procedural_semantics(logical_form, i)
        answer = nlp.answer_question(procedural_semantics, i)
        print(answer)
        print('--$$--')

    print('Done !')
    print('\n')
    exit(0)