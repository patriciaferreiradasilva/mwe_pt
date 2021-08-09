import pandas as pd
from io import open
from conllu import parse_incr
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import pairwise_distances

class MWESimilarityIndexer:
    
    def __init__(self,corpus_path,cm_list):
        self.corpus_path = corpus_path
        self.cm_list = cm_list
         
    def cm_gc_table(self):
        
        stop_words=['_','ADP','DET','PUNCT','SCONJ','CCONJ','PROPN','NUM','AUX','PRON','PART','SYM','INTJ']
        sm1=[]
        sm2=[]
        sm3=[]
        for target_cm in self.cm_list:
            p1=[]
            p2=[]
            data_file = open(self.corpus_path, "r", encoding="utf-8")
        
            for tokenlist in parse_incr(data_file):
                sentence=''
                lemma=''
                for token in tokenlist:
                    lemma=lemma+' '+token['lemma']
                    #Registro das sentenças para vetorização com exclusão de stop words
                    if token['upos'] not in stop_words:
                        sentence=sentence+' '+token['form']
                if target_cm in lemma:
                    p1.append(sentence)
                elif target_cm.split(' ')[-1] in lemma:
                    p2.append(sentence)
            vectorizer = CountVectorizer()
            
            p1p2_vectors = vectorizer.fit_transform(p1+p2)

            sim_matrix_p1p2 = 1-pairwise_distances(p1p2_vectors, metric="cosine")      

            sum=0
            n=0.001
            for i in range(len(p1)):
                for j in range(i+1,len(p1)):
                    sum+=sim_matrix_p1p2[i][j]
                    n+=1
            sm1.append(sum/n)
    
            sum=0
            n=0.001
            for i in range(len(p1),len(p1+p2)):
                for j in range(i+1,len(p1+p2)):
                    sum+=sim_matrix_p1p2[i][j]
                    n+=1
            sm2.append(sum/n)
        
            sum=0
            n=0.001
            for i in range(sim_matrix_p1p2.shape[0]):
                for j in range(i+1,sim_matrix_p1p2.shape[1]):
                    sum+=sim_matrix_p1p2[i][j]
                    n+=1
            sm3.append(sum/n)
        
        cm_gc_dict = {'CM': self.cm_list, 'SM1': sm1, 'SM2': sm2, 'SM3':sm3}
        cm_gc_table=pd.DataFrame(cm_gc_dict)
        return(cm_gc_table)