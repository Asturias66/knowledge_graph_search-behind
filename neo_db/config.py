from py2neo import Graph
graph = Graph('http://localhost:7474/', auth=("neo4j", "123456"))


HISTORY_LIST = {
    "HistoryPerson1":'人物',
    "HistoryEvent":'历史事件',
    "HistoryLaw":'法律',
    "HistoryLocation":'地点',
    "HistoryOrganization":'组织',
    "HistoryDate":'时间'
}