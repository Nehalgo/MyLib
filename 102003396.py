import pandas as pd
import sys
import math

def normalize(list):
    den=0
    for i in range(1,len(list)):
        den = den+ list[i]*list[i]
    den1 = math.sqrt(den)

    list = list.apply(lambda x: x/den1)
    return list

def main(argv):
    if len(sys.argv)!=5:
        print(" Only 5 parameters required!")
        exit()
    input = argv[1]
    weight = list(sys.argv[2].split(","))
    impact = list(sys.argv[3].split(","))
    result = argv[4]

    try:
        df=pd.read_csv(input)
    except FileNotFoundError:
        print("File not found")
        exit()

    ncol = len(df.columns)
    if ncol<3:
        print("No of columns are less than 3.")
        exit()
    if len(impact) != (ncol-1):
        print("No of impacts not equal to the number of columns.")
        exit()

    if len(weight) != (ncol-1):
        print("No of weights not equal to the number of columns.")
        exit()

    l1 = {'-','+'}
    if set(impact) != l1:
        print("Impacts should be either '+' or '-'.")
        exit()

    df["P1"] = pd.to_numeric(df["P1"], downcast="float")
    df["P2"] = pd.to_numeric(df["P2"], downcast="float")
    df["P3"] = pd.to_numeric(df["P3"], downcast="float")
    df["P4"] = pd.to_numeric(df["P4"], downcast="float")
    df["P5"] = pd.to_numeric(df["P5"], downcast="float")
    
    df1=df.copy()
    for i in range(1,len(df1.iloc[1])):
        df1.iloc[:,i] = normalize(df1.iloc[:,i])

    for i in range(1,len(df1.iloc[1])):
        df1.iloc[:,i]=df1.iloc[:,i].apply(lambda x: x*float(weight[i-1]))

    best = []
    worst = []
    for i in range(1,len(df1.iloc[1])):
        if (impact[i-1]=='+'):
            best.append(max(df1.iloc[:,i]))
            worst.append(min(df1.iloc[:,i]))
        else :
            best.append(min(df1.iloc[:,i]))
            worst.append(max(df1.iloc[:,i]))

    score=[]
    S_n = []
    S_p = []
    for i in range(len(df1)):
        dist_w, dist_b = 0,0
        for j in range(1,ncol):
            dist_w = dist_w + (df1.iloc[i,j] - worst[j-1])**2
            dist_b = dist_b + (df1.iloc[i,j] - best[j-1])**2
        dist_w = dist_w**0.5
        dist_b = dist_b**0.5
        S_n.append(dist_w)
        S_p.append(dist_b)
        score.append(dist_w/(dist_w + dist_b))

    df1['Topsis Score'] = score
    df1['Rank'] = df1['Topsis Score'].rank(method='max', ascending=False)
    df1 = df1.astype({"Rank": int})
    df1.to_csv(sys.argv[4],index=False)

if __name__=="__main__":
    main(sys.argv)