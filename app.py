from flask import Flask, render_template, request, jsonify
from inteligent_QA.chatbot_graph import ChatBotGraph
from neo_db.query_graph import queryAllrelation
from success import getkeywordFromGraph,\
                    getAttributeFromGraph,\
                    getPeopleFromGraph,\
                    getChildEventFromGraph,\
                    getAllEventFromGraph,\
                    getTimeRecallDetailFromGraph,\
                    getMoreKeyWordFromGraph,\
                    getSpaceRecallDetailFromGraph,\
                    getSelectionFromGraph,\
                    getKeyWordsWithEventsFromGraph,\
                    getMovieFromRequest

from inteligent_QA.KBQA import QAnalysis



app = Flask(__name__)

# faiss_engine  # transform


def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response


# 路由
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index(name=None):
    return render_template('index.html', name=name)


# 智能问答
@app.route('/search_everything', methods=['GET', 'POST'])
def search_everything():
    user_question = request.args.get('user_question')
    print("我提的问题是：", user_question)

    # transform the query
    # user_question
    # 怕这个函数调用太慢的话可以把handler放到外面去
    handler = ChatBotGraph()  # neo4j
    answer = handler.chat_main(user_question)
    json_data = answer
    print("json_data:", json_data)
    return jsonify(json_data)


@app.route('/get_all_relation', methods=['GET', 'POST'])
def get_all_relation():
    return render_template('all_relation.html')


# 展示出这个疾病所有的关系
@app.route('/searchAllrelation', methods=['GET', 'POST'])
def searchAllrelation():
    name = request.args.get('name')
    print("要查询的疾病：", name)
    json_data = queryAllrelation(str(name))
    print("json_data:", json_data)
    return jsonify(json_data)

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


if __name__ == '__main__':
    print("app")
    app.run(debug=False, host='0.0.0.0', port=80)
