import csv
import sys

def biologicalSequenceAlignment(a, b, matchReward, mismatchPenalty, gapPenalty):
    
    # Initializing scoring matrix
    m, n = len(b), len(a)

    arr = [[0] * (n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        arr[i][0] = i * gapPenalty
    for j in range(1, n+1):
        arr[0][j] = j * gapPenalty

    for i in range(1, m+1):
        for j in range(1, n+1):
            matchingStringScore = matchReward if (b[i-1] == a[j-1]) else mismatchPenalty
            diagonal = arr[i-1][j-1] + matchingStringScore
            left = arr[i][j-1] + gapPenalty
            up = arr[i-1][j] + gapPenalty
            arr[i][j] = max(diagonal, left, up)

    # Backtracking 
    alignmentA = ''
    alignmentB = ''
    i, j = m, n
    while i > 0 or j > 0:
        matchingStringScore = matchReward if (b[i-1] == a[j-1]) else mismatchPenalty
        diagonal = arr[i-1][j-1] + matchingStringScore
        left = arr[i][j-1] + gapPenalty
        up = arr[i-1][j] + gapPenalty
        scores = (diagonal, left, up)

        # Comparing maximum scores to determine direction
        mergedScores = {}
        for k in range(len(scores)):
            mergedScores[scores[k]] = k
            
        maxScore = float("-inf")
        for score in scores:
            if score > maxScore:
                maxScore = score

        for score, index in mergedScores.items():
            if score == maxScore:
                direction = index
                break

        # Diagonal
        if direction == 0:
            if len(alignmentA) == len(alignmentB):
                alignmentA = a[j-1] + alignmentA
                alignmentB = b[i-1] + alignmentB
            else:
                alignmentA = '-' + alignmentA
                alignmentB = '-' + alignmentB
            i -= 1
            j -= 1
        
        # Left
        elif direction == 1:
            alignmentA = a[j-1] + alignmentA
            alignmentB = '-' + alignmentB
            j -= 1
        
        # Up
        else:
            alignmentA = '-' + alignmentA
            alignmentB = b[i-1] + alignmentB
            i -= 1

        # Adds gaps when necessary
        if len(alignmentA) > len(alignmentB):
            alignmentB = '-' * (len(alignmentA) - len(alignmentB)) + alignmentB

    return alignmentA, alignmentB, arr[-1][-1]


if len(sys.argv) > 1:
    with open(sys.argv[1], 'r') as file:
        csvreader = list(csv.reader(file))[1:]
        for row in csvreader:
            input = biologicalSequenceAlignment(row[0],row[1],1,-1,-2)
            print(input[0],input[1],input[2])