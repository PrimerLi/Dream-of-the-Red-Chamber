# Dream-of-the-Red-Chamber
# 红楼梦人物关系图
Network representation of character relationhips in Dream of the Red Chamber by Cao Xueqin

This project aims to analyze the relationships between characters in Dream of the Red Chamber. 

The corpus is from wiki source. See this link: https://zh.m.wikisource.org/zh/%E8%84%82%E7%A1%AF%E9%BD%8B%E9%87%8D%E8%A9%95%E7%9F%B3%E9%A0%AD%E8%A8%98

Run the file parser.py to generate scenes.txt, hyperedges.csv and edges.csv. 

The file scenes.txt summarizes all the character appearance times in each scene in the book. 

The file hyperedges.csv contains a hypergraph representation of the book. Each line of the file represents a hyperedge in the hypergraph. This file is used for performing hypergraph analysis. 

The file edges.csv is obtained from hyperedges.csv by running the file expand.py. Edges.csv contains a graph representation of the book. 
