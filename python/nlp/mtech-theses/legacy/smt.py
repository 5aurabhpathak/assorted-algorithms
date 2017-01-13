#SMT:- Stsatical Machine Transaltion 
import sys
import codecs

def smt_word(str,words,loc):
	max=0;
	index=0;
	count={};
	for i in range(0,len(str)):
		str1=str[i];
		temp1=str1.split("=");
		count[temp1[1]]=0;
	
	for i in range(0,len(words)):
		if(i==loc):
			continue;
		fr_db = codecs.open('data/DB/db_ebmt.txt', encoding='utf-8',mode='r');
		for line in fr_db:
			temp2=line.split("=");
			if(find(words[i],temp2[0])==1 and find(words[loc],temp2[0])==1):
				for j in range(0,len(str)):
					str1=str[j];
					temp1=str1.split("=");
					if(find(temp1[1],temp2[1])==1):
						count[temp1[1]]+=1;
		
	#print count;
		
	for i in range(0,len(str)):
		str1=str[i];
		temp1=str1.split("=");
		if max<count[temp1[1]]:
			max=count[temp1[1]];
			index=i;
			
	return str[index];
		
def find(word,str):
	word_list=str.split(" ");
	for i in range(0,len(word_list)):
		if word==word_list[i]:
			return 1;
			
	return 0;
