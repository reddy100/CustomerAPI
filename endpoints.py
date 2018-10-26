import csv
import re
from Trie import Trie
regex = re.compile('[^a-zA-Z]')

class SimpleAPI():
    def __init__(self):
        self.titleTrie = Trie()
        self.categoryNameTrie = Trie()
        self.brandNameTrie = Trie()

        self.productDict={}
        self.productIdDict={}
        self.titleDict={}
        self.brandIdDict={}
        self.brandNameDict={}
        self.categoryIdDict={}
        self.categoryNameDict={}

        self.keywordFrequencyDict={}

    def _combinations(self, L, final,tmp=None):
        if tmp is None:
            tmp = []
        if L==[]:
            final.append(tmp)
        else:
            for i in L[0]:
                self._combinations(L[1:], final,tmp+[i])
        return final

    def _getListOfTypeCombinations(self, conditions):
        listOfTypes = []
        for condition in conditions:
            listOfTypes.append(self._combinations([[condition['type']], [value.lower() for value in condition['values']]], []))
        listOfTypeCombinations = self._combinations(listOfTypes, [])
        return listOfTypeCombinations

    def _addToDict(self, d, key, value):
        if key in d:
            d.get(key).append(value)
        else:
            d[key]=[value]

    def _addToFreqDict(self, keyList):
        for keys in keyList.split():
            keys = regex.sub(' ', keys).split()
            for key in keys:
                if key in self.keywordFrequencyDict:
                    self.keywordFrequencyDict[key] = self.keywordFrequencyDict[key] + 1
                else:
                    self.keywordFrequencyDict[key] = 1

    def initializeApi(self, fileName):
        with open(fileName,encoding='utf8') as in_file:
            for line in in_file:
                output = []
                columns = line.split("\t")
                for index, c in enumerate(columns):
                    c=c.lower()
                    output.append(c)
                    if index==1:
                        self._addToFreqDict(c)
                        self.titleTrie.insert(c)
                    elif index==3:
                        self.brandNameTrie.insert(c)
                    elif index==5:
                        self.categoryNameTrie.insert(c)
                        self.productIdDict[output[0]]=output[0]
                self._addToDict(self.titleDict, output[1], output[0])
                self._addToDict(self.brandIdDict, output[2], output[0])
                self._addToDict(self.brandNameDict, output[3], output[0])
                self._addToDict(self.categoryIdDict, output[4], output[0])
                self._addToDict(self.categoryNameDict, output[5][:-1], output[0])
                self.productDict[output[0]]=output

    def endpoint1(self, type, prefix):
        prefix=prefix.lower()
        if type=='title':
            return list(self.titleTrie.allWordsStartingWithPrefix(prefix))
        elif type=='category':
            return list(self.categoryNameTrie.allWordsStartingWithPrefix(prefix))
        elif type=='brand':
            return list(self.brandNameTrie.allWordsStartingWithPrefix(prefix))

    def endpoint2(self, conditions, pagination):
        responseHeadings = ['productId', 'title', 'brandId', 'brandName', 'categoryId', 'categoryName']
        fromPagination = pagination['from']
        sizePagination = pagination['size']
        resultingProductIds=[]
        listOfTypeCombinations = self._getListOfTypeCombinations(conditions)
        for typeCombination in listOfTypeCombinations:
            setList=[]
            for type in typeCombination:
                setList.append(eval('self.'+type[0]+'Dict.get(\''+type[1]+'\')'))
            resultingProductIdsByTypeCombination = set.intersection(*list(map(set, setList)))
            resultingProductIds+=resultingProductIdsByTypeCombination
        paginatedResultingProductIds = resultingProductIds[fromPagination:fromPagination+sizePagination]
        searchResults=[]
        for productId in paginatedResultingProductIds:
            searchResults.append(dict(zip(responseHeadings, self.productDict[productId])))
        return searchResults

    def endpoint3(self, keywords):
        searchResult = {}
        searchResult['keywordFrequencies']=[]
        for keyword in keywords:
            keywordFrequency = self.keywordFrequencyDict.get(keyword.lower(), 0)
            searchResult['keywordFrequencies']=searchResult['keywordFrequencies']+[[keyword, str(keywordFrequency)]]
        return searchResult

    def closeEndpoint(self):
        self.titleTrie = None
        self.categoryNameTrie = None
        self.brandNameTrie = None

        self.productDict={}
        self.productIdDict={}
        self.titleDict={}
        self.brandIdDict={}
        self.brandNameDict={}
        self.categoryIdDict={}
        self.categoryNameDict={}

        self.keywordFrequencyDict={}
