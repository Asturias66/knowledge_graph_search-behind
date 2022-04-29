# search
import re

import requests

from neo_db.config import graph, HISTORY_LIST

# getSelectionFromGraph
def getSelectionFromGraph():
    data = graph.run(
        "match(p) -[r]->(n) return labels(p),p.name"
    )
    data = list(data)
    json_data = []
    value_list = []
    # 给node_label分类
    for i in data:
        # print("i[p.name]:",i['p.name'])
        # print("i[labels(p)]:", i['labels(p)'][0])

        nodeLabel_item = {}
        if i['labels(p)'][0] not in value_list:

            value_list.append(i['labels(p)'][0])
            nodeLabel_item["children"] = []
            nodeLabel_item["isLeaf"] = False
            nodeLabel_item["leaf"] = False
            nodeLabel_item['label'] = HISTORY_LIST[i['labels(p)'][0]]
            nodeLabel_item['value'] = HISTORY_LIST[i['labels(p)'][0]]
            json_data.append(nodeLabel_item)

    name_list = []
    for i in data:
        if i['p.name'] not in name_list:
            name_list.append(i['p.name'])
            for nodeLabel_dict in json_data:
                if HISTORY_LIST[i['labels(p)'][0]] == nodeLabel_dict['value']:
                    put_dict = {'value': i['p.name'], 'label': i['p.name'], 'isLeaf': True, 'children': None,
                                'leaf': True}

                    nodeLabel_dict['children'].append(put_dict)

    #     else:
    #         for
    #         nodeLabel_item_children_dict = {}
    #         if i['p.name'] not in name_list:
    #             name_list.append(i['p.name'])
    #             nodeLabel_item_children_dict['value'] = i['p.name']
    #             nodeLabel_item_children_dict['label'] = i['p.name']
    #             nodeLabel_item_children_dict['isLeaf'] = True
    #             nodeLabel_item_children_dict['children'] = None
    #             nodeLabel_item_children_dict['leaf'] = True
    #             nodeLabel_item['children'].append(nodeLabel_item_children_dict)
    #         # else:
    #
    #
    #
    #
    #
    #
    # print("value_list:",value_list)

    return json_data


# getMoreKeyWord
def getMoreKeyWordFromGraph(keyword):
    data = graph.run(
        "match data=(na:HistoryPerson1{name:'%s'})-[rel*1..2]->(nb) return na,rel,nb" % (keyword)
    ).data()

    json_data = {'nodes': [], "links": []}
    d = []

    for i in data:
        # print("i:",i)
        if len(i['rel']) == 1:
            # print('没有子节点')
            # print('i[rel]:',i['rel'])
            for item in i['rel']:
                # print("item:",item)
                start = str(item).split(")-[")[0].split("(")[1]
                end = str(item).split("->(")[1].split(")")[0]

                start_label_data = graph.run("match (n{name:'%s'}) return labels(n)" % (start))
                start_label_data = list(start_label_data)
                start_label = start_label_data[0][0][0]
                # print("start_label:", start_label)

                end_label_data = graph.run("match (n{name:'%s'}) return labels(n)" % (end))
                end_label_data = list(end_label_data)
                end_label = end_label_data[0][0][0]
                # print("end_label:",end_label)

                if start + '_' + start_label not in d:
                    d.append(start + "_" + start_label)
                if end + '_' + end_label not in d:
                    d.append(end + "_" + end_label)
                d = list(set(d))

                link_item = {}

                link_item['source'] = start
                link_item['target'] = end
                link_item['category'] = i['rel'][0]['name']
                link_item['label'] = i['rel'][0]['name']

                json_data['links'].append(link_item)


        else:
            # print("含有子节点")
            indexFrom1 = 1
            while indexFrom1 < len(i['rel']):
                print("i['rel']:",str(i['rel'][indexFrom1]))
                start = str(i['rel'][indexFrom1]).split(")-[")[0].split("(")[1]
                # end_string = str(i['rel'][indexFrom1]).split("->(")[1][-1]
                # print("end_string:",end_string)
                end = str(i['rel'][indexFrom1]).split("->(")[1].split(")")[0]

                start_label_data = graph.run("match (n{name:'%s'}) return labels(n)" % (start))
                start_label_data = list(start_label_data)
                start_label = start_label_data[0][0][0]
                # print("start_label:", start_label)

                print("start:",start)
                print("end:",end)
                end_label_data = graph.run("match (n{name:'%s'}) return labels(n)" % (end))
                end_label_data = list(end_label_data)
                print("end_label_data:",end_label_data)
                if end_label_data != []:
                    end_label = end_label_data[0][0][0]
                    # print("end_label:",end_label)

                    if start+'_'+start_label not in d:
                        d.append(start + "_" + start_label)
                    if end+'_'+end_label not in d:
                        d.append(end + "_" + end_label)
                    d = list(set(d))
                    link_item = {}

                    link_item['source'] = start
                    link_item['target'] = end
                    link_item['category'] = i['rel'][indexFrom1]['name']
                    link_item['label'] = i['rel'][indexFrom1]['name']

                    json_data['links'].append(link_item)



                indexFrom1 += 1
    # print("d:",d)
    # print("len(d):",len(d))
    name_dict = {}
    count = 0
    for m in d:
        j_array = m.split("_")
        data_item = {}
        name_dict[j_array[0]] = count
        count += 1
        data_item['id'] = j_array[0]
        data_item['label'] = j_array[0]
        data_item['category'] = HISTORY_LIST[j_array[1]]
        json_data['nodes'].append(data_item)


    return json_data


