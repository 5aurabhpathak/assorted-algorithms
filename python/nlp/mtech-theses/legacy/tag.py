# coding=utf-8
import sys
import codecs
import name
import search
import os
import Translation as trans
import smt

def sub_tag(tag_list):
	if "ANIMT" in tag_list or "PRON" in tag_list :
		return "<ANIMT>";
	if "VERB," in tag_list:
		return "<VERB>";
	if "ADJ," in tag_list:
		return "<ADJ>";
	if "ADV," in tag_list:
		return "<ADV>";
	if "N," in tag_list:
		return "<NOUN>";	

def tag1(str_list,eb,dir):
	tag_list = list();
	word_list= list();
	result=list();
	for i in range(0,len(str_list)):
		tag_list.append("<nan>");
		word_list.append("<nan>");
		
	count=0;
	while count < len(str_list):
		flag=0;
		tag_word="";
		#Find in Example DB 
		try:
			ans=eb[str_list[count]];
		except KeyError, e:
			ans=0;
		
		if(ans!=0):
			tag_list[count]="<Example>";
			word_list[count]=ans;
			count=count+1;
			continue;
		
		#find in Dir
		try:
			ans=dir[str_list[count]][0];
			if len(dir[str_list[count]])>1:		#Using SMT
				ans=smt.smt_word(dir[str_list[count]],str_list,count);
				
		except KeyError, e:
			ans=0;
			
		if(ans==0):
			tag_list[count]="<Name>";
			word_list[count]=trans.cov(str_list[count]);
			if(word_list[count]=="Rha" or word_list[count]=="Rhe" or word_list[count]=="Rhi" or word_list[count]=="ThaS" or word_list[count]=="Thi" or word_list[count]=="The" or word_list[count]=="Huu" or word_list[count]=="Huumn"):
				tag_list[count]="<NaN>";

			ans=name.del_word(count,str_list);
			if(ans!=0):
				if(ans!=1):
					word_list[count-1]+="'s";
				str_list=str_list[:count]+str_list[count+1:];	
				tag_list=tag_list[:count]+tag_list[count+1:];
				word_list=word_list[:count]+word_list[count+1:];
				count-=1;
			count=count+1;
			continue;
		else:
			temp=ans.split('=');
			tag_word=temp[2];
			tag_list[count]=sub_tag(tag_word);
			word_list[count]=temp[1];
		
		name_ans=0;	
		name_ans=name.is_Name(count,str_list);	
		if (name_ans==1):
			if (tag_list[count]!="<ANIMT>"):
				tag_list[count]="<Name>";
				word_list[count]=trans.cov(str_list[count]);
			#Delete next word which define noun.
			str_list=str_list[:count+1]+str_list[count+2:];	
			tag_list=tag_list[:count+1]+tag_list[count+2:];
			word_list=word_list[:count+1]+word_list[count+2:];
			#count=count+1;
		
		if (name_ans==2):
			if (tag_list[count]!="<ANIMT>"):
				tag_list[count]="<Name>";
				word_list[count]=trans.cov(str_list[count])+"'s";
			#Delete next word which define noun.
			str_list=str_list[:count+1]+str_list[count+2:];	
			tag_list=tag_list[:count+1]+tag_list[count+2:];
			word_list=word_list[:count+1]+word_list[count+2:];
		
		join_word=name.join_word(str_list[count]);
		if join_word!=0:
			tag_list[count]="<Join>";
			if join_word==1:
				word_list[count]="and";
			else:
				word_list[count]="or";
				
		count=count+1;
	
	#pass 2
	
	for i in range(1,len(word_list)-1):
		if(tag_list[i-1]=="<Name>" and tag_list[i+1]=="<Name>" and tag_list[i]!="<Join>" and tag_list[i]!="<ANIMT>"):
			tag_list[i]="<Name>";
			word_list[i]=trans.cov(str_list[i]);
	
	#print "Tagged output after pass 1:"
	#print tag_list;
	#print word_list;
	result.append(tag_list);		#Tags
	result.append(word_list);		#English Translation
	result.append(str_list);		#Hindi Words
	return result;