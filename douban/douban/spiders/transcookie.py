class transCookie():
    def __init__(self, cookie):
        self.cookie = cookie

    def stringToDict(self):
        '''
        将浏览器的cookie值进行dict转换
        :return:
        '''
        itemDict = {}
        items = self.cookie.split(';')
        for item in items:
            key = item.split('=')[0].replace(" ", '')
            vulue = item.split('=')[1]
            itemDict[key] = vulue
        return itemDict


if __name__ == '__main__':
    cookie = 'll="118106"; bid=8SocNSPlV5M; _pk_ses.100001.8cb4=*; dbcl2="177982783:gtao4YQEac8"; ck=SU2O; _pk_id.100001.8cb4=94baa95dbd8aa235.1553693681.1.1553693713.1553693681.; ap_v=0,6.0; __yadk_uid=M1YDUdzwSpIOiNmNwGoCMzn9HjJdwc0e; push_noty_num=0; push_doumail_num=0; __utma=30149280.1515886352.1553693715.1553693715.1553693715.1; __utmc=30149280; __utmz=30149280.1553693715.1.1.utmcsr=api.weibo.com|utmccn=(referral)|utmcmd=referral|utmcct=/oauth2/authorize; __utmt=1; __utmv=30149280.17798; __utmb=30149280.2.10.1553693715'
    trans = transCookie(cookie)
    a = trans.stringToDict()
    with open("cookie.txt", 'a')as f:
        f.write(str(a) + '\n')
        print("success write")
