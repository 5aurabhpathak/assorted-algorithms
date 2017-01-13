# coding=utf-8
import sys
import codecs

def find_tns(words):
	n=len(words);
	str1="Rha";
	str2="have";
	str3="Rhe";
	str4="Rhi";
	if words[n-1]==str2:
		if words[n-2]==str1:
			return 11;	#Single Present Continues
		if words[n-2]==str3:
			return 12;	#Multiple Present Continues
		if words[n-2]==str4:
			return 14;	#Multiple Present Continues	
		return 13;	#Simple present
	
	str5="Tha";
	str6="Thi";
	str7="The";
	if words[n-1]==str5 or words[n-1]==str6 or words[n-1]==str7:
		if words[n-2]==str1:
			return 21;	#Single Past Continues
		if words[n-2]==str3:
			return 22;	#Multiple Past Continues
		if words[n-2]==str4:
			return 24;	#Single/multiple Past Continues	
		
		return 23;	#Simple past
	
	str8="Huu";
	str9="Huumn";
	if words[n-1]==str8 or words[n-1]==str9:
		if words[n-2]==str1:
			return 31;	#Single Past Continues
		if words[n-2]==str3:
			return 32;	#Multiple Past Continues
		if words[n-2]==str4:
			return 34;	#Single/multiple Past Continues	
		
		return 33;
	
	return 0;

def trans_rule(words,tag):
	#print words;
	#print tag;
	count=0;
	str="";
	sov=list();
	tense=0;	#11: Single Present continues 12: Multiple Present continues 21: Single past 22: Multiple past
	for i in range(0,len(words)):
		sov.append("<nan>");
	
	flag=0;
	#Find Subject,Object and Verb
	for i in range(0,len(tag)):
		#print words[i];
		#print tag[i];
		if tag[i]=="<Name>" or tag[i]=="<Join>" :
			sov[i]="<S>";
		elif tag[i]=="<ANIMT>":
			n=len(words[i]);
			sov[i]="<S>";
			if(words[i][n-1]=='s' and words[i]!="this"):
				flag=1;
		elif tag[i]=="<VERB>":
			sov[i]="<V>";
		elif tag[i]=="<ADJ>":
			sov[i]="<ADJ>";
		else:
			sov[i]="<O>";
	
	#Find tense
	tns=find_tns(words);
	if(tns==11 or tns==12 or tns==14 or tns==21 or tns==22 or tns==24 or tns==31 or tns==32 or tns==34):
		words=words[:-2];
		tag=tag[:-2];
		
	if(tns==13 or tns==33):
		words=words[:-1];
		tag=tag[:-1];
	
	count=0;
	flag1=0;
	#Subject
	for i in range(0,len(tag)):
		if sov[i]=="<S>":
			str+=words[i]+" ";
			if words[i]=="I":
				str+="am"+" ";
			if len(words[i])>2 and words[i][len(words[i])-2]=="'":
				flag1=1;
			count+=1;
		if words[i]=="they" or words[i]=="They":
			count+=1;
		if flag==1:
			count+=2;

	if((tns==11 or (tns==13 or tns==14)) and count==1 and flag1==0):
		str+="is"+" ";
	
	elif(tns==12 or((tns==13 or tns==14) and count>1)and flag1==0):
		str+="are"+" ";
		
	elif((tns==21 or (tns==23 or tns==24)) and count==1 and flag1==0):
		str+="was"+" ";
	
	if(tns==22 or((tns==23 or tns==24) and count>1)and flag1==0):
		str+="were"+" ";
		
	#Adjective
	for i in range(0,len(tag)):
		if sov[i]=="<ADJ>":
			str+=words[i]+" ";
	#Verb
	for i in range(0,len(tag)):
		if sov[i]=="<V>":
			if(tns==11 or tns==12 or tns==14 or tns==21 or tns==22 or tns==24 or tns==31):
				str+=words[i]+"ing ";
			else:
				str+=words[i]+" ";
	#Object
	for i in range(0,len(tag)):
		if sov[i]=="<O>":
			str+=words[i]+" ";
			
	str=str[:-1]+".";
	print str;