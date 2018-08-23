# -*- coding: utf8 -*-

from collections import deque


class Vertex(object):
    __slots__ = ['name', 'links', 'color', 'predict']

    def __init__(self, name):
        self.name = name
        self.links = dict()
        self.color = 'White'
        self.predict = None

    def add_neighbor(self, name, weight=0):
        self.links[name] = weight

    def get_name(self):
        return self.name

    def get_weight(self, name):
        return self.links[name]

    def get_links(self):
        return self.links.keys()

    def __str__(self):
        return '{!s} links: {!s}'.format(self.name, [x.name for x in self.links])


class Graph(object):

    def __init__(self):
        self.vertex_list = dict()
        self.count_vertex = 0

    def add_vertex(self, name):
        self.count_vertex += 1
        self.vertex_list[name] = Vertex(name)

    def add_edge(self, from_vertex, to_vertex, cost=0):
        if to_vertex not in self.vertex_list:
            self.add_vertex(to_vertex)
        if from_vertex not in self.vertex_list:
            self.add_vertex(from_vertex)
        self.vertex_list[from_vertex].add_neighbor(self.vertex_list[to_vertex], cost)

    def get_vertex(self, name):
        if name in self.vertex_list:
            return self.vertex_list[name]
        return None

    def get_links(self):
        return self.vertex_list.items()

    def __iter__(self):
        return iter(self.vertex_list.values())

    @staticmethod
    def dfs(start_vertex):
        start_vertex.color = 'Black'
        stack = deque()
        stack.append(start_vertex)
        while stack:
            vertex = stack.pop()
            for each in vertex.get_links():
                if each.color == 'White':
                    each.color = 'Black'
                    each.predict = vertex
                    stack.append(each)

    @staticmethod
    def bfs(start_vertex):
        start_vertex.color = 'Black'
        queue = deque()
        queue.append(start_vertex)
        while queue:
            vertex = queue.popleft()
            for each in vertex.get_links():
                if each.color == 'White':
                    each.color = 'Black'
                    each.predict = vertex
                    queue.append(each)

    def is_connected(self):
        self.dfs(self.get_vertex(list(self.vertex_list.keys())[0]))
        for vertex in self.vertex_list.keys():
            if self.vertex_list[vertex].color != 'Black':
                return False
        return True


def build_word_graph(file_word):
    d = dict()
    g = Graph()

    with open(file_word, 'r', encoding='utf-8') as wfile:
        for line in wfile:
            word = line[:-1]
            for i in range(len(word)):
                bucket = word[:i] + '_' + word[i + 1:]
                if bucket in d:
                    d[bucket].append(word)
                else:
                    d[bucket] = [word]

        for bucket in d.keys():
            for word1 in d[bucket]:
                for word2 in d[bucket]:
                    if word1 != word2:
                        g.add_edge(word1, word2)

    return g


def travel(vertex):
    v = vertex
    while v.predict:
        print(v.name, end=' -> ')
        v = v.predict
    print(v.name)


if __name__ == '__main__':
    g = build_word_graph('word_file.txt')
    gg = build_word_graph('word_file.txt')
    g.bfs(g.get_vertex('fool'))
    gg.dfs(gg.get_vertex('fool'))
    travel(g.get_vertex('sage'))
    travel(gg.get_vertex('sage'))
    print(gg.is_connected())
    print(g.is_connected())