# getSpaceRecallDetailFromGraph
def getSpaceRecallDetailFromGraph(space):
    data = graph.run(
        "MATCH (n{name:'%s'}) RETURN properties(n)['时间线']" % (space)
    )
    data = list(data)
    json_data = []
    for i in data:
        print("i[properties(n)[时间线]:", i["properties(n)['时间线']"])
        for timeLine_item in eval(i["properties(n)['时间线']"]):
            print("timeLine_item:", timeLine_item)
            # print("timeLine_item的长度：",len(timeLine_item))
            timeLine_item[-2] = timeLine_item[-2].split(':')[1]
            json_data.append(timeLine_item)
    return json_data



# getMovieFromRequest
def getMovieFromRequest(keyword):
    s = requests.session()
    url = "https://movie.douban.com/j/search_subjects?type=movie&tag=" + keyword + "&sort=recommend&page_limit=100&page_start=0"
    header = {
        "User-Agent": "Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.50"}
    resp = s.get(url, headers=header).json()
    return resp




# getTimeRecallDetail
def getTimeRecallDetailFromGraph(time):
    data = graph.run(
        "MATCH (n{name:'%s'}) RETURN properties(n)['时间线']" % (time)
    )
    data = list(data)
    json_data = []
    for i in data:
        print("i[properties(n)[时间线]:", i["properties(n)['时间线']"])
        for timeLine_item in eval(i["properties(n)['时间线']"]):
            print("timeLine_item:",timeLine_item)
            # print("timeLine_item的长度：",len(timeLine_item))
            timeLine_item[3] = timeLine_item[3].split(':')[1]
            json_data.append(timeLine_item)
    return json_data





# getPeople
def getPeopleFromGraph(object,subject):
    data = graph.run(
        "match(p {name:'%s'}) -[r]->(n {name:'%s'}) return p.name,r.name,n.name union match(p{name:'%s'}) -[r]->(n{name:'%s'}) return p.name,r.name,n.name"% (object,subject,subject,object)
    )
    data = list(data)
    json_data = []
    for i in data:
        relation_dict = {}
        relation_dict['object'] = i['n.name']
        relation_dict['predicate'] = i['r.name']
        relation_dict['subject'] = i['p.name']


        json_data.append(relation_dict)

    return json_data


# getAllEvent
def getAllEventFromGraph():
    data = graph.run(
        "MATCH (n:HistoryEvent) RETURN properties(n)"
    )
    data = list(data)
    json_data = []
    for i in data:
        # print("i[properties(n).keys():",i["properties(n)"].keys())

        data = [x for i, x in enumerate(i["properties(n)"].keys()) if x.find('时间') != -1 and x != '时间线']
        # print("没有时间线，但有时间：",data)
        if len(data) != 0:
            for key,value in i["properties(n)"].items():
                if key =='时间线':

                    if len(value)>3:
                        event_dict = {}
                        event_dict['title'] = i["properties(n)"]['name']
                        if len(data) != 0:
                            event_dict['time'] = i["properties(n)"][data[0]]
                        else:
                            event_dict['time'] = None
                        event_dict['location'] = None
                        # print('event_dict:',event_dict)
                        json_data.append(event_dict)
                        print("json_data:", json_data)


        # if i["properties(n)['时间线']"]!=None:
        #     if len(eval(i["properties(n)"]['时间线'])) > 3 and '时间' in i["properties(n)"].keys():
        #         event_dict = {}
        #         event_dict['title'] = i["properties(n)"]['name']
        #
        #         event_dict['time'] = i["properties(n)"]['时间']
        #         event_dict['location'] = None
        #         # print('event_dict:',event_dict)
        #         json_data.append(event_dict)
        #         print("json_data:",json_data)

    return json_data


# getChildEvent
def getChildEventFromGraph(event):
    print("event:",event)
    data = graph.run(
    "MATCH (n{name:'%s'}) RETURN properties(n)['时间线']" % (event)
    )
    data = list(data)
    print("getAttributeFromGraph返回的结果:",data)

    return get_json_dataForTimeLines(data,event)

def get_json_dataForTimeLines(data,event):
    json_data = {'counties': [], "series": []}


    json_data['counties'].append(event)
    for i in data:
        if i["properties(n)['时间线']"] != None:
            timeLine = eval(i["properties(n)['时间线']"])
            for timeLine_item in timeLine:

                timeLine_item[-2] = timeLine_item[-2].split(':')[1]

                if timeLine_item[-1] != '0,0':
                    list_timeLine_item = []
                    list_timeLine_item.append(timeLine_item)
                    json_data['series'].append(list_timeLine_item)

    return json_data







# getAttribute
def getAttributeFromGraph(subject):
    data = graph.run(
    "MATCH (n{name:'%s'}) RETURN properties(n)" % (subject)
    )
    data = list(data)
    print("getAttributeFromGraph返回的结果:",data)

    return get_json_dataForAttribute(data,subject)



def get_json_dataForAttribute(data,subject):
    json_data = {'nodes': [], "links": []}
    d = []

    for i in data:
        # print("for i in data:")
        # print(i['properties(n)'])
        for key,value in i['properties(n)'].items():
            print("key:",key+'_'+"value:",value)
            if key != '时间线' and key !='img':
                d.append(value+"___"+key)
                d = list(set(d))

    print("d=list(set(d)):", d)
    name_dict = {}
    count = 0
    for j in d:
        j_array = j.split("___")

        data_item = {}
        name_dict[j_array[0]] = count
        count += 1
        data_item['id'] = j_array[0]
        data_item['label'] = j_array[0]
        data_item['category'] = j_array[1]

        # data_item['category'] = CA_LIST[j_array[1]]
        # print("data_item['category']:", data_item['category'])
        json_data['nodes'].append(data_item)
    # for i in data:
        link_item = {}

        link_item['source'] = subject
        link_item['target'] = j_array[0]
        link_item['category'] = j_array[1]
        link_item['label'] = j_array[1]

        json_data['links'].append(link_item)



    # print("json_data:", json_data)
    return json_data

