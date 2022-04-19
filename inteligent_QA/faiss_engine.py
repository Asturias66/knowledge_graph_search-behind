# 找一个医疗领域的w2v词向量和分词器

# 任务定义：语义匹配
# X = <query, description>
# Y = {0, 1}

import torch
import torch.nn as nn


class Encoder(nn.Module):
    def __init__(self, config):
        super(Encoder, self).__init__()
        # TODO 找一个医疗领域的预训练词向量
        self.emb = torch.embedding()

        self.lstm = nn.LSTM(bidirectional=True,
                            hidden_size=config.hidden_size,
                            batch_first=True)

    def forward(self, query):
        vec = self.emb(query)
        vec = self.lstm(vec)

        return vec


# class SingleTower(nn.Module):
#     def __init__(self, config):
#         super(SingleTower, self).__init__()
#
#         self.encoder = Encoder(config)
#         self.fc = nn.Linear(config.hidden_size*2, 1)
#
#     def forward(self, query, description):
#         v1 = self.encoder(query)
#         v2 = self.encoder(description)
#
#         # TODO 拼接两个张量
#         v = torch.cat([v1, v2], axis=1)
#
#         return self.fc(v)


class DoubleTower(nn.Module):
    def __init__(self, config):
        super(DoubleTower, self).__init__()
        self.encoder1 = Encoder(config)
        self.encoder2 = Encoder(config)

        self.fc = nn.Linear(config.hidden_size, 1)

    def forward(self, query, description):
        v1 = self.encoder1(query)
        v2 = self.encoder2(description)

        # TODO 拼接两个张量
        v = torch.cat([v1, v2], axis=1)

        return self.fc(v)

    def predict(self, x, x_type='q'):
        if x_type == 'q':
            return self.encoder1(x)
        else:
            return self.encoder2(x)





