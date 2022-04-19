

from inteligent_QA import question_classifier, question_parser, answer_search

'''问答类'''
# import answer_search
# import question_classifier
# import question_parser


class ChatBotGraph:
    def __init__(self):

        self.classifier = question_classifier.QuestionClassifier()

        self.parser = question_parser.QuestionParser()

        self.searcher = answer_search.AnswerSearcher()


    def chat_main(self, sent):

        answer = '请您详细描述您的问题。'
        res_classify = self.classifier.classify(sent)
        if not res_classify:
            return answer
        res_sql = self.parser.parser_main(res_classify)
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers)

if __name__ == '__main__':
    handler = ChatBotGraph()
    print("handler")
    while 1:
        question = input('用户:')
        answer = handler.chat_main(question)
        print('智能医疗助手:', answer)

