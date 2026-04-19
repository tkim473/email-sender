import pandas as pd
from config import *
import numpy as np

def get_verses():


    #read into dataframe
    df = pd.read_csv(gs_url)

    verse_list = df[df.columns[1]]
    verse_list = list(filter(lambda x: x == x, verse_list))
    print(verse_list)

    #display verse
    display_list = df[df.columns[2]]
    disp_verse = display_list[len(display_list)-1]
    print(disp_verse)
    return verse_list, disp_verse
