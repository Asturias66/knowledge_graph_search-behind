# coding:utf-8


import hanlp
from py2neo import Graph
graph = Graph('http://localhost:7474/', auth=("neo4j", "123456"))

procressNum = 0

def QAnalysis(question):
    HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)  # 世界最大中文语料库
    # 命名实体识别ner
    hanLPResult = HanLP(question, tasks=["tok/coarse","ner/msra", "pos/ctb"])  # "srl"
    tok = hanLPResult.to_dict()["tok/coarse"]
    nerMsra = hanLPResult.to_dict()["ner/msra"]
    ner = [item for item in nerMsra]
    ctb = hanLPResult.to_dict()["pos/ctb"]
    print(tok)
    print(ner)
    print(ctb)
    json_data = {'answer':''}
    json_data['answer'] = QClassify(question,tok,ctb,ner)
    return json_data

def QClassify(question,tok,ctb,ner):
    answer = ''
    # 是否多意图
    if(question.count("？")==0):
        print("未检测到问题")
        answer = '抱歉，未检测到问题，请您输入您的问题。'
        print("答案是：", answer)
        return answer

    elif(question.count("？")==1):
        print("单意图问题")
        if(len(ner)==1):
            print("查实体")
            if(ctb.count("NN") == 1):
                print("单跳查询")
                try:
                    index = ctb.index("NN")
                    node = list(ner[0])[0]
                    relax = tok[index]
                    print("要查询的内容为:<{},{},?>".format(node,relax))

                    answerData = graph.run(
                       "match(p{name:'%s'}) -[r{name:'%s'}]->(n) return r.name,p.name,n.name"%(node,relax)
                    )
                    answerData = list(answerData)

                    answerList = []
                    for i in answerData:
                        answerList.append(i['n.name'])
                    if len(answerList) != 0:
                        answerStr = "、".join(answerList)
                        answer = node + '的' + relax + '是：' + answerStr + '。'
                        print("答案是：",answer)
                        return answer
                    else:
                        answer = '抱歉，无法检索出' + node + '的' + relax + '。'
                        print("答案是：", answer)
                        return answer

                except:
                    print("无法识别出要检索的关系")
                    answer = '抱歉，无法识别出要检索的关系，请您详细描述您的问题。'
                    print("答案是：", answer)
                    return answer

            elif(ctb.count("NN")>1):
                print("多跳链式查询")
                indexList = [i for i in range(len(ctb)) if ctb[i] == "NN"]
                node = list(ner[0])[0]
                text = "要查询的内容为:" + node

                childAnswer = ''
                answer = ''
                answerList = []

                for i in range(len(indexList)):
                    if i == 0:
                        answerData = graph.run(
                            "match(p{name:'%s'}) -[r{name:'%s'}]->(n) return r.name,p.name,n.name" % (node,tok[indexList[i]])
                        )
                        answerData = list(answerData)
                        for j in answerData:
                            answerList.append(j['n.name'])
                        answerStr = "、".join(answerList)
                        answer = node + '的' + tok[indexList[i]] + '是：' + answerStr + '。'
                    else:
                        for next_item in answerList:
                            node = next_item
                            print("新的node:", node)
                            childData = graph.run(
                                "match(p{name:'%s'}) -[r{name:'%s'}]->(n) return r.name,p.name,n.name" % (node, tok[indexList[i]])
                            )

                            # if len(childData.data()) == 0:
                            #     childAnswer = childAnswer + ',' + node + "的" + tok[indexList[i]] + '未搜索到'

                            for j in childData:
                                child_node = j['n.name']
                                if child_node != '':
                                    childAnswer = childAnswer + '，' + node + "的" + tok[indexList[i]] + '是' + child_node
                                else:
                                    childAnswer = childAnswer + '，' + node + "的" + tok[indexList[i]] + '未搜索到'
                childAnswer = childAnswer[1:] + '。'
                print(answer)
                print(childAnswer)
                answer = answer + childAnswer
                print("答案是：", answer)
                return answer

        elif(len(ner)==2):
            if(("P" in ctb) or ("VC" in ctb)):
                if("VV" in ctb):
                    if(ctb.index("NN")):
                        relax = tok[ctb.index("NN")]
                    else:
                        relax = "未知关系"
                    print("查两个实体的关系/属性交集")
                    print("要查询的内容为:<{},{},?> 交集<{},{},?>".format(ner[0], relax, ner[1], relax))
                    # 添加查询语句，ner[0]为中心节点1的名称，ner[1]中心节点2的名称，查询之后返回二者共有的关系relax所对应的节点
                else:
                    print("查两个实体的关系/属性")
                    print("要查询的内容为:<{},?,{}>".format(ner[0], ner[1]))

                    answerData = graph.run(
                        "match(p {name:'%s'}) -[r]->(n {name:'%s'}) return r.name" % (ner[0][0], ner[1][0])
                    )
                    answerData = list(answerData)
                    for j in answerData:
                        answer = str(j['r.name'])
                        if answer != '':
                            answer = ner[1][0] + '是' + ner[0][0] + '的' + answer + '。'
                            print(answer)
                            return answer
                        else:
                            answer = '未检索到' + ner[0][0] + ner[1][0] + '的关系。'
                            print("答案是：", answer)
                            return answer
                    # 添加查询语句，ner[0]为中心节点1的名称，ner[1]中心节点2的名称，查询之后返回二者关系的名称

            elif("CC" in ctb):
                index = ctb.index("NN")
                relax = tok[index]
                if(tok[index] == "关系"):
                    print("查两个实体的关系/属性")
                    print("要查询的内容为:<{},{},{}>".format(ner[0], relax, ner[1]))
                    answerData = graph.run(
                        "match(p {name:'%s'}) -[r]->(n {name:'%s'}) return r.name" % (ner[0][0], ner[1][0])
                    )
                    answerData = list(answerData)
                    for j in answerData:
                        answer = str(j['r.name'])
                        if answer != '':
                            answer = ner[1][0] + '是' + ner[0][0] + '的' + answer
                            print(answer)
                            return answer
                        else:
                            answer = '未检索到' + ner[0][0] + ner[1][0] + '的关系'
                            print("答案是：", answer)
                            return answer
                    # 添加查询语句，ner[0]为中心节点1的名称，ner[1]中心节点2的名称，查询之后返回二者关系的名称
                else:
                    print("查两个实体的关系/属性交集")
                    print("要查询的内容为:<{},{},?> 交集<{},{},?>".format(ner[0], relax, ner[1], relax))
                    # 添加查询语句，ner[0]为中心节点1的名称，ner[1]中心节点2的名称，查询之后返回二者共有的关系relax所对应的节点
        else:
            print("未知问题类型")
            answer = '抱歉，未知问题类型，请您重新输入您的问题。'
            print("答案是：", answer)
            return answer
    else:
        print("多意图问题")
    print("返回answer:",answer)
    return answer

