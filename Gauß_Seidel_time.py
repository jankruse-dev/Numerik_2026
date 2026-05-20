import numpy as np 
import time 

# Erstellung einer Beispielmatrix anhand der vorgegebenen Code.py
def gen_matrix(size):
    '''
    Generiert ein size x size lineares Gleichungssystem.

    Parameters
    ----------
    size : int
        Gewuenschte Groesse des LGS.

    Returns
    -------
    A : numpy.array
        Koeffizientenmatrix.
    b : numpy array
        rechte Seite des Gleichungssystems.

    '''
    A = (np.diag(np.full(size, 4)) + 
         np.diag(np.full(size,-1), k=1)[:-1, :-1] + 
         np.diag(np.full(size,-1), k=-1)[:-1,:-1])
    b = np.arange(0, size)
    return (A, b)

# Konvergenzkriterien prüfen
## Symmetrie 
def symmetrie(matrix):
    n = matrix.shape[0]
    if np.allclose(matrix, matrix.T):
        print(f'{n}x{n}-Matrix ist symmetrisch')
        return True
    else:
        print(f'{n}x{n}-Matrix nicht symmetrisch')
        return False

## Positiv definit
### Zeilensummenkriterium 
def sum_krit(matrix):
    n = matrix.shape[0]
    for i in range(n): # Zeilenindex
        # Zeile i als 1d-Array festlegen
        row = matrix[i] 
        # Boolsche Maske definieren, Array mit True
        maske = np.ones(len(row), dtype=bool) 
        # Hauptdiagonalelement --> Zeilenindex = Spaltenindex i=j
        maske[i] = False # Hauptdiagonalelement nicht mit summieren
        krit = abs(np.sum(row[maske])) / abs(row[i]) # Summe aller Zeilenelemente / Hauptdiagonalelement
        if krit >= 1:
            print(f'{n}x{n}-Matrix ist NICHT positiv definit')
            break
            
    print(f'{n}x{n}-Matrix ist positv definit')
    
    return True 

# Liste mit den benötigten Matrizendimensionen
sizes = [10, 100, 200, 400, 600, 800, 1000, 2000, 4000, 6000, 8000, 10000]

# Dictionary mit den benötigten Matrizen in Form von {'size':[A, b]}
A_dict = {}

# Alle benötigten Matrizen erstellen
for size in sizes:
    A, b = gen_matrix(size) # A, b für size berechnen
    A_dict.setdefault(f'{size}', []).append(A) # A in Liste einsetzen (setdefault erstellt Liste)
    A_dict.setdefault(f'{size}', []).append(b) # A in Liste einsetzen (Liste wird erkannt)
    A_dict.setdefault(f'{size}', []).append(np.zeros(size, dtype=float)) # Startvektor x_0 als Nullvektor


def check_konvergenz(A_dict):
    
    for size, Matrix in A_dict.items():
        A = Matrix[0] # Matrix aus Dict extrahieren
        sym = symmetrie(A)
        # Wenn nicht symmetrisch oder positiv definit dann löschen
        if not sym:
            del A_dict[f'{size}']
        pos = sum_krit(A)
        if not pos:
            del A_dict[f'{size}']
    return A_dict

def gauss_solver_matrix(A, b, x_0, accuracy: int = 1e-4):
    '''
    Ax = b
    Solver nach Gauss-Seidel in Matrixschreibweise

    A --> Ausgangsmatrix
    b --> Ergebnisvektor
    x --> Startvektor als Nullvektor
    accuracy --> Genauigkeit der Annäherung

    Return 
    -----
    Vektor x -> numpy.ndarray
    '''
    # strikte linke untere Dreiecksmatrix aus A erstellen
    L = np.tril(A, k=-1)
    # strikte rechte obere Dreiecksmatrix aus A erstellen
    R = np.triu(A, k=1)
    # Diagonalmatrix aus A erstellen
    D = np.diag(np.diag(A))
    # Probe ob A = L + D + R --> True 
    if not np.allclose(A, L + D + R):
        raise ValueError('A ≠ L + D + R')
    
    # Solverlogik 
    x_m = x_0
    r = 1

    # Inverse berechnen
    inverse = np.linalg.inv(D + L)
    
    # Iterationschritt
    m = 0 
    while r >= accuracy:
        # Gauss-Seidel-Verfahren
        x_m_new = -inverse @ R @ x_m + inverse @ b
        # Berechung des Residuums 
        r = np.linalg.norm(b - A @ x_m_new) 
        # Alten Iterationschritt überschreiben
        x_m = x_m_new

        m += 1

    # Probe --> Ax = b --> berücksichtigt die Genauigkeit der Annäherung
    if not np.allclose(b, A @ x_m_new, atol=accuracy):
        raise ValueError(f'Probe fehlgeschlagen: {A @ x_m_new} ≠ {b}')

    print(f'Ergebnis nach {m} Iterationsschritten')    

    x_solve = x_m_new
    return x_solve

def gauss_solver_index(A, b, x_0, accuracy:int = 1e-4):
    '''
    Ax = b
    Solver nach Gauss-Seidel in Indexschreibweise

    A --> Ausgangsmatrix
    b --> Ergebnisvektor
    x --> Startvektor als Nullvektor
    accuracy --> Genauigkeit der Annäherung

    Return 
    -----
    Vektor x -> numpy.ndarray
    '''
    # Residuum initialisieren
    r = 1

    # Nullvektor als für die erste Iteration
    x = x_0 # x_m --> Loesungsvektor x

    m = 0 # Anzahl der Iterationen
    # Dimension der Matrix bestimmen
    n = A.shape[0]
    # Schleife solange bis das Residuum kleiner gleich ist als die geforderte Genauigkeit
    while r >= accuracy:
        for i in range(n): # Zeilenindex i 
            # Summen entsprechen Skalarprodukten
            x[i] = ((b[i] - 
                    np.dot(A[i, :i], x[:i]) - # Summe der aktuellen Iteration
                    np.dot(A[i, i+1:], x[i+1:])) # Summe der letzten Iteration
                    / A[i, i])
        
        # Iterationschritt erweitern
        m += 1
        # Berechung des Residuums 
        r = np.linalg.norm(b - A @ x)

    # Probe --> Ax = b --> berücksichtigt die Genauigkeit der Annäherung
    if not np.allclose(b, A @ x, atol=accuracy):
        raise ValueError(f'Probe fehlgeschlagen: {A @ x} ≠ {b}')
             
    print(f'Ergebnis nach {m} Iterationsschritten')
    return x
            
#A_dict = check_konvergenz(A_dict)           

A = A_dict['10'][0]
b = A_dict['10'][1]
x = A_dict['10'][2]

# Laufzeit Matrixschreibweise
time_start_matrix = time.time()

for matrix in A_dict.values():
    A = matrix[0]
    b = matrix[1]
    x = matrix[2]
    x_solve = gauss_solver_matrix(A, b, x)

time_end_matrix = time.time()

time_matrix = time_end_matrix - time_start_matrix
min = time_matrix // 60
sek = time_matrix % 60
print(f'Berechnung in Matrixschreibweise in {min:.0f}:{sek:.0f}')

# Laufzeit Indexschreibweise
time_start_index = time.time()

for matrix in A_dict.values():
    A = matrix[0]
    b = matrix[1]
    x = matrix[2]
    x_solve = gauss_solver_index(A, b, x)

time_end_index = time.time()

time_index = time_end_index - time_start_index

min = time_index // 60
sek = time_index % 60
print(f'Berechnung in Matrixschreibweise in {min:.0f}:{sek:.0f}')




        
    






    
    

    







    




