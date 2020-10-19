

def get_stock_list():
    stock_list = [['瑞軒','2489'],['可寧衛','8422'],['中華電信','2412'],['台灣大哥大','3045'],['第一金','2892'],['遠傳電信','4904'],['統一','1216'],['富邦金','2881'],['鴻海','2317'],['台積電','2330']]
    stock_list.append(['正新','2105'])
    stock_list.append(['中信金','2891'])
    stock_list.append(['聯華食','1231'])
    stock_list.append(['聯華','1229'])
    return stock_list

def get_stock_thre():
    thre_dic = {'第一金':16.5,'聯華':36,'中華電信':105,'台灣大哥大':105,'可寧衛':170,'瑞軒':16,'富邦金':50,'鴻海':91,'台積電':200}
    thre_dic['正新'] = 50
    thre_dic['統一'] = 60
    thre_dic['聯華食'] = 30
    thre_dic['中信金'] = 35
    return thre_dic

def get_stock_default():
#     return '統一','1216'
#     return  '鴻海','2317'
    # return  '中華電信','2412'
#     return  '瑞軒','2489'
    # return  '正新','2105'
#     return  '可寧衛','8422'
#     return  '富邦金','2881'
#     return  '台積電','2330'
    # return  '聯華食','1231'
    # return  '聯華','1229'
#     return  '第一金','2892'
    # return  '遠傳電信','4904'
    # return  '台灣大哥大','3045'
    return '中信金','2891'
