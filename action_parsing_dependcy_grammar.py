def shift_action(stack: list, bufer: list):
    stack.append(bufer.pop(0))
    relation = ''
    action = 'shift_action'
    return action, stack, bufer, relation

def LAwh_count_action(stack: list, bufer: list):
    stack.remove('bao nhiêu')
    relation = '{WH_count(môn học, bao nhiêu)}'
    action = 'LAwh_count_action'
    return action, stack, bufer, relation

def LA_dobj_action(stack: list, bufer: list):
    stack.remove('môn học')
    relation = '{dobj(dạy, môn học)}'
    action = 'LA_dobj_action'
    return action, stack, bufer, relation

def LA_dobj_only_action(stack: list, bufer: list):
    stack.remove('môn học')
    bufer.remove('chỉ')
    relation = '{dobj_only(dạy, môn học)}'
    action = 'LA_dobj_only_action'
    return action, stack, bufer, relation

def LA_dobj_no_action(stack: list, bufer: list):
    stack.remove('môn học')
    bufer.remove('không')
    relation = '{dobj_no(dạy, môn học)}'
    action = 'LA_dobj_no_action'
    return action, stack, bufer, relation

def RAroot_action(stack: list, bufer: list):
    stack.append(bufer.pop(0))
    relation = '{root(root, dạy)}'
    action = 'RAroot_action'
    return action, stack, bufer, relation

def RAhk_time_action(stack: list, bufer: list):
    stack.append(bufer.pop(0))
    relation = '{hk_time(dạy, học kỳ)}'
    action = 'RAhk_time_action'
    return action, stack, bufer, relation

def RAnum_hk_action(stack: list, bufer: list):
    hoc_ky = bufer.pop(0)
    stack.append(hoc_ky)
    relation = '{num_hk(học kỳ, %s)}'%(str(hoc_ky))
    action = 'RAnum_hk_action'
    return action, stack, bufer, relation

def REDUCE_action(stack: list, bufer: list):
    stack.pop(-1)
    relation = ''
    action = 'REDUCE_action'
    return action, stack, bufer, relation

def RAnh_mod_action(stack: list, bufer: list):
    stack.append(bufer.pop(0))
    relation = '{nh_mod(học kỳ, năm học)}'
    action = 'RAnh_mod_action'
    return action, stack, bufer, relation

def RAnum_nh_action(stack: list, bufer: list):
    nam_hoc = bufer.pop(0)
    stack.append(nam_hoc)
    relation = '{num_nh(năm học, %s)}'%(str(nam_hoc))
    action = 'RAnum_nh_action'
    return action, stack, bufer, relation

def RAquery_action(stack: list, bufer: list):
    stack.append(bufer.pop(0))
    relation = ''
    action = 'RAquery_action'
    return action, stack, bufer, relation

def LAgive_each_action(stack : list, bufer: list):
    stack.pop(-1)
    relation = '{give_each(%s, cho biết)}'%(str(bufer[0]))
    action = 'LAgive_each_action'
    return action, stack, bufer, relation

def LAgive_only_action(stack : list, bufer: list):
    stack.pop(-1)
    relation = '{give_only(%s, cho biết)}'%(str(bufer[0]))
    action = 'LAgive_only_action'
    return action, stack, bufer, relation

def LAma_mod_action(stack : list, bufer: list):
    stack.remove('mã')
    relation = '{ma_mod(môn học, mã)}'
    action = 'LAma_mod_action'
    return action, stack, bufer, relation

def RAnum_ma_action(stack: list, bufer: list):
    ma_so = bufer.pop(0)
    stack.append(ma_so)
    relation = '{num_ma(mã số, %s)}'%(str(ma_so))
    action = 'RAnum_ma_action'
    return action, stack, bufer, relation

def RAname_mh_action(stack: list, bufer: list):
    mon_hoc= bufer.pop(0)
    stack.append(mon_hoc)
    relation = '{name_mh(môn học, %s)}'%(str(mon_hoc))
    action = 'RAname_mh_action'
    return action, stack, bufer, relation

def LAnum_mod_action(stack: list, bufer: list):
    hoc_ki = stack.pop(-1)
    relation = '{num_det(học kỳ, %s)}'%(str(hoc_ki))
    action = 'LAnum_mod_action'
    return action, stack, bufer, relation

def RAhk_same_action(stack: list, bufer: list):
    cung_hoc_ky= bufer.pop(0)
    stack.append(cung_hoc_ky)
    relation = '{hk_same(học kỳ, %s)}'%(str(cung_hoc_ky))
    action = 'RAhk_same_action'
    return action, stack, bufer, relation

def RAnh_same_action(stack: list, bufer: list):
    cung_nam_hoc= bufer.pop(0)
    stack.append(cung_nam_hoc)
    relation = '{nh_same(năm học, %s)}'%(str(cung_nam_hoc))
    action = 'RAnh_same_action'
    return action, stack, bufer, relation

def RA_dobj_action(stack: list, bufer: list):
    bufer.remove('môn học')
    relation = '{dobj(môn học, dạy)}'
    action = 'RA_dobj_action'
    return action, stack, bufer, relation

def RAnum_or_nh_action(stack: list, bufer: list):
    nam_hoc = '1 hoặc 2'
    stack.append(nam_hoc)
    relation = '{num_or_nh(năm học, %s)}'%(str(nam_hoc))
    action = 'RAnum_or_nh_action'
    return action, stack, bufer, relation