import pandas as pd
import action_parsing_dependcy_grammar as apdg
import copy

class NPL:
    def __init__(self) -> None:
        pass

    def read_questions(self):
        list_questions = list()
        with open('input/query.txt', 'r', encoding='utf-8') as f:
            questions = f.readlines()
            for q in questions:
                list_questions.append(q.strip().lower())
        return list_questions
    
    def sentence_segment(self, sentence : str):
        result = list()

        sentence = sentence.lower() # Lower case word
        sentence = sentence[3:] # Remove numberic question
        sentence = sentence.replace(',', '') # Remove , symbol
        sentence = sentence.replace(':', '') # Remove : symbol

        remove_word = ['có', 'được','trong', 'thứ', 'và', 'vào', 'nào']
        split_sentence = sentence.split()
        len_sentence = len(split_sentence)
        temp = list()
        for i in range(len_sentence):
            if split_sentence[i] not in remove_word:
                temp.append(split_sentence[i])
        temp = ' '.join(temp)
        temp = temp.replace('.', '') # Remove punch because we have '?' symbol

        temp_copy = copy.deepcopy(temp)
        temp_copyy = copy.deepcopy(temp)

        action_word = ['dạy']
        collect_word = ['cho biết', 'bao nhiêu', 'tên môn học', 'môn học', 'môn học', 'cùng học kỳ', 'học kỳ', 'cùng năm học', 'năm học thứ', 'năm học', 'mã số', 'mã số', '?']

        collect_word.extend(action_word)
        replace_index = list()

        for cw in collect_word:
            if cw in temp:
                result.append(cw)
                temp = temp.replace(cw, '', 1)
                replace_index.append(temp_copyy.find(cw))
                temp_copyy = temp_copyy.replace(cw, '@'*len(cw), 1)
        temp = temp.strip()
        replace_index,  result= (list(t) for t in zip(*sorted(zip(replace_index, result)))) 

        insert_word = dict()
        for i in range(1, len(replace_index)):
            pre_index  = replace_index[i-1] + len(result[i-1]) + 1 
            if  pre_index == replace_index[i]:
                continue
            else:
                insert_word[i] = temp_copy[pre_index:replace_index[i]].rstrip()

        count = 0
        for k, v in insert_word.items():
            result.insert(k + count, v)
            count += 1
        return result

    def parsing_dependency_grammar(self, sentence : list, index_sentence: int):
        action_word = 'dạy'
        query_word = '?'

        relation_sentences = list()

        data = list()
        action = ''
        stack = list()
        bufer = list()
        relation = ''

        # Start state
        action = ''
        stack.append('root')
        bufer = copy.deepcopy(sentence)
        relation = ''
        data.append([action, ','.join(stack), ','.join(bufer), relation])

        next_number_state = ''

        # loop state
        while True:
            if 'bao nhiêu' == stack[-1]:
                action, stack, bufer, relation = apdg.LAwh_count_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])
                action, stack, bufer, relation = apdg.shift_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])

            elif bufer[0] == 'chỉ' and action_word == bufer[1]:
                action, stack, bufer, relation = apdg.LA_dobj_only_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])
            
            elif bufer[0] == 'môn học' and bufer[1] == 'không' and bufer[2] == action_word:
                bufer.insert(0, 'bao nhiêu')
                action = 'add word to full meaning'
                relation = 'môn học -> bao nhiêu môn học'
                data.append([action, ','.join(stack), ','.join(bufer), relation])

            elif stack[-1] == 'môn học' and bufer[0] == 'không' and bufer[1] == action_word and bufer[2].isnumeric():
                action, stack, bufer, relation = apdg.LA_dobj_no_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])
                next_number_state = 'không dạy'

            elif 'môn học' == stack[-1] and 'mã số' != stack[-2] and 'mã số' != bufer[0] and bufer[0] != 'chỉ':
                action, stack, bufer, relation = apdg.LA_dobj_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])

            elif 'môn học' == bufer[0] and stack[-1] == action_word:
                action, stack, bufer, relation = apdg.RA_dobj_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])

            elif 'môn học' == stack[-1] and 'mã số' == stack[-2] and 'mã số' != bufer[0] and bufer[0] != 'chỉ':
                action, stack, bufer, relation = apdg.RAname_mh_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])
                action, stack, bufer, relation = apdg.REDUCE_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])
                action, stack, bufer, relation = apdg.REDUCE_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])
                action, stack, bufer, relation = apdg.REDUCE_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])

            elif action_word == bufer[0] and bufer[0] != 'chỉ':
                action, stack, bufer, relation = apdg.RAroot_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])
            
            elif 'học kỳ' == bufer[0] and 'một' != stack[-1] and 'hai' != stack[-1] and 'cả 2' != stack[-1] and 'cả hai' != stack[-1] and '1 hoặc 2' != stack[-1]:
                next_number_state = 'học kỳ'
                action, stack, bufer, relation = apdg.RAhk_time_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])

            elif bufer[0].replace(' ', '').isnumeric() and next_number_state == 'học kỳ':
                action, stack, bufer, relation = apdg.RAnum_hk_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])
                next_number_state = ''
                if stack[-1].isnumeric() and bufer[0] == 'năm học' and not bufer[1].isnumeric():
                    continue
                action, stack, bufer, relation = apdg.REDUCE_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])

            elif bufer[0] == '1 hoặc 2' and next_number_state == 'học kỳ':
                action, stack, bufer, relation = apdg.RAnum_hk_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])
                action, stack, bufer, relation = apdg.REDUCE_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])


            elif 'năm học' == bufer[0] and not stack[-1].isnumeric():
                if len(bufer) > 2:
                    if bufer[1].isnumeric() or bufer[2].isnumeric() or bufer[1] == '1 2' or bufer[1] == '1 hoặc 2':
                        next_number_state = 'năm học'
                        action, stack, bufer, relation = apdg.RAnh_mod_action(stack, bufer)
                        data.append([action, ','.join(stack), ','.join(bufer), relation])

                elif stack[-1] == 'học kỳ' and bufer[0] == 'năm học' and not bufer[1].isnumeric():
                    bufer.insert(1, '1 hoặc 2')
                    bufer.insert(0, '1 hoặc 2')
                    action = 'convert word to full meaning'
                    relation = 'học kỳ năm học -> học kì 1 hoặc 2 năm học 1 hoặc 2'
                    data.append([action, ','.join(stack), ','.join(bufer), relation])

            elif bufer[0].isnumeric() and bufer[1] == 'năm học' and not bufer[2].isnumeric() and next_number_state != 'không dạy':
                bufer.pop(0)
                bufer.insert(1, '1 hoặc 2')
                action = 'convert word to full meaning'
                relation = '1 năm học -> năm học 1 hoặc 2'
                data.append([action, ','.join(stack), ','.join(bufer), relation])

            elif stack[-1] == 'năm học' and stack[-2].isnumeric():
                stack.pop(-2)
                bufer.insert(0, '1 2')
                action, stack, bufer, relation = apdg.RAnum_nh_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])
                action, stack, bufer, relation = apdg.REDUCE_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])

            elif stack[-1] == 'năm học' and bufer[0] == '1 hoặc 2':
                action, stack, bufer, relation = apdg.RAnum_nh_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])
                action, stack, bufer, relation = apdg.REDUCE_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])
                action, stack, bufer, relation = apdg.REDUCE_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])
                action, stack, bufer, relation = apdg.REDUCE_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])

            elif bufer[0].replace(' ', '').isnumeric() and next_number_state == 'năm học':
                action, stack, bufer, relation = apdg.RAnum_nh_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])
                next_number_state = ''
                action, stack, bufer, relation = apdg.REDUCE_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])

            elif not bufer[0].isnumeric() and 'năm học' in stack and 'học kỳ' in stack and bufer[0] == 'không':
                action, stack, bufer, relation = apdg.RAnum_or_nh_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])
                action, stack, bufer, relation = apdg.REDUCE_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])
                action, stack, bufer, relation = apdg.REDUCE_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])
                action, stack, bufer, relation = apdg.REDUCE_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])

            elif query_word == bufer[0] and stack[-1] != action_word and stack[-1] != 'root':
                action, stack, bufer, relation = apdg.REDUCE_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])
            
            elif query_word == bufer[0] and (stack[-1] == action_word or stack[-1] == 'root'):
                action = 'RAquery_action'
                stack.append(bufer.pop(-1))
                relation = '{query(%s, ?)}'%(stack[-1])
                data.append([action, ','.join(stack), ','.join(bufer), relation])

            elif ('tên môn học' == bufer[0] or 'môn học' == bufer[0]) and 'cho biết' == stack[-1]:
                action, stack, bufer, relation = apdg.LAgive_each_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])
                action, stack, bufer, relation = apdg.shift_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])
                action, stack, bufer, relation = apdg.shift_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])
                if next_number_state != 'cho biết nhiều':
                    next_number_state = 'cho biết'

            elif 'môn học' == bufer[0] and 'mã' == stack[-1] and ((next_number_state != 'cho biết' and next_number_state != 'cho biết nhiều' and next_number_state ) or ('tên môn học' == stack[-2] and next_number_state != 'cho biết nhiều')):
                action, stack, bufer, relation = apdg.LAma_mod_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])
                action, stack, bufer, relation = apdg.REDUCE_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])

            elif 'học kỳ' == bufer[0] and ('một' == stack[-1] or 'hai' == stack[-1] or 'cả 2' == stack[-1] or 'cả hai' == stack[-1] or '1 hoặc 2' == stack[-1]):
                action, stack, bufer, relation = apdg.LAnum_mod_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])
            
            elif bufer[0].isnumeric() and 'mã số' == stack[-1]:
                action, stack, bufer, relation = apdg.RAnum_ma_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])
                action, stack, bufer, relation = apdg.REDUCE_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])
                action, stack, bufer, relation = apdg.REDUCE_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])
                if stack[-1] == 'môn học':
                    action, stack, bufer, relation = apdg.REDUCE_action(stack, bufer)
                    data.append([action, ','.join(stack), ','.join(bufer), relation])

            elif 'mã số' == bufer[0] and 'cho biết'== stack[-1]:
                action, stack, bufer, relation = apdg.LAgive_only_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])

            elif 'cùng học kỳ' == bufer[0]:
                action, stack, bufer, relation = apdg.RAhk_same_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])
                action, stack, bufer, relation = apdg.REDUCE_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])

            elif 'cùng năm học' == bufer[0]:
                action, stack, bufer, relation = apdg.RAnh_same_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])
                action, stack, bufer, relation = apdg.REDUCE_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])

            elif bufer[0] == 'môn học' and bufer[1] == 'năm học' and stack[-1] == 'mã' and stack[-2] == 'tên môn học' and next_number_state == 'cho biết nhiều':
                bufer.pop(0)
                bufer.pop(0)
                bufer.insert(0, 'mã môn học')
                action, stack, bufer, relation = apdg.LAgive_each_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])
                bufer.insert(0, 'năm học')
                action, stack, bufer, relation = apdg.LAgive_each_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])
                bufer.remove('mã môn học')
                bufer.remove('năm học')

            elif stack[-1] == action_word and bufer[0].isnumeric() and bufer[1] == 'năm học' and not bufer[2].isnumeric() and next_number_state != 'không dạy':
                bufer.pop(0)
                bufer.insert(1, '1 hoặc 2')
                bufer.insert(0, 'học kỳ')
                bufer.insert(0, '1 hoặc 2')
                action = 'convert word to full meaning'
                relation = 'chỉ dạy 1 năm học -> dạy 1 hoặc 2 học kỳ năm học 1 hoặc 2'
                data.append([action, ','.join(stack), ','.join(bufer), relation])

            elif bufer[0] == 'tên' and bufer[1] == 'mã số' and bufer[2] == 'môn học':
                bufer.pop(0)
                bufer.pop(0)
                bufer.pop(0)
                bufer.insert(0, 'môn học')
                bufer.insert(0, 'mã')
                bufer.insert(0, 'tên môn học')
                action = 'convert word to full meaning'
                relation = 'tên mã số môn học -> tên môn học mã môn học'
                data.append([action, ','.join(stack), ','.join(bufer), relation])
                next_number_state = 'cho biết nhiều'    

            elif stack[-1] == action_word and bufer[0].isnumeric() and bufer[1] == 'năm học' and not bufer[2].isnumeric() and next_number_state == 'không dạy':
                bufer.pop(0)
                bufer.pop(0)
                bufer.insert(0, '1 hoặc 2')
                bufer.insert(0, 'năm học')
                bufer.insert(0, '1 2')
                bufer.insert(0, 'học kỳ')
                action = 'convert word to full meaning'
                relation = 'không dạy trong 1 năm -> không dạy 1 và 2 học kỳ năm học 1 hoặc 2'
                data.append([action, ','.join(stack), ','.join(bufer), relation])
                next_number_state = 'cho biết'                

            else:
                action, stack, bufer, relation = apdg.shift_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])

            if len(bufer) == 0:
                break

        df = pd.DataFrame(data, columns=['Action', 'Stack ', 'Bufer', 'Relation'])
        relation_sentences.extend([index_sentence + 1, df['Relation'].tolist()])
        df.to_excel(f'result/parsing_dependency_grammar/{index_sentence + 1}.xlsx')
        
        return relation_sentences
    
    def grammatical_relations(self, relation : list):
        relation_values = list(filter(None, relation[1]))
        relation_values.remove('{query(?, ?)}')
        relation_values.remove('{root(root, dạy)}')

        data = list()
        rela = list()
        next_rela = list()

        grela = ''

        while len(relation_values) > 0 or len(next_rela) > 0:
            rela.clear()
            grela = ''

            if '{WH_count(môn học, bao nhiêu)}' in relation_values:
                rela.append('{WH_count(môn học, bao nhiêu)}')
                grela = 'WH_count MH ? m1'
                relation_values.remove('{WH_count(môn học, bao nhiêu)}')
                data.append([','.join(rela), grela])

            elif '{dobj(dạy, môn học)}' in relation_values:
                rela.append('{dobj(dạy, môn học)}')
                grela = 'môn học ? m1'
                relation_values.remove('{dobj(dạy, môn học)}')
                data.append([','.join(rela), grela])

            elif '{hk_time(dạy, học kỳ)}' in relation_values and '{num_hk(học kỳ, 1)}' in relation_values:
                rela.append('{hk_time(dạy, học kỳ)}')
                grela = 'HK ? hk'
                relation_values.remove('{hk_time(dạy, học kỳ)}')
                data.append([','.join(rela), grela])

                rela.clear()
                grela = ''
        
                rela.append('{num_hk(học kỳ, 1)}')
                grela = 'HK ? nk=1'
                relation_values.remove('{num_hk(học kỳ, 1)}')
                data.append([','.join(rela), grela])

                rela.clear()
                grela = ''

                rela.append('HK ? hk')
                rela.append('HK ? nk=1')
                grela = 'HK=1'

                next_rela.append('HK=1')

            elif '{nh_mod(học kỳ, năm học)}' in relation_values and '{num_nh(năm học, 1)}' in relation_values:
                rela.append('{nh_mod(học kỳ, năm học)}')
                grela = 'NH ? nh'
                relation_values.remove('{nh_mod(học kỳ, năm học)}')
                data.append([','.join(rela), grela])

                rela.clear()
                grela = ''
        
                rela.append('{num_nh(năm học, 1)}')
                grela = 'NH ? nh=1'
                relation_values.remove('{num_nh(năm học, 1)}')
                data.append([','.join(rela), grela])

                rela.clear()
                grela = ''

                rela.append('HK ? hk')
                rela.append('HK ? nk=1')
                grela = 'NH=1'

                next_rela.append('NH=1')

            elif 'HK=1' in next_rela and 'NH=1' in next_rela:
                rela.append('HK=1')
                rela.append('NH=1')
                grela = 'HK=1&NH1'
                data.append([','.join(rela), grela])
                next_rela.clear()

        df = pd.DataFrame(data, columns=['Relation', 'Grammatical relations'])
        df.to_excel(f'result/grammatical_relations/{relation[0]}.xlsx')

    def logical_form(self):
        pass

    def procedural_semantics(self):
        pass

if __name__ == '__main__':
    nlp = NPL()
    list_questions = nlp.read_questions()
    list_questions = ['1) Có bao nhiêu môn học được dạy trong học kỳ 1, năm học thứ 1 ?.']
    for i, s in enumerate(list_questions):
        print(s)
        sentence = nlp.sentence_segment(s)
        relation_sentences = nlp.parsing_dependency_grammar(sentence, i)
        nlp.grammatical_relations(relation_sentences)
        print('--$$--')

    print('Done !')
    print('\n')
    exit(0)