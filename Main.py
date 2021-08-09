import wget

from MWEExtractor import MWEExtractor
from MWESimilarityIndexer import MWESimilarityIndexer


class Main:
    
    def __init__(self):
        self._CORPUS = 'process.conllu'
    
    def main(self):
        
        # firt user input
        sn = input("Você quer fazer downlaod de um corpus novo (S/N) ?  ")
        if sn == 'S' :
            url = input("Por favor informar a URL do corpus no formato conlu ?  ")
            wget.download(url, 'process.conllu')

        # second user input
        n = input("Para quantos verbos você quer avaliar as combinações multi palavras ? (min. 1 max. 30)")
        n = int(n) 
        if n < 1 or n > 30:
            print('valor de N invalido assumindo defult de 3')
            n = 2
        
        mweExtractor = MWEExtractor(self._CORPUS,n)
        
        commonVerbsVDETN = mweExtractor.common_verbs_vdetn()
        
        verbs = mweExtractor.list_verbs(commonVerbsVDETN)
                    
        cmList = mweExtractor.get_cm_list(verbs)
        
        cmProbTable = mweExtractor.cm_prob_table(cmList, verbs)
        
        n = input("Quantas vezes mais provável deve ser aparecimento do substantivo na CM? ")
        n = int(n) 
        if n < 1:
            print('valor de N invalido assumindo defult de 5')
            n = 5
        prob=(n-1)*100
        
        freq = input("Qual o mínimo necessário de ocorrências da CM (mínimo: 2)?")
        freq = int(n) 
        if freq < 2:
            print('valor de N invalido. Assumindo defult de 2')
            freq = 2
        freq = freq-1
        
        # TODO externalize to util function
        cmFiltered=cmProbTable[(cmProbTable['Delta (%)']>prob) & (cmProbTable['Freq']>freq)]
        cmTargetList = cmFiltered['CM'].tolist()
        for cm in cmTargetList:
            print(cm)
        
        mweIndexer = MWESimilarityIndexer(self._CORPUS,cmTargetList)
        
        cmSimilarityTable=mweIndexer.cm_gc_table()
        
        print(cmSimilarityTable)    
    
if __name__ == "__main__":
    m = Main()
    m.main()