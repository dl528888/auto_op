#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import paramiko
import threading
import time
import readline
import subprocess
import socket
def op_log(log):
	f=file(op_log_file,'a')
        date=time.strftime('%Y-%m-%d %H:%M:%S')
        record = '%s   %s\n' %(date,log)
        f.write(record)
def CountLine(groupName):
        fileName = '%s/%s' %(GroupDir,groupName)
        lineNumber = 0
        f = file(fileName)
        while True:
                line = f.readline()
                if len(line) == 0:break
                if line.startswith('#'):continue
                filename=line.split(' ')
                lineNumber += 1
        return  lineNumber
def List_group(GroupDir):
        GroupList=os.listdir(GroupDir)
	if len(GroupList) == 0:
		print 'now goup is empty!'
	else:
		print 'now there is group is'
		for i in GroupList:
			print '\033[1;32m%s\033[0m[\033[1;36m%s\033[0m]'%(i,CountLine(i))

def List_group_name(GroupDir):
        GroupList=os.listdir(GroupDir)
        return GroupList
def AddGroup():
		while True:
				new_group=raw_input('please input new group name:')
				NewGroupName = '%s/%s' % (GroupDir,new_group)
				if new_group  in os.listdir(GroupDir):
					    print 'Group %s is exist!'%new_group
					    continue
				else:
					    F = file(NewGroupName,'w')
					    msg = 'Created group %s successful.' % new_group
					    print msg
					    op_log(msg)
					    break
                AddServer = raw_input('Do you want to add new server to Group \033[32;40;1m%s\033[0m [ Y / N ]:' % new_group)
                if AddServer == 'Y' or AddServer == 'y':
                        while True:
                                NewServerIP2 = raw_input('Input new server IP or Hostname:')
                                if len(NewServerIP2) == 0:continue
				IP2_port = raw_input("Input newser's port:")
				if len(IP2_port) == 0:continue
                                while True:
                                        IP2_user = raw_input("Input newser's username:")
                                        if len(IP2_user) == 0:continue
                                        IP2_pass = raw_input("Input newser's password:")
                                        if len(IP2_pass) == 0:
                                                print 'Error: password cannot be empty,please try again.'
                                                continue
                                        else:break
                                NewServerIP = '%s %s %s %s \n' % (NewServerIP2,IP2_port,IP2_user,IP2_pass)
                                F.write(NewServerIP)
                                msg = 'New server \033[32;40;1m%s\033[0m added successfully.' % NewServerIP2
				print msg
				op_log(msg)
                                KeepAddServer = raw_input('Keep on adding new server?:[ Y / N ]')
                                if KeepAddServer == 'Y' or KeepAddServer == 'y':continue
                                else:break
                F.flush()
                F.close()


def RenameGroup():
                print '---------------'
                LoadSuccess=False
                while not LoadSuccess:
                        Group_name=raw_input('Which group name do you want to change?:')
                        GroupFile='%s/%s' %(GroupDir,Group_name)

                        try:
                                file(GroupFile)
                                LoadSuccess=True
                        except IOError:
                                print '\033[31;1mGroup name not exist\033[0m'
                while True:
                        NewGroupName2=raw_input('New name:')
                        NewGroupName = NewGroupName2.strip()
                        if len(NewGroupName)==0:continue
                        New_G_file='%s/%s' %(GroupDir,NewGroupName)
                        GroupRename='mv %s %s' %(GroupFile,New_G_file)
                        os.system(GroupRename)
                        msg= '\033[36;1m group name of %s changed to %s\033[0m' %(Group_name,NewGroupName)
                        print msg
			op_log(msg)
                        break

def DelGroup():
        G_name = raw_input('please inupt you want to del group name:')
        GroupList =os.listdir(GroupDir)
        IsFileExist = G_name in GroupList
        if IsFileExist is True:
                print G_name
                D_option = raw_input('Are you sure you want to delete group\033[32;40;1m%s\033[0m [ Y / N ]: ' % G_name)
                if D_option == 'Y' or D_option == 'y':
                        GroupFile='%s/%s' % (GroupDir,G_name)
                        os.system('rm -rf %s' % GroupFile)
                        print 'Deleted group %s\n ' % G_name
                        op_log('Deleted Group %s' % G_name)
                else:
                        print '\033[33;40;1mNo action\033[0m'
        else:
                print '\n\033[31;49;1mError+++: Wrong group name,check again.\033[0m\n'

def show_host():
	LoadSucess=False;
	while not LoadSucess:
		try:
			global GroupName
			GroupName=raw_input('\nInput Group name which the server is in:')
			global GroupFile
			GroupFile='%s/%s' %(GroupDir,GroupName)
			file(GroupFile)
			print '\033[32;40;1m------------------------Server List----------------------------\033[0m'
			show_host_command = ((subprocess.Popen("cat %s|awk '{print $1}'"%GroupFile, shell=True, stdout=subprocess.PIPE)).stdout.read())
			print show_host_command
			op_log("show group %s server list"%GroupName+str(show_host_command.strip('\n').split('\n')))
			LoadSucess=True
		except IOError:
			print '\n\033[31;40;1mNo such group name found,please try again.\033[0m'

def add_host():
	show_host()
	global GroupFile
	print 'groupfile is %s' % GroupFile
	f=file(GroupFile,'a')
	while True:
		NewServerIP2 = raw_input('Input new server IP or Hostname:')
		if len(NewServerIP2) == 0:continue
		IP2_port = raw_input("Input newser's port:")
		if len(IP2_port) == 0:continue
		while True:
			IP2_user = raw_input("Input newser's username:")
			if len(IP2_user) == 0:continue
			IP2_pass = raw_input("Input newser's password:")
			if len(IP2_pass) == 0:
				print 'Error: password cannot be empty,please try again.'
				continue
			else:break
		NewServerIP = '%s %s %s %s \n' % (NewServerIP2,IP2_port, IP2_user,IP2_pass)
		f.write(NewServerIP)
		op_log("add new host ip %s port %s"%(NewServerIP2,IP2_port ))
		print 'New server \033[32;40;1m%s\033[0m added successfully.' % NewServerIP2
		KeepAddServer = raw_input('Keep on adding new server?:[ Y / N ]')
		if KeepAddServer == 'Y' or KeepAddServer == 'y':continue
		else:
			f.close()
			break
def del_host():
	show_host()
	while True:
		f=file(GroupFile)
		print '\n\033[33;40;1mNotice: All matched IP adresses will be deleted,becare\033[0m'
		IP=raw_input('Input the server IP which you want to delete:')

		if len(IP) ==0:continue
		NotMatchedRow = 0
		while True:
			line = f.readline()
			if len(line) ==0:break
			OldIP=line.split()[0]
			if IP == OldIP:
				os.system("grep ^%s %s|awk '{print $1}'" %(IP,GroupFile))
				MatchNumbers=os.system("grep ^%s %s|wc -l|xargs echo -e '\033[33;40;1mmatched rows:\033[0m'" %(IP,GroupFile))
				DelAllMatches = raw_input('Do you want to delete all the matched rows?(y/n)')
				if DelAllMatches == 'y':
					NotMatchedRow = -1
					DelIP = "sed -i '/%s/d' %s" %(IP,GroupFile)
					os.system(DelIP)
				else:break
				msg = 'User deleted server %s from group %s' % (IP, GroupName)
				op_log(msg)
				print 'IP %s has been deleted from group %s ' % (IP, GroupName)

			else:
				NotMatchedRow += 1
		if NotMatchedRow > 0: print '\033[33;1m 0 matched rows!\033[0m'

def ssh2(ip, port, username,passwd,cmd):
    try:
	print '-------------------------------'
        print  'start to connect ip %s port %s username %s  at time %s'%(ip,port,username,time.strftime('%Y-%m-%d %H:%M:%S'))
	ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port,username,passwd,timeout=5)
	print 'exec result is'
        for m in cmd:
            stdin, stdout, stderr = ssh.exec_command(m)
            out = stdout.readlines()
            for o in out:
                print "\033[1;32m%s\033[0m"%o,
	msg = "\033[1;32m%s exec command %s OK!\033[0m"%(ip,cmd)
	print msg
	op_log(msg)
        print 'end time is', time.strftime('%Y-%m-%d %H:%M:%S')
	print '-------------------------------'
        ssh.close()
    except paramiko.SSHException, e:
	msg = "\033[1;32m%s exec command %s Fail!\033[0m"%(ip,cmd)
	op_log(msg+' Fail reasion is:'+str(e))
        print e
def ssh2_put(ip, port, username,passwd, file1, file2):
    try:
	print '-------------------------------'
	print 'start to connect ip %s port %s username %s  at time %s'%(ip,port,username,time.strftime('%Y-%m-%d %H:%M:%S'))
        tcpsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        tcpsock.settimeout(5)
        tcpsock.connect((ip,port),)
        ssh = paramiko.Transport(tcpsock)
        ssh.connect(username=username,password=passwd)
        sftp = paramiko.SFTPClient.from_transport(ssh)
        remotepath = file2
        localpath = file1
        sftp.put(localpath, remotepath)
        sftp.close()
        msg = "\033[1;32m%s exec put %s to %s OK!\033[0m"% (ip, localpath, remotepath)
	print msg
	op_log(msg)
        print 'end time is', time.strftime('%Y-%m-%d %H:%M:%S')
	print '-------------------------------'
        ssh.close()
    except paramiko.SSHException, e:
	msg = "\033[1;32m%s exec command %s Fail!\033[0m"%(ip,cmd)
	op_log(msg+'Fail reasion is:'+str(e))
        print e

def ssh2_get(ip, port, username,passwd, file1, file2):
    try:
	print '-------------------------------'
	print 'start to connect ip %s port %s username %s  at time %s'%(ip,port,username,time.strftime('%Y-%m-%d %H:%M:%S'))
        tcpsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        tcpsock.settimeout(5)
        tcpsock.connect((ip,port),)
        ssh = paramiko.Transport(tcpsock)
        ssh.connect(username=username,password=passwd)
        sftp = paramiko.SFTPClient.from_transport(ssh)
	file3 = '%s_%s' % (file1, ip)
        remotepath = file2
        localpath = file3
        sftp.get(remotepath, localpath)
        sftp.close()
        msg = "\033[1;32m%s exec get %s from %s OK!\033[0m"% (ip, remotepath, localpath)
	print msg
	op_log(msg)
        print 'end time is', time.strftime('%Y-%m-%d %H:%M:%S')
	print '-------------------------------'
        ssh.close()
    except paramiko.SSHException, e:
	msg = "\033[1;32m%s exec command %s Fail!\033[0m"%(ip,cmd)
	op_log(msg+'Fail reasion is:'+str(e))
        print e

if __name__=='__main__':
	WorkDir='/tmp/auto'
	GroupDir='%s/server_list'%WorkDir
	op_log_dir = '%s/logs'%WorkDir
	op_log_file='%s/operation.log' %op_log_dir
	if not os.path.exists(GroupDir):
		os.makedirs(GroupDir)
	if not os.path.exists(op_log_dir):
		os.mkdir(op_log_dir)
	LimitedCmd=['shutdown','reboot','rm','halt','dd','fsck']
	try:
		while True:
			show_menu = '''\033[32;40;1m------------------------------------Memu list-----------------------------------------------------------
				1. Add new group
				2. Rename group name
				3. Delete group
				4. List group member
				5. List host in the group
				6. Add new server to group
				7. Delete server from group
				8. Command excution on group servers
			        9. Command excution on one server
			        10. Upload or download on group servers
			        11. Upload or download on one server
				12. Quit
--------------------------------Input number of you want to exec command---------------------------------\033[0m'''
			author_info = '''\033[1;32m                                                                               Author is DengLei\033[0m'''
			try:
				print show_menu
				print author_info
				memu_choice=raw_input('please input you choice:')
				if memu_choice == '1':
					AddGroup()
					continue
				elif memu_choice == '2':
					RenameGroup()
					continue
				elif memu_choice == '3':
					DelGroup()
					continue
				elif memu_choice == '4':
					List_group(GroupDir)
					continue
				elif memu_choice == '5':
					show_host()
					continue
				elif memu_choice == '6':
					add_host()
					continue
				elif memu_choice == '7':
					del_host()
					continue
				elif memu_choice == '8':
					try:
						while True:
							List_group(GroupDir)
							group_choice = raw_input('please input you choice group:')
							if group_choice not in List_group_name(GroupDir):
								print 'You choice %s group not exist!'%group_choice
							else:
								print 'You choice \033[1;32m%s\033[0m group'%group_choice
								while True:
									status = True
									try:
										request= raw_input('please input you want to select command,Ctrl + C to quit:')
										if request == 'y' or request == 'Y':
											continue
										elif request == 'n' or request == 'N':
											break
										elif request == 'q' or request == 'quit':
											break
										else:
											for i in LimitedCmd:
												if i in request:
													print 'the command %s is not exec in remote'%request
													status = False
											if status is True:
												cmd=[request]
												filename=open(GroupDir+os.sep+group_choice,'r')
												while True:
													line = filename.readline()
													if len(line) == 0:break
													name = line.strip('\n').split(' ')
													a=threading.Thread(target=ssh2,args=(name[0], int(name[1]), name[2],name[3],cmd))
													a.start()
													a.join()
												filename.close()
									except KeyboardInterrupt:
										break
										print 'you command is CTRL+C go back'
									except EOFError:
										break
										print 'you command is CTRL+D go back'
					except KeyboardInterrupt:
						print ''
						print 'you command is CTRL+C to quit'
					except EOFError:
						print ''
						print 'you command is CTRL+D to quit'
					print 'ssh finish!'
					continue
				elif memu_choice == '9':
					try:
						while True:
							List_group(GroupDir)
							show_host()
							choice_host = raw_input('Please input you want to execute the command of the host name:')
							check_host_exist = open(GroupFile)
							if choice_host not in check_host_exist.read():
								print 'You input host is not exist in %s' % GroupFile
							else:
								while True:
									status = True
									try:
										request= raw_input('please input you want to select command,Ctrl + C to quit:')
										if request == 'y' or request == 'Y':
											continue
										elif request == 'n' or request == 'N':
											break
										elif request == 'q' or request == 'quit':
											break
										else:
											for i in LimitedCmd:
												if i in request:
													print 'the command %s is not exec in remote'%request
													status = False
											if status is True:
												cmd=[request]
												name = ((subprocess.Popen("grep ^%s %s"%(choice_host,GroupFile ), shell=True, stdout=subprocess.PIPE)).stdout.read()).strip('\n').split(' ')
												a=threading.Thread(target=ssh2,args=(name[0], int(name[1]), name[2],name[3],cmd))
												a.start()
												a.join()
												check_host_exist.close()
									except KeyboardInterrupt:
										break
										print 'you command is CTRL+C go back'
									except EOFError:
										break
										print 'you command is CTRL+D go back'
					except KeyboardInterrupt:
						print ''
						print 'you command is CTRL+C to quit'
					except EOFError:
						print ''
						print 'you command is CTRL+D to quit'
					print 'ssh finish!'
					continue
				elif memu_choice == '10':
					while True:
						file_memu = '''\033[32;40;1m------------------------------------Memu list-----------------------------------------------------------
				1. Upload file to remote group servers
				2. Download file to remote group server
				3. Quit
--------------------------------Input number of you want to exec command---------------------------------\033[0m'''
						print file_memu
						print author_info
						choice_file_memu = raw_input('please input you choice:')

						if choice_file_memu == '1':
							try:
								while True:
									List_group(GroupDir)
									group_choice = raw_input('please input you choice group:')
									if group_choice not in List_group_name(GroupDir):
										print 'You choice %s group not exist!'%group_choice
									else:
										print 'You choice \033[1;32m%s\033[0m group'%group_choice
										while True:
											status = True
											try:
												file1= raw_input('please input you want to upload localpath file name,Ctrl + C to quit:')
												if len(file1) == 0:continue
												file2 = raw_input('please input you want to upload remotepath file name,Ctrl + C to quit:')
												if len(file2) == 0:continue
												request = raw_input('Are you sure upload file from %s to %s in the %s group '%(file1, file2, group_choice))
												if request == 'n' or request == 'N':
													break
												elif request == 'q' or request == 'quit':
													break
												elif request == 'y' or request == 'Y':
													if status is True:
														filename=open(GroupDir+os.sep+group_choice,'r')
														while True:
															line = filename.readline()
															if len(line) == 0:break
															name = line.strip('\n').split(' ')
															a=threading.Thread(target=ssh2_put,args=(name[0], int(name[1]), name[2],name[3], file1, file2))
															a.start()
															a.join()
														filename.close()
											except KeyboardInterrupt:
												break
												print 'you command is CTRL+C go back'
											except EOFError:
												break
												print 'you command is CTRL+D go back'
							except KeyboardInterrupt:
								print ''
								print 'you command is CTRL+C to quit'
							except EOFError:
								print ''
								print 'you command is CTRL+D to quit'
							print 'ssh finish!'
							continue
						elif choice_file_memu == '2':
							try:
								while True:
									List_group(GroupDir)
									group_choice = raw_input('please input you choice group:')
									if group_choice not in List_group_name(GroupDir):
										print 'You choice %s group not exist!'%group_choice
									else:
										print 'You choice \033[1;32m%s\033[0m group'%group_choice
										while True:
											status = True
											try:
												file1= raw_input('please input you want to download localpath file name,Ctrl + C to quit:')
												if len(file1) == 0:continue
												file2 = raw_input('please input you want to download remotepath file name,Ctrl + C to quit:')
												if len(file2) == 0:continue
												request = raw_input('Are you sure download file from %s to %s in the %s group '%(file1, file2, group_choice))
												if request == 'n' or request == 'N':
													break
												elif request == 'q' or request == 'quit':
													break
												elif request == 'y' or request == 'Y':
													if status is True:
														filename=open(GroupDir+os.sep+group_choice,'r')
														while True:
															line = filename.readline()
															if len(line) == 0:break
															name = line.strip('\n').split(' ')
															a=threading.Thread(target=ssh2_get,args=(name[0], int(name[1]), name[2],name[3], file1, file2))
															a.start()
															a.join()
														filename.close()
											except KeyboardInterrupt:
												break
												print 'you command is CTRL+C go back'
											except EOFError:
												break
												print 'you command is CTRL+D go back'
							except KeyboardInterrupt:
								print ''
								print 'you command is CTRL+C to quit'
							except EOFError:
								print ''
								print 'you command is CTRL+D to quit'
							print 'ssh finish!'
							continue
						elif choice_file_memu == '3':
							break

				elif memu_choice == '11':
					while True:
						file_memu = '''\033[32;40;1m------------------------------------Memu list-----------------------------------------------------------
				1. Upload file to remote one server
				2. Download file to remote one server
				3. Quit
--------------------------------Input number of you want to exec command---------------------------------\033[0m'''
						print file_memu
						print author_info
						choice_file_memu = raw_input('please input you choice:')

						if choice_file_memu == '1':
							try:
								while True:
									List_group(GroupDir)
									show_host()
									choice_host = raw_input('Please input you want to execute the command of the host name:')
									check_host_exist = open(GroupFile)
									if choice_host not in check_host_exist.read():
										print 'You input host is not exist in %s' % GroupFile
									else:
										while True:
											status = True
											try:
												file1= raw_input('please input you want to upload localpath file name,Ctrl + C to quit:')
												if len(file1) == 0:continue
												file2 = raw_input('please input you want to upload remotepath file name,Ctrl + C to quit:')
												if len(file2) == 0:continue
												request = raw_input('Are you sure upload file from %s to %s in the %s host '%(file1, file2, choice_host))
												if request == 'n' or request == 'N':
													break
												elif request == 'q' or request == 'quit':
													break
												elif request == 'y' or request == 'Y':
													if status is True:
														name = ((subprocess.Popen("grep ^%s %s"%(choice_host,GroupFile ), shell=True, stdout=subprocess.PIPE)).stdout.read()).strip('\n').split(' ')
														a=threading.Thread(target=ssh2_put,args=(name[0], int(name[1]), name[2],name[3], file1, file2))
														a.start()
														a.join()
														check_host_exist.close()
											except KeyboardInterrupt:
												break
												print 'you command is CTRL+C go back'
											except EOFError:
												break
												print 'you command is CTRL+D go back'
							except KeyboardInterrupt:
								print ''
								print 'you command is CTRL+C to quit'
							except EOFError:
								print ''
								print 'you command is CTRL+D to quit'
							print 'ssh finish!'
							continue
						elif choice_file_memu == '2':
							try:
								while True:
									List_group(GroupDir)
									show_host()
									choice_host = raw_input('Please input you want to execute the command of the host name:')
									check_host_exist = open(GroupFile)
									if choice_host not in check_host_exist.read():
										print 'You input host is not exist in %s' % GroupFile
									else:
										while True:
											status = True
											try:
												file1= raw_input('please input you want to download localpath file name,Ctrl + C to quit:')
												if len(file1) == 0:continue
												file2 = raw_input('please input you want to download remotepath file name,Ctrl + C to quit:')
												if len(file2) == 0:continue
												request = raw_input('Are you sure download file from %s to %s in the %s host '%(file1, file2, choice_host))
												if request == 'n' or request == 'N':
													break
												elif request == 'q' or request == 'quit':
													break
												elif request == 'y' or request == 'Y':
													if status is True:
														name = ((subprocess.Popen("grep ^%s %s"%(choice_host,GroupFile ), shell=True, stdout=subprocess.PIPE)).stdout.read()).strip('\n').split(' ')
														a=threading.Thread(target=ssh2_get,args=(name[0], int(name[1]), name[2],name[3], file1, file2))
														a.start()
														a.join()
														check_host_exist.close()
											except KeyboardInterrupt:
												break
												print 'you command is CTRL+C go back'
											except EOFError:
												break
												print 'you command is CTRL+D go back'
							except KeyboardInterrupt:
								print ''
								print 'you command is CTRL+C to quit'
							except EOFError:
								print ''
								print 'you command is CTRL+D to quit'
							print 'ssh finish!'
							continue
						elif choice_file_memu == '3':
							break
				elif memu_choice == '12':
					break
				elif memu_choice == 'exit' or memu_choice == 'quit' or memu_choice == 'q':
					break
			except KeyboardInterrupt:
			        print 'you command is CTRL+C go back'
	                except EOFError:
				print 'you command is CTRL+D go back'
	except KeyboardInterrupt:
		print ''
		print 'you command is CTRL+C to quit'
	except EOFError:
		print ''
		print 'you command is CTRL+D to quit'

