from py2neo import Graph
graph = Graph('http://localhost:7474/', auth=("neo4j", "123456"))


CA_LIST = {"疾病":0,
           "所属科室":1,
           "并发症":2,
           "症状":3,
           "诊断检查":4,
           "好评药品":5,
           "忌吃":6,
           "推荐食谱":7,
           "宜吃":8,
           "易发人群":9,
           "持续时间":10,
           "防御措施":11,
           "治愈概率":12,
           "治疗方式":13,
           "疾病的相关介绍":14,
           "疾病原因":15,
           }

HISTORY_LIST = {
    "HistoryPerson1":'人物',
    "HistoryEvent":'历史事件',
    "HistoryLaw":'法律',
    "HistoryLocation":'地点',
    "HistoryOrganization":'组织',
    "HistoryDate":'时间'
}