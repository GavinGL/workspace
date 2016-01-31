#!/usr/bin/env python

#It can be used to rename files (in addition to myself) in current dir,add numbers ahead.

import os,re

def rename():
	path="./"
	
	filelist=os.listdir(path)
	filelist.remove('rename.py')
	i=0
	for files in filelist:
		olddir=os.path.join(path,files)
		if os.path.isdir(olddir):
			continue
		filename=os.path.splitext(files)[0]
		filetype=os.path.splitext(files)[1]
		m = filename.split('_')[-1]
		nstr='%03d_' %i
		newdir=os.path.join(path,nstr+m+filetype)
		os.rename(olddir,newdir)
		i=i+1

rename()
