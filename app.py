import os
from PIL import Image

import glob
import json
from flask import Flask, request, jsonify
from neo_db.query_graph import getkeywordFromGraph,\
                    getAttributeFromGraph,\
                    getPeopleFromGraph,\
                    getChildEventFromGraph,\
                    getAllEventFromGraph,\
                    getTimeRecallDetailFromGraph,\
                    getMoreKeyWordFromGraph,\
                    getSpaceRecallDetailFromGraph,\
                    getSelectionFromGraph,\
                    getKeyWordsWithEventsFromGraph,\
                    getMovieFromRequest,\
                    getIdentityTipsFromRequest,\
                    getRandomOptions,\
                    getMoreTest

from chatbot_graph.question_answer import QAnalysis



app = Flask(__name__)


def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response


# getkeyword
@app.route('/getkeyword', methods=['GET', 'POST'])
def getkeyword():
    keyword = request.args.get('keyword')
    print("要查询的keyword：", keyword)
    json_data = getkeywordFromGraph(str(keyword))
    print("json_data:", json_data)
    return jsonify(json_data)

# getSpace
@app.route('/getSpace', methods=['GET', 'POST'])
def getSpace():
    space = request.args.get('space')
    print("要查询的space：", space)
    json_data = getkeywordFromGraph(str(space))
    print("json_data:", json_data)
    return jsonify(json_data)

# getSpaceRecallDetail
@app.route('/getSpaceRecallDetail', methods=['GET', 'POST'])
def getSpaceRecallDetail():
    space = request.args.get('space')
    print("要查询的space：", space)
    json_data = getSpaceRecallDetailFromGraph(str(space))
    print("json_data:", json_data)
    return jsonify(json_data)

# getAttribute
@app.route('/getAttribute', methods=['GET', 'POST'])
def getAttribute():
    subject = request.args.get('subject')
    print("要查询的subject：", subject)
    json_data = getAttributeFromGraph(str(subject))
    print("json_data:", json_data)
    return jsonify(json_data)


#getOptions
@app.route('/getOptions', methods=['GET', 'POST'])
def getOptions():
    keyword = request.args.get('keyword')
    print("要查询的keyword：", keyword)
    json_data = getRandomOptions(str(keyword))
    print("json_data:", json_data)
    return jsonify(json_data)

#getNew
@app.route('/getNew', methods=['GET', 'POST'])
def getNew():
    json_data = getMoreTest('data/history/PERSON')
    print("json_data:", json_data)
    return jsonify(json_data)


# getChildEvent
@app.route('/getChildEvent', methods=['GET', 'POST'])
def getChildEvent():
    event = request.args.get('event')
    print("要查询的event：", event)
    json_data = getChildEventFromGraph(str(event))
    print("json_data:", json_data)
    return jsonify(json_data)


# getPeople_获取人物的时间线
@app.route('/peopleReminiscence/getPeople', methods=['GET', 'POST'])
def getPeopleRelation():
    people = request.args.get('people')
    print("要查询的people：", people)
    json_data = getChildEventFromGraph(str(people))
    print("json_data:", json_data)
    return jsonify(json_data)




# getAllEvent
@app.route('/getAllEvent', methods=['GET', 'POST'])
def getAllEvent():
    # event = request.args.get('event')
    # print("要查询的event：", event)
    json_data = getAllEventFromGraph()
    print("json_data:", json_data)
    return jsonify(json_data)

# getPeople
@app.route('/relation/getPeople', methods=['GET', 'POST'])
def getPeople():
    object = request.args.get('object')
    subject = request.args.get('subject')
    print("要查询的object和subject：", object,subject)
    json_data = getPeopleFromGraph(str(object),str(subject))
    print("json_data:", json_data)
    return jsonify(json_data)


# getTimeRecallDetail
@app.route('/getTimeRecallDetail', methods=['GET', 'POST'])
def getTimeRecallDetail():
    time = request.args.get('time')
    print("要查询的time：",time)
    json_data = getTimeRecallDetailFromGraph(str(time))
    print("json_data:", json_data)
    return jsonify(json_data)

