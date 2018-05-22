class TransCookie(object):
    def __init__(self, cookie):
        self.cookie = cookie

    def stringToDict(self):
        if isinstance(self.cookie,str):
            itemDict = {}
            items = self.cookie.split(';')
            for item in items:
                key = item.split('=')[0].replace(' ', '')  # 记得去除空格
                value = item.split('=')[1]
                itemDict[key] = value
            return itemDict
        return "kidding me?"

    def dictToString(self):
        if isinstance(self.cookie,dict):
            cookie_list = []
            for k,v in self.cookie.items():
                temp = k+"="+v+";"
                cookie_list.append(temp)
            cookiestr = "".join(cookie_list)
            return cookiestr[:-1]
        return "kidding me?"