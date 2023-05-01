# Ages range from 19-24
f_speakers = ['CHL',
              'CLA',
              'GAB',
              'GIA',
              'JAD',
              'ELI',
              'CAR',
              'REB',
              'ELE',
              'ABI',
              'ELL',
              'JAS',
              'AVE',
              'HER',
              'LAR'
              ]
m_speakers = ['MIG',
              'TOM',
              'RIC',
              'LUK',
              'TIM',
              'CON',
              'EVN',
              'ABE',
              'MAT',
              'NAT',
              'ANT',
              ]

all_speakers = f_speakers + m_speakers
print(all_speakers)
all_speaker_genders = dict(zip(m_speakers, 'M'*len(m_speakers))) | dict(zip(f_speakers, 'F'*len(f_speakers)))
print(all_speaker_genders)


import os
import glob
import pandas as pd

all_dfs = []
current_directory = os.getcwd()
for filename in glob.glob(current_directory + '\\*.tsv'): # https://stackoverflow.com/questions/18262293/how-to-open-every-file-in-a-folder
    df = pd.read_csv(filename, sep="\t")
    all_dfs.append(df[['surface', 'speaker', 'langid']])
final_df = pd.concat(all_dfs)
final_df = final_df[final_df['speaker'].isin(all_speakers)]
final_df['speaker'] = final_df['speaker'].map(all_speaker_genders)
final_df = final_df[final_df['langid'].isin(['eng', 'spa'])]
final_df.rename(columns = {'surface':'word', 'speaker':'gender', 'langid':'language'}, inplace=True)
final_df['is_cs'] = (final_df['language'] != final_df['language'].shift(1)).astype(int)

# final_df.to_csv("spanish_words.csv")