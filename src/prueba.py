import os
import warnings
import seaborn as sns
#from tqdm import tqdm

warnings.filterwarnings('ignore')
sns.set()
for i in range(5):
    minner_comand = 'python '+'--'+'version'
    print(minner_comand)
    os.system(minner_comand)