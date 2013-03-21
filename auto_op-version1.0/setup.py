#!/usr/bin/python
#-*- coding: utf-8 -*-
import sys,os,time,readline
option=sys.argv
build_file='build.cfg'
def setup_build():
        try:
                option[1]
        except IndexError:
                print '\nError:no argument detected,use --help for helps\n '
                sys.exit()
        if option[1] == 'build':
                try:
                        option[2]
                except IndexError:
                        print '\nError:You must specify where to install this program\n'
                        sys.exit()

                if  option[2].startswith('--prefix='):
                        print 'Start to check pre-installation environment...................................\n'
                        while True:
                                try:
                                        Dir=option[2].split()[0][9:] #pick up direcotry name
                                        if option[2].split()[0][-1] == '/':
                                                RealDir=option[2].split()[0][9:-1]
                                        else:
                                                RealDir=Dir
					os.lstat(Dir)
					f = file(build_file,'w')
					record_dir='WorkingDir=%s\n' % RealDir
					f.write(record_dir)					
                                        try:
                                                import paramiko
					except ImportError:
						print 'The localhost have not paramiko module,try to auto install'
						os.system('wget http://ftp.dlitz.net/pub/dlitz/crypto/pycrypto/pycrypto-2.3.tar.gz')
						os.system('wget http://www.lag.net/paramiko/download/paramiko-1.7.7.1.tar.gz')
						os.system('tar -zxvf pycrypto-2.3.tar.gz')
						os.system('cd pycrypto-2.3;python setup.py build && python setup.py install')
						os.system('tar xvzf paramiko-1.7.7.1.tar.gz')
						os.system('cd paramiko-1.7.7.1;python setup.py build && python setup.py install')
					try:
						import paramiko
					except ImportError:
						print 'Error:module paramiko install failed ,please install it manually.'
						sys.exit()
				except OSError:
					CreateDir=os.system('mkdir -p %s' % Dir)
					if CreateDir == 0:
						print '\033[31;40;1mdirecotry not exsit,creating successful........\033[0m'
						continue
					else:
						print 'Error: directory not exist and has no permission to create.'
						sys.exit()
				time.sleep(3)
				print "If no error printed out , you can run '\033[32;40;1mpython setup.py install\033[0m' to install the program \n"
				break
		else:
			print '\nError:You must specify install directory for this program\n'
	elif option[1] == 'install':
		f = file(build_file)
		line = f.readline()
		name=line.strip('\n').split('=')[0]
		name_info=line.strip('\n').split('=')[1]
		f.close()
		FileCopy='cp -rp auto_op.py %s' % name_info
		print 'Extract files to working directory...\n'
		SetDir = "sed -i 's#/tmp/auto#%s#' %s/auto_op.py" %(name_info, name_info)
		os.system(FileCopy)
		os.system(SetDir)
		time.sleep(3)
		print '\n\033[32;1mComplete ok\nNow you can run %s/auto_op.py start manage your network.\033[0m' %name_info
		
	elif option[1].startswith('--help'):
		print '''
	--help			Show helps
	build --prefix=dir	Check and prepare the pre-installation environment
	install			install software'''
	else:print '\nWrong option, try --help for helps\n'
setup_build()
