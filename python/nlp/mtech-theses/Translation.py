# coding=utf-8
import codecs
import string

#fr = codecs.open('input', encoding='utf-8',mode='r')
#fw = codecs.open('output', encoding='utf-8',mode='w+')
#str_list = fr.read().split()

def cov(str):
	tmp_phone = ''
	for e in str:
		if e == 'अ'.decode('utf-8'):	
			tmp_phone = tmp_phone + 'a'
		elif e == 'आ'.decode('utf-8'):
			tmp_phone = tmp_phone +  'aa'
		elif  e == 'ा'.decode('utf-8'):	
			tmp_phone = tmp_phone +  'a'
		elif e == 'इ'.decode('utf-8') or e == 'ि'.decode('utf-8'):
			tmp_phone = tmp_phone + 'i'
		elif e == 'ई'.decode('utf-8') or e == 'ी'.decode('utf-8'):	
			tmp_phone = tmp_phone + 'i'
		elif e == 'उ'.decode('utf-8') or e == 'ु'.decode('utf-8'):	
			tmp_phone = tmp_phone + 'u'
		elif e == 'ऊ'.decode('utf-8') or e == 'ू'.decode('utf-8'):	
			tmp_phone = tmp_phone + 'uu'
		elif e == 'ए'.decode('utf-8') or e == 'े'.decode('utf-8'):	
			tmp_phone = tmp_phone + 'e'
		elif e == 'ऐ'.decode('utf-8') or e == 'ै'.decode('utf-8'):	
			tmp_phone = tmp_phone + 'ee'
		elif e == 'ओ'.decode('utf-8') or e == 'ो'.decode('utf-8'):	
			tmp_phone = tmp_phone + 'o'
		elif e == 'औ'.decode('utf-8') or e == 'ौ'.decode('utf-8'):	
			tmp_phone = tmp_phone + 'oo'
		elif e == 'अं'.decode('utf-8') or e == 'ँ'.decode('utf-8'):
			tmp_phone = tmp_phone + 'mn'
		elif e == 'ं'.decode('utf-8'): 
			tmp_phone = tmp_phone + 'n'
		elif e == 'क'.decode('utf-8'):	
			tmp_phone = tmp_phone + 'k'
		elif e == 'ख'.decode('utf-8'):	
			tmp_phone = tmp_phone + 'kh'
		elif e == 'ग'.decode('utf-8'):	
			tmp_phone = tmp_phone + 'ga'
		elif e == 'घ'.decode('utf-8'):	
			tmp_phone = tmp_phone + 'gh'
		elif e == 'ङ'.decode('utf-8'):	
			tmp_phone = tmp_phone + 'wn'
		elif e == 'च'.decode('utf-8'):	
			tmp_phone = tmp_phone + 'ch'
		elif e == 'छ'.decode('utf-8'):	
			tmp_phone = tmp_phone + 'chh'
		elif e == 'ज'.decode('utf-8'):	
			tmp_phone = tmp_phone + 'ja'
		elif e == 'झ'.decode('utf-8'):	
			tmp_phone = tmp_phone + 'jh'
		elif e == 'ञ'.decode('utf-8'):	
			tmp_phone = tmp_phone + 'zn'
		elif e == 'ट'.decode('utf-8'):	
			tmp_phone = tmp_phone + 't'
		elif e == 'ठ'.decode('utf-8'):	
			tmp_phone = tmp_phone + 'th'
		elif e == 'ड'.decode('utf-8'):	
			tmp_phone = tmp_phone + 'd'
		elif e == 'ढ'.decode('utf-8'):	
			tmp_phone = tmp_phone + 'ddh'
		elif e == 'ण'.decode('utf-8'):	
			tmp_phone = tmp_phone + 'an'
		elif e == 'त'.decode('utf-8'):	
			tmp_phone = tmp_phone + 't'
		elif e == 'थ'.decode('utf-8'):	
			tmp_phone = tmp_phone + 'th'
		elif e == 'द'.decode('utf-8'):	
			tmp_phone = tmp_phone + 'd'
		elif e == 'ध'.decode('utf-8'):	
			tmp_phone = tmp_phone + 'dh'
		elif e == 'न'.decode('utf-8'):	
			tmp_phone = tmp_phone + 'n'
		elif e == 'प'.decode('utf-8'):	
			tmp_phone = tmp_phone + 'p'
		elif e == 'फ'.decode('utf-8'):	
			tmp_phone = tmp_phone + 'ph'
		elif e == 'ब'.decode('utf-8'):	
			tmp_phone = tmp_phone + 'b'
		elif e == 'भ'.decode('utf-8'):	
			tmp_phone = tmp_phone + 'bh'
		elif e == 'म'.decode('utf-8'):	
			tmp_phone = tmp_phone + 'm'
		elif e == 'य'.decode('utf-8'):	
			tmp_phone = tmp_phone + 'y'
		elif e == 'र'.decode('utf-8'):	
			tmp_phone = tmp_phone + 'r'
		elif e == 'ल'.decode('utf-8'):	
			tmp_phone = tmp_phone + 'l'
		elif e == 'व'.decode('utf-8'):	
			tmp_phone = tmp_phone + 'v'
		elif e == 'श'.decode('utf-8'):	
			tmp_phone = tmp_phone + 'sh'
		elif e == 'ष'.decode('utf-8'):	
			tmp_phone = tmp_phone + 'shh'
		elif e == 'स'.decode('utf-8'):	
			tmp_phone = tmp_phone + 's'
		elif e == 'ह'.decode('utf-8'):	
			tmp_phone = tmp_phone + 'h'

	return tmp_phone.title();
	#fw.write(tmp_phone.title()+ ' ')
