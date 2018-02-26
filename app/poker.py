


PUKE = ['fangp01', 'fangp02', 'fangp03', 'fangp04', 'fangp05', 'fangp06', 'fangp07', 'fangp08', 'fangp09', 'fangp10',
'fangp11', 'fangp12', 'fangp13', 'hongt01', 'hongt02', 'hongt03', 'hongt04', 'hongt05', 'hongt06', 'hongt07', 'hongt08',
'hongt09', 'hongt10', 'hongt11', 'hongt12', 'hongt13', 'heit01', 'heit02', 'heit03', 'heit04', 'heit05', 'heit06', 'heit07',
'heit08', 'heit09', 'heit10', 'heit11', 'heit12', 'heit13', 'meih01', 'meih02', 'meih03', 'meih04', 'meih05', 'meih06',
'meih07', 'meih08', 'meih09', 'meih10', 'meih11', 'meih12', 'meih13']

HUASE_NUMBER= {'heit':0.4,'hongt':0.3,'meih':0.2,'fangp':0.1}

BEI_LV = {0:1,1:1,2:1,3:1,4:1,5:1,6:1,7:1,8:2,9:2,10:3}

def calcniuniu(pai):
    l2 = [int(i[-2:]) if int(i[-2:])<10 else 10 for i in pai]
    diansu = 0
    for i in itertools.combinations(l2,3):
        if sum(i)%10==0:
            diansu=(sum(l2)-sum(i))%10
            if diansu == 0:
                diansu = 10
    l3 = {int(i[-2:])+HUASE_NUMBER[i[0:-2]]:i for i in pai}
    return diansu,l3[max(l3.keys())],max(l3.keys())

def compare(pai1,pai2):
    """
    参数1，庄的牌，参数2，玩家的牌,庄小，返回+，庄大，返回-
    """
    if pai1[0]+pai1[2]/100 < pai2[0]+pai2[2]/100:
        return BEI_LV[pai2[0]]
    else:
        return -1 * BEI_LV[pai1[0]]

def calcmark(pai):
    paixu = json.loads(pai.paixu)
    if pai.zhuang == 1:
        zhuang = int(pai.user1_xiazhu)
        pai.user2_mark = int(pai.user2_xiazhu) * zhuang * compare(calcniuniu(paixu[0]),calcniuniu(paixu[1]))
        pai.user3_mark = int(pai.user3_xiazhu) * zhuang * compare(calcniuniu(paixu[0]),calcniuniu(paixu[2]))
        pai.user4_mark = int(pai.user4_xiazhu) * zhuang * compare(calcniuniu(paixu[0]),calcniuniu(paixu[3]))
        pai.user5_mark = int(pai.user5_xiazhu) * zhuang * compare(calcniuniu(paixu[0]),calcniuniu(paixu[4]))
        pai.user1_mark = -pai.user2_mark-pai.user3_mark-pai.user4_mark-pai.user5_mark
    elif pai.zhuang == 2:
        zhuang = int(pai.user2_xiazhu)
        pai.user1_mark = int(pai.user1_xiazhu) * zhuang * compare(calcniuniu(paixu[1]),calcniuniu(paixu[0]))
        pai.user3_mark = int(pai.user3_xiazhu) * zhuang * compare(calcniuniu(paixu[1]),calcniuniu(paixu[2]))
        pai.user4_mark = int(pai.user4_xiazhu) * zhuang * compare(calcniuniu(paixu[1]),calcniuniu(paixu[3]))
        pai.user5_mark = int(pai.user5_xiazhu) * zhuang * compare(calcniuniu(paixu[1]),calcniuniu(paixu[4]))
        pai.user2_mark = -pai.user1_mark-pai.user3_mark-pai.user4_mark-pai.user5_mark
    elif pai.zhuang == 4:
        zhuang = int(pai.user3_xiazhu)
        pai.user2_mark = int(pai.user2_xiazhu) * zhuang * compare(calcniuniu(paixu[2]),calcniuniu(paixu[1]))
        pai.user1_mark = int(pai.user1_xiazhu) * zhuang * compare(calcniuniu(paixu[2]),calcniuniu(paixu[0]))
        pai.user4_mark = int(pai.user4_xiazhu) * zhuang * compare(calcniuniu(paixu[2]),calcniuniu(paixu[3]))
        pai.user5_mark = int(pai.user5_xiazhu) * zhuang * compare(calcniuniu(paixu[2]),calcniuniu(paixu[4]))
        pai.user3_mark = -pai.user1_mark-pai.user2_mark-pai.user4_mark-pai.user5_mark
        print(type(pai.user2_mark),pai.user2_mark)
    elif pai.zhuang ==8:
        zhuang = int(pai.user4_xiazhu)
        pai.user2_mark = int(pai.user2_xiazhu) * zhuang * compare(calcniuniu(paixu[3]),calcniuniu(paixu[1]))
        pai.user3_mark = int(pai.user3_xiazhu) * zhuang * compare(calcniuniu(paixu[3]),calcniuniu(paixu[2]))
        pai.user1_mark = int(pai.user1_xiazhu) * zhuang * compare(calcniuniu(paixu[3]),calcniuniu(paixu[0]))
        pai.user5_mark = int(pai.user5_xiazhu) * zhuang * compare(calcniuniu(paixu[3]),calcniuniu(paixu[4]))
        pai.user4_mark = -pai.user1_mark-pai.user2_mark-pai.user3_mark-pai.user5_mark
    elif pai.zhuang == 16:
        zhuang = int(pai.user5_xiazhu)
        pai.user2_mark = int(pai.user2_xiazhu) * zhuang * compare(calcniuniu(paixu[4]),calcniuniu(paixu[1]))
        pai.user3_mark = int(pai.user3_xiazhu) * zhuang * compare(calcniuniu(paixu[4]),calcniuniu(paixu[2]))
        pai.user4_mark = int(pai.user4_xiazhu) * zhuang * compare(calcniuniu(paixu[4]),calcniuniu(paixu[3]))
        pai.user1_mark = int(pai.user1_xiazhu) * zhuang * compare(calcniuniu(paixu[4]),calcniuniu(paixu[0]))
        pai.user5_mark = -pai.user1_mark-pai.user2_mark-pai.user3_mark-pai.user4_mark
    return pai