#getTime
@app.route('/getTime', methods=['GET', 'POST'])
def getTime():
    time = request.args.get('time')
    print("要查询的time：",time)
    json_data = getkeywordFromGraph(str(time))
    print("json_data:", json_data)
    return jsonify(json_data)

#getMoreKeyWord
@app.route('/getMoreKeyWord', methods=['GET', 'POST'])
def getMoreKeyWord():
    keyword = request.args.get('keyword')
    print("要查询的keyword：",keyword)
    json_data = getMoreKeyWordFromGraph(str(keyword))
    print("json_data:", json_data)
    return jsonify(json_data)


# getSelection
@app.route('/getSelection', methods=['GET', 'POST'])
def getSelection():
    json_data = getSelectionFromGraph()
    print("json_data:", json_data)
    return jsonify(json_data)

# getKeyWordsWithEvents
@app.route('/getKeyWordsWithEvents', methods=['GET', 'POST'])
def getKeyWordsWithEvents():
    keyword = request.args.get('keyword')
    print("要查询的keyword：",keyword)
    json_data = getKeyWordsWithEventsFromGraph(keyword)
    print("json_data:", json_data)
    return jsonify(json_data)


# getMovie
@app.route('/getMovie', methods=['GET', 'POST'])
def getMovie():
    keyword = request.args.get('keyword')
    print("要查询的keyword：",keyword)
    json_data = getMovieFromRequest(keyword)
    print("json_data:", json_data)
    return jsonify(json_data)


# queryAnswer
@app.route('/queryAnswer', methods=['GET', 'POST'])
def queryAnswer():
    question = request.args.get('question')
    print("要查询的question：",question)
    answer = QAnalysis(question)
    print("answer:", answer)
    return jsonify(answer)

def getPhotos(filePath):
# 获取图片
    # 获取read_path下的所有文件名称（顺序读取的）
    files = os.listdir(filePath)
    photoData = []
    for file_name in files:
        # print('file_name:',file_name)
        # 读取单个文件内容
        file_object = open(filePath + '/' + file_name, 'r', encoding='utf-8')
        read_data = file_object.read()  # 读取数据

        dataJson = json.loads(read_data)
        # print('dataJson:',dataJson)
        if dataJson['attributes']['img'] != '':
            # print('dataJson:',dataJson['attributes']['img'])
            photoData.append(dataJson['attributes']['img'])
            photoData.append(file_name.split('_')[0])

    print("photoData:",photoData)

def changePhotoSize(file, outdir, width, height):
    for file_item in glob.glob(file):  # 图片所在的目录
        imgFile = Image.open(file_item,"r")
        try:
            newImage = imgFile.resize((width, height), Image.BILINEAR)
            newImage.save(os.path.join(outdir, os.path.basename(file)))
        except Exception as e:
            print(e)

# getIdentityTips
@app.route('/getIdentityTips', methods=['GET', 'POST'])
def getIdentityTips():
    keyword = request.args.get('keyword')
    print("要查询的keyword：",keyword)
    json_data = getIdentityTipsFromRequest(keyword)
    print("json_data:", json_data)
    return jsonify(json_data)


if __name__ == '__main__':
    # getPhotos('data/history/PERSON')

    # path = "data/img"  # 图片所在的文件夹路径
    # for maindir, subdir, file_name_list in os.walk(path):
    #     print(file_name_list)
    #     for file_name in file_name_list:
    #         image = os.path.join(maindir, file_name)  # 获取每张图片的路径
    #         file = Image.open(image)
    #         out = file.resize((450, 450), Image.ANTIALIAS)  # 以高质量修改图片尺寸为（400，48）
    #         out.save(image)  # 以同名保存到原路径

    print("app")
    app.run(debug=False, host='0.0.0.0', port=80)