# getKeyWordsWithEvents
def getKeyWordsWithEventsFromGraph(keyword):
    data = graph.run(
        "match(p {name:'%s'}) -[r]->(n) return p.name,r.name,n.name,labels(p),labels(n) union match(p) -[r]->(n{name:'%s'}) return p.name,r.name,n.name,labels(p),labels(n)" % (
        keyword, keyword)
    )
    data = list(data)
    # print("getkeywordFromGraph返回的结果:", data)

    json_data = {'nodes': [], "links": []}
    d = []

    for i in data:
        # print("for i in data:")
        # print(i["p.name"], i["r.name"], i["n.name"],i["labels(p)"][0],i["labels(n)"][0])

        d.append(i['p.name'] + "_" + i["labels(p)"][0])
        d.append(i['n.name'] + "_" + i["labels(n)"][0])

        d = list(set(d))
    print("没加event的d:", d)
    # # 给event加关系
    eventData = None
    for j in d:
        # label = j.split("_")[1]
        if j.split("_")[1] == 'HistoryEvent' and j.split("_")[0] != keyword:
            print("j.split(_)[0]:",j.split("_")[0])
            eventData = graph.run(
                "match(p {name:'%s'}) -[r]->(n) return p.name,r.name,n.name,labels(p),labels(n) union match(p) -[r]->(n{name:'%s'}) return p.name,r.name,n.name,labels(p),labels(n)"
                % (j.split("_")[0], j.split("_")[0])
            )

            eventData = list(eventData)
            print("加关系for循环里面的eventData:", eventData)

            for event_node in eventData:
                event_node_item = event_node['p.name'] + "_" + event_node["labels(p)"][0]
                if event_node_item not in d:
                    d.append(event_node_item)
                event_node_item = event_node['n.name'] + "_" + event_node["labels(n)"][0]
                if event_node_item not in d:
                    d.append(event_node_item)
                d = list(set(d))

            for event_item in eventData:
                link_item = {}
                link_item['source'] = event_item['p.name']
                link_item['target'] = event_item['n.name']
                link_item['category'] = event_item["r.name"]
                link_item['label'] = event_item['r.name']

                json_data['links'].append(link_item)

    print("加event的d:", d)
    print("eventData:",eventData)

    name_dict = {}
    count = 0
    for j in d:
        j_array = j.split("_")

        data_item = {}
        name_dict[j_array[0]] = count

        # data_item['id'] = count
        count += 1
        data_item['id'] = j_array[0]
        # print("data_item['id']:", data_item['id'])
        data_item['label'] = j_array[0]
        data_item['category'] = HISTORY_LIST[j_array[1]]


        # print("data_item['category']:", data_item['category'])
        json_data['nodes'].append(data_item)
    for i in data:
        link_item = {}

        link_item['source'] = i['p.name']
        link_item['target'] = i['n.name']
        link_item['category'] = i["r.name"]
        link_item['label'] = i['r.name']

        json_data['links'].append(link_item)




    return json_data


# getkeyword
def getkeywordFromGraph(keyword):
    data = graph.run(
    "match(p {name:'%s'}) -[r]->(n) return p.name,r.name,n.name,labels(p),labels(n) union match(p) -[r]->(n{name:'%s'}) return p.name,r.name,n.name,labels(p),labels(n)" % (keyword,keyword)
    )
    data = list(data)
    print("getkeywordFromGraph返回的结果:",data)

    return get_json_dataForKeywords(data)


def get_json_dataForKeywords(data):
    json_data = {'nodes': [], "links": []}
    d = []

    for i in data:
        # print("for i in data:")
        # print(i["p.name"], i["r.name"], i["n.name"],i["labels(p)"][0],i["labels(n)"][0])

        d.append(i['p.name']+"_"+i["labels(p)"][0])
        d.append(i['n.name'] + "_" + i["labels(n)"][0])

        d = list(set(d))
    # print(" d=list(set(d)):", d)
    name_dict = {}
    count = 0
    for j in d:
        j_array = j.split("_")

        data_item = {}
        name_dict[j_array[0]] = count

        # data_item['id'] = count
        count += 1
        data_item['id'] = j_array[0]
        # print("data_item['id']:",data_item['id'])
        data_item['label'] = j_array[0]
        data_item['category'] = HISTORY_LIST[j_array[1]]


        # print("data_item['category']:", data_item['category'])
        json_data['nodes'].append(data_item)
    for i in data:
        link_item = {}

        link_item['source'] = i['p.name']
        link_item['target'] = i['n.name']
        link_item['category'] = i["r.name"]
        link_item['label'] = i['r.name']

        # 获取imgUrl
        imgUrl = graph.run(
            "MATCH (n{name:'%s'}) RETURN properties(n)['img']" % (i[2])
        )
        for i in imgUrl:

            link_item['img'] = i[0]


        json_data['links'].append(link_item)



    return json_data