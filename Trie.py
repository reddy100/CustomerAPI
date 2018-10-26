class TrieNode:
    def __init__(self):
        self.end = False
        self.children = {}

    def allWords(self, prefix):
        if self.end:
            yield prefix

        for letter, child in self.children.items():
            yield from child.allWords(prefix + letter)

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        curr = self.root
        for letter in word:
            node = curr.children.get(letter)
            if not node:
                node = TrieNode()
                curr.children[letter] = node
            curr = node
        curr.end = True

    def search(self, word):
        curr = self.root
        for letter in word:
            node = curr.children.get(letter)
            if not node:
                return False
            curr = node
        return curr.end

    def allWordsStartingWithPrefix(self, prefix):
        cur = self.root
        for c in prefix:
            cur = cur.children.get(c)
            if cur is None:
                return  # No words with given prefix

        yield from cur.allWords(prefix)

if __name__ == '__main__':
    keys = ["th/e.", "a", "therfgl;'e", "answer", "any",
            "by", "their", "bye"]
    t=Trie()
    for i in keys:
        t.insert(i)
    print(list(t.allWordsStartingWithPrefix("th")))