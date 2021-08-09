import pandas as pd
from io import open
from conllu import parse_incr

class MWEExtractor:
    
    def __init__(self, corpus_path, amount):
        self.corpus_path = corpus_path
        self.amount = amount

    def common_verbs_vdetn(self):
        data_file = open(self.corpus_path, "r", encoding="utf-8")
        punct=['.',',',';','?','!',':']
        verb_det_n_list={}
        for tokenlist in parse_incr(data_file):
            a=0
            while a+3<len(tokenlist):
                if (tokenlist[a]['upos']=='VERB' and 
                    tokenlist[a+1]['upos']=='DET' and 
                    tokenlist[a+2]['upos']=='NOUN' and 
                    (tokenlist[a+3]['upos']=='ADV' or 
                    (tokenlist[a+3]['form'] in punct) or
                    tokenlist[a+3]['upos']=='CCONJ')):
                    if tokenlist[a]['lemma'] in verb_det_n_list:
                        verb_det_n_list[tokenlist[a]['lemma']]+=1
                    else:
                        verb_det_n_list[tokenlist[a]['lemma']]=1
                if (tokenlist[a]['upos']=='VERB' and 
                    tokenlist[a+1]['upos']=='NOUN' and 
                    (tokenlist[a+2]['upos']=='ADV' or 
                    (tokenlist[a+2]['form'] in punct) 
                    or tokenlist[a+2]['upos']=='CCONJ')):
                    if tokenlist[a]['lemma'] in verb_det_n_list:
                        verb_det_n_list[tokenlist[a]['lemma']]+=1
                    else:
                        verb_det_n_list[tokenlist[a]['lemma']]=1
                a+=1

        common_verbs_vdetn={}
        print('Lista dos %s verbos mais comuns em estruturas V+(DET)+N' % self.amount)
        for (key,value) in sorted(verb_det_n_list.items(), key=lambda x: x[1], reverse=True)[:self.amount]:
            common_verbs_vdetn[key]=value
            print(key,value)
                 
        return common_verbs_vdetn
    
    def list_verbs(self,commonVerbsVDETN):
        verbs=[]
        for (key,_) in sorted(commonVerbsVDETN.items(), key=lambda x: x[1], reverse=True):
            verbs.append(key)
        return verbs 

    def get_cm_list(self, verbs):
        data_file = open(self.corpus_path, "r", encoding="utf-8")
        cm_list={}
        print('Recuperando lista com as Combinações Multipalavras para a lista de verbos:\n')
        print(verbs)
        for verb in verbs:
            cm_list[verb]={}
           
        for tokenlist in parse_incr(data_file):
            a=0
            while a+2<len(tokenlist)+1:
                for verb in verbs:
                    if tokenlist[a]['lemma']==verb and tokenlist[a]['upos']=='VERB':
                        if tokenlist[a+1]['upos']=='DET' and tokenlist[a+2]['upos']=='NOUN':
                            verb_det_n=tokenlist[a]['lemma']+' '+tokenlist[a+2]['lemma']
                        elif tokenlist[a+1]['upos']=='NOUN':
                            verb_det_n=tokenlist[a]['lemma']+' '+tokenlist[a+1]['lemma']
                            
                        if verb_det_n in cm_list[verb]:
                            cm_list[verb][verb_det_n]+=1
                        else:
                            print(verb_det_n)
                            cm_list[verb][verb_det_n]=1
                a+=1
        return(cm_list)

    def create_bag_of_words(self):
        bag_of_words={}
        
        #Removi nomes próprios e números em função do header com o nome do artigo
        pos_search=['VERB','ADJ','NOUN','ADV','X']
        data_file = open(self.corpus_path, "r", encoding="utf-8")
        for tokenlist in parse_incr(data_file):
            for token in tokenlist:
                if token['upos']in pos_search:
                    if token['lemma'] in bag_of_words:
                        bag_of_words[token['lemma']]+=1
                    else:
                        bag_of_words[token['lemma']]=1
        return(bag_of_words)

    def cm_prob_table(self,cm_list, verbs):
        bag_of_words = self.create_bag_of_words()
        colloc=[]
        freq=[]
        pw1w2=[]
        pw1nw2=[]
        for verb in verbs:
            for cm in cm_list[verb]:
                colloc.append(cm)
                freq.append(cm_list[verb][cm])
                prob_indep=((bag_of_words[cm.split(' ')[-1]]-cm_list[verb][cm])/
                            (sum(bag_of_words.values())-sum(cm_list[cm.split(' ')[0]].values())))
                pw1nw2.append(prob_indep)
                prob_dep=cm_list[verb][cm]/sum(cm_list[cm.split(' ')[0]].values())
                pw1w2.append(prob_dep)
        
        cm_prob_dict = {'CM': colloc, 'Freq': freq, 'Pw1-w2': pw1nw2, 'Pw1w2':pw1w2}
        cm_prob_table=pd.DataFrame(cm_prob_dict)
        cm_prob_table['Delta (%)']=(cm_prob_table['Pw1w2']-cm_prob_table['Pw1-w2'])*100/(cm_prob_table['Pw1-w2']+0.0001)
        
        return(cm_prob_table)
