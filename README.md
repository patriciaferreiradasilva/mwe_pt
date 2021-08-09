# MWE_pt

MWE_pt is a tool to extract relevant multi word expressions in the form of nominal compounds (VERB+det+N) for corpora in portuguese language in the CONLL-U format.

## Installation

Use the package manager [requirements.txt](https://github.com/patriciaferreiradasilva/mwe_pt/blob/master/requirements.txt) to the required packages.

```bash
pip install -r requirements.txt
```

## Usage

```python
import foobar

# initialize MWEExtractor with target corpus
MWEExtractor(_CORPUS, n)

# ranks most common verbs in VERB+(det)+N structures along with their frequencies
MWEExtractor.common_verbs_vdetn()

# lists most common verbs
MWEExtractor.list_verbs(commonVerbsVDETN)

# ranks most common MWEs in VERB+(det)+N structures along with their frequencies
MWEExtractor.get_cm_list(verbs)

# returns table of statistical relavance of MWE
MWEExtractor.cm_prob_table(cmList, verbs)

# initialize MWESimilarytyIndexer with target corpus amd MWE lis
MWESimilarityIndexer(_CORPUS,cmTargetList)

#returns table with MWE compositionality analysis
MWESimilarityIndexer.cm_gc_table()
```

# Status
Lacks compositionality analysis of nominal compounds based on word2vec sentence vectorization.
Current vectorizer is TF-IDF based.
