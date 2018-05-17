# coding:utf8


CN_NUM = {
    u'〇': 0,
    u'一': 1,
    u'二': 2,
    u'三': 3,
    u'四': 4,
    u'五': 5,
    u'六': 6,
    u'七': 7,
    u'八': 8,
    u'九': 9,
    u'零': 0,
    u'壹': 1,
    u'贰': 2,
    u'叁': 3,
    u'肆': 4,
    u'伍': 5,
    u'陆': 6,
    u'柒': 7,
    u'捌': 8,
    u'玖': 9,
    u'两': 2,
}
CN_UNIT = {
    u'十': 10,
    u'拾': 10,
    u'百': 100,
    u'佰': 100,
    u'千': 1000,
    u'仟': 1000,
    u'万': 10000,
    u'萬': 10000,
    u'亿': 100000000,
    u'億': 100000000,
    u'兆': 1000000000000,
}


def tab_and_sum(tmp_list):
    """对单位: 千,百,十,个 自动补全和求和

    示例:
        [9]                        [9, 1]                    9
        [10, 1]                    [1, 10, 1, 1]             11
        [1, 100, 2, 10, 3]         [1, 100, 2, 10, 3, 1]     123
        [1, 1000, 2, 100, 3, 1]    [1, 1000, 2, 100, 3, 1]   1203
    """
    if tmp_list:
        tmp_list = list(filter(lambda x: x != 0, tmp_list))
        if tmp_list[0] >= 10:
            tmp_list.insert(0, 1)
        if tmp_list[-1] < 10:
            tmp_list.append(1)
    else:
        tmp_list = []
    return sum(num * unit for num, unit in zip(tmp_list[0::2], tmp_list[1::2]))


def cn2dig(cn):
    cn = list(cn)
    tmp_list = []
    result = 0
    while cn:
        cur_char = cn.pop(0)
        if cur_char in CN_NUM:
            cur_num = CN_NUM.get(cur_char)
            tmp_list.append(cur_num)
            continue
        if cur_char in CN_UNIT:
            cur_unit = CN_UNIT.get(cur_char)
            if cur_unit in [1000000000000, 100000000, 10000]:
                result += tab_and_sum(tmp_list) * cur_unit
                tmp_list = []
            else:
                tmp_list.append(cur_unit)
    result += tab_and_sum(tmp_list)
    return result


if __name__ == '__main__':
    test_dig = [
        u'九',
        u'十一',
        u'一百二十三',
        u'一千二百零三',
        u'一万一千一百零一',
        u'十万零三千六百零九',
        u'一百二十三万四千五百六十七',
        u'一千一百二十三万四千五百六十七',
        u'一亿一千一百二十三万四千五百六十七',
        u'一百零二亿五千零一万零一千零三十八',
        u'一千一百一十一亿一千一百二十三万四千五百六十七',
        u'一兆一千一百一十一亿一千一百二十三万四千五百六十七',
    ]

    for cn in test_dig:
        print(cn2dig(cn))