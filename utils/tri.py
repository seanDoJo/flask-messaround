class TNode:
    def __init__(self):
        self.suffixes = []
        self.branches = {}

    def __repr__(self):
        return self.suffixes

    def __str__(self):
        return self.suffixes

class Tri:
    def __init__(self):
        self.root = TNode()

    def _subsequences(self, l):
        spl = l.split()
        sub = []
        for i in range(0, len(spl)):
            for j in range(i+1, len(spl)+1):
                sub.append(' '.join(spl[i:j]))
        return sub

    def insert(self, key):
        l = key.lower()
        words = self._subsequences(l)
        for w in words:
            self._insert(0, w, key, self.root)

    def _insert(self, i, l, key, node):
        c = l[i]
        if i == len(l)-1:
            if c not in node.branches:
                node.branches[c] = TNode()
            node.branches[c].suffixes.append(key)
            return True

        if c not in node.branches:
            node.branches[c] = TNode()

        return self._insert(i+1, l, key, node.branches[c])

    def lookup(self, key):
        l = key.lower()
        t = self.goto(l, self.root)
        if t is None:
            return []
        return self._lookup(t)

    def _lookup(self, node):
        if not len(node.branches):
            return node.suffixes

        poss = []
        for branch in node.branches:
            for p in self._lookup(node.branches[branch]):
                poss.append(p)
        return poss

    def goto(self, key, node):
        if not len(key):
            return node
        if key[0] not in node.branches:
            return None
        return self.goto(key[1:], node.branches[key[0]])
