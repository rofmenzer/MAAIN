def matXvec(C, L, I, U):
   
   V = [0,] * len(U)
   # u =  [1, 2, 3, 4]
   for i in range(len(U)):
      
      for j in range(L[i], L[i+1]):
         V[i] += (C[j] * U[I[j]]) 

   return(V)


def CLI(mat):
    C = []
    L = []
    I = []

    lval = 0
    
    for i in range(len(mat)):
        L.append(lval)
        ival = 0
        for j in range(len(mat[i])):
            if(mat[i][j] != 0):
                C.append(mat[i][j])
                
                lval = lval + 1

                I.append(ival)
            ival = ival + 1    
            
    L.append(lval)

    return (C,L,I)



mat = [[0,0,1,0],[2,3,0,4],[0,5,6,7],[0,0,0,0]]
(C,L,I) = CLI(mat)
print(C,L,I)

print(matXvec(C,L,I, [1, 2, 3, 4]))


#matXvec([1/2, 1/2, 1/3, 1/3, 1/3, 1/3, 1], [0, 2, 2, 5, 6], [1, 2, 0, 1, 3, 2], [1, 2, 3, 4])
