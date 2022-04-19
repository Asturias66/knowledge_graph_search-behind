
# 知识图谱入库脚本

import os
import json
from py2neo import Graph,Node



class HistoryGraph:
    # 配置ip地址、端口、用户名、密码连接Neo4j
    def __init__(self):

        self.g = Graph(
            host="localhost",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
            http_port=7474,  # neo4j 服务器监听的端口号
            user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
            password="123456")

    def getRelationFromFile(self,filePath):
        # 获取read_path下的所有文件名称（顺序读取的）
        # startNode = ''
        # if 'DATE' in filePath:
        #     startNode = 'DATE'
        # if 'EVENT' in filePath:
        #     startNode = 'EVENT'
        # if 'LAW' in filePath:
        #     startNode = 'LAW'
        # if 'LOCATION' in filePath:
        #     startNode = 'LOCATION'
        # if 'ORGANIZATION' in filePath:
        #     startNode = 'ORGANIZATION'
        # if 'PERSON' in filePath:
        #     startNode = 'PERSON'


        person = []
        date = []
        location = []
        organization = []
        event = []

        rel_person = []
        rel_date = []
        rel_location = []
        rel_organization = []
        rel_event = []
        files = os.listdir(filePath)
        info = []
        for file_name in files:
            # 读取单个文件内容
            file_object = open(filePath + '/' + file_name, 'r', encoding='utf-8')
            read_data = file_object.read()  # 读取数据

            entity = file_name.split('_')[0]

            dataJson = json.loads(read_data)
            for key, value in dataJson['relation'].items():
                if key == 'person':
                    rel_person.append([entity,value])
                    for key, val in value.items():
                        if val not in person:
                            person.append(val)
                if key == 'event':
                    rel_event.append([entity,value])
                    for key, val in value.items():
                        if val not in event:
                            event.append(val)
                if key == 'location':
                    rel_location.append([entity,value])
                    for key, val in value.items():
                        if val not in event:
                            location.append(val)
                if key == 'date':
                    rel_date.append([entity,value])
                    for key, val in value.items():
                        if val not in date:
                            date.append(val)
                if key == 'organization':
                    rel_organization.append([entity,value])
                    for key, val in value.items():
                        if val not in organization:
                            organization.append(val)
        return rel_person,rel_event,rel_location,rel_date,rel_organization,person,event,location,date,organization

    def getNodesFromAllFile(self,filePath):
        # 获取read_path下的所有文件名称（顺序读取的）
        files = os.listdir(filePath)
        info = []
        for file_name in files:
            # 读取单个文件内容
            file_object = open(filePath + '/' + file_name, 'r', encoding='utf-8')
            read_data = file_object.read()  # 读取数据

            dataJson = json.loads(read_data)

            # 创建节点属性
            property_dict = {}
            property_dict['name'] = file_name.split('_')[0]
            for key, value in dataJson['attributes'].items():
                property_dict[key] = value
            property_dict['时间线'] = str(dataJson['timeLine'])
            print(property_dict)
            info.append(property_dict)
        return info

        '''建立节点'''

    '''读取文件,获得实体，实体关系'''
    def read_nodes(self):
        print("读取文件")
        # 共6类节点（实体）
        person = []
        law = []
        event = []
        relic = []
        date = []
        location = []

        # person = self.getNodesFromAllFile('data/JsonCenter/person')
        # document = self.getNodesFromAllFile('data/JsonCenter/document')
        # event = self.getNodesFromAllFile('data/JsonCenter/event')
        # relic = self.getNodesFromAllFile('data/JsonCenter/relic')
        # time = self.getNodesFromAllFile('data/JsonCenter/time')
        # location = self.getNodesFromAllFile('data/JsonCenter/location')

        person = self.getNodesFromAllFile('data/history/PERSON')
        event = self.getNodesFromAllFile('data/history/EVENT')
        law = self.getNodesFromAllFile('data/history/LAW')
        location = self.getNodesFromAllFile('data/history/LOCATION')
        organization = self.getNodesFromAllFile('data/history/ORGANIZATION')
        date = self.getNodesFromAllFile('data/history/DATE')

        # print(len(person))
        # print(len(event))
        # print(len(law))
        # print(len(location))
        # print(len(organization))
        # print(len(date))

        person_extra = []
        event_extra = []
        location_extra = []
        date_extra = []
        organization_extra = []


        rel_person_person, rel_person_event, rel_person_location, rel_person_date, rel_person_organization, person0, event0, location0, date0, organization0 = self.getRelationFromFile('data/history/PERSON')
        person_extra.append(person0)
        event_extra.append(event0)
        location_extra.append(location0)
        date_extra.append(date0)
        organization_extra.append(organization0)
        rel_event_person, rel_event_event, rel_event_location, rel_event_date, rel_event_organization, person0, event0, location0, date0, organization0 = self.getRelationFromFile(
            'data/history/EVENT')
        person_extra.append(person0)
        event_extra.append(event0)
        location_extra.append(location0)
        date_extra.append(date0)
        organization_extra.append(organization0)
        rel_law_person, rel_law_event, rel_law_location, rel_law_date, rel_law_organization, person0, event0, location0, date0, organization0 = self.getRelationFromFile(
            'data/history/LAW')
        person_extra.append(person0)
        event_extra.append(event0)
        location_extra.append(location0)
        date_extra.append(date0)
        organization_extra.append(organization0)
        rel_location_person, rel_location_event, rel_location_location, rel_location_date, rel_location_organization, person0, event0, location0, date0, organization0 = self.getRelationFromFile(
            'data/history/LOCATION')
        person_extra.append(person0)
        event_extra.append(event0)
        location_extra.append(location0)
        date_extra.append(date0)
        organization_extra.append(organization0)
        rel_organization_person, rel_organization_event, rel_organization_location, rel_organization_date, rel_organization_organization, person0, event0, location0, date0, organization0 = self.getRelationFromFile(
            'data/history/ORGANIZATION')
        person_extra.append(person0)
        event_extra.append(event0)
        location_extra.append(location0)
        date_extra.append(date0)
        organization_extra.append(organization0)
        rel_date_person, rel_date_event, rel_date_location, rel_date_date, rel_date_organization, person0, event0, location0, date0, organization0 = self.getRelationFromFile(
            'data/history/DATE')
        person_extra.append(person0)
        event_extra.append(event0)
        location_extra.append(location0)
        date_extra.append(date0)
        organization_extra.append(organization0)

        for i in range(0,6):
            print(person_extra[i])
            allPerson = []
            allDate = []
            allLocation = []
            allEvent = []
            allOrganization = []
            for p in person:
                allPerson.append(p['name'])
            for p in date:
                allDate.append(p['name'])
            for p in location:
                allLocation.append(p['name'])
            for p in event:
                allEvent.append(p['name'])
            for p in organization:
                allOrganization.append(p['name'])

            for j in person_extra[i]:
                if j not in allPerson:
                    property_dict = {}
                    property_dict['name'] = j
                    person.append(property_dict)
            for j in event_extra[i]:
                if j not in allEvent:
                    property_dict = {}
                    property_dict['name'] = j
                    event.append(property_dict)
            for j in location_extra[i]:
                if j not in allLocation:
                    property_dict = {}
                    property_dict['name'] = j
                    location.append(property_dict)
            for j in date_extra[i]:
                if j not in allDate:
                    property_dict = {}
                    property_dict['name'] = j
                    date.append(property_dict)
            for j in organization_extra[i]:
                if j not in allOrganization:
                    property_dict = {}
                    property_dict['name'] = j
                    organization.append(property_dict)

        return person,event,law,location,organization,date,rel_person_person, rel_person_event, rel_person_location, rel_person_date, rel_person_organization,rel_event_person, rel_event_event, rel_event_location, rel_event_date, rel_event_organization,\
               rel_location_person, rel_location_event, rel_location_location, rel_location_date, rel_location_organization,rel_organization_person, rel_organization_event, rel_organization_location, rel_organization_date, rel_organization_organization,rel_date_person, rel_date_event, rel_date_location, rel_date_date, rel_date_organization,rel_law_person, rel_law_event, rel_law_location, rel_law_date, rel_law_organization


    '''创建知识图谱中心疾病的节点'''

    def create_nodes(self, NodeLabel, infos):
        print("创建知识图谱中心疾病的节点属性")
        for property_dict in infos:
            print("property_dict:", property_dict)

            # 初步生成节点
            node = Node(NodeLabel)
            self.g.create(node)

            # 给节点加属性
            for key, value in property_dict.items():
                # print("key:",key,"value:",value)
                node.update({key: value})
                self.g.push(node)
        return

        '''创建知识图谱实体节点类型schema'''
    def create_graphnodes(self):
            print("创建知识图谱实体节点类型schema")
            person,event,law,location,organization,date,rel_person_person, rel_person_event, rel_person_location, rel_person_date, rel_person_organization,rel_event_person, rel_event_event, rel_event_location, rel_event_date, rel_event_organization,\
               rel_location_person, rel_location_event, rel_location_location, rel_location_date, rel_location_organization,rel_organization_person, rel_organization_event, rel_organization_location, rel_organization_date, rel_organization_organization,rel_date_person, rel_date_event, rel_date_location, rel_date_date, rel_date_organization,rel_law_person, rel_law_event, rel_law_location, rel_law_date, rel_law_organization = self.read_nodes()
            self.create_nodes("HistoryPerson1",person)
            self.create_nodes("HistoryEvent", event)
            self.create_nodes("HistoryLaw", law)
            self.create_nodes("HistoryLocation", location)
            self.create_nodes("HistoryOrganization", organization)
            self.create_nodes("HistoryDate", date)
            return

    '''创建实体关联边'''
    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        print("创建实体关联边")
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            try:
                self.g.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return

    '''创建实体关联边'''

    def create_singlerelationship(self, start_node, end_node, edge, rel_type, rel_name):
        print("创建实体关联边")
        count = 0
        # # 去重处理
        # set_edges = []
        # for edge in edges:
        #     set_edges.append('###'.join(edge))
        # all = len(set(set_edges))
        # for edge in set(set_edges):
        #     edge = edge.split('###')
        p = edge[0]
        q = edge[1]
        query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
            start_node, end_node, p, q, rel_type, rel_name)
        try:
            self.g.run(query)
            count += 1
            print(rel_type, count, all)
        except Exception as e:
            print(e)
        return

    def create_singlerelationshipForEvent_Date(self, start_node, end_node, edge, rel_type, rel_name):
        print("创建实体关联边")
        count = 0
        # # 去重处理
        # set_edges = []
        # for edge in edges:
        #     set_edges.append('###'.join(edge))
        # all = len(set(set_edges))
        # for edge in set(set_edges):
        #     edge = edge.split('###')
        p = edge[0]
        q = edge[1]
        data = "MATCH (n{name:'%s'}) RETURN n" %()


        query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
            start_node, end_node, p, q, rel_type, rel_name)
        try:
            self.g.run(query)
            count += 1
            print(rel_type, count, all)
        except Exception as e:
            print(e)
        return



    '''创建实体关系边'''
    def create_graphrels(self):
        # 获得各个实体之间的关系
        person, event, law, location, organization, date, rel_person_person, rel_person_event, rel_person_location, rel_person_date, rel_person_organization, rel_event_person, rel_event_event, rel_event_location, rel_event_date, rel_event_organization, \
        rel_location_person, rel_location_event, rel_location_location, rel_location_date, rel_location_organization, rel_organization_person, rel_organization_event, rel_organization_location, rel_organization_date, rel_organization_organization, rel_date_person, rel_date_event, rel_date_location, rel_date_date, rel_date_organization,rel_law_person, rel_law_event, rel_law_location, rel_law_date, rel_law_organization = self.read_nodes()
        print(person)
        print(event)
        print(law)
        print(location)
        print(organization)
        print(date)
        print(rel_person_person)
        for rela in rel_person_person:
            edge = []
            edge.append(rela[0])
            for key,value in rela[1].items():
                if(len(edge) == 1):
                    edge.append(value)
                else:
                    edge[1] = value
                key = key.rstrip('0123456789')
                self.create_singlerelationship('HistoryPerson1', 'HistoryPerson1', edge, 'person_person', key)
        for rela in rel_person_event:
            edge = []
            edge.append(rela[0])
            for key,value in rela[1].items():
                if (len(edge) == 1):
                    edge.append(value)
                else:
                    edge[1] = value
                key = key.rstrip('0123456789')
                self.create_singlerelationship('HistoryPerson1', 'HistoryEvent', edge, 'person_event', key)
        for rela in rel_person_location:
            edge = []
            edge.append(rela[0])
            for key,value in rela[1].items():
                if (len(edge) == 1):
                    edge.append(value)
                else:
                    edge[1] = value
                key = key.rstrip('0123456789')
                self.create_singlerelationship('HistoryPerson1', 'HistoryLocation', edge, 'person_location', key)
        for rela in rel_person_date:
            edge = []
            edge.append(rela[0])
            for key,value in rela[1].items():
                if (len(edge) == 1):
                    edge.append(value)
                else:
                    edge[1] = value
                key = key.rstrip('0123456789')
                self.create_singlerelationship('HistoryPerson1', 'HistoryDate', edge, 'person_date', key)
        for rela in rel_person_organization:
            edge = []
            edge.append(rela[0])
            for key,value in rela[1].items():
                if (len(edge) == 1):
                    edge.append(value)
                else:
                    edge[1] = value
                key = key.rstrip('0123456789')
                self.create_singlerelationship('HistoryPerson1', 'HistoryOrganization', edge, 'person_organization', key)
        for rela in rel_event_person:
            edge = []
            edge.append(rela[0])
            for key,value in rela[1].items():
                if (len(edge) == 1):
                    edge.append(value)
                else:
                    edge[1] = value
                key = key.rstrip('0123456789')
                self.create_singlerelationship('HistoryEvent', 'HistoryPerson1', edge, 'event_person', key)
        for rela in rel_event_event:
            edge = []
            edge.append(rela[0])
            for key,value in rela[1].items():
                if (len(edge) == 1):
                    edge.append(value)
                else:
                    edge[1] = value
                key = key.rstrip('0123456789')
                self.create_singlerelationship('HistoryEvent', 'HistoryEvent', edge, 'event_event', key)
        for rela in rel_event_location:
            edge = []
            edge.append(rela[0])
            for key,value in rela[1].items():
                if (len(edge) == 1):
                    edge.append(value)
                else:
                    edge[1] = value
                key = key.rstrip('0123456789')
                self.create_singlerelationship('HistoryEvent', 'HistoryLocation', edge, 'event_location', key)
        for rela in rel_event_date:
            edge = []
            edge.append(rela[0])
            for key,value in rela[1].items():
                if (len(edge) == 1):
                    edge.append(value)
                else:
                    edge[1] = value
                key = key.rstrip('0123456789')
                self.create_singlerelationship('HistoryEvent', 'HistoryDate', edge, 'event_date', key)
        print('球球建event_date')
        for rela in rel_event_organization:
            edge = []
            edge.append(rela[0])
            for key,value in rela[1].items():
                if (len(edge) == 1):
                    edge.append(value)
                else:
                    edge[1] = value
                key = key.rstrip('0123456789')
                self.create_singlerelationship('HistoryEvent', 'HistoryOrganization', edge, 'event_organization', key)
        for rela in rel_location_person:
            edge = []
            edge.append(rela[0])
            for key,value in rela[1].items():
                if (len(edge) == 1):
                    edge.append(value)
                else:
                    edge[1] = value
                key = key.rstrip('0123456789')
                self.create_singlerelationship('HistoryLocation', 'HistoryPerson1', edge, 'location_person', key)
        for rela in rel_location_event:
            edge = []
            edge.append(rela[0])
            for key,value in rela[1].items():
                if (len(edge) == 1):
                    edge.append(value)
                else:
                    edge[1] = value
                key = key.rstrip('0123456789')
                self.create_singlerelationship('HistoryLocation', 'HistoryEvent', edge, 'location_event', key)
        for rela in rel_location_location:
            edge = []
            edge.append(rela[0])
            for key,value in rela[1].items():
                if (len(edge) == 1):
                    edge.append(value)
                else:
                    edge[1] = value
                key = key.rstrip('0123456789')
                self.create_singlerelationship('HistoryLocation', 'HistoryLocation', edge, 'location_location', key)
        for rela in rel_location_date:
            edge = []
            edge.append(rela[0])
            for key,value in rela[1].items():
                if (len(edge) == 1):
                    edge.append(value)
                else:
                    edge[1] = value
                key = key.rstrip('0123456789')
                self.create_singlerelationship('HistoryLocation', 'HistoryDate', edge, 'location_date', key)
        for rela in rel_location_organization:
            edge = []
            edge.append(rela[0])
            for key,value in rela[1].items():
                if (len(edge) == 1):
                    edge.append(value)
                else:
                    edge[1] = value
                key = key.rstrip('0123456789')
                self.create_singlerelationship('HistoryLocation', 'HistoryOrganization', edge, 'location_organization', key)
        for rela in rel_organization_person:
            edge = []
            edge.append(rela[0])
            for key,value in rela[1].items():
                if (len(edge) == 1):
                    edge.append(value)
                else:
                    edge[1] = value
                key = key.rstrip('0123456789')
                self.create_singlerelationship('HistoryOrganization', 'HistoryPerson1', edge, 'organization_person', key)
        for rela in rel_organization_event:
            edge = []
            edge.append(rela[0])
            for key,value in rela[1].items():
                if (len(edge) == 1):
                    edge.append(value)
                else:
                    edge[1] = value
                key = key.rstrip('0123456789')
                self.create_singlerelationship('HistoryOrganization', 'HistoryEvent', edge, 'organization_event', key)
        for rela in rel_organization_location:
            edge = []
            edge.append(rela[0])
            for key,value in rela[1].items():
                if (len(edge) == 1):
                    edge.append(value)
                else:
                    edge[1] = value
                key = key.rstrip('0123456789')
                self.create_singlerelationship('HistoryOrganization', 'HistoryLocation', edge, 'organization_location', key)
        for rela in rel_organization_date:
            edge = []
            edge.append(rela[0])
            for key,value in rela[1].items():
                if (len(edge) == 1):
                    edge.append(value)
                else:
                    edge[1] = value
                key = key.rstrip('0123456789')
                self.create_singlerelationship('HistoryOrganization', 'HistoryDate', edge, 'organization_date', key)
        for rela in rel_organization_organization:
            edge = []
            edge.append(rela[0])
            for key,value in rela[1].items():
                if (len(edge) == 1):
                    edge.append(value)
                else:
                    edge[1] = value
                key = key.rstrip('0123456789')
                self.create_singlerelationship('HistoryOrganization', 'HistoryOrganization', edge, 'organization_organization', key)
        for rela in rel_date_person:
            edge = []
            edge.append(rela[0])
            for key,value in rela[1].items():
                if (len(edge) == 1):
                    edge.append(value)
                else:
                    edge[1] = value
                key = key.rstrip('0123456789')
                self.create_singlerelationship('HistoryDate', 'HistoryPerson1', edge, 'date_person', key)
        for rela in rel_date_event:
            edge = []
            edge.append(rela[0])
            for key,value in rela[1].items():
                if (len(edge) == 1):
                    edge.append(value)
                else:
                    edge[1] = value
                key = key.rstrip('0123456789')
                self.create_singlerelationship('HistoryDate', 'HistoryEvent', edge, 'date_event', key)
        for rela in rel_date_location:
            edge = []
            edge.append(rela[0])
            for key,value in rela[1].items():
                if (len(edge) == 1):
                    edge.append(value)
                else:
                    edge[1] = value
                key = key.rstrip('0123456789')
                self.create_singlerelationship('HistoryDate', 'HistoryLocation', edge, 'date_location', key)
        for rela in rel_date_date:
            edge = []
            edge.append(rela[0])
            for key,value in rela[1].items():
                if (len(edge) == 1):
                    edge.append(value)
                else:
                    edge[1] = value
                key = key.rstrip('0123456789')
                self.create_singlerelationship('HistoryDate', 'HistoryDate', edge, 'date_date', key)
        for rela in rel_date_organization:
            edge = []
            edge.append(rela[0])
            for key,value in rela[1].items():
                if (len(edge) == 1):
                    edge.append(value)
                else:
                    edge[1] = value
                key = key.rstrip('0123456789')
                self.create_singlerelationship('HistoryDate', 'HistoryOrganization', edge, 'date_organization', key)
        for rela in rel_law_person:
            edge = []
            edge.append(rela[0])
            for key,value in rela[1].items():
                if (len(edge) == 1):
                    edge.append(value)
                else:
                    edge[1] = value
                key = key.rstrip('0123456789')
                self.create_singlerelationship('HistoryLaw', 'HistoryPerson1', edge, 'law_person', key)
        for rela in rel_law_event:
            edge = []
            edge.append(rela[0])
            for key,value in rela[1].items():
                if (len(edge) == 1):
                    edge.append(value)
                else:
                    edge[1] = value
                key = key.rstrip('0123456789')
                self.create_singlerelationship('HistoryLaw', 'HistoryEvent', edge, 'law_event', key)
        for rela in rel_law_location:
            edge = []
            edge.append(rela[0])
            for key,value in rela[1].items():
                if (len(edge) == 1):
                    edge.append(value)
                else:
                    edge[1] = value
                key = key.rstrip('0123456789')
                self.create_singlerelationship('HistoryLaw', 'HistoryLocation', edge, 'law_location', key)
        for rela in rel_law_date:
            edge = []
            edge.append(rela[0])
            for key,value in rela[1].items():
                if (len(edge) == 1):
                    edge.append(value)
                else:
                    edge[1] = value
                key = key.rstrip('0123456789')
                self.create_singlerelationship('HistoryLaw', 'HistoryDate', edge, 'law_date', key)
        for rela in rel_law_organization:
            edge = []
            edge.append(rela[0])
            for key,value in rela[1].items():
                if (len(edge) == 1):
                    edge.append(value)
                else:
                    edge[1] = value
                key = key.rstrip('0123456789')
                self.create_singlerelationship('HistoryLaw', 'HistoryOrganization', edge, 'law_organization', key)






if __name__ == '__main__':
    handler = HistoryGraph()
    print("step1:导入图谱节点中")

    handler.create_graphnodes()
    print("step2:导入图谱边中")
    handler.create_graphrels()
    print("over")





