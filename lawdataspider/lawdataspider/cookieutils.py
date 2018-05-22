class transCookie(object):
    def __init__(self, cookie):
        self.cookie = cookie

    def stringToDict(self):
        itemDict = {}
        items = self.cookie.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')  # 记得去除空格
            value = item.split('=')[1]
            itemDict[key] = value
        return itemDict