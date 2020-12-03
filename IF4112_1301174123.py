
import random
import math

x1 = [-3,3]
x2 = [-2,2]
pop_num = 75 # jumlah populasi per generasi
generasi = 1000 // pop_num #maksimal jumlah generasi
seleksi_ortu_num = 20 # jumlah anak
cross_prob = 0.9 #probabilitas croosover
mutasi_prob = 0.5 # probabilitas mutasi
nilai = 0.5  # kalkulasi crossover
t = 50 #maks seleksi ortu
best_prob = 0.05
creep = 0.001
stop = 100



def generate_ortu(pop_num): #menciptakan populasi
    popls = []
    for i  in range (pop_num):
        kromosom = []
        kromosom.append(random.uniform(0, 1))
        kromosom.append(random.uniform(0, 1))
        popls.append(kromosom)
    return popls

def dekodeKromosom(value,x): #mendekode kromosom dan menjadikan nilainya real
     return (value * (abs(x[0]) + abs(x[1]))) - abs(x[0]) 


def rumus ( x, y) : # rumus yang ada di soal
    a= 4-(2.1*x**2) + (x**4/3)*x**2
    b = x*y 
    c = -4+(4*y**2)*y**2  
    return a+b+c



def fitness (value): # rumus  minimum nilai fitness
    return 1/(value+1)

def kromosomFit(pops,x1,x2):  #cari kromosom fitnes
    fit = []
    for i in range (len(pops)):
        kromosom_fit = []
        kromosom_fit.append(i)
        kromosom_fit.append(fitness(rumus(dekodeKromosom(pops[i][0], x1),dekodeKromosom(pops[i][1],x2))))
        fit.append(kromosom_fit)
    return fit




def seleksiOrtu (fitnesse, num_ortu, pops, best_prob, t): #menseleksi orangtua yang terpilih
    seleksi_ortu = []
    for i in range(num_ortu):
        turnament = []
        pilih = []
        dipilih =  False
        for  j in range(t):
            while True:
                psi = random.randrange(len(pops))
                if psi not in pilih:
                    pilih.append(psi)
                    break
            turnament.append(fitnesse[psi])
        rand = random.uniform(0, 1)
        turnament.sort(key = lambda x: x[1] , reverse = True)
        prev = 0
        for j in range (t):
            if rand >= prev and rand <= (1 - (best_prob * ((1-best_prob) ** j))):
                seleksi_ortu.append(pops[turnament[j][0]])
                dipilih = True
                break
            prev = 1 - (best_prob * ((1- best_prob) ** j))
        if dipilih == False:
            seleksi_ortu.append(pops[turnament[t-1][0]])
                                
    return seleksi_ortu

def crossover (ortu, cross_prob, nilai, mutasi_prob, creep):
        anak = []
        for i in range(0,len(ortu),2):
            a = random.uniform(0,1)
            if a >= (1 - cross_prob):
                anak_kr = []
                n_x = (nilai * ortu[i][0]) + ((1 - nilai) * ortu[i + 1][0])
                n_y = (nilai * ortu[i][1]) + ((1 - nilai) * ortu[i + 1][1])
                anak_kr.append(n_x)
                anak_kr.append(n_y)
                anak.append(mutasi(anak_kr, mutasi_prob, creep))
                anak.append(mutasi(anak_kr, mutasi_prob, creep))
            else:
                mutasi(ortu[i], mutasi_prob, creep)
                mutasi(ortu[i + 1], mutasi_prob, creep)
                anak.append(ortu[i])
                anak.append(ortu[i + 1])
        return anak

def mutasi(anak, mutasi_prob, creep):
        a = random.uniform(0, 1)
        if a <= cross_prob:
            xy = random.choice([0,1])
            s = random.choice([ (-1 * creep), creep])
            if(s == (-1 * creep)):
                if(anak[xy] <= creep):
                    anak[xy] = 0
                else:
                    anak[xy] += s
            elif(s == creep):
                if(anak[xy] >= (1- creep)):
                    anak[xy] = 1
                else :
                    anak[xy] += s
        return anak

def gantiPopulasi(pops, anak,x1 ,x2):
        populasi_fit = kromosomFit(pops,x1,x2)
        populasi_fit.sort(key = lambda x : x[1] , reverse = True)
        populasi_fit = populasi_fit[:len(populasi_fit) - (len(pops)-len(anak))]
        populasi_fit.sort(key=lambda x: x[0], reverse=True)
        for i in populasi_fit:
            pops.pop(i[0])
        for i in  anak:
            pops.append(i)
        return pops



def best_individu(pops, x1,x2):
        populasi_fit = kromosomFit(pops,x1,x2)
        populasi_fit.sort(key=lambda x: x[1] , reverse =True)
        return populasi_fit[0] [0]

    

#main Program
pops  = generate_ortu(pop_num)
solusi = pops[best_individu(pops,x1,x2)]
sc = 0
for  i in range (generasi):
    fts = kromosomFit(pops, x1,x2)
    seleksi_ort = seleksiOrtu(fts, seleksi_ortu_num,pops,best_prob,t)
    anak = crossover(seleksi_ort, cross_prob, nilai, mutasi_prob, creep)
    gantiPopulasi(pops, anak, x1, x2)
    best = pops[best_individu(pops,x1,x2)]
    if (rumus(dekodeKromosom(best[0], x1), dekodeKromosom(best[1],x2)) < rumus(dekodeKromosom(solusi[0], x1),dekodeKromosom(solusi[1],x2))): 
        sc = 0
        solusi = best
    else:
        sc += 1
    if sc >= stop:
                
        break   

                                    
                                
print()                               

print(kromosomFit(pops,x1,x2))
print(rumus(dekodeKromosom(solusi[0],x1), dekodeKromosom(solusi[1],x2)))
                                    
            

                                       
    


