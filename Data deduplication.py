#Author:Ranchal Prakash (150107047) IIT Guwahati
# Importing the libraries
import pandas as pd
import datetime

# Importing the dataset
dataset = pd.read_csv('Deduplication Problem - Sample Dataset.csv')
m,n= dataset.shape
#Converting date of birth into datetime format
for i in range(m):
    if datetime.datetime.strptime(dataset.dob[i],"%d/%m/%y") > datetime.datetime.strptime("01/01/20","%m/%d/%y"):
        dataset.dob[i]=datetime.datetime.strptime(dataset.dob[i],"%d/%m/%y")-datetime.timedelta(days=(100*365.24+1))
    else:
        dataset.dob[i]=datetime.datetime.strptime(dataset.dob[i],"%d/%m/%y")

#sorting w.r.t date of birth
dataset.sort_values(['dob'],inplace = True)
dataset.reset_index(drop=True, inplace=True)

#Creating resultant matrix 
end=1;freq=1;
result = pd.DataFrame(columns=dataset.columns) 


#String matching function, Similar to levenshtein distance
def LD(s, t):
    if s == "":
        return len(t)
    if t == "":
        return len(s)
    for i in range(min(len(t),len(s))):
        if s[i] == t[i]:
            cost = 0
        else:
            cost = 1
       
    res = cost+max(len(t),len(s))-i;
    return res
#Finding duplicate names
result.loc[0]=dataset.loc[0]
s=" ";
for i in range(1,m):
    flag=1; 
    j=1
    while ((dataset.dob.iloc[i]==result.dob.iloc[end-j]) & (j<=end)): 
        if dataset.gn.iloc[i]==result.gn.iloc[end-j]:
            fn_flag=0;
            ln_flag=0;
            fn=dataset.fn.iloc[i].split()
            ln=dataset.ln.iloc[i].split()
            unq_fn=result.fn.iloc[end-j].split()
            unq_ln=result.ln.iloc[end-j].split()

            for k in range(len(fn)):
                low_fn=len(fn[k])
                for p in range(len(unq_fn)):
                    if (len(fn[k])==1) & (fn[k]==unq_fn[p][0]):
                        fn[k]=unq_fn[p]
                    elif (len(unq_fn[p])==1) & (unq_fn[p]==fn[k][0]):
                        unq_fn[p]=fn[k]
                    l_dist=LD(fn[k],unq_fn[p])
                    if l_dist<low_fn:
                        low_fn=l_dist
                if (low_fn<2) & (len(fn[k])>2):
                    fn_flag=1;
            for u in range(len(ln)):
                low_ln=len(ln[u])
                for v in range(len(unq_ln)):
                    if (len(ln[u])==1) & (ln[u]==unq_ln[v][0]):
                        ln[u]=unq_ln[v]
                    elif (len(unq_ln[v])==1) & (unq_ln[v]==ln[u][0]):
                        unq_ln[v]=ln[u]
                    l_dist=LD(ln[u],unq_ln[v])
                    if l_dist<low_ln:
                        low_ln=l_dist
                if (low_ln<2) & (len(ln[u])>2):
                    ln_flag=1;
            if (fn_flag==1) & (ln_flag==1):
                flag=0
                result.fn.iloc[end-j]=s.join(list(set().union(fn,unq_fn)))
                result.ln.iloc[end-j]=s.join(list(set().union(ln,unq_ln)))
                break
            else:
                freq=freq+1
        j=j+1
    if ((dataset.dob.iloc[i]!=result.dob.iloc[end-j]) & (flag==1)):
        freq=1
    if flag==1:
        result.loc[end]=dataset.loc[i]
        end=end+1
result.to_csv('unique_data.csv')
                           
                
