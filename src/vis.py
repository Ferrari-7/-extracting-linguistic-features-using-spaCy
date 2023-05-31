import os
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns

# Loading the grammatical class data
def load_data_class():
    # listing all the tables made from the "feature_extract.py" script
    tables = os.listdir(os.path.join("out"))

    dataframes = []
    for table in tables: 
        path = os.path.join("out", table)
        df = pd.read_csv(path) # reading current data frame in loop
        
        # going over the columns with the RelFreq values and finding the mean value
        noun_mean = df.loc[:, "RelFreq NOUN"].mean()
        verb_mean = df.loc[:, "RelFreq VERB"].mean() 
        adj_mean = df.loc[:, "RelFreq ADJ"].mean()
        adv_mean = df.loc[:, "RelFreq ADV"].mean()

        # getting the name of the essay by removing the file extension (a1.csv --> a1) 
        essay = os.path.splitext(table)[0]
        
        # making a dict for the current table in loop with the information extracted above
        new_data = {"essay" : essay, "NOUN" : noun_mean, "VERB" : verb_mean, "ADJ" : adj_mean, "ADV": adv_mean}
        # appending dict to list above
        dataframes.append(new_data)

    # making a data frame from list of dicts
    df = pd.DataFrame.from_records(dataframes)
    df = df.round(2) # rounding of decimals

    return df

# Make visualization showing mean RelFreq of the three grammatical classes
def make_vis_class(df):

    # defining order for x-axis in plot
    order = ["a1", "a2", "a3", "a4", "a5", "b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8", "c1"]

    # re-aranging data to make visualization
    df = df.melt("essay", var_name="category", value_name="mean_RelFreq")

    # making seaborn categorical plot
    sns.catplot(data = df, 
            x="essay", 
            y="mean_RelFreq", 
            hue='category', # making points for each category
            kind='point',
            order=order)
    
    # saving plot
    plt.savefig(os.path.join("vis", "vis_class.png"))

# Doing the same but for uniqie PER, LOC AND ORGS
def load_data_NER():
    tables = os.listdir(os.path.join("out"))

    dataframes = []
    for table in tables: 
        path = os.path.join("out", table)
        df = pd.read_csv(path)
        
        PER_mean = df.loc[:, "Unique PER"].mean()
        LOC_mean = df.loc[:, "Unique LOC"].mean() 
        ORG_mean = df.loc[:, "Unique ORG"].mean()

        essay = os.path.splitext(table)[0]
        
        new_data = {"essay" : essay, "PER" : PER_mean, "LOC" : LOC_mean, "ORG" : ORG_mean}
        dataframes.append(new_data)

    df2 = pd.DataFrame.from_records(dataframes)
    df2 = df2.round(2)

    return df2

def make_vis_NER(df2):
    # clear plot
    plt.clf()

    # making order for x-axis in plot
    order = ["a1", "a2", "a3", "a4", "a5", "b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8", "c1"]

    # re-aranging data to make visualization
    df2 = df2.melt("essay", var_name="category", value_name="NER_unique_occurences")

    # making seaborn categorical plot
    sns.catplot(data = df2, 
            x="essay", 
            y="NER_unique_occurences", 
            hue='category', 
            kind='point',
            palette="Set2",
            order=order)
    
    # saving plot
    plt.savefig(os.path.join("vis", "vis_NER.png"))


def main():
    df = load_data_class()
    make_vis_class(df)
    df2 = load_data_NER()
    make_vis_NER(df2)

if __name__=="__main__":
    main()

