
Insructions to Run:

1. Run pip install -r requirements.txt

2. Change dataFileName in app.py to point to .tsv file in local

3. Run python app.py

4. The Endpoints take json data


Specs:

1. As I cannot use a database I have made the decision to preload all the data into the datastructures that I found to be most useful for this exercise. This has some memory overhead and is a little slow during startup. But it provides for fast and efficient user querying thereafter.

2. I create all my datastructures while parsing the .tsv file. 

Endpoint1:
1. I used a Trie Data structure for this part. This allows me to store each letter of every word as TrieNode in order. Searching is O(m) where m is the maximum string length and inserting is O(key_length)


2.  Memory requirements are O(alphabet_size * length_of_string* N) where N is the number of keys. This might be a little too much, but that is the tradeoff for fast querying by user.

Endpoint2:
1. While parsing .tsv file i create dictionaries for each column and store the key as that column value and the value as the ProductID(as this is unique for products). This then allows me to cross reference and filter out products.

2. Creating and searching a dictionary is constant time.

Endpoint 3:
1. Once again while initially parsing through the .tsv file I make a dictionary and store all the frequencies of each word in the title.

2. I have chosen to ignore punctuation when finding frequency of keywords. I use regex to ignore punctuation


Memory usage for the dictionaries is still constant

I wasted too much time on finding the various combinations of types for Endpoint2

Assumptions:

1. Names of categories will be as listed below:

['productId', 'title', 'brandId', 'brandName', 'categoryId', 'categoryName']

And user queries will not deviate from them

2. Pagination will be valid

3. Requests will be valid



