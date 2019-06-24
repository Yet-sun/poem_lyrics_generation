# encoding: utf-8

VOCAB_SIZE = 6272  # 词汇表大小

SHARE_EMD_WITH_SOFTMAX = True  # 是否在embedding层和softmax层之间共享参数

MAX_GRAD = 5.0  # 最大梯度，防止梯度爆炸

LEARN_RATE = 0.0005  # 初始学习率

LR_DECAY = 0.92  # 学习率衰减

LR_DECAY_STEP = 600  # 衰减步数

BATCH_SIZE = 64  # batch大小

CKPT_PATH = 'D:/mycode/Python_project/poem_backend/poem_app/chinese_poem_generate/ckptckpt/model_ckpt'  # 模型保存路径

VOCAB_PATH = 'D:/mycode/Python_project/poem_backend/poem_app/chinese_poem_generate/vocab/poetry.vocab'  # 词表路径

EMB_KEEP = 0.5  # embedding层dropout保留率

RNN_KEEP = 0.5  # lstm层dropout保留率
