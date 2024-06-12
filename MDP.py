import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mgimg


def trans_mat(state_x, state_y, mice, cat, cheese, fear, hunger, length,height):  # X ve Y KONUMUNA GÖRE GEÇİŞ OLASILIK MATRİSİNİ VERİR.

    # trans = np.array([[0.85, 0.05, 0.05, 0.05],  # KÖŞE OLMAYAN DEĞERLERİN GEÇİŞ OLASILIKLARINI VERİR.
    #                   [0.05, 0.85, 0.05, 0.05],  # SOLDAN SAĞA YUKARI, AŞAĞI, SOL ve SAĞA GEÇME OLASILILARINI VERİR.
    #                   [0.05, 0.05, 0.85, 0.05],
    #                   [0.05, 0.05, 0.05, 0.85]])

    trans = np.array([[0.7, 0.1, 0.1, 0.1],  # KÖŞE OLMAYAN DEĞERLERİN GEÇİŞ OLASILIKLARINI VERİR.
                      [0.1, 0.7, 0.1, 0.1],  # SOLDAN SAĞA YUKARI, AŞAĞI, SOL ve SAĞA GEÇME OLASILILARINI VERİR.
                      [0.1, 0.1, 0.7, 0.1],
                      [0.1, 0.1, 0.1, 0.7]])

    if state_y + 1 > height - 1:  # KOORDİNATI KÖŞEDE OLAN DURUMLAR İÇİN BÜTÜN SÜTUNLARINA 0 VEKTÖRÜ KOYAR.
        trans[:, 0] = np.zeros([4, ])  # YUKARI İÇİN
    if state_y - 1 < 0:
        trans[:, 1] = np.zeros([4, ])  # AŞAĞI İÇİN
    if state_x - 1 < 0:
        trans[:, 2] = np.zeros([4, ])  # SOL İÇİN
    if state_x + 1 > length - 1:
        trans[:, 3] = np.zeros([4, ])  # SAĞ İÇİN

    for i in range(np.size(trans[:, 1])):  # MATRİSİN HER SATIRININ TOPLAM 1 OLUP OLMADIĞINI KONTROL EDER.
        if round(sum(trans[i, :]), 1) != 1:  # 1'DEN FARKLI İSE SATIRIN TOPLAMINI 1'DEN ÇIKARAK 0 OLMAYAN...
            fark = 1 - round(sum(trans[i, :]), 1)  # ...ELEMANLARA EŞİT BİR ŞEKİLDE EKLER.
            bolum = np.count_nonzero(trans[i, :])
            eklenti = fark / bolum
            for j in range(np.size(trans[1, :])):
                if trans[i, j] != 0:
                    trans[i, j] += eklenti

    action_fear = np.array([cat_dis(mice + np.array([0, 100, 0]), cat), cat_dis(mice + np.array([0, -100, 0]), cat),
                            cat_dis(mice + np.array([-100, 0, 0]), cat), cat_dis(mice + np.array([+100, 0, 0]), cat)])

    ind_fear = np.where(np.max(action_fear) == action_fear)

    action_hunger = np.array(
        [cheese_dis(mice + np.array([0, 100, 0]), cheese), cheese_dis(mice + np.array([0, -100, 0]), cheese),
         cheese_dis(mice + np.array([-100, 0, 0]), cheese), cheese_dis(mice + np.array([+100, 0, 0]), cheese)])

    ind_hunger = np.where(np.min(action_hunger) == action_hunger)

    # action_nest = np.array([nest_dis(mice+np.array([0,100,0]),nest),nest_dis(mice+np.array([0,-100,0]),nest),
    #                    nest_dis(mice+np.array([-100,0,0]),cheese),cheese_dis(mice+np.array([+100,0,0]),cheese)])
    #
    # ind_nest = np.where(np.min(action_hunger) == action_hunger)

    for i in range(np.size(trans, 1)):
        if np.all(trans[:, i] != np.zeros(4)):
            if i == ind_fear[0][0]:
                trans[:, i] = trans[:, i] + fear
            else:
                trans[:, i] = trans[:, i] - fear / (np.count_nonzero(trans[i, :]) - 1)
            if i == ind_hunger[0][0]:
                trans[:, i] = trans[:, i] + hunger
            elif i != ind_hunger[0][0]:
                trans[:, i] = trans[:, i] - hunger / (np.count_nonzero(trans[i, :]) - 1)

    for i in range(np.size(trans, 0)):
        for j in range(np.size(trans, 1)):
            if trans[i, j] >= 1:
                trans[i, j] = 1
            if trans[i, j] <= 0:
                trans[i, j] = 0

    for i in range(np.size(trans, 0)):
        trans[i, :] = trans[i, :] / np.sum(trans[i, :])

    return trans


