# -*- coding: utf-8 -*-
import os
import gensim.models.word2vec as word2vec
import pkg_resources
from sklearn.externals import joblib

class NameSex:
	def __init__(self, model1 = 'freq_log', model2 = 'w2v_knn', percentage1 = 0.75, percentage2 = 0.25):
		pkg_resources.resource_filename('namesex', './models') 
		self.model1 = model1
		self.model2 = model2
		self.percentage1 = percentage1
		self.percentage2 = percentage2
		self.basevec = []
		self.w2v = word2vec.Word2Vec.load('./namesex/models/namesex.w2v')
		tmp = open('./namesex/models/basevec.txt', 'r')
		for line in tmp:
			for word in line:
				self.basevec.append(word)

	def uni_model(self, namelist, model = None, prob = True):
		if model == None:
			model = self.model1
		mod = joblib.load('./namesex/models/'+model+'.pkl')
		veclist = []
		if model=='freq_log' or model=='freq_knn':
			for name in namelist:
				nlen = len(name)
				vec = [0]*len(self.basevec)
				if nlen < 3:
					char1 = name[nlen-1]
					if self.basevec.count(char1) != 0:
						vec[self.basevec.index(char1)]+=1
				else:
					char1 = name[nlen-1]
					char2 = name[nlen-2]
					if self.basevec.count(char1) != 0:
						vec[self.basevec.index(char1)]+=1
					if self.basevec.count(char2) != 0:
						vec[self.basevec.index(char2)]+=1
				veclist.append(vec)
		elif model=='w2v_log' or model=='w2v_knn':
			for name in namelist:
				nlen = len(name)
				vec = [0]*len(self.basevec)
				if nlen < 3:
					try:
						x = self.w2v[name[nlen-1]]
						veclist.append(x)
					except KeyError:
						print("bad")
				else:
					try:
						x = self.w2v[name[nlen-2]]+self.w2v[name[nlen-1]]
						veclist.append(x)
					except KeyError:
						print("bad word")
		if prob == True:
			return mod.predict_proba(veclist)
		else:
			return mod.predict(veclist)

 
	def predict_prob(self, namelist):
		return self.percentage1*self.uni_model(namelist, self.model1) + self.percentage2*self.uni_model(namelist, self.model2)

	def predict(self, namelist):
		return self.percentage1*self.uni_model(namelist, self.model1, False) + self.percentage2*self.uni_model(namelist, self.model2, False)