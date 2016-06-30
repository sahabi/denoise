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
			imageBuilder[i][j] = -1

	for i, row in enumerate(evals):
		state = row[0]
		action = row[1]
		evaluation = row[2]
		if i == 0:
			currentState = state
			currentCol = 0
			imageBuilder[1-action][currentCol] = evaluation
			actionLast = action
		else:
			if state == currentState:
				if action == actionLast:
					action = 1 - action
					evaluation = 1 - evaluation
				if imageBuilder[1-action][currentCol] == -1:
					imageBuilder[1-action][currentCol] = evaluation
				else:
					currentCol = currentCol + 1
					imageBuilder[1-action][currentCol] = evaluation
					imageBuilder[action][currentCol] = -1
			else:
				currentState = state
				currentCol = currentCol + 1
				imageBuilder[1 - action][currentCol] = evaluation
				imageBuilder[action][currentCol] = -1
			actionLast = action

	for i in range(len(evals)):
		if imageBuilder[0][i] != -1:
			imageBuilder[0][i] = 1 - imageBuilder[0][i]
######
	deNoiseImage = list_2D(currentCol, ROW)
	finalDeNoiseImage = list_2D(currentCol, ROW)
	count = 0
	nNew = currentCol
	imageBuilder = imageBuilder[:][0:nNew+1]	

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

	for i in range(ROW):
		for j in range(nNew):

			if (g.get_segment(j+i*nNew)):
				deNoiseImage[i][j] = 1
			else:
				deNoiseImage[i][j] = 0

	for j in range(nNew):
		finalDeNoiseImage[0][j] = 1 - deNoiseImage[0][j]
		finalDeNoiseImage[1][j] = deNoiseImage[1][j]

	return (flow, deNoiseImage, finalDeNoiseImage, imageBuilder)

if __name__ == "__main__":
	denoise(getEvals(),.3,.5)