# -*- coding:utf-8 -*- 
# __author__ = 'Zhong.zy'
'''

Naive Bayes Classifior for Senz+ Activity

'''
from __future__ import division
from numpy import *


class NaiveBayes(object):

    def __init__(self):
        self.sampleCount = 0
        self.modelDict= {} # keep P(feature_i|label_j) = .. , P(label_i) = ..
        self.labelSet = set([])

    def train(self,samples,labels): #samples and labels cannot contain '|'
        self.sampleCount = len(samples)
        #count label
        for label in labels:
            self.labelSet.add(label)
            if label in self.modelDict:
                self.modelDict[label] += 1
            else:
                self.modelDict[label] = 1
        #count feature|label
        for i,sample in enumerate(samples):
            for j,feature in enumerate(sample):
                feature_label = 'f'+str(j)+'='+feature+'|'+labels[i]
                if feature_label in self.modelDict:
                    self.modelDict[feature_label] += 1
                else:
                    self.modelDict[feature_label] = 1
        #calulate probability
        for key in self.modelDict:
            index = key.find('|')
            if index != -1:         #key is feature|label
                self.modelDict[key] /= self.modelDict[key[index+1:]]    #P(feature_i|label_j)

        for key in self.labelSet:   #key is label
                self.modelDict[key] /= self.sampleCount                 #P(label_i)

    def getLabelProbability(self,targetLabel,features):
        targetProbability = 0.0
        sumProbability = 0.0

        for label in self.labelSet:
            probability = 1.0
            for i,feature in enumerate(features):
                feature_label = 'f'+str(i)+'='+feature+'|'+label
                if feature_label in self.modelDict:
                    probability *= self.modelDict[feature_label]
                else: # if not exit in samples, make it 1/count(label)
                    probability *= 1.0/(self.modelDict[label]*self.sampleCount)              
            probability *= self.modelDict[label]
            #get sum
            sumProbability += probability

        for label in self.labelSet:
            probability = 1.0
            for i,feature in enumerate(features):
                feature_label = 'f'+str(i)+'='+feature+'|'+label
                if feature_label in self.modelDict:
                    probability *= self.modelDict[feature_label]
                else: # if not exit in samples, make it 1/count(label)
                    probability *= 1.0/(self.modelDict[label]*self.sampleCount)
            probability *= self.modelDict[label]
            #get sum
            sumProbability += probability
            #get target
            if label == targetLabel:
                targetProbability = probability
                    
        if not sumProbability:
            return 0

        return targetProbability/sumProbability        


#
#   Testing 
#
if __name__ == "__main__":
    file=open("users.txt",'r')
    features=[]         
    labels=[]           

    print 'Reading trainning data from users.txt ...\n'
    for line in file:  
        tempVec=line.strip().split(',')
        labels.append(tempVec[-1])
        features.append(tempVec[:-1])
    
    Bay=NaiveBayes()
    print 'Trainning ...\n'
    Bay.train(features,labels)

    print 'Testing with the trainning data(冏 Orz) ...\n'
    print 'RESULT:'
    for i,feature in enumerate(features):
        Probability = Bay.getLabelProbability(labels[i],feature)
        print labels[i]+':'+str(Probability)


   
        

            
                    
                
