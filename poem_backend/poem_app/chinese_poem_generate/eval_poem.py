# encoding: utf-8
import tensorflow as tf
import numpy as np
from .rnn_models import EvalModel
from .utils import *

x_data = tf.placeholder(tf.int32, [1, None])

emb_keep = tf.placeholder(tf.float32)  # embedding层dropout保留率

rnn_keep = tf.placeholder(tf.float32)  # lstm层dropout保留率

# 验证用模型
model = EvalModel(x_data, emb_keep, rnn_keep)

# 模型保存，Saver对象
saver = tf.train.Saver()
graph = tf.get_default_graph()
sess = tf.Session(graph=graph)
ckpt = tf.train.get_checkpoint_state('D:\\mycode\\Python_project\\poem_backend\\poem_app\\chinese_poem_generate\\ckpt')

# 单词到id的映射
word2id_dict = read_word_to_id_dict()
# id到单词的映射
id2word_dict = read_id_to_word_dict()


def generate_word(prob):
    """
    选择概率最高的前100个词，并用轮盘赌法选取最终结果
    :param prob: 概率向量
    :return: 生成的词
    """
    prob = sorted(prob, reverse=True)[:100]
    index = np.searchsorted(np.cumsum(prob), np.random.rand(1) * np.sum(prob))
    return id2word_dict[int(index)]


def generate_poem():
    """
    随机生成一首诗歌
    :return:
    """
    with tf.Session() as sess:
        # 加载最新的模型
        saver = tf.train.import_meta_graph(ckpt.model_checkpoint_path + '.meta')
        saver.restore(sess, ckpt.model_checkpoint_path)
        # 预测第一个词
        rnn_state = sess.run(model.cell.zero_state(1, tf.float32))
        x = np.array([[word2id_dict['s']]], np.int32)
        prob, rnn_state = sess.run([model.prob, model.last_state],
                                   {model.data: x, model.init_state: rnn_state, model.emb_keep: 1.0,
                                    model.rnn_keep: 1.0})
        word = generate_word(prob)
        poem = ''
        # 循环操作，直到预测出结束符号‘e’
        while word != 'e':
            poem += word
            x = np.array([[word2id_dict[word]]])
            prob, rnn_state = sess.run([model.prob, model.last_state],
                                       {model.data: x, model.init_state: rnn_state, model.emb_keep: 1.0,
                                        model.rnn_keep: 1.0})
            word = generate_word(prob)
        # 打印生成的诗歌
        # print(poem)
        # 返回打印的诗歌
        poem = str(poem).split("。")

        return poem


def generate_acrostic(head, type):
    """
    生成藏头诗
    :param head:每行的第一个字组成的字符串
    :return:
    """
    if type != 5 and type != 7:
        error = 'The second para has to be 5 or 7!'
        print(error)
        return error

    with tf.Session() as sess:
        # 加载最新的模型
        # ckpt = tf.train.get_checkpoint_state('ckpt')
        saver = tf.train.import_meta_graph(ckpt.model_checkpoint_path + '.meta')
        saver.restore(sess, ckpt.model_checkpoint_path)
        # 进行预测
        rnn_state = sess.run(model.cell.zero_state(1, tf.float32))
        char_list = ["<unknow>", 'e', 's']
        poem = ''
        cnt = 1
        # 一句句生成诗歌
        for x in head:
            word = x
            len_of_sentence = 0
            while word != '，' and word != '。' and word != '？':
                while len_of_sentence < type:
                    if word != '，' and word != '。' and word != '？':
                        poem += word
                        x = np.array([[word2id_dict[word]]])
                        prob, rnn_state = sess.run([model.prob, model.last_state],
                                                   {model.data: x, model.init_state: rnn_state, model.emb_keep: 1.0,
                                                    model.rnn_keep: 1.0})
                        word = generate_word(prob)
                        len_of_sentence += 1
                    else:
                        # 如果生成了 '，'或'。'或'？'，则重新生成一个字
                        word = generate_word(prob)
                else:
                    break
            # 根据单双句添加标点符号
            if cnt & 1:
                poem += '，'
            else:
                poem += '。\n'
            cnt += 1

        if len(poem) > 66:
            print('poem is too long，try again.')

        # 诗中若出现"<unknow>" or 'e' or 's'，则重新生成一首诗
        if any(char in poem for char in char_list):
            print("characters error")
            poem = generate_acrostic(head, type)
        # 打印生成的诗歌
        # print(poem)
        poem = str(poem).split("。")

        return poem


if __name__ == '__main__':
    head = u'我爱中国'
    type = 7
    # generate_acrostic(head, type)
    generate_poem()