def value_func(val, dis_fac, iteration, a, length, height, rew, mice, cat, cheese, fear, hunger):  # BÜTÜN DURUMLARIN VALUE DEĞERLERİNİ HESAPLAR.
    for k in range(iteration):  # GİRDİ OLARAK BİR ÖNCEKİ VALUE DEĞER MATRİSİNİ, DİSCOUNT FACTORU, İTERASYON SAYISI ve...
        for i in range(length):  # ...ÖĞRENME HIZINI ALIR
            for j in range(height):  # İŞLEM İÇİN V(S) DEĞERİNİ ÇEKER. EĞER SINIRLARI AŞIYORSA DEĞER 0'DIR.
                v_next = np.zeros(4, )
                if j + 1 <= height - 1:
                    v_next[0] = val[i, j + 1]
                if j - 1 >= 0:
                    v_next[1] = val[i, j - 1]
                if i - 1 >= 0:
                    v_next[2] = val[i - 1, j]
                if i + 1 <= length - 1:
                    v_next[3] = val[i + 1, j]
                # TEMPORAL DİFFERENCE YAPAR. V(S)=V(S) + ÖĞRENME HIZI * ( R(S) + DİSCOUNT FACTOR * (V(S')) - V(S) )
                val[i, j] = val[i, j] + a * (
                        rew[i, j] + dis_fac * np.max(
                    np.dot(trans_mat(i, j, mice, cat, cheese, fear, hunger, length, height), v_next)) - val[i, j])
    return val


def policy(mice_mat, val_, length, height, mice, cat, cheese, fear, hunger):  # FARENİN YAPMASI GEREKEN POLİCY'İ VERİR. BUNU İÇİN...
    mice_x = int((mice_mat[0] - mice_mat[2] / 2) / 100)  # ...FARENİN KONUMUNU ve VALUE MATRİSİNİ KULLANIR.
    mice_y = int((mice_mat[1] - mice_mat[2] / 2) / 100)  # KONUMDAN MATRİS SATIR ve SÜTUNLARINA GEÇER.
    v_next = np.zeros(4, )  # SINIRDA OLAN DEĞERLERİN VALUELARINI 0'LAR.
    if mice_y + 1 <= height - 1:
        v_next[0] = val_[mice_x, mice_y + 1]
    if mice_y - 1 >= 0:
        v_next[1] = val_[mice_x, mice_y - 1]
    if mice_x - 1 >= 0:
        v_next[2] = val_[mice_x - 1, mice_y]
    if mice_x + 1 <= length - 1:
        v_next[3] = val_[mice_x + 1, mice_y]
    matrix = np.dot(trans_mat(mice_x, mice_y, mice, cat, cheese, fear, hunger, length, height),
                    v_next)  # GEÇİŞ OLASILIKLARI İLE VALUE DEĞERİNİ ÇARPAR.
    utility = np.max(matrix)  # ÇARPIMIN EN YÜKSEK DEĞERİNİ BELİRLER.
    indeks = np.where(utility == matrix)[0][0]  # EN YÜKSEK DEĞERİN HANGİ ACTİON'A DENK GELDİĞİNİ BELİRLER.
    prob = trans_mat(mice_x, mice_y, mice, cat, cheese, fear, hunger, length, height)[
        indeks]  # BU ACTİONA DENK GELEN GEÇİŞ OLASILIĞINI BELİRLER.
    action_set = ['UP', 'DOWN', 'LEFT', 'RIGHT']  # OLASILIKLAR DAHİLİNDE ACTİON GERÇEKLEŞİR.
    action = np.random.choice(action_set, 1, p=prob)

    if action[0] == 'UP':  # ACTİON'A GÖRE YUKARI, AŞAĞI, SOL ve SAĞA KONUM DEĞİŞTİRİR.
        mice_y += 1
    elif action[0] == 'DOWN':
        mice_y -= 1
    elif action[0] == 'LEFT':
        mice_x -= 1
    elif action[0] == 'RIGHT':
        mice_x += 1
    return np.array([(mice_x * 100) + mice_mat[2] / 2, (mice_y * 100) + mice_mat[2] / 2, 100]), prob, action


def reward_func(grid, cheese_loc, cat_loc):  # KONUMA GÖRE ÖDÜLLER BELİRLENİR.

    che = [int(cheese_loc[0] / 100), int(cheese_loc[1] / 100)]
    catt = [int(cat_loc[0] / 100), int(cat_loc[1] / 100)]

    reward = np.zeros(grid)+0.01
    rew = +10
    pun = -50

    reward[che[0], che[1]] = rew
    reward[catt[0], catt[1]] = pun

    z = np.zeros([8, 2])
    it = 0
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if not (i == 0 and j == 0):
                z[it] = np.array([i, j])
                it += 1

    reward_cheese = che - z
    reward_cat = catt - z

    for i in np.arange(grid[0]):
        for j in np.arange(grid[1]):
            if (i == reward_cheese[:, 0]).any() and (j == reward_cheese[:, 1]).any():
                reward[i, j] += rew

            if (i == reward_cat[:, 0]).any() and (j == reward_cat[:, 1]).any():
                reward[i, j] += pun
    return reward


def cat_dis(mice, cat):
    mice_cat = mice - cat
    mice_cat_dis = np.sqrt(mice_cat[0] ** 2 + mice_cat[1] ** 2)
    return mice_cat_dis


def cheese_dis(mice, cheese):
    mice_cheese = mice - cheese
    mice_cheese_dis = np.sqrt(mice_cheese[0] ** 2 + mice_cheese[1] ** 2)
    return mice_cheese_dis


def nest_dis(mice, nest):
    mice_nest = mice - nest
    mice_nest_dis = np.sqrt(mice_nest[0] ** 2 + mice_nest[1] ** 2)
    return mice_nest_dis


def cat_rotation(cheese):
    cheese_x = cheese[0]
    cheese_y = cheese[1]

    rotation = np.array([[0, -2], [1, -1], [2, 0], [1, 1], [0, +2], [-1, 1], [-2, 0], [-1, -1]])

    return np.array([cheese_x, cheese_y]) - rotation


def mdp(cat_pic, mice_pic, cheese_pic, nest_pic, value_initial, discount, lear_rate, length, height):  # ANA FONKSİYON
    fig, ax = plt.subplots()
    plt.axis([0, length * 100, 0, height * 100])  # GRAFİĞİN BOYUTLARINI BELİRLER.

    iteration = 0

    cat_ = cat_pic[0]  # ELEMANLARIN BAŞLANGIÇ KONUMLARINI GİRER.
    mice_ = mice_pic
    cheese_ = cheese_pic
    nest_ = nest_pic
    value_ = value_initial

    hunger = 0.2
    fear = 0
    peynir_flag = 0

    reward = reward_func(np.array([length, height]), cheese_, cat_)
    print(reward)

    imobj_cat = ax.imshow(img_cat,  # RESİMLERİ BASTIRIR.
                          extent=[cat_[0] - cat_[2] / 2,
                                  cat_[0] + cat_[2] / 2,
                                  cat_[1] - cat_[2] / 2,
                                  cat_[1] + cat_[2] / 2],
                          zorder=1)

    imobj_mice = ax.imshow(img_mice, extent=[mice_[0] - mice_[2] / 2,
                                             mice_[0] + mice_[2] / 2,
                                             mice_[1] - mice_[2] / 2,
                                             mice_[1] + mice_[2] / 2], zorder=1)

    imobj_cheese = ax.imshow(img_cheese,
                             extent=[cheese_[0] - cheese_[2] / 2,
                                     cheese_[0] + cheese_[2] / 2,
                                     cheese_[1] - cheese_[2] / 2,
                                     cheese_[1] + cheese_[2] / 2], zorder=1)
    imobj_nest = ax.imshow(img_nest,
                           extent=[nest_[0] - nest_[2] / 2,
                                   nest_[0] + nest_[2] / 2,
                                   nest_[1] - nest_[2] / 2,
                                   nest_[1] + nest_[2] / 2], zorder=1)

    plt.imshow(np.flip(np.transpose(value_), 0),
               extent=[0, length * 100, 0, height * 100])  # BAŞLANGIÇ VALUE DEĞERLERİ GÖSTERİR.
    plt.pause(.5)

    while True:
        mice_cat = mice_ - cat_
        mice_cat_dis_old = np.sqrt(mice_cat[0] ** 2 + mice_cat[1] ** 2)

        value_ = value_func(value_, discount, 20, lear_rate, length, height, reward, mice_, cat_, cheese_, fear, hunger)  # BİR ÖNCEKİ VALUE DEĞERLERİ KULLANILARAK...
        mice_, prob_, action_ = policy(mice_, value_, length, height, mice_, cat_, cheese_, fear, hunger)  # YENİ VALUELAR BELİRLENİR. BU VALUELARA GÖRE FARE BİR POLİCY OLUŞTURARAK...
        # FARE HAREKET EDER.

        imobj_cat.set_extent([cat_[0] - cat_[2] / 2,  # YENİ KONUMLARA GÖRE GRAFİĞİ GÜNCELER.
                              cat_[0] + cat_[2] / 2,
                              cat_[1] - cat_[2] / 2,
                              cat_[1] + cat_[2] / 2])

        plt.imshow(np.flip(np.transpose(value_), 0), extent=[0, length * 100, 0, height * 100])

        plt.title(["açlık: ", hunger, "korku: ", fear, prob_, action_])
        plt.pause(0.5)  # GRAFİKLER ARASINDAKİ SANİYE CİNSİNDEN BEKLEME.

        imobj_mice.set_extent([mice_[0] - mice_[2] / 2,
                               mice_[0] + mice_[2] / 2,
                               mice_[1] - mice_[2] / 2,
                               mice_[1] + mice_[2] / 2])
        imobj_nest.set_extent([nest_[0] - nest_[2] / 2,
                               nest_[0] + nest_[2] / 2,
                               nest_[1] - nest_[2] / 2,
                               nest_[1] + nest_[2] / 2])

        if peynir_flag == 0:
            cheese_ = cheese_pic
        elif peynir_flag == 1:
            cheese_ = mice_

        imobj_cheese.set_extent([cheese_[0] - cheese_[2] / 2,
                                 cheese_[0] + cheese_[2] / 2,
                                 cheese_[1] - cheese_[2] / 2,
                                 cheese_[1] + cheese_[2] / 2])

        iteration += 1
        cat_ = cat_pic[np.mod(iteration, np.size(cat_pic, 0))]

        mice_cat = mice_ - cat_
        mice_cat_dis_new = np.sqrt(mice_cat[0] ** 2 + mice_cat[1] ** 2)

        fear += (mice_cat_dis_old - mice_cat_dis_new) / 10000

        if peynir_flag == 0:
            reward = reward_func(np.array([length, height]), cheese_, cat_)
        else:
            reward = reward_func(np.array([length, height]), nest_, cat_)

        if np.all(mice_ == cheese_) and peynir_flag == 0:
            hunger = 0
            peynir_flag += 1
        else:
            hunger += 0.001

        imobj_cat.set_extent([cat_[0] - cat_[2] / 2,  # YENİ KONUMLARA GÖRE GRAFİĞİ GÜNCELER.
                              cat_[0] + cat_[2] / 2,
                              cat_[1] - cat_[2] / 2,
                              cat_[1] + cat_[2] / 2])

        if np.all(mice_ == cat_):  # FARE PEYNİRE VARIRSA veya KEDİYE YAKALANIRSA İŞLEM BİTER.
            break
        if np.all(mice_ == nest_) and peynir_flag == 1:
            break

    plt.colorbar()
    plt.show()
    return


fname_cat = 'cat.png'  # RESİMLER AKTARILIR.
fname_mice = 'mice.png'
fname_cheese = 'cheese.png'
fname_nest = "nest.png"
img_cat = mgimg.imread(fname_cat)
img_mice = mgimg.imread(fname_mice)
img_cheese = mgimg.imread(fname_cheese)
img_nest = mgimg.imread(fname_nest)

square = 12

grid_dim = np.array([square, square])  # GRİDİN BOYUTUNU BELİRLER

mice_loc = np.array([1, 1])  # YUVA, FARE, KEDİ ve PEYNİRİN BAŞLANGIÇ KONUMLARI GİRİLİR.
cheese_loc = np.array([6, 6])

# mice_loc_x=np.random.randint(low=1,high=13)
# mice_loc_y=np.random.randint(low=1,high=13)
# mice_loc=np.array([mice_loc_x,mice_loc_y])
#
# cheese_loc_x=np.random.randint(low=3,high=11)
# cheese_loc_y=np.random.randint(low=3,high=11)
# cheese_loc = np.array([cheese_loc_x,cheese_loc_y])

nest_loc = mice_loc
cat_loc = cat_rotation(cheese_loc)

nest = np.array([nest_loc[0] * 100 + 50, nest_loc[1] * 100 + 50, 100])  # KONUMLARIN GRAFİKTEKİ BOYUTUNA ÇEVİRİR.
mice = np.array([mice_loc[0] * 100 + 50, mice_loc[1] * 100 + 50, 100])
cat = np.transpose(np.array([cat_loc[:, 0] * 100 + 50, cat_loc[:, 1] * 100 + 50, 100 * np.ones(np.size(cat_loc, 0))]))
cheese = np.array([cheese_loc[0] * 100 + 50, cheese_loc[1] * 100 + 50, 100])

value_init = np.zeros(grid_dim)  # VALUE DEĞERLERİ 0 İLE BAŞLATILIR.

mdp(cat, mice, cheese, nest, value_init, 0.9, 0.9, grid_dim[0], grid_dim[1])
