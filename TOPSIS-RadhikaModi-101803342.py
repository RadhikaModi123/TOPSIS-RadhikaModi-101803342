import sys
import pandas as pd
def main():
    if len(sys.argv)!=5:
        raise Exception('Incorrect number of parameters!')
    try:
        df=pd.read_csv(sys.argv[1])
        if len(df.columns)<3:
            raise Exception('Input file must contain three or more columns!')
        df1=df.copy()
        w=sys.argv[2].split(',')
        im=sys.argv[3].split(',')
        if len(w)!=(len(df.columns)-1) or len(im)!=(len(df.columns)-1):
            raise Exception('Number of weights,impacts and columns are not same!')
        def solve(n):
            s=0
            for x in n:
                s=s+x**2
            r=s**(1/2)
            return r
        i=1
        while i<len(df.columns):
            r=solve(df.iloc[:,i])
            df.iloc[:,i]=df.iloc[:,i].apply(lambda x:x/r)
            i=i+1
        i=0
        while i<len(w):
            w[i]=float(w[i])
            i=i+1
        i=1
        while i<len(df.columns):
            df.iloc[:,i]=df.iloc[:,i].apply(lambda x:x*w[i-1])
            i=i+1
        l1=['V+']
        l2=['V-']
        i=1
        while i<len(df.columns):
            if im[i-1]=='+':
                l1.append(df.iloc[:,i].max())
                l2.append(df.iloc[:,i].min())
            else:
                l1.append(df.iloc[:,i].min())
                l2.append(df.iloc[:,i].max())
            i=i+1
        df=df.append(pd.Series(l1,index=df.columns),ignore_index=True)
        df=df.append(pd.Series(l2,index=df.columns),ignore_index=True)
        l1=[]
        l2=[]
        rows=df.shape[0]
        temp=rows-2
        j=0
        while j<temp:
            s1,s2=0,0
            i=1
            while i<len(df.columns):
                s1=s1+(df.iloc[j,i]-df.iloc[rows-2,i])**2
                s2=s2+(df.iloc[j,i]-df.iloc[rows-1,i])**2
                i=i+1
            l1.append(s1**(1/2))
            l2.append(s2**(1/2))
            j=j+1
        df.drop([rows-1,rows-2],inplace=True)
        df['S+']=l1
        df['S-']=l2
        df['S+ + S-']=df['S+']+df['S-']
        df1['Topsis Score']=df['S-']/df['S+ + S-']
        df1['Rank']=df1['Topsis Score'].rank(ascending=False)
        df1.to_csv(sys.argv[4],index=False)
    except FileNotFoundError:
        print('File not found!')
    
if __name__=="__main__":
    main()

