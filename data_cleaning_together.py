import os
import glob
import epitran
import eng_to_ipa as p
import re

def is_cs(str):
   if re.search("[\u4e00-\u9FFF]", str) and re.search('[a-zA-Z]+', str): # https://medium.com/the-artificial-impostor/detecting-chinese-characters-in-unicode-strings-4ac839ba313a
      return True
   return False 

current_directory = os.getcwd()

unwanted_sounds = set()
parens = re.compile("\(.*?\)")
brackets = re.compile("\[.*?\]")
tags = re.compile("#.*?#")

def clean_utterance(utterance):
   utterance = utterance.replace("<unk>", '')
   utterance = re.sub("\(.*?\)", '', utterance)
   utterance = re.sub("\[.*?\]", '', utterance)
   utterance = re.sub("\［.*?\］", '', utterance)
   utterance = re.sub("【.*?】", '', utterance)
   utterance = re.sub("\#.*?\#", '', utterance)  
   utterance = re.sub("[^ a-zA-Z\u4e00-\u9FFF]", '', utterance) 
   #utterance = re.sub('\~|\,|\.|!|\?|\*|\\|\[|\]|\(|\)|\@|#|【|】|［|］|{|}', '', utterance) 
   return utterance 

all_utterances = []
for filename in glob.glob(current_directory + '\\phaseI\\*.txt'): # https://stackoverflow.com/questions/18262293/how-to-open-every-file-in-a-folder
   with open(os.path.join(current_directory + "\\phaseI\\", filename), 'r', encoding="utf8") as f:
      lines = f.readlines()
      for line in lines:
         utterance = line.strip().split("\t")[-1] 
         utterance = clean_utterance(utterance)
         all_utterances.append(utterance)

#chars_to_remove = ['~', ',', '.', '!', '?', '*', '\\', '[', ']', '(', ')', '@']
for filename in glob.glob(current_directory + '\\phaseII\\*.txt'): # https://stackoverflow.com/questions/18262293/how-to-open-every-file-in-a-folder
   with open(os.path.join(current_directory + "\\phaseII\\", filename), 'r', encoding="utf8") as f:
      lines = f.readlines()
      for line in lines:
         line = line.strip().split("\t")
         utterance = line[-1]
         utterance = clean_utterance(utterance) 
         all_utterances.append(utterance)

spaced_sentences = []
for sentence in all_utterances:
   sentence = re.sub("[\u4e00-\u9FFF]", lambda ele: " " + ele[0] + " ", sentence)
   sentence = re.sub(" +", " ", sentence)
   sentence = sentence.strip()
   spaced_sentences.append(sentence)


final_path = current_directory + "\\cleaned_data\\all_utterances.txt"
if os.path.exists(final_path):
    # delete the file
    os.remove(final_path)
with open(final_path, 'w', encoding="utf8") as fp:
   for item in spaced_sentences:
      # write each item on a new line
      fp.write("%s\n" % item)

epi = epitran.Epitran('cmn-Hans', cedict_file='cedict_ts.txt')

all_words = []
all_ipas = []
# languages = []
# first_ipa = []
# last_ipa = []
# first_syllable = []
# last_syllable = []
for line in spaced_sentences:
  line = line.strip()
  if len(line) > 0:
    line = re.sub(" +", " ", line)
    convert_eng = p.convert(line)
    convert_eng = convert_eng.replace('*', '')
    converted_eng_zh = epi.transliterate(convert_eng)
    ipas = converted_eng_zh.split()
    all_ipas += ipas
    line = line.split()
    all_words += line

   # for word in line:
   #    if re.search("[\u4e00-\u9FFF]", word): # cn
   #       languages.append(0)
   #       zh_ipa = epi.transliterate(word)
   #       all_ipas.append(zh_ipa)
   #       first_ipa.append(zh_ipa[0])
   #       last_ipa.append(zh_ipa[-1])
   #       first_syllable.append(zh_ipa)
   #       last_syllable.append(zh_ipa)
   #       all_words.append(word)
   #    else: # en
   #       en_ipa = p.convert(word)
   #       if len(en_ipa) > 0:
   #          if "*" in en_ipa:
   #             languages.append(2) # cannot be transliterated
   #             all_ipas.append("*")
   #             first_ipa.append("*")
   #             last_ipa.append("*")
   #             first_syllable.append("*")
   #             last_syllable.append("*")
   #             all_words.append(word)
   #          else:
   #             languages.append(1)
   #             all_ipas.append(en_ipa)
   #             if en_ipa[0] == 'ˈ' or en_ipa[0] == 'ˌ':
   #                en_ipa = en_ipa[1:]
   #             first_ipa.append(en_ipa[0])
   #             last_ipa.append(en_ipa[-1])
   #             syllables = re.split('ˈ|ˌ', en_ipa)
   #             first_syllable.append(syllables[0])
   #             last_syllable.append(syllables[-1])
   #             all_words.append(word)

final_path = current_directory + "\\cleaned_data\\transliterations.txt"
if os.path.exists(final_path):
    # delete the file
    os.remove(final_path)
with open(final_path, 'w', encoding="utf8") as fp:
   for item in all_ipas:
      # write each item on a new line
      fp.write("%s\n" % item)

final_path = current_directory + "\\cleaned_data\\all_words.txt"
if os.path.exists(final_path):
    # delete the file
    os.remove(final_path)
with open(final_path, 'w', encoding="utf8") as fp:
   for item in all_words:
      # write each item on a new line
      fp.write("%s\n" % item)

# final_path = current_directory + "\\cleaned_data\\languages.txt"
# if os.path.exists(final_path):
#     # delete the file
#     os.remove(final_path)
# with open(final_path, 'w', encoding="utf8") as fp:
#    for item in languages:
#       # write each item on a new line
#       fp.write("%s\n" % item)
      
# final_path = current_directory + "\\cleaned_data\\first_ipas.txt"
# if os.path.exists(final_path):
#     # delete the file
#     os.remove(final_path)
# with open(final_path, 'w', encoding="utf8") as fp:
#    for item in first_ipa:
#       # write each item on a new line
#       fp.write("%s\n" % item)

# final_path = current_directory + "\\cleaned_data\\last_ipas.txt"
# if os.path.exists(final_path):
#     # delete the file
#     os.remove(final_path)
# with open(final_path, 'w', encoding="utf8") as fp:
#    for item in last_ipa:
#       # write each item on a new line
#       fp.write("%s\n" % item)

# final_path = current_directory + "\\cleaned_data\\first_syllables.txt"
# if os.path.exists(final_path):
#     # delete the file
#     os.remove(final_path)
# with open(final_path, 'w', encoding="utf8") as fp:
#    for item in first_syllable:
#       # write each item on a new line
#       fp.write("%s\n" % item)

# final_path = current_directory + "\\cleaned_data\\last_syllables.txt"
# if os.path.exists(final_path):
#     # delete the file
#     os.remove(final_path)
# with open(final_path, 'w', encoding="utf8") as fp:
#    for item in last_syllable:
#       # write each item on a new line
#       fp.write("%s\n" % item)
