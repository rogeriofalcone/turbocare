def FmtNum(v, minwidth=0, trailing=2):
	V = '%f' % v
	I = V[0:V.find('.')]
	D = V[V.find('.'):]
	f_I = ''
	H = [y for y in I]
	H.reverse()
	for x, i in zip(H,range(0,len(I))):
		if i in [3,5,7,9,11,13,15,17]:
			f_I = x+','+f_I
		else:
			f_I = x+f_I
	if trailing > 0:
		f_D = D[0:trailing+1]
	else:
		f_D = ''
	return f_I+f_D
