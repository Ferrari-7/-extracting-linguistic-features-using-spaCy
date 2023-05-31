# create a spacy NLP class
import spacy
nlp = spacy.load("en_core_web_md")
# Importing Pandas to create tables
import pandas as pd
# Importing re for the preprocessing step. I will use regex to remove the metadata between the pointed brackets "<>". 
import re
import os

def peform_feature_extraction():
    # Assigning the list of folders in "USEcorpus" to the variable that I can run my loop through.
    corpus = os.listdir(os.path.join("in", "USEcorpus"))
    for folder in corpus :
        # Assigning the list of files in each folder to a variable that I can run my loop through.
        essays = os.listdir(os.path.join("in", "USEcorpus", folder))

        # Making an empty list where the results will be appended to. This list will be used to make the data frame at the end of the each loop.
        results = []
        # Looping through each essay:
        for essay in essays :
            filename = os.path.join("in", "USEcorpus", folder, essay)
            
            # reading the file using "latin-1" encoding
            with open(filename, "r", encoding="latin-1") as file:
                text = file.read()
            
            # Preprocessing process: I'm removing metadata that occurs between pointed bracket "<>" using regex.
            # the regex catches any character (except <) inclosed by pointed brackets, replaces it with nothing and thereby removes it.
            text = re.sub("<[^<]*>", "", text)

            # Creating a doc object. The text is now read as a sequence of token objects.
            doc = nlp(text)

            # Extracting information for each essay in each folder
            # RELATIVE FREQUENCY NOUNS
            # I'm making a loop that runs through each token in the doc object, registers if the token is a noun and if so adds 1 to counter.
            noun_count = 0
            for token in doc :
                if token.pos_ == "NOUN" :
                    noun_count += 1
            # Next, I calculate the relative frequency by deviding the number of nouns with the amount of tokens in the text and multiplying by 10.000.
            relative_freq_noun = (noun_count/len(doc)) * 10000 
            # I then do the same for verbs, adjectives and adverbs respectively.

            # VERBS
            verb_count = 0
            for token in doc :
                if token.pos_ == "VERB" :
                    verb_count += 1
            relative_freq_verb = (verb_count/len(doc)) * 10000

            # ADJECTIVES
            adj_count = 0
            for token in doc :
                if token.pos_ == "ADJ" :
                    adj_count += 1
            relative_freq_adj = (adj_count/len(doc)) * 10000

            # ADVERBS 
            adv_count = 0
            for token in doc :
                if token.pos_ == "ADV" :
                    adv_count += 1
            relative_freq_adv = (adv_count/len(doc)) * 10000

            # UNIQUE PERSONS
            # I'm making a loop which runs through each entity in the text, checks if the label of the entity is person and if so adds the entity to a list.
            # I then use the set() function to get unique entities. The total will be counted using the length function on the set.
            list_per = []
            for ent in doc.ents :
                if ent.label_ == "PERSON" :
                    list_per.append(ent)
            unique_per_total = len(set(list_per))
            # I repeat the steps for locations and organisations.

            # UNIQUE LOCATIONS
            list_loc = []
            for ent in doc.ents :
                if ent.label_ == "LOC" :
                    list_loc.append(ent)
            unique_loc_total = len(set(list_loc))

            # UNIQUE ORGANISATIONs
            list_org = []
            for ent in doc.ents :
                if ent.label_ == "ORG" :
                    list_org.append(ent)
            unique_org_total = len(set(list_org))

            # Appending filenames and results to empty list called results.
            results.append((((((((essay, relative_freq_noun, relative_freq_verb, relative_freq_adj, relative_freq_adv, unique_per_total, unique_loc_total, unique_org_total))))))))
        
        # MAKING DATA FRAME USING PANDAS
        table = pd.DataFrame(results,
                            columns=["Filename", "RelFreq NOUN", "RelFreq VERB", "RelFreq ADJ", "RelFreq ADV", "Unique PER", "Unique LOC", "Unique ORG"])
        # Rounding decimals in the dataframe
        table = table.round(2)
        # SAVING TABLE as CVS in the folder called "out". 
        # Since I'm still in the loop, I'm giving the table the same name as the respective folder and adding ".csv".
        outpath = os.path.join("out", folder + ".csv")
        table.to_csv(outpath)

def main():
    peform_feature_extraction()

if __name__=="__main__":
    main()
