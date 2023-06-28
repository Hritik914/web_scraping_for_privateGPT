import pandas as pd

column_names = ['Doctor', 'Speciality']

df = pd.read_csv('MayoClinic.csv', header=None)

df.columns = column_names
df['Hospital'] = 'MayoClinic'
df = df[df['Doctor'].notna()]
df['Speciality'].fillna('No Data', inplace=True)

df.to_csv('cleaned_MayoClinic.csv', index=False)