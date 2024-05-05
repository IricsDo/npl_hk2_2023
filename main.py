import pandas as pd
import action_parsing_dependcy_grammar as apdg
import copy
import re
class NPL:
    def __init__(self) -> None:
        self.df = pd.read_excel('input/data.xlsx', dtype={'TT': str, 'Môn học': str, 'MSMH': str, 'NH1': str, 'NH2': str})

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
        condition_state = ''

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
                condition_state = 'chỉ dạy'
            
            elif bufer[0] == 'môn học' and bufer[1] == 'không' and bufer[2] == action_word:
                bufer.insert(0, 'bao nhiêu')
                action = 'add word to full meaning'
                relation = 'môn học -> bao nhiêu môn học'
                data.append([action, ','.join(stack), ','.join(bufer), relation])

            elif stack[-1] == 'môn học' and bufer[0] == 'không' and bufer[1] == action_word and bufer[2].isnumeric() and condition_state != 'chỉ dạy':
                action, stack, bufer, relation = apdg.LA_dobj_no_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])
                next_number_state = 'không dạy'

            elif 'môn học' == stack[-1] and 'mã số' != stack[-2] and 'mã số' != bufer[0] and bufer[0] != 'chỉ' and condition_state != 'chỉ dạy':
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
                if not bufer[2].isnumeric() and bufer[2] == 'không':
                    bufer[0] = '1 2'
                    next_number_state = 'cả 2'
                    condition_state = 'cả 2'
                action, stack, bufer, relation = apdg.RAnum_hk_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])
                if stack[-1].isnumeric() and bufer[0] == 'năm học' and not bufer[1].replace(' ', '').isnumeric():
                    next_number_state = ''
                    continue
                action, stack, bufer, relation = apdg.REDUCE_action(stack, bufer)
                data.append([action, ','.join(stack), ','.join(bufer), relation])
                next_number_state = ''

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
                    elif condition_state == 'cả 2':
                        bufer.insert(1, '1 hoặc 2')
                        bufer.insert(0, '1 2')
                        action = 'convert word to full meaning'
                        relation = 'học kỳ năm học -> học kì 1 và 2 năm học 1 hoặc 2'
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

            elif 'môn học' == bufer[0] and 'mã' == stack[-1] and ((next_number_state != 'cho biết' and next_number_state != 'cho biết nhiều' and next_number_state ) or ('tên môn học' == stack[-2] and next_number_state != 'cho biết nhiều') or condition_state == 'chỉ dạy'):
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
                if stack[-1] == 'môn học' and bufer[-2].isnumeric():
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
        relation_sentences = df['Relation'].tolist()
        df.to_excel(f'result/parsing_dependency_grammar/{index_sentence + 1}.xlsx')
        
        return relation_sentences
    
    def grammatical_relations(self, relation : list, index_sentence: int):

        pre_logical_form = list()

        relation_values = list(filter(None, relation))
        if '{query(?, ?)}' in relation_values:
            relation_values.remove('{query(?, ?)}')
        if '{root(root, dạy)}' in relation_values:
            relation_values.remove('{root(root, dạy)}')
        if '{num_det(học kỳ, cả hai)}' in relation_values and '{num_hk(học kỳ, 1 2)}' in relation_values:
            relation_values.remove('{num_det(học kỳ, cả hai)}')
        if '{dobj(dạy, môn học)}' in relation_values and '{dobj_only(dạy, môn học)}' in relation_values:
            relation_values.remove('{dobj_only(dạy, môn học)}')

        temp = copy.deepcopy(relation_values)
        for rv in temp:
            if '{'not in rv and '}' not in rv:
                relation_values.remove(rv)

        data = list()
        rela = list()
        logical = list()
        next_rela = list()

        grela = ''

        while len(relation_values) > 0 or len(next_rela) > 0:
            rela.clear()
            grela = ''

            if '{WH_count(môn học, bao nhiêu)}' in relation_values:
                rela.append('{WH_count(môn học, bao nhiêu)}')
                grela = '(WH_count MH ? m1)'
                relation_values.remove('{WH_count(môn học, bao nhiêu)}')
                data.append([','.join(rela), grela])
                logical.append(grela)
                
            elif '{dobj(dạy, môn học)}' in relation_values:
                rela.append('{dobj(dạy, môn học)}')
                grela = '(MH ? m1)'
                relation_values.remove('{dobj(dạy, môn học)}')
                data.append([','.join(rela), grela])
                logical.append(grela)

            elif '{dobj_only(dạy, môn học)}' in relation_values:
                rela.append('{dobj_only(dạy, môn học)}')
                grela = '(MH_ONLY ? m1)'
                relation_values.remove('{dobj_only(dạy, môn học)}')
                data.append([','.join(rela), grela])
                logical.append(grela)

            elif '{dobj_no(dạy, môn học)}' in relation_values:
                rela.append('{dobj_no(dạy, môn học)}')
                grela = '(MH_NO ? m1)'
                relation_values.remove('{dobj_no(dạy, môn học)}')
                data.append([','.join(rela), grela])
                logical.append(grela)

            elif '{hk_time(dạy, học kỳ)}' in relation_values:
                rela.append('{hk_time(dạy, học kỳ)}')
                grela = '(HK ? hk)'
                relation_values.remove('{hk_time(dạy, học kỳ)}')
                data.append([','.join(rela), grela])

                rela.clear()
                grela = ''
                next_hk = ''

                if '{num_hk(học kỳ, 1)}' in relation_values:
                    next_hk = '1'
                    remove_word = next_hk
                    rela.append('{num_hk(học kỳ, %s)}'%(next_hk))
                    relation_values.remove('{num_hk(học kỳ, %s)}'%(remove_word))

                elif '{num_hk(học kỳ, 2)}' in relation_values:
                    next_hk = '2'
                    remove_word = next_hk
                    rela.append('{num_hk(học kỳ, %s)}'%(next_hk))
                    relation_values.remove('{num_hk(học kỳ, %s)}'%(remove_word))

                elif '{num_hk(học kỳ, 1 hoặc 2)}' in relation_values:
                    next_hk = '1^2'
                    remove_word = '1 hoặc 2'
                    rela.append('{num_hk(học kỳ, %s)}'%(next_hk))
                    relation_values.remove('{num_hk(học kỳ, %s)}'%(remove_word))

                elif '{num_hk(học kỳ, 1 2)}' in relation_values:
                    next_hk = '1&2'
                    remove_word = '1 2'
                    rela.append('{num_hk(học kỳ, %s)}'%(next_hk))
                    relation_values.remove('{num_hk(học kỳ, %s)}'%(remove_word))
                    
                elif '{num_det(học kỳ, cả hai)}' in relation_values:
                    next_hk = '1&2'
                    remove_word = 'cả hai'
                    rela.append('{num_det(học kỳ, %s)}'%(next_hk))
                    relation_values.remove('{num_det(học kỳ, %s)}'%(remove_word))

                elif '{num_det(học kỳ, cả 2)}' in relation_values:
                    next_hk = '1&2'
                    remove_word = 'cả 2'
                    rela.append('{num_det(học kỳ, %s)}'%(next_hk))
                    relation_values.remove('{num_det(học kỳ, %s)}'%(remove_word))

                else:
                    continue

                grela = '(HK ? nk=%s)'%(next_hk)
                data.append([','.join(rela), grela])

                rela.clear()
                grela = ''

                rela.append('HK ? hk')
                rela.append('HK ? nk=%s'%(next_hk))
                grela = '(HK=%s)'%(next_hk)
                data.append([','.join(rela), grela])

                next_rela.append('HK=%s'%(next_hk))

            elif '{nh_mod(học kỳ, năm học)}' in relation_values:
                rela.append('{nh_mod(học kỳ, năm học)}')
                grela = '(NH ? nh)'
                relation_values.remove('{nh_mod(học kỳ, năm học)}')
                data.append([','.join(rela), grela])

                rela.clear()
                grela = ''
                next_nh = ''
                remove_word = ''
                if '{num_nh(năm học, 1)}' in relation_values:
                    next_nh = '1'
                    remove_word = next_nh
                elif '{num_nh(năm học, 2)}' in relation_values:
                    next_nh = '2'
                    remove_word = next_nh
                elif '{num_nh(năm học, 1 2)}' in relation_values:
                    next_nh = '1&2'
                    remove_word = '1 2'
                elif '{num_nh(năm học, 1 hoặc 2)}' in relation_values:
                    next_nh = '1^2'
                    remove_word = '1 hoặc 2'
                else:
                    continue

                rela.append('{num_nh(năm học, %s)}'%(next_nh))
                grela = '(NH ? nh=%s)'%(next_nh)
                relation_values.remove('{num_nh(năm học, %s)}'%(remove_word))
                data.append([','.join(rela), grela])

                rela.clear()
                grela = ''

                rela.append('NH ? nh')
                rela.append('NH ? nh=%s'%(next_nh))
                grela = '(NH=%s)'%(next_nh)
                data.append([','.join(rela), grela])

                next_rela.append('NH=%s'%(next_nh))

            elif len(relation_values) == 0:

                nh = ''
                if 'NH=1' in next_rela:
                    nh = '1'
                elif 'NH=2' in next_rela:
                    nh = '2'
                elif 'NH=1&2' in next_rela:
                    nh = '1&2'
                elif 'NH=1^2' in next_rela:
                    nh = '1^2'
                else:
                    continue

                set_nh = ''
                remove_word = ''
                rela.append('NH=%s'%(nh))

                if 'HK=1' in next_rela:
                    set_nh = '1'
                    remove_word = set_nh
                elif 'HK=2' in next_rela:
                    set_nh = '2'
                    remove_word = set_nh
                elif 'HK=1&2' in next_rela:
                    set_nh = '1&2'
                    remove_word = set_nh
                elif 'HK=1 hoặc 2' in next_rela:
                    set_nh = '1^2'
                    remove_word = '1 hoặc 2'
                elif 'HK=1^2' in next_rela:
                    set_nh = '1^2'
                    remove_word = '1^2'
                else:
                    continue

                rela.append('HK=%s'%(set_nh))
                grela = '((HK=%s)&(NH=%s))'%(set_nh, nh)
                data.append([','.join(rela), grela])
                next_rela.clear()
                logical.append(grela)

            elif len(relation_values) == 0:
                
                hk = ''
                if 'HK=1' in next_rela:
                    hk = '1'
                elif 'HK=2' in next_rela:
                    hk = '2'
                elif 'HK=1&2' in next_rela:
                    hk = '1&2'
                elif 'HK=1^2' in next_rela:
                    hk = '1^2'
                else:
                    continue

                set_nh = ''
                remove_word = ''
                rela.append('HK=%s'%(hk))

                if 'NH=1' in next_rela:
                    set_nh = '1'
                    remove_word = set_nh
                elif 'NH=2' in next_rela:
                    set_nh = '2'
                    remove_word = set_nh
                elif 'NH=1&2' in next_rela:
                    set_nh = '1&2'
                    remove_word = set_nh
                elif 'NH=1 hoặc 2' in next_rela:
                    set_nh = '1^2'
                    remove_word = '1 hoặc 2'
                elif 'NH=1^2' in next_rela:
                    set_nh = '1^2'
                    remove_word = '1^2'
                else:
                    continue

                rela.append('NH=%s'%(set_nh))
                grela = '((HK=%s)&(NH=%s))'%(hk, set_nh)
                data.append([','.join(rela), grela])
                next_rela.clear()
                logical.append(grela)

            elif 'HK=1^2' in next_rela and 'NH=1^2' in next_rela and len(relation_values) == 0:
                rela.append('HK=1^2')
                rela.append('NH=1^2')
                grela = '((HK=1^2)&(NH=1^2))'
                data.append([','.join(rela), grela])
                next_rela.clear()
                logical.append(grela)

            elif '{give_each(tên môn học, cho biết)}' in relation_values:
                rela.append('{give_each(tên môn học, cho biết)}')
                grela = '(EACH ? m1)'
                relation_values.remove('{give_each(tên môn học, cho biết)}')
                data.append([','.join(rela), grela])
                logical.append(grela)

            elif '{give_each(môn học, cho biết)}' in relation_values:
                rela.append('{give_each(môn học, cho biết)}')
                grela = '(EACH ? m1)'
                relation_values.remove('{give_each(môn học, cho biết)}')
                data.append([','.join(rela), grela])
                logical.append(grela)

            elif '{ma_mod(môn học, mã)}' in relation_values: 
                rela.append('{ma_mod(môn học, mã)}')
                grela = '(MSMH ? m1)'
                relation_values.remove('{ma_mod(môn học, mã)}')
                data.append([','.join(rela), grela])
                logical.append(grela)

            elif '{give_each(mã môn học, cho biết)}' in relation_values:
                rela.append('{give_each(mã môn học, cho biết)}')
                grela = '(MSMH ? m1)'
                relation_values.remove('{give_each(mã môn học, cho biết)}')
                data.append([','.join(rela), grela])
                logical.append(grela)
            
            elif '{give_each(năm học, cho biết)}' in relation_values:
                rela.append('{nh_mod(học kỳ, năm học)}')
                grela = '(NH ? nh)'
                relation_values.remove('{give_each(năm học, cho biết)}')
                data.append([','.join(rela), grela])

            elif '{hk_time(dạy, học kỳ)}' in relation_values:

                rela.append('{hk_time(dạy, học kỳ)}')
                grela = '(HK ? hk)'
                relation_values.remove('{hk_time(dạy, học kỳ)}')
                data.append([','.join(rela), grela])

                rela.clear()
                grela = ''

                if '{num_det(học kỳ, cả hai)}' in relation_values:
                    rela.append('{num_det(học kỳ, cả hai)}')
                    grela = '(HK=1&2)'
                    relation_values.remove('{num_det(học kỳ, cả hai)}')
                    data.append([','.join(rela), grela])

                    rela.clear()
                    grela = ''

                    rela.append('HK=1&2')
                    rela.append('HK ? hk')
                    grela = '(HK=1&2)'
                    data.append([','.join(rela), grela])

                    next_rela.append('HK=1&2')

                else:
                    continue

            elif re.search(r"\d{6}", ''.join(relation_values)):
                number = re.search(r"\d{6}", ''.join(relation_values)).group()
                rela.append('{num_ma(mã số, %s)}'%(number))
                grela = '(MSMH = %s)'%(number)
                relation_values.remove('{num_ma(mã số, %s)}'%(number))
                data.append([','.join(rela), grela])
                logical.append(grela)

            elif '{give_only(mã số, cho biết)}' in relation_values:
                rela.append('{give_only(mã số, cho biết)}')
                grela = '(ONLY ? mh1)'
                relation_values.remove('{give_only(mã số, cho biết)}')
                data.append([','.join(rela), grela])
                logical.append(grela)

            elif re.findall(r"{name_mh.+}",''.join(relation_values)) and len(relation_values) == 1:
                mh = re.search(r', .+', ''.join(relation_values)).group()
                mh = mh.replace(',', '')
                mh = mh.replace(')}', '')
                mh = mh.strip()
                mh = mh.replace('“', '')
                mh = mh.replace('”', '')
                mh = '(' + mh + ')'
                rela.append(mh)
                grela = mh
                relation_values.remove(re.search(r"{name_mh.+}", ''.join(relation_values)).group())
                data.append([','.join(rela), grela])
                logical.append(grela)

            elif '{hk_same(học kỳ, cùng học kỳ)}' in relation_values:
                rela.append('{hk_same(học kỳ, cùng học kỳ)}')
                grela = '(HK ? hk=cùng)'
                relation_values.remove('{hk_same(học kỳ, cùng học kỳ)}')
                data.append([','.join(rela), grela])
                logical.append(grela)

            elif '{nh_same(năm học, cùng năm học)}' in relation_values:
                rela.append('{nh_same(năm học, cùng năm học)}')
                grela = '(NH ? nh=cùng)'
                relation_values.remove('{nh_same(năm học, cùng năm học)}')
                data.append([','.join(rela), grela])
                logical.append(grela)


        df = pd.DataFrame(data, columns=['Relation', 'Grammatical relations'])
        pre_logical_form = logical
        df.to_excel(f'result/grammatical_relations/{index_sentence+1}.xlsx')

        return pre_logical_form
    
    def logical_form(self, pre_logical_form: list, index_sentence : int):
        pre_logical_form_values = list(filter(None, pre_logical_form))
            
        logical_form = ''.join(pre_logical_form_values)
        logical_form = '(' + logical_form + ')'

        with open(f'result/logical_form/{index_sentence + 1}.txt', 'w', encoding='utf-8') as f:
            f.write(logical_form)
        
        return logical_form

    def procedural_semantics(self, logical_form : list, index_sentence: int):
        procedural_semantics = copy.deepcopy(logical_form)

        if 'EACH ? m1' in logical_form:
            procedural_semantics = procedural_semantics.replace('EACH ? m1', 'ITERATE ? m1 (CHECK-ALL-TRUE)')

        if 'WH_count MH ? m1' in logical_form:
            procedural_semantics = procedural_semantics.replace('WH_count MH ? m1', 'PRINT-ALL ? m1')

        with open(f'result/procedural_semantics/{index_sentence + 1}.txt', 'w', encoding='utf-8') as f:
            f.write(procedural_semantics)

        return procedural_semantics

    def answer_question(self, final_resutl: str, index_sentence : int):
        answer = ''

        while True:
            if '(PRINT-ALL ? m1)(MH ? m1)' in final_resutl:
                if '((HK=1)&(NH=1))' in final_resutl:
                    answer = str(self.df['NH1'].to_list().count('10'))
                    break
                elif '((HK=2)&(NH=1))' in final_resutl:
                    answer = str(self.df['NH1'].to_list().count('02'))
                    break
                elif '((HK=1&2)&(NH=1))' in final_resutl:
                    answer = str(self.df['NH1'].to_list().count('12'))
                    break
                elif '((HK=1)&(NH=2))' in final_resutl:
                    answer = str(self.df['NH2'].to_list().count('10'))
                    break
                elif '((HK=2)&(NH=2))' in final_resutl:
                    answer = str(self.df['NH2'].to_list().count('02'))
                    break
                elif '((HK=1&2)&(NH=2))' in final_resutl:
                    answer = str(self.df['NH2'].to_list().count('12'))
                    break
                elif '((HK=1)&(NH=1&2))' in final_resutl:
                    answer = str(self.df['NH1'].to_list().count('10') + self.df['NH2'].to_list().count('10'))
                    break
                elif '((HK=2)&(NH=1&2))' in final_resutl:
                    answer = str(self.df['NH1'].to_list().count('02') + self.df['NH2'].to_list().count('02'))
                    break
                elif '((HK=1&2)&(NH=1&2))' in final_resutl:
                    answer = str(self.df['NH1'].to_list().count('12') + self.df['NH2'].to_list().count('12'))
                    break
            elif '(MH ? m1)(ITERATE ? m1 (CHECK-ALL-TRUE))(MSMH ? m1)' in final_resutl:
                indexs = list()
                if '((HK=1&2)&(NH=1))' in final_resutl:
                    indexs = [i for i, x in enumerate(self.df['NH1'].to_list()) if x == '12']
                elif '((HK=1&2)&(NH=2))' in final_resutl:
                    indexs = [i for i, x in enumerate(self.df['NH2'].to_list()) if x == '12']
                elif '((HK=1&2)&(NH=1&2))' in final_resutl:
                    index1 = [i for i, x in enumerate(self.df['NH1'].to_list()) if x == '12']
                    index2 = [i for i, x in enumerate(self.df['NH2'].to_list()) if x == '12']
                    indexs = list(set(index1).intersection(index2))
                else:
                    continue
                mh = self.df['Môn học'].to_list()
                ms = self.df['MSMH'].to_list()
                for i in indexs:
                    answer +=  mh[i] + '-' + ms[i] + '\n'
                break
            elif '(ITERATE ? m1 (CHECK-ALL-TRUE))' in final_resutl and re.search(r"(MSMH = \d{6})", final_resutl):
                if '(HK=1^2)&(NH=1^2)' in final_resutl:
                    ms = self.df['MSMH'].to_list()
                    nh = ms.index(re.search(r"\d{6}", final_resutl).group())
                    nh1 = self.df['NH1'].to_list()[nh]
                    nh2 = self.df['NH2'].to_list()[nh]

                    if nh1 != '00':
                        if nh1 == '10':
                            answer += 'học kỳ 1, năm học 1' + '\n'
                        elif nh1 == '02':
                            answer += 'học kỳ 2, năm học 1' + '\n'
                        else:
                            answer += 'cả 2 học kỳ, năm học 1' + '\n'
                    if nh2 != '00':
                        if nh2 == '10':
                            answer += 'học kỳ 1, năm học 2' + '\n'
                        elif nh2 == '02':
                            answer += 'học kỳ 2, năm học 2' + '\n'
                        else:
                            answer += 'cả 2 học kỳ, năm học 2' + '\n' 
                    break   
                else:
                    mh = self.df['Môn học'].to_list()
                    ms = self.df['MSMH'].to_list()
                    answer = mh[ms.index(re.search(r"\d{6}", final_resutl).group())]
                    break
            elif '(ONLY ? mh1)' in final_resutl:
                mh = self.df['Môn học'].to_list()
                ms = self.df['MSMH'].to_list()
                name = final_resutl.replace('(ONLY ? mh1)', '')
                name = name.replace('((', '')
                name = name.replace('))', '')
                name = name.capitalize()
                answer = ms[mh.index(name)]
                break
            elif '(MH ? m1)(MH ? m1)' in final_resutl and '(HK ? hk=cùng)(NH ? nh=cùng)' in final_resutl:
                string = final_resutl.replace('(MH ? m1)(MH ? m1)', '')
                string = string.replace('(HK ? hk=cùng)(NH ? nh=cùng)', '')
                string = string.replace('((', '')
                string = string.replace('))', '')
                string = string.replace(')(', '|')
                string = string.split('|')
                ms1 = re.search(r"\d{6}", string[0]).group()
                ms2 = re.search(r"\d{6}", string[1]).group()
                ms = self.df['MSMH'].to_list()
                i1 = ms.index(ms1)
                i2 = ms.index(ms2)
                nh1 = self.df['NH1'].to_list()
                nh2 = self.df['NH2'].to_list()
                if nh1[i1] == nh1[i2] or nh2[i2] == nh2[i1]:
                    answer = 'Có'
                else:
                    answer = 'Không'
                break
            elif '(MH ? m1)' in final_resutl and re.search(r"(MSMH = \d{6})", final_resutl):
                ms = self.df['MSMH'].to_list()
                index = ms.index(re.search(r"\d{6}", final_resutl).group())
                nh1 = self.df['NH1'].to_list()
                nh2 = self.df['NH2'].to_list()
                if nh1[index] == '12' or nh2[index] == '12':
                    answer = 'Có'
                else:
                    answer = 'Không'
                break
            elif '((MH_ONLY ? m1)(ITERATE ? m1 (CHECK-ALL-TRUE))(MSMH ? m1)((HK=1^2)&(NH=1^2)))'in final_resutl:
                nh1 = self.df['NH1'].to_list()
                nh2 = self.df['NH2'].to_list()
                index1 =  [i for i, x in enumerate(nh1) if x == '00']
                for i in index1:
                    hk = nh2[i]
                    if hk == '10':
                        answer += self.df['Môn học'].to_list()[i] + '-' + self.df['MSMH'].to_list()[i] + '-' + 'học kỳ 1 năm học thứ 2' + '\n'
                    elif hk == '02':
                        answer += self.df['Môn học'].to_list()[i] + '-' + self.df['MSMH'].to_list()[i] + '-' + 'học kỳ 2 năm học thứ 2'+ '\n'
                    elif hk == '12':
                        answer += self.df['Môn học'].to_list()[i] + '-' + self.df['MSMH'].to_list()[i] + '-' + 'học kỳ 1 và 2 năm học thứ 2'+ '\n'
                
                index2 =  [i for i, x in enumerate(nh2) if x == '00']
                for i in index2:
                    hk = nh1[i]
                    if hk == '10':
                        answer += self.df['Môn học'].to_list()[i] + '-' + self.df['MSMH'].to_list()[i] + '-' + 'học kỳ 1 năm học thứ 1'+ '\n'
                    elif hk == '02':
                        answer += self.df['Môn học'].to_list()[i] + '-' + self.df['MSMH'].to_list()[i] + '-' + 'học kỳ 2 năm học thứ 1'+ '\n'
                    elif hk == '12':
                        answer += self.df['Môn học'].to_list()[i] + '-' + self.df['MSMH'].to_list()[i] + '-' + 'học kỳ 1 và 2 năm học thứ 1'+ '\n'
                break
            elif '((PRINT-ALL ? m1)(MH_NO ? m1)(ITERATE ? m1 (CHECK-ALL-TRUE))(MSMH ? m1)((HK=1&2)&(NH=1^2)))' in final_resutl:
                nh1 = self.df['NH1'].to_list()
                nh2 = self.df['NH2'].to_list()

                index1 =  [i for i, x in enumerate(nh1) if x == '00']
                for i in index1:
                    hk = nh1[i]
                    answer += self.df['Môn học'].to_list()[i] + '-' + self.df['MSMH'].to_list()[i] + '-' + 'năm học thứ 1'+ '\n'
                
                index2 =  [i for i, x in enumerate(nh2) if x == '00']
                for i in index2:
                    hk = nh2[i]
                    answer += self.df['Môn học'].to_list()[i] + '-' + self.df['MSMH'].to_list()[i] + '-' + 'năm học thứ 2'+ '\n'
                
                break

        with open(f'result/answer_question/{index_sentence + 1}.txt', 'w', encoding='utf-8') as f:
            f.write(answer)

        return answer
if __name__ == '__main__':
    nlp = NPL()
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