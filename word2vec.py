import gensim, logging
import os
import json
from collections import defaultdict
from flags import FLAGS

VOCAB_SIZE = FLAGS.vocab_size - 3
LEN = FLAGS.sequence_length
DIR = FLAGS.data_dir

def fre_word():
    word_f = open(os.path.join(DIR, 'word'), 'w')
    word_count = defaultdict(lambda: 0)
    for i, l in enumerate(open(os.path.join(DIR, 'source_train'), 'r')):
      for w in l.split(' +++$+++ ')[1].split():
        word_count[w] += 1
    
    word_count = sorted(word_count.items(), key=lambda d: d[1], reverse=True)
    cnt = 0
    for w in word_count:
      if cnt < VOCAB_SIZE:
        word_f.write(w[0]+'\n')
        cnt += 1
    word_f.close()

class MySentences(object):
  def __init__(self, filename, dfile):
    self.filename = filename
    self.dfile = dfile
 
  def __iter__(self):
    word = []
    for l in open(self.dfile):
      word.append(l.strip())

    for line in open(self.filename):
      sent = line.split(' +++$+++ ')[1].split()
      sent = [w if w in word else '__UNK__' for w in sent]
      sent = ['__BOS__'] + sent
      for _ in range(LEN + 2 - len(sent)):
        sent = sent + ['__EOS__']
      sent[-1] = '__EOS__'
      yield sent

fre_word()

sentences = MySentences(os.path.join(DIR, 'source_train'), os.path.join(DIR, 'word'))
model = gensim.models.Word2Vec(sentences, size=200, window=5, workers=7, iter=10)
model.save(os.path.join(DIR, 'word_vec'))

i = 0
word_id_dict = dict()
for word in model.wv.vocab:
  word_id_dict[word] = i
  i += 1
fp = open(os.path.join(DIR, 'dict'),'w')
json.dump(word_id_dict,fp, ensure_ascii=False)

