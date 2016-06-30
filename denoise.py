from math import log
import maxflow
import sys
from Moutils.Moutils import list_2D

def denoise(evals,param_arg,betaswtr_arg,states):

	param = param_arg
	betaswtr = betaswtr_arg
	ROW = 2

	w1 = -log(1 - param)
	w2 = -log(param)
	wh = -log(0.5)

	evals.sort()

	evaluations = evals

	nCols = 0
	NEVALS = len(evals)
	g = maxflow.Graph[float](200, 200)

	imageBuilder = list_2D(NEVALS, ROW)

	for i in range(ROW):
		for j in range(NEVALS):
			imageBuilder[i][j] = 9

	nodeNumber = 0
	actionLast = [0,0]

	for i in range(NEVALS):

		if evaluations[i][0] > nodeNumber:

			if actionLast[0] > actionLast[1]:
				imageBuilder[1][nCols+actionLast[1]] = 0
				nCols = nCols + actionLast[0]
			elif actionLast[1] > actionLast[0]:
				imageBuilder[0][nCols+actionLast[0]] = 0
				nCols = nCols + actionLast[1]
			else:
				nCols = nCols + actionLast[1]

			actionLast[0] = 0
			actionLast[1] = 0
			nodeNumber += 1

			if nodeNumber > states:
				break

		if evaluations[i][1] == 0:

			if actionLast[0] == actionLast[1] or actionLast[0] < actionLast[1]:
				imageBuilder[0][nCols+actionLast[0]] = 1 - evaluations[i][2]
				actionLast[0] = actionLast[0] + 1
			else:
				imageBuilder[1][nCols+actionLast[1]] = 1 - evaluations[i][2]
				actionLast[1] = actionLast[1] + 1

		else:

			if actionLast[1] == actionLast[0] or actionLast[1] < actionLast[0]:
				imageBuilder[1][nCols+actionLast[1]] = evaluations[i][2]
				actionLast[1] = actionLast[1] + 1
			else:
				imageBuilder[0][nCols+actionLast[0]] = evaluations[i][2]
				actionLast[0] = actionLast[0] + 1

	if actionLast[0] > actionLast[1]:
		imageBuilder[1][nCols+actionLast[1]] = 3
		nCols = nCols + actionLast[0]
	elif actionLast[0] > actionLast[1]:
		imageBuilder[0][nCols+actionLast[0]] = 3
		nCols = nCols + actionLast[1]
	else:
		nCols = nCols + actionLast[1]

	deNoiseImage = list_2D(nCols, ROW)
	finalDeNoiseImage = list_2D(nCols, ROW)
	count = 0
	nNew = nCols	

	for i in range(ROW):
		for j in range(nNew):
			g.add_nodes(1)
			if imageBuilder[i][j] == 0:
				g.add_tedge(j+i*nNew,w1,w2)
			else:
				g.add_tedge(j+i*nNew,w2,w1)

	for i in range(nNew - 1):
		g.add_edge( i,i+1, betaswtr, betaswtr );
		g.add_edge( i+nNew,i+1+nNew, betaswtr, betaswtr );
		g.add_edge( i, i+nNew, betaswtr, betaswtr );	

	g.add_edge( nNew-1,2*nNew-1, betaswtr, betaswtr );

	flow = g.maxflow();
	#print 'Maxflow Value: {}'.format(flow)
	for i in range(ROW):
		for j in range(nNew):
			#print g.get_segment(j+i*nNew)
			if (g.get_segment(j+i*nNew)):
				deNoiseImage[i][j] = 1
			else:
				deNoiseImage[i][j] = 0

	#print 'Denoised Image:'
	#print deNoiseImage

	for j in range(nNew):
		finalDeNoiseImage[0][j] = 1 - deNoiseImage[0][j]
		finalDeNoiseImage[1][j] = deNoiseImage[1][j]

	#print 'Final Denoised Image:'
	#print finalDeNoiseImage

	return (flow, deNoiseImage, finalDeNoiseImage, imageBuilder)


if __name__ == "__main__":
	denoise(getEvals(),.3,.5)