import torch
import pykakasi
# import MeCab
from transformers import AutoTokenizer, AutoModelForMaskedLM, pipeline

# pretrain_model = "cl-tohoku/bert-base-japanese-char-v2"
pretrain_model = "nlp-waseda/roberta-base-japanese"


# model_name = "model-toho_char-kanji_hiragana-8"
# model_name = "model-toho_char-kanji-8"
model_name = "model-waseda_roberta-kanji_hiragana-8"
# model_name = "model-waseda_roberta-kanji-8"

model = AutoModelForMaskedLM.from_pretrained(model_name)

tokenizer = AutoTokenizer.from_pretrained(pretrain_model)
unmasker = pipeline('fill-mask', model=model, tokenizer=tokenizer)

# kanji to katagana

# def mecab_list(text):
#     tagger = MeCab.Tagger()
#     tagger.parse('')
#     node = tagger.parseToNode(text)
#     word_class = []
#     while node:
#         word = node.surface
#         wclass = node.feature.split(',')
#         if wclass[0] != u'BOS/EOS':
#             if wclass[6] == None:
#                 word_class.append((word,wclass[0],wclass[1],wclass[2],""))
#             else:
#                 word_class.append((word,wclass[0],wclass[1],wclass[2],wclass[6]))
#         node = node.next
#     return word_class


kks = pykakasi.kakasi()

# a function return the #katagana
def num(text):
#   return len(mecab_list(text)[0][4])
    b=kks.convert(text)
    n = 0
    for line in b:
        n += len(line['hira'])
    return n


def nonminus(a):
    if a > 0:
        return a
    else:
        return 0

# a function for predicting in loop
# def prediction(input_text, n=5):
#     while n < 17:
#         pre = unmasker(input_text + '[MASK]' + '[PAD]' * nonminus(17-n-2) + '[SEP]')
#         if (pre[0]['token_str'][0] != input_text[-1]) and (pre[0]['token_str'][0] != input_text[-2]):
#             input_text = input_text + pre[0]['token_str']
#             n += num(pre[0]['token_str'])
#         elif (pre[1]['token_str'][0] != input_text[-1]) and (pre[1]['token_str'][0] != input_text[-2]):
#             input_text = input_text + pre[1]['token_str']
#             n += num(pre[1]['token_str'])
#         else:
#             input_text = input_text + pre[2]['token_str']
#             n += num(pre[2]['token_str'])
#     return(input_text)


def prediction(input_text, n=5):
    while n < 17:
        pre = unmasker(input_text + '[MASK]' + '[PAD]' * nonminus(17-n-2) + '[SEP]')
        if (pre[0]['token_str'][0] != input_text[-1]) and (pre[0]['token_str'][0] != input_text[-2]):
            input_text = input_text + pre[0]['token_str']
            n += num(pre[0]['token_str'])

        else:
            input_text = input_text + pre[1]['token_str']
            n += num(pre[1]['token_str'])
        print(input_text)
    return(input_text)

# def prediction(input_text, n=5):
#     while n < 17:
#         pre = unmasker(input_text + '[MASK]'+'[PAD]'*(17-n-2)+'[SEP]')
#         input_text = input_text + pre[0]['token_str']
#         n += num(pre[0]['token_str'])
#     return(input_text)

# test
# print("上5（かみご）5音の言葉: (終わりしたいならendを入れ)")

# with open("test_text/text_for_final.txt", 'r') as f1, open("2-output_for_%s.txt"%(model_name), 'w') as f2:
#     for line in f1:
#         l = line[:(len(line)-1)]
#         output = prediction(l)
#         print(output)
#         f2.write(output+'\n')

# import datasets
# with open("test_text/text_for_final.txt", 'r') as f1:
#     for line in f1:
#         l = line[:(len(line)-2)]
#         output = prediction(l)
#         print(output)

input_text = input()
while(input_text != "end"):
    result = prediction(input_text)
    print("result: ", result)
    print("\n上5（かみご）5音の言葉")
    input_text = input()
