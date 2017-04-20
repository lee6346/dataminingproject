%matplotlib inline
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
import matplotlib as mpl
import matplotlib.pyplot as plt


incidents = plt.subplot2grid((4,4), (0, 0), rowspan=3, colspan=4)
incidents.plot(df.index , df.nkill)
plt.title('Terrorist incidents')

pop = plt.subplot2grid((4,4), (3,0), rowspan=1, colspan=4)
pop.bar(df.index, df['Volume'])
plt.title('Population')

plt.gcf().set_size_inches(15,8)