import unittest

from pandas.core.frame import DataFrame

from MWEExtractor import MWEExtractor
from MWESimilarityIndexer import MWESimilarityIndexer

_CORPUS = 'process.conllu'
mweExtractor = MWEExtractor(_CORPUS,3);

class Test(unittest.TestCase):

    def test_common_verbs_vdetn_result_equals(self):
        result = {'ter': 4, 'receber': 2, 'assumir': 2}
        commonVerbsVDETN = mweExtractor.common_verbs_vdetn()
        print(commonVerbsVDETN)
        self.assertEqual(commonVerbsVDETN,result)
    
    def test_list_verbs_equals(self):
        result = ['ter', 'receber', 'assumir']
        commonVerbsVDETN = mweExtractor.common_verbs_vdetn()
        verbs = mweExtractor.list_verbs(commonVerbsVDETN)
        print(verbs)
        self.assertEqual(verbs,result)
        
    def test_cmList_equals(self):
        result = {'ter': {'ter curso': 1, 'ter recurso': 3, 'ter possibilidade': 1, 'ter filho': 1, 'ter direito': 5, 'ter paridade': 1, 'ter correção': 
1, 'ter aumento': 2, 'ter esperança': 1, 'ter canção': 1, 'ter música': 3, 'assumir poder': 1, 'ter efeito': 1, 'ter obrigação': 2, 'ter repercussão': 3, 'ter marca': 1, 'ter emprego': 1, 'ter problema': 5, 'ter função': 2, 'ter pele': 5, 'ter segurança': 1, 'ter químico': 2, 'ter preço': 1, 'ter início': 1}, 'receber': {'ter recurso': 1, 'receber benefício': 1, 'ter aumento': 1, 'ter direito': 2, 'assumir poder': 1, 'ter emprego': 1, 'ter pele': 2, 'receber remédio': 1}, 'assumir': {'assumir poder': 1, 'assumir cargo': 1}}
        commonVerbsVDETN = mweExtractor.common_verbs_vdetn()
        verbs = mweExtractor.list_verbs(commonVerbsVDETN)
        cmList = mweExtractor.get_cm_list(verbs)
        print(cmList)
        self.assertDictEqual(cmList,result)    
        
    def test_cm_prob_table_is_instance(self):
        commonVerbsVDETN = mweExtractor.common_verbs_vdetn()
        verbs = mweExtractor.list_verbs(commonVerbsVDETN)
        cmList = mweExtractor.get_cm_list(verbs)
        cmProbTable = mweExtractor.cm_prob_table(cmList, verbs)
        print(cmProbTable)
        self.assertIsInstance(cmProbTable,DataFrame)
        
    def test_cm_gc_table_is_instance(self):
        commonVerbsVDETN = mweExtractor.common_verbs_vdetn()
        verbs = mweExtractor.list_verbs(commonVerbsVDETN)
        cmList = mweExtractor.get_cm_list(verbs)
        cmProbTable = mweExtractor.cm_prob_table(cmList, verbs)
        cmFiltered=cmProbTable[(cmProbTable['Delta (%)']>400) & (cmProbTable['Freq']>2)]
        cmTargetList = cmFiltered['CM'].tolist()
        mweIndexer = MWESimilarityIndexer(_CORPUS,cmTargetList)
        cmSimilarityTable=mweIndexer.cm_gc_table()
        print(cmSimilarityTable)
        self.assertIsInstance(cmProbTable,DataFrame)                    
        
if __name__ == '__main__':
    unittest.main()