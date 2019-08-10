'''
page number for each file:
1:12
2:10
3:10
4:10
5:8
6:12
total: 62
'''
import csv
import cv2
import numpy as np

Filter_mode = 0
'''
Filte mode:
0: no filter
1: SD mask
2: Button mask
3: all mask
'''

path1 = 'E:\\19_data\\'
path2 = '\\MoniChrome\\Experiment1\\DatabaseInfo\\User\\'
picpath = 'E:\\19_data\\Pic\\'

seq = ('ID', '1-1', '1-2', '1-3', '1-4', '1-5', '1-6', '1-7', '1-8', '1-9', '1-10', '1-11', '1-12', '2-1', '2-2', '2-3', '2-4', '2-5', '2-6', '2-7', '2-8', '2-9', '2-10', '3-1', '3-2', '3-3', '3-4', '3-5', '3-6', '3-7', '3-8', '3-9', '3-10', '4-1', '4-2', '4-3', '4-4', '4-5', '4-6', '4-7', '4-8', '4-9', '4-10', '5-1', '5-2', '5-3', '5-4', '5-5', '5-6', '5-7', '5-8', '6-1', '6-2', '6-3', '6-4', '6-5', '6-6', '6-7', '6-8', '6-9', '6-10', '6-11', '6-12')
Timedict = dict.fromkeys(seq)
Gazedict = dict.fromkeys(seq)
Pointdict = dict.fromkeys(seq)
F_Pointdict = dict.fromkeys(seq)
Timedict['ID'] = list()
Gazedict['ID'] = list()
Pointdict['ID'] = list()
F_Pointdict['ID'] = list()
Pictures = list()


for i in range(1, 7):
	if i == 1 or i == 6:
		for j in range(1, 13):
			pg = str(i) + '-' + str(j)
			Timedict[pg] = list()
			Gazedict[pg] = list()
			Pointdict[pg] = list()
			F_Pointdict[pg] = list()
			pic = picpath + pg + '.png'
			Pictures.append(cv2.imread(pic))
	elif i == 5:
		for j in range(1, 9):
			pg = str(i) + '-' + str(j)
			Timedict[pg] = list()
			Gazedict[pg] = list()
			Pointdict[pg] = list()
			F_Pointdict[pg] = list()
			pic = picpath + pg + '.png'
			Pictures.append(cv2.imread(pic))
	else:
		for j in range(1, 11):
			pg = str(i) + '-' + str(j)
			Timedict[pg] = list()
			Gazedict[pg] = list()
			Pointdict[pg] = list()
			F_Pointdict[pg] = list()
			pic = picpath + pg + '.png'
			Pictures.append(cv2.imread(pic))
			
#cv2.imshow('My Image', Pictures[0])
#cv2.waitKey(0)
#cv2.destroyAllWindows()
#print(Timedict)

#建立 rngdict
rngdict = {}
fp = open('rnglist', 'r')
all_lines = fp.readlines()
fp.close()
for i in range(1110):
	all_lines[i] = all_lines[i].strip('\n')
	#print(str(int(all_lines[i])) + ' ' + str(len(all_lines[i])))
	if len(all_lines[i]) >= 6: #student ID		
		rngdict[all_lines[i]] = list()
		for j in range(6):
			#print(int(all_lines[i+j+1]))
			rngdict[all_lines[i]].append(int(all_lines[i+j+1]))
		i+=7
#print(rngdict['710143'][5])

pagefile = open('newpagecut_mod.csv', newline='')
prows = csv.DictReader(pagefile)

for prow in prows:
	if not prow['ID']:
		break
	ID = str(int(prow['ID']))
	Timedict['ID'].append(ID)
	Gazedict['ID'].append(ID)
	Pointdict['ID'].append(ID)
	print(ID)
	
	GazeStart = []
	GazeDuration = []
	FixationX = []
	FixationY = []
	path = path1 + ID + path2 + 'GazeFixation.csv'
	with open(path, newline='') as gazefile:
		grows = csv.DictReader(gazefile)
		for grow in grows:
			GazeStart.append(int(grow['StartTime(ms)']))
			GazeDuration.append(int(grow['Duration(ms)']))
			FixationX.append(int(float(grow['PositionX(px)'])))
			FixationY.append(int(float(grow['PositionY(px)'])-100))
	now = 0
	gc = 0
	for ptr in range(6):
		if rngdict[ID][ptr] == 1:
			#print('#1')
			for pg in range(2, 14):
				pgno = '1-' + str(pg-1)
				#print(str(now + pg) + ' - ' + str(now + pg - 1))
				start = int(prow[str(now + pg - 1)])
				over = int(prow[str(now + pg)])
				if over - start > 0:
					Timedict[pgno].append(over - start)
				
				#gaze part	
				while gc < len(GazeStart) and GazeStart[gc] < start:
					gc +=1
				while gc < len(GazeStart) and GazeStart[gc] >= start and GazeStart[gc] < over:
					if GazeStart[gc] + GazeDuration[gc] > over:
						Gazedict[pgno].append(over - GazeStart[gc])
					else:
						Gazedict[pgno].append(GazeDuration[gc])
					Pointdict[pgno].append([FixationX[gc], FixationY[gc]])
					#cv2.circle(Pictures[pg - 2], (FixationX[gc], FixationY[gc]), 30, (0, 255, 255), 5)
					gc +=1
				
			now += 13
		elif rngdict[ID][ptr] == 2:
			#print('#2')
			for pg in range(2, 12):
				pgno = '2-' + str(pg-1)
				#print(str(now + pg) + ' - ' + str(now + pg - 1))
				start = int(prow[str(now + pg - 1)])
				over = int(prow[str(now + pg)])
				if over - start > 0:
					Timedict[pgno].append(over - start)
				
				#gaze part	
				while gc < len(GazeStart) and GazeStart[gc] < start:
					gc +=1
				while gc < len(GazeStart) and GazeStart[gc] >= start and GazeStart[gc] < over:
					if GazeStart[gc] + GazeDuration[gc] > over:
						Gazedict[pgno].append(over - GazeStart[gc])
					else:
						Gazedict[pgno].append(GazeDuration[gc])
					Pointdict[pgno].append([FixationX[gc], FixationY[gc]])
					#cv2.circle(Pictures[pg - 2 + 12], (FixationX[gc], FixationY[gc]), 30, (0, 255, 255), 5)
					gc +=1
					
			now += 11
		elif rngdict[ID][ptr] == 3:
			#print('#3')
			for pg in range(2, 12):
				pgno = '3-' + str(pg-1)
				#print(str(now + pg) + ' - ' + str(now + pg - 1))
				start = int(prow[str(now + pg - 1)])
				over = int(prow[str(now + pg)])
				if over - start > 0:
					Timedict[pgno].append(over - start)
				
				#gaze part	
				while gc < len(GazeStart) and GazeStart[gc] < start:
					gc +=1
				while gc < len(GazeStart) and GazeStart[gc] >= start and GazeStart[gc] < over:
					if GazeStart[gc] + GazeDuration[gc] > over:
						Gazedict[pgno].append(over - GazeStart[gc])
					else:
						Gazedict[pgno].append(GazeDuration[gc])
					Pointdict[pgno].append([FixationX[gc], FixationY[gc]])
					#cv2.circle(Pictures[pg - 2 + 22], (FixationX[gc], FixationY[gc]), 30, (0, 255, 255), 5)
					gc +=1
					
			now += 11
		elif rngdict[ID][ptr] == 4:
			#print('#4')
			for pg in range(2, 12):
				pgno = '4-' + str(pg-1)
				#print(str(now + pg) + ' - ' + str(now + pg - 1))
				start = int(prow[str(now + pg - 1)])
				over = int(prow[str(now + pg)])
				if over - start > 0:
					Timedict[pgno].append(over - start)
				
				#gaze part	
				while gc < len(GazeStart) and GazeStart[gc] < start:
					gc +=1
				while gc < len(GazeStart) and GazeStart[gc] >= start and GazeStart[gc] < over:
					if GazeStart[gc] + GazeDuration[gc] > over:
						Gazedict[pgno].append(over - GazeStart[gc])
					else:
						Gazedict[pgno].append(GazeDuration[gc])
					Pointdict[pgno].append([FixationX[gc], FixationY[gc]])
					#cv2.circle(Pictures[pg - 2 + 32], (FixationX[gc], FixationY[gc]), 30, (0, 255, 255), 5)
					gc +=1
				
			now += 11
		elif rngdict[ID][ptr] == 5:
			#print('#5')
			for pg in range(2, 10):
				pgno = '5-' + str(pg-1)
				#print(str(now + pg) + ' - ' + str(now + pg - 1))
				start = int(prow[str(now + pg - 1)])
				over = int(prow[str(now + pg)])
				if over - start > 0:
					Timedict[pgno].append(over - start)
					
				#gaze part	
				while gc < len(GazeStart) and GazeStart[gc] < start:
					gc +=1
				while gc < len(GazeStart) and GazeStart[gc] >= start and GazeStart[gc] < over:
					if GazeStart[gc] + GazeDuration[gc] > over:
						Gazedict[pgno].append(over - GazeStart[gc])
					else:
						Gazedict[pgno].append(GazeDuration[gc])
					Pointdict[pgno].append([FixationX[gc], FixationY[gc]])
					#cv2.circle(Pictures[pg - 2 + 42], (FixationX[gc], FixationY[gc]), 30, (0, 255, 255), 5)
					gc +=1
				
			now += 9
		elif rngdict[ID][ptr] == 6:
			#print('#6')
			for pg in range(2, 14):
				pgno = '6-' + str(pg-1)
				#print(str(now + pg) + ' - ' + str(now + pg - 1))
				start = int(prow[str(now + pg - 1)])
				over = int(prow[str(now + pg)])
				if over - start > 0:
					Timedict[pgno].append(over - start)
					
				#gaze part	
				while gc < len(GazeStart) and GazeStart[gc] < start:
					gc +=1
				while gc < len(GazeStart) and GazeStart[gc] >= start and GazeStart[gc] < over:
					if GazeStart[gc] + GazeDuration[gc] > over:
						Gazedict[pgno].append(over - GazeStart[gc])
					else:
						Gazedict[pgno].append(GazeDuration[gc])
					Pointdict[pgno].append([FixationX[gc], FixationY[gc]])
					#cv2.circle(Pictures[pg - 2 + 50], (FixationX[gc], FixationY[gc]), 30, (0, 255, 255), 5)
					gc +=1
				
			now += 13

#print(Timedict)
#print(Gazedict)
#print(Pointdict)
totallength = []

totalfixation = []
fixationnum = []
fixationavglen = []
MeanPoint = []
WeightedPoint = []
standarddeviation = []

F_totalfixation = []
F_fixationnum = []
F_fixationavglen = []
F_MeanPoint = []
F_WeightedPoint = []

for i in range(62):
	totallength.append(0)
	totalfixation.append(0)
	fixationnum.append(0)
	fixationavglen.append(0)
	MeanPoint.append([0,0])
	WeightedPoint.append([0,0])
	standarddeviation.append(0)
	F_totalfixation.append(0)
	F_fixationnum.append(0)
	F_fixationavglen.append(0)
	F_MeanPoint.append(0)
	F_WeightedPoint.append(0)

ct = 0
for i in range(1, 7):
	r = 0
	if i == 1 or i == 6:
		r = 13
	elif i == 5:
		r = 9
	else:
		r = 11
	
	for j in range(1, r):
		pg = str(i) + '-' + str(j)
		#for k in range(len(Timedict[pg])):
		#	totallength[ct] +=Timedict[pg][k]
		totallength[ct] = sum(Timedict[pg])
		tX = 0
		tY = 0
		tXX = 0
		tYY = 0
		totalfixation[ct] = sum(Gazedict[pg])
		fixationnum[ct] = len(Gazedict[pg])
		fixationavglen[ct] = np.mean(Gazedict[pg])
		standarddeviation[ct] = np.std(Gazedict[pg])
		M = max(Gazedict[pg])
		#print(totalfixation[ct])
		#print(fixationnum[ct])
		for k in range(len(Gazedict[pg])):
			tX +=Pointdict[pg][k][0]
			tY +=Pointdict[pg][k][1]
			tXX +=Pointdict[pg][k][0]*Gazedict[pg][k]
			tYY +=Pointdict[pg][k][1]*Gazedict[pg][k]
		MeanPoint[ct] = [tX/fixationnum[ct], tY/fixationnum[ct]]
		WeightedPoint[ct] = [tXX/totalfixation[ct], tYY/totalfixation[ct]]

		tX = 0
		tY = 0
		tXX = 0
		tYY = 0
		for k in range(len(Pointdict[pg])):
			Mask = lambda x,y : True if x > 1675 and y > 761 else False
			if Filter_mode == 0:
				# no filter
				cv2.circle(Pictures[ct], (Pointdict[pg][k][0], Pointdict[pg][k][1]), 30, (0, 255, 255), 5)
				F_totalfixation[ct] +=Gazedict[pg][k]
				F_fixationnum[ct] +=1
				tX +=Pointdict[pg][k][0]
				tY +=Pointdict[pg][k][1]
				tXX +=Pointdict[pg][k][0]*Gazedict[pg][k]
				tYY +=Pointdict[pg][k][1]*Gazedict[pg][k]
				F_Pointdict[pg].append([Pointdict[pg][k][0], Pointdict[pg][k][1]])
			elif Filter_mode == 1:
				# SD filter
				if Gazedict[pg][k] >= standarddeviation[ct] and Gazedict[pg][k] <= M - standarddeviation[ct]:
					cv2.circle(Pictures[ct], (Pointdict[pg][k][0], Pointdict[pg][k][1]), 30, (0, 255, 255), 5)
					F_totalfixation[ct] +=Gazedict[pg][k]
					F_fixationnum[ct] +=1
					tX +=Pointdict[pg][k][0]
					tY +=Pointdict[pg][k][1]
					tXX +=Pointdict[pg][k][0]*Gazedict[pg][k]
					tYY +=Pointdict[pg][k][1]*Gazedict[pg][k]
					F_Pointdict[pg].append([Pointdict[pg][k][0], Pointdict[pg][k][1]])
			elif Filter_mode == 2:
				# right bottom mask filter
				if not Mask(Pointdict[pg][k][0], Pointdict[pg][k][1]):
					cv2.circle(Pictures[ct], (Pointdict[pg][k][0], Pointdict[pg][k][1]), 30, (0, 255, 255), 5)
					F_totalfixation[ct] +=Gazedict[pg][k]
					F_fixationnum[ct] +=1
					tX +=Pointdict[pg][k][0]
					tY +=Pointdict[pg][k][1]
					tXX +=Pointdict[pg][k][0]*Gazedict[pg][k]
					tYY +=Pointdict[pg][k][1]*Gazedict[pg][k]
					F_Pointdict[pg].append([Pointdict[pg][k][0], Pointdict[pg][k][1]])
			elif Filter_mode == 3:
				# double filter
				if Gazedict[pg][k] >= standarddeviation[ct] and Gazedict[pg][k] <= M - standarddeviation[ct]:
					if not Mask(Pointdict[pg][k][0], Pointdict[pg][k][1]):
						#print(Pointdict[pg][k])
						cv2.circle(Pictures[ct], (Pointdict[pg][k][0], Pointdict[pg][k][1]), 30, (0, 255, 255), 5)
						F_totalfixation[ct] +=Gazedict[pg][k]
						F_fixationnum[ct] +=1
						tX +=Pointdict[pg][k][0]
						tY +=Pointdict[pg][k][1]
						tXX +=Pointdict[pg][k][0]*Gazedict[pg][k]
						tYY +=Pointdict[pg][k][1]*Gazedict[pg][k]
						F_Pointdict[pg].append([Pointdict[pg][k][0], Pointdict[pg][k][1]])
		F_fixationavglen[ct] = F_totalfixation[ct]/F_fixationnum[ct]
		F_MeanPoint[ct] = [tX/F_fixationnum[ct], tY/F_fixationnum[ct]]
		F_WeightedPoint[ct] = [tXX/F_totalfixation[ct], tYY/F_totalfixation[ct]]
		#cv2.circle(Pictures[ct], (int(MeanPoint[ct][0]), int(MeanPoint[ct][1])), 30, (0, 0, 255), 5)
		#cv2.circle(Pictures[ct], (int(WeightedPoint[ct][0]), int(WeightedPoint[ct][1])), 30, (18, 153, 255), 5)
		#cv2.circle(Pictures[ct], (int(F_MeanPoint[ct][0]), int(F_MeanPoint[ct][1])), 30, (255, 0, 0), 5)
		#cv2.circle(Pictures[ct], (int(F_WeightedPoint[ct][0]), int(F_WeightedPoint[ct][1])), 30, (255, 144, 30), 5)
		ct +=1
	
#print(MeanPoint)


#ouput pictures
picpath = ''
if Filter_mode == 0:
	picpath = 'Outpic//nofilter//'
	fixpath = 'Fixpic//nofilter//'
elif Filter_mode == 1:
	picpath = 'Outpic//filter_A//'
	fixpath = 'Fixpic//filter_A//'
elif Filter_mode == 2:
	picpath = 'Outpic//filter_B//'
	fixpath = 'Fixpic//filter_B//'
elif Filter_mode == 3:
	picpath = 'Outpic//filter_AandB//'
	fixpath = 'Fixpic//filter_AandB//'
for i in range(62):
	if i < 12:
		pg = '1-' + str(i+1)
	elif i < 22:
		pg = '2-' + str(i-12+1)
	elif i < 32:
		pg = '3-' + str(i-22+1)
	elif i < 42:
		pg = '4-' + str(i-32+1)
	elif i < 50:
		pg = '5-' + str(i-42+1)
	else:
		pg = '6-' + str(i-50+1)
	picname = picpath + pg + '.png'
	fixpic = fixpath + pg + '.png'
	#cv2.imwrite(picname, Pictures[i])
	cv2.imwrite(fixpic, Pictures[i])

'''
#print(['Page#', 'Length(ms)', 'TotalFixationLength(ms)','FixatoinTimePercentage', 'FixationNumbers', 'FixationAvgDuration(ms)', 'MeanTimetoFixation(ms)'])
for i in range(1, 63):
	if i <= 12:
		pg = '1-' + str(i)
	elif i <= 22:
		pg = '2-' + str(i-12)
	elif i <= 32:
		pg = '3-' + str(i-22)
	elif i <= 42:
		pg = '4-' + str(i-32)
	elif i <= 50:
		pg = '5-' + str(i-42)
	else:
		pg = '6-' + str(i-50)
	tX = 0
	tY = 0
	for idx in range(len(Pointdict[pg])):
		tX +=abs(Pointdict[pg][idx][0] - MeanPoint[i-1][0])
		tY +=abs(Pointdict[pg][idx][1] - MeanPoint[i-1][1])
	diversity = pow(pow(tX/len(Pointdict[pg]), 2)+pow(tY/len(Pointdict[pg]), 2), 0.5)
	print(diversity)
	#print([pg, totallength[i-1], totalfixation[i-1], totalfixation[i-1]/totallength[i-1], fixationnum[i-1], totalfixation[i-1]/fixationnum[i-1], totallength[i-1]/fixationnum[i-1]])

'''
'''
csvname = ''
if Filter_mode == 0:
	csvname = 'ResultPages_nofilter.csv'
	with open(csvname, 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['PageID', 'Length(ms)', 'TotalFixationLength(ms)','FixatoinTimePercentage', 'FixationNumbers', 'FilteredFixationNumbers', 'FixationAvgDuration(ms)', 'MeanTimetoFixation(ms)', 'DiversityofFixations', 'DiversityofWeightedFixations'])
		for i in range(1, 63):
			if i <= 12:
				pgno = '1-' + str(i)
				pg = '1_' + str(i)
			elif i <= 22:
				pgno = '2-' + str(i-12)
				pg = '2_' + str(i-12)
			elif i <= 32:
				pgno = '3-' + str(i-22)
				pg = '3_' + str(i-22)
			elif i <= 42:
				pgno = '4-' + str(i-32)
				pg = '4_' + str(i-32)
			elif i <= 50:
				pgno = '5-' + str(i-42)
				pg = '5_' + str(i-42)
			else:
				pgno = '6-' + str(i-50)
				pg = '6_' + str(i-50)
			tX = 0
			tY = 0
			tXX = 0
			tYY = 0
			for idx in range(len(Pointdict[pgno])):
				tX +=abs(Pointdict[pgno][idx][0] - MeanPoint[i-1][0])
				tY +=abs(Pointdict[pgno][idx][1] - MeanPoint[i-1][1])
				tXX +=abs(Pointdict[pgno][idx][0] - WeightedPoint[i-1][0])
				tYY +=abs(Pointdict[pgno][idx][1] - WeightedPoint[i-1][1])
			diversity = pow(pow(tX/len(Pointdict[pgno]), 2)+pow(tY/len(Pointdict[pgno]), 2), 0.5)
			Weighteddiversity = pow(pow(tXX/len(Pointdict[pgno]), 2)+pow(tYY/len(Pointdict[pgno]), 2), 0.5)
			writer.writerow([pg, totallength[i-1], totalfixation[i-1], totalfixation[i-1]/totallength[i-1], fixationnum[i-1], F_fixationnum[i-1], totalfixation[i-1]/fixationnum[i-1], totallength[i-1]/fixationnum[i-1], diversity, Weighteddiversity])

else:
	if Filter_mode == 1:
		csvname = 'ResultPages_A.csv'
	elif Filter_mode == 2:
		csvname = 'ResultPages_B.csv'
	elif Filter_mode == 3:
		csvname = 'ResultPages_AB.csv'
	with open(csvname, 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['PageID', 'Length(ms)', 'F_TotalFixationLength(ms)','F_FixatoinTimePercentage', 'FilteredFixationNumbers', 'F_FixationAvgDuration(ms)', 'F_MeanTimetoFixation(ms)', 'F_DiversityofFixations'])
		for i in range(1, 63):
			if i <= 12:
				pgno = '1-' + str(i)
				pg = '1_' + str(i)
			elif i <= 22:
				pgno = '2-' + str(i-12)
				pg = '2_' + str(i-12)
			elif i <= 32:
				pgno = '3-' + str(i-22)
				pg = '3_' + str(i-22)
			elif i <= 42:
				pgno = '4-' + str(i-32)
				pg = '4_' + str(i-32)
			elif i <= 50:
				pgno = '5-' + str(i-42)
				pg = '5_' + str(i-42)
			else:
				pgno = '6-' + str(i-50)
				pg = '6_' + str(i-50)
			tX = 0
			tY = 0
			tXX = 0
			tYY = 0
			for idx in range(len(F_Pointdict[pgno])):
				tX +=abs(F_Pointdict[pgno][idx][0] - MeanPoint[i-1][0])
				tY +=abs(F_Pointdict[pgno][idx][1] - MeanPoint[i-1][1])
				tXX +=abs(F_Pointdict[pgno][idx][0] - WeightedPoint[i-1][0])
				tYY +=abs(F_Pointdict[pgno][idx][1] - WeightedPoint[i-1][1])
			F_diversity = pow(pow(tX/len(F_Pointdict[pgno]), 2)+pow(tY/len(F_Pointdict[pgno]), 2), 0.5)
			writer.writerow([pg, totallength[i-1], F_totalfixation[i-1], F_totalfixation[i-1]/totallength[i-1], F_fixationnum[i-1], F_fixationavglen[i-1], totallength[i-1]/F_fixationnum[i-1], F_diversity])
'''