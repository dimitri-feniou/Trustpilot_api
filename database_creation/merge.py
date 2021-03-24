import os
import os.path
import glob
import pandas as pd

currdir = os.getcwd()
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

df = pd.concat([pd.read_csv(f) for f in all_filenames])

print(df.info())
df = df.drop(columns='Unnamed: 0')
df = df.reset_index(drop=True)

print(df.review)

df.to_csv('trustpilot_final.csv')