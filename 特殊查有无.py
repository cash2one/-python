#ecoding:utf-8
nav_yishu = ['舞蹈','乐器','美术','声乐','表演','艺考']
nav_xiqu = ['摄影','DJ','魔术','书法','风水','国学']
nav_shenghuo = ['礼仪','茶艺','插花','烹饪','形体','园艺']
nav = [nav_yishu,nav_xiqu,nav_shenghuo]
for temp in nav:
    if '礼仪' in temp:
        print temp[0],'ok'