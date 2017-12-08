# coding=utf-8

# |预订|6j000D751105|D7511|CBQ|GGQ|CBQ|GGQ|11:05|14:15|03:10|N|ML%2Bx6lkKgJpuLx6xD3bKtQ44qdgn%2BhwjcZRC%2FFyqR1dg2CiT|20171207|3|Q6|01|06|0|0|||||||无||||无|无|||O0O0M0|OOM"
# zOwAGjLpDkcDnN1fVE7sx0sOxTXohrpggabLEqtGuwhvLf%2FF%2BWFdSUzN92sXXCukEHHJIi1xZs%2Bp%0AfmLBhAo%2FbShCzqxD%2B4p94JiaDYWl%2FoInd59Ew8OWXyv9mop8ON9iPnjskIavGI086zUWRI7JnRtQ%0AQqOeILnPNCHkh5BYitIUtNULZi%2BD4Mwtths5YJ6iygfT8iksw9D8KVKieqi0FXrys1cQEpJZt%2BEa%0AXgad1xs%3D
# |预订
# |6j000D753500
# |D7535|CBQ|GGQ|CBQ|GGQ
# |15:17|18:38|03:21
# |Y|gRFjGpoWeGNvK5D6IUdOTAC4cW8xjYXPK4isa8afKmM4bY2u
# |20171207|3|Q6|01|07|0|0|||||||无||||无|20|||O0O0M0|OOM  30 31 32


# %u6F6E%u6C55%2CCBQ 潮汕,CBQ
# %u5E7F%u5DDE%u4E1C%2CGZQ  广州东,GZQ


class ResultItem(object):
    status = False
    secretStr = ''
    no = ''
    startStation = ''
    endStation = ''
    startTime = ''
    endTime = ''

    date = ''

    specialClass = ''
    firstClass = ''
    secondClass = ''
    noClass = ''

    def __init__(self, item, stationMap):
        itemList = item.split('|')

        self.secretStr = itemList[0]
        self.no = itemList[3]
        self.startStation = stationMap[itemList[6]]
        self.endStation = stationMap[itemList[7]]

        # if len(self.startStation) == 2:
        #     self.startStation = self.startStation + '站'
        # if len(self.endStation) == 2:
        #     self.endStation = self.endStation + '站'

        self.startTime = itemList[8]
        self.endTime = itemList[9]

        self.status = itemList[11] == "Y"

        self.date = itemList[13]

        self.noClass = itemList[26]
        self.secondClass = itemList[30]
        self.firstClass = itemList[31]
        self.specialClass = itemList[32]
