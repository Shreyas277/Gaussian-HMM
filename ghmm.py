# Ganapati bappa moraya
import random
import numpy as np
import matplotlib.pyplot as plt

timestamp=100
d=5
k=10
features=7
y = np.random.rand(1, timestamp)
y=y.astype(int)
x= np.random.rand(features, timestamp)

T=np.ones((k,k))
Priors=[(1/k)]*features
Intial_Transition_probabilities=np.array([ [(d/(d+k-1)) if i==j else 1/(d+k-1) for i in range(k)] for j in range(k) ])

Intialised_list = random.choices(range(1, k+1), k=100)
print(Intialised_list)
def gaussain(mu,sigma,x):
    values=(1/(np.sqrt(2*np.pi)*sigma))*np.exp(-0.5*((x-mu)**(2))*(1/sigma**2))
    return values

# I am going to design this function in such a way that given the current iteration it would give me the mean, covarience parameters from it.
def mean_cov(L,features,k):
    num_cluster={}
    mean_cluster=[]
    std_cluster=[]
    for i in range(1,k+1):
        num_cluster[i]=[]
    for i in range(1,timestamp): 
        num_cluster[L[i]].append(x[:,i])
    print(num_cluster[1])
    for i in range(1,k+1):
        mean=[0]*features
        square=[0]*features
        for j in range(len(num_cluster[i])):
            mean+=num_cluster[i][j]
            square+=(num_cluster[i][j])**2
        mean=mean*(1/len(num_cluster[i]))
        std=np.sqrt(square*(1/len(num_cluster[i]))-(mean)**2)
        mean_cluster.append(mean)
        std_cluster.append(std)
    
    return mean_cluster,std_cluster
mean_cluster,std_cluster=mean_cov(Intialised_list,features,k)

#Now we have obtained the intalised mean and the covarience so we should go on and construct the probability matrix for the entire timestamps and states
def construct_gaussain_matrix(mean_cluster,std_cluster,x,y):
    mean_cluster,std_cluster=np.array(mean_cluster),np.array(std_cluster)
    Gaussain_matix=np.array([[[0.0]*features]*k]*timestamp)
    for i in range(timestamp):
        for j in range(k):
            Gaussain_matix[i][j]=gaussain(mean_cluster[j],std_cluster[j],x[:,i])
    return Gaussain_matix

Gaussian_Matrix=construct_gaussain_matrix(mean_cluster,std_cluster,x,y)

def markov_probab_of_state_k(Transition_probab_Matrix, Gaussian_Matrix,state,timestamp):
    term2_whole=np.array([Gaussian_Matrix[timestamp][q]*Transition_probab_Matrix[q][state] for q in range(k)])
    return term2_whole.sum(axis=0)

def posterior_gaussian_probab(Transition_probab_Matrix, Gaussian_Matrix,Priors):
    Posterior_Matrix=Gaussian_Matrix.copy()
    for i in range(timestamp):
        term3=[]
        for j in range(k):
        #We want to find the probability of the state k given y
        #First probability of y given k thats just the old term of gaussian
            term1=np.array(Gaussian_Matrix[i][j])
            # probability that the state it self is k now this can be broken down into 2 scenarios
            # case1 where the t=0 where each state is equally likely 
            # case 2 where t>0 and the probability of that particular state would depend on the summation of the 
            # probability of the prev state into probability to transition to this state k.
            if i==0:
                term2=np.array(Priors)
            else:
                term2=markov_probab_of_state_k(Transition_probab_Matrix,Gaussian_Matrix,j,i)
                term3.append(term2)
            #print(term1)
            #print(term2)
            Posterior_Matrix[i][j]=term1*term2
        term3=np.array(term3)
        term3=term3.sum(axis=0)
        for j in range(k):
            Posterior_Matrix[i][j]*=(1/term3)
    return Posterior_Matrix

Posterior_Matrix=posterior_gaussian_probab(Intial_Transition_probabilities,Gaussian_Matrix,Priors)

print("The Gaussian Matrix is")
print(Gaussian_Matrix[3])
print("The Posterior Matrix is")
print(Posterior_Matrix[3])

#Now we need to find the transition probabilty from i to state j for time=t
def prob_i_to_j(i,j,Posterior_Matrix,Old_Transition_Matrix,timestamp):
    #New_Transition_mat=np.zeros(Old_Transition_Matrix.shape)
    print('*'*8)
    print(Posterior_Matrix[timestamp-1][4])
    print(Old_Transition_Matrix[4][j])
    #prob_state_i=np.array([Posterior_Matrix[timestamp-1]*Old_Transition_Matrix[:,j]]).sum(axis=0)
    elem=np.array([Posterior_Matrix[timestamp-1][q]*Old_Transition_Matrix[q][j] for q in range(k)])
    elem=elem.sum(axis=0)
    
    #now the probability that we came from the state i given that next state is j is given by
    p_i_to_j=Posterior_Matrix[timestamp-1][i]*Old_Transition_Matrix[i][j]*(1/prob_state_i)
    return p_i_to_j

A=np.array([[1,2],[2,3]])
B=np.array([1,2])
print(A.shape)
print(B.shape)

P=prob_i_to_j(2,3,Posterior_Matrix,Intial_Transition_probabilities,timestamp)
print(P)
'''
def constructing_probability_matrix(mean_cluster, )

print(mean_cluster)

'''


