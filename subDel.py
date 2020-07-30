import os,itertools,sys,subprocess,shlex,re
import numpy as np
#---------------------------------------------------------------------------------------#
def shout(cmd):
	p = subprocess.Popen( shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE )
	out, err = p.communicate()
	return out
#---------------------------------------------------------------------------------------#
def runList(*keys):
	kDict = { k:[] for k in keys }
	out = shout('squeue -u ug36')
	jobList = np.array( [ x.split() for x in out.split('\n')[1:-1] ])
	jID = jobList[:,0].astype(np.int)
	WorkDir = []; JobName = [];
	for job in jID:
		out = shout('scontrol show job %d' % job)
		res = dict(re.findall(r'(\w*)=([\w*{\.,\/\-}]+\w*)?-*', out))
		for key in keys:
			if key in res.keys():
				kDict[key].append( res[key] )
	return kDict
#---------------------------------------------------------------------------------------#
def fexists(rDict, fname):
	# True If job is running currently
	runBool = False
	try:
		ind = rDict['JobName'].index(fname)
		if rDict['WorkDir'][ind] == os.getcwd():
			runBool = True
	except ValueError:
		pass
	return runBool
#---------------------------------------------------------------------------------------#
rDict = runList('JobName', 'WorkDir', 'JobId')
#---------------------------------------------------------------------------------------#
ind = np.array(rDict['WorkDir']) == os.getcwd()

jobCurr = np.array(rDict['JobId'])[ind]
print '\n'.join(np.array(rDict['JobName'])[ind])
print "Delete all the above (%d) files? (y/n)" % sum(ind)

response = raw_input(">")
if response == 'y':
	for jId in jobCurr:
		os.system('scancel %s' % jId)
	print "Deleted %d files." % sum(ind)
else:
	print "Exiting."
