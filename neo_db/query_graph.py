from neo_db.config import graph, CA_LIST


# 查询单个信息
def query(name):
    print("name:",name)
    data = graph.run(
    "match(p:Disease {name:'%s'}) -[r:acompany_with]->(n) return p.name, r.name, n.name,p.cure_way,n.cure_way" % (name)
    )
    # print("返回的结果：", data)
    data = list(data)
    print("disease-data:",data)
    return get_json_data(data)


# 查询所有信息
def queryAllrelation(name):
    # print("name:",name)
    data = graph.run(
        # "match(p {name:'%s'}) -[r]->(n) return p,r,n" % (name)
    "match(p:Disease {name:'%s'}) -[r]->(n) return p.name, p.cause,p.cure_way,p.desc,r.name, n.name,p.easy_get,p.cured_prob,p.prevent,p.cure_lasttime" % (name)
    )
    # print("返回的结果：", data)
    data = list(data)
    # print("queryAllrelation返回的结果:",data)

    return get_json_data(data)


def get_json_data(data):
    json_data={'data':[],"links":[]}
    d=[]
    print("get_json_data的data:", data)
    
    for i in data:
        print("for i in data:")
        print(i["p.name"], i["r.name"], i["n.name"])

        d.append(i['p.name'] + "_" + "疾病")
        d.append(i['n.name']+"_"+str(i["r.name"]))
        print("i['n.name']+_+str(ir.name]):",i['n.name']+"_"+str(i["r.name"]))
        d.append(i['p.easy_get'] + "_" + "易发人群")
        d.append(i['p.cured_prob'] + "_" + "治愈概率")
        d.append(i['p.cure_lasttime'] + "_" + "持续时间")
        d.append(i['p.prevent'] + "_" + "防御措施")
        d.append(i['p.desc'] + "_" + "疾病的相关介绍")
        d.append(str(i['p.cure_way']) + "_" + "治疗方式")
        d.append(i['p.cause'] + "_" + "疾病原因")
        d=list(set(d))
    # print(" d=list(set(d)):", d)
    name_dict={}
    count=0
    for j in d:
        j_array=j.split("_")
    
        data_item={}
        name_dict[j_array[0]]=count
        count+=1
        data_item['name']=j_array[0]
        # print("--------------------")
        # print("j_array:", j_array)
        # print(" data_item['name']:", data_item['name'])
        data_item['category'] = CA_LIST[j_array[1]]
        # print("data_item['category']:", data_item['category'])
        json_data['data'].append(data_item)
        # print("json_data['data']:", json_data['data'])
    for i in data:
   
        link_item = {}
        
        link_item['source'] = name_dict[i['p.name']]
        
        link_item['target'] = name_dict[i['n.name']]
        link_item['value'] = i['r.name']
        json_data['links'].append(link_item)

    # print("json_data:", json_data)
    return json_data
# f = codecs.open('./static/test_data.json','w','utf-8')
# f.write(json.dumps(json_data,  ensure_ascii=False))

        



