import sys
import subprocess
import os
import time
from subprocess import PIPE, Popen
from threading  import Thread

try:
	from Queue import Queue, Empty
except ImportError:
	from queue import Queue, Empty  # python 3.x

def enqueue_output(out, queue, line):
	for line in iter(out.readline, b''):
		queue.put(line)
	out.close()

def readFromGATT(q, l):
	command = ['gatttool', '-b', 'E9:0B:1C:50:81:E5', '--addr-type=random', '--char-write-req', '--handle=0x000e', '--value=0100', '--listen']
	# gatttool -b E9:0B:1C:50:81:E5 --addr-type=random --char-write-req --handle=0x000e --value=0100 --listen
	ON_POSIX = 'posix' in sys.builtin_module_names
	p = Popen(command, stdout=PIPE, close_fds=ON_POSIX)
	t = Thread(target=enqueue_output, args=(p.stdout, q, l))
	t.daemon = True # thread dies with the program
	t.start()
	return t;

'''
if(len(sys.argv)!=2):
	print("you have to pass your password as argument, please retype the command\n");
	exit(0);
command_up=["echo "+ str(sys.argv[1]), ' |',' sudo -S', ' hciconfig', ' hci0', ' up']
subprocess.call(command_up, shell=True)
time.sleep(3);
'''
flag=True;
ln='';
q=Queue();
T=readFromGATT(q, ln);
counter=0;
z='';
print(T);
list_notes=['DO','RE','MI','FA','SOL','LA','SI']
prev_state=-1;

# ... do the writing loop
while True:
	# read line without blocking
	try:  line = q.get(timeout=1.2) # or q.get(timeout=.1)
	except Empty:
		
		if(counter==3):
			counter=0;
			'''
			command_down=["echo " + str(sys.argv[1]), ' |',' sudo -S', ' hciconfig', 'hci0', ' down']
			time.sleep(0.5);
			command_up=["echo "+ str(sys.argv[1]), ' |',' sudo -S', ' hciconfig', ' hci0', ' up']
			subprocess.call(command_down, shell=True)
			subprocess.call(command_up, shell=True)
			time.sleep(6)
			'''
			try: 
				T._stop();
			except Exception as e:
				time.sleep(0);
		else:
			time.sleep(2)
			counter+=1;
			continue;

		print("error in reading");
		for i in range(0,3):
			time.sleep(2);
			print("trying again");
			T=readFromGATT(q, ln);
		
	else: # got line
		counter=0;
		if(flag==False):
			#extract and clean out the "YAWN|PITCH|ROLL" values
			tosend=str(line[35:-2]);
			res=tosend.split('7c');
			l='';
			print(tosend)
			print(res[0])
			#YAWN
			numb=res[0].split(" ");
			print(len(numb))
			for i in range(1, (len(numb)-1)):
				if(numb[i]=='00'):
					l=l+"0";
				else:
					l=l+str(chr(int(numb[i],16)));
			l=l.strip();
			if(l.endswith('.')):
				l=l[:-1];
				
			nl=float(l);
			nl=nl+180;

			#print(nl)

			if(nl>0 and nl<45): curr_state=1; #do
			if(nl>45 and nl<90): curr_state=2; #re
			if(nl>90 and nl<135): curr_state=3; #mi
			if(nl>135 and nl<180): curr_state=4; #fa
			if(nl>225 and nl<270): curr_state=5; #sol
			if(nl>270 and nl<315): curr_state=6; #la
			if(nl>315 and nl<360): curr_state=7; #si

			#print(nl)
			if( prev_state < 0 ): #case of starting point with prev_state=-1
				prev_state=curr_state;
 
			if(prev_state!=curr_state):
				if( ((prev_state%7)+1)==curr_state ): #if the previous state is before the current state
					#se vengo dalla nota prima
					#(prev_state%7)+1 not allowed 7 but until 6.
					if( nl< ((45*(curr_state-1))+15) ):
						curr_state=curr_state - 1;
				#print(curr_state)
				#operations to be done if the note changes
				#print(list_notes[curr_state-1]);
				#os.system("echo '"+str(curr_state)+"' \\; | pdsend 3002");
				prev_state=curr_state;

			'''
			for r in res:
				numb=r.split(" ");
				#print(numb);
				for i in range(1, (len(numb)-1)):
					l=l+ chr(int(numb[i],16));
				l=l+"|";
			print(l);
			
			#print(nl+180);
			'''	
		else:
			flag=False;



