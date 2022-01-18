# -*- coding: utf-8 -*-

import re
import sys

from ltp import LTP


def gen_my_word_list(text):
    my_word_list = ['中华人民共和国最高人民法院', '男', '女']

    nations = ['阿昌族', '鄂温克族', '傈僳族', '水族', '白族', '高山族', '珞巴族', '塔吉克族', '保安族', '仡佬族', '满族', '塔塔尔族',
               '布朗族', '哈尼族', '毛南族', '土家族', '布依族', '哈萨克族', '门巴族', '土族', '朝鲜族', '蒙古族', '佤族', '达斡尔族',
               '赫哲族', '苗族', '维吾尔族', '傣族', '回族', '仫佬族', '乌孜别克族', '德昂族', '基诺族', '纳西族', '锡伯族', '东乡族',
               '京族', '怒族', '瑶族', '侗族', '景颇族', '普米族', '彝族', '独龙族', '柯尔克孜族', '羌族', '裕固族', '俄罗斯族',
               '拉祜族', '撒拉族', '藏族', '鄂伦春族', '黎族', '畲族', '壮族', '汉族']
    for nation in nations:
        my_word_list.append(nation)

    provinces = ['河北省', '山西省', '辽宁省', '吉林省', '甘肃省', '江苏省', '浙江省', '安徽省', '福建省', '江西省', '山东省',
                 '河南省', '湖北省', '湖南省', '广东省', '海南省', '四川省', '贵州省', '云南省', '陕西省', '青海省', '黑龙江省',
                 '内蒙古自治区', '广西壮族自治区', '西藏自治区', '宁夏回族自治区', '新疆维吾尔自治区', '北京市', '天津市', '上海市', '重庆市']
    posts = ['市', '区', '县', '乡', '镇', '人民法院']
    for province in provinces:
        tmp = province + '[\u4e00-\u9fa5]*'
        for post in posts:
            mo = r'' + tmp + post
            pattern = re.compile(mo)
            my_word_list.extend(pattern.findall(text))

    mo = r'[\u4e00-\u9fa5]*公司'
    pattern = re.compile(mo)
    my_word_list.extend(pattern.findall(text))

    mo = r'犯[\u4e00-\u9fa5]*罪'
    pattern = re.compile(mo)
    my_word_list.extend(pattern.findall(text))

    return my_word_list


def gen_nlp_result(segments, part_of_speech):
    verb, noun, name, time = [], [], [], []
    noun_signs = ['ns', 'nz', 'b', 'nl', 'ni']
    for i in range(len(segments)):
        word = segments[i]
        pos = part_of_speech[i]
        if pos in noun_signs and word not in noun:
            tmp = str(word).find("人民法院")
            if tmp != -1:
                noun.append(str(word)[0:tmp+4])
            else:
                noun.append(word)
        elif pos == 'v' and len(word) < 10 and word not in verb:
            verb.append(word)
        elif pos == 'nh' and len(word) < 10 and word not in name:
            name.append(word)
        elif pos == 'nt' and word not in time:
            time.append(word)
    return [name, noun, verb, time]


def nlp(text):
    ltp = LTP()

    my_word_list = gen_my_word_list(text)
    ltp.add_words(words=my_word_list, max_window=4)

    seg, hidden = ltp.seg([text])
    part_of_speech = ltp.pos(hidden)[0]
    segments = seg[0]

    nlp_result = gen_nlp_result(segments, part_of_speech)

    name = nlp_result[0]
    noun = nlp_result[1]
    verb = nlp_result[2]
    time = nlp_result[3]
    # print(segments)
    # print(part_of_speech)
    for w in noun:
        print(w + ",", end='')
    print('#', end='')
    for w in verb:
        print(w + ",", end='')
    print('#', end='')
    for w in name:
        print(w + ",", end='')
    print('#', end='')
    for w in time:
        print(w + ",", end='')


if __name__ == '__main__':
    # print(sys.argv[0])
    if len(sys.argv) > 1:
        nlp(sys.argv[1])
    else:
        nlp('徐瀚林闯入江苏省高级人民法院')
