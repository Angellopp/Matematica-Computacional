import numpy as np
M = float('inf')

def imprimir_matriz_con_formato(matriz, zeta, encabezado_fila, encabezado_columna, d):
    # Redondear los valores
    matriz = np.around(matriz, 3)

    # Obtener las dimensiones de la matriz
    filas = len(matriz)
    columnas = len(matriz[0]) if filas > 0 else 0

    # Imprimir el encabezado de columna
    encabezado = f"{str(encabezado_columna[0]):^16} | "  # Añade la línea vertical
    for i in range(columnas):
        encabezado += f"{str(encabezado_fila[i]):^8}"  # Ajusta el encabezado al centro
    print(encabezado)
    
    # Imprimir la línea separadora del encabezado
    linea_separadora = "-" * (8 * columnas + 2 * (columnas - 1))  # Ajusta la longitud
    print(linea_separadora)
    
    # Imprimir la matriz con formato
    for i in range(filas):
        fila = f"{'M' if d[i] == float(2e9) else d[i]:^8}"  # Añade la línea vertical
        fila += f"{str(encabezado_columna[i + 1]):^8} | "  # Añade la línea vertical
        for j in range(columnas):
            fila += f"{matriz[i][j]:^8}"  # Ajusta el valor al centro
        print(fila)
        
        # Imprimir línea separadora si no es la última fila
        if i == filas - 1:
            print("-" * (8 * columnas + 2 * (columnas - 1)))  # Ajusta la longitud
    
    zz = f"{str(zeta[0]):^16} | "
    for i in range(columnas-1):
        zz += f"{str(zeta[i+1]):^8}"  # Ajusta el valor al centro
    print(zz)

def simplex_step(tableau, n, m, zeta, encabezado_columna, d):
    # Encontrar la columna pivote
    zeta = [float(s) for s in zeta[1:n+1]]
    # zeta = np.array(zeta)
    j = np.argmin(zeta - np.dot(d, tableau[:, :n]))
    # Encontrar la fila pivote
    ratios = np.divide(tableau[:, -1], tableau[:, j], out=np.full_like(tableau[:, -1], 'inf'), where=(tableau[:, j] != 0))
    indices_positivos = np.where(ratios > 0)[0]
    i = indices_positivos[np.argmin(ratios[indices_positivos])]
    # Reemplazar Xi por A y ci por M
    encabezado_columna[i+1] = "X" + str(j+1)
    d[i] = zeta[j]
    
    # Hacer la fila pivote igual a 1
    tableau[i, :] /= tableau[i, j]

    # Hacer las demás filas igual a 0
    for k in range(m):
        if k != i:
            tableau[k, :] -= tableau[k, j] * tableau[i, :]

def main():
    print("Método Simplex - Resolución de Problemas de Programacion Lineal")
    m = 2
    n = 3
    
    A = np.zeros((m, n))
    b = np.zeros(m)
    c = np.zeros(n)
    d = np.zeros(m)
    A = [[1, 2, 3],
         [2, 2, 1]]
    b = [5, 6]
    c = [3, 4, 5]
    c = np.array(c)

    tableau = np.zeros((m, 2*m + n + 1))
    encabezado_fila = [""] * (2*m+n+1)
    encabezado_columna = [""] * (m+1)
    zeta = [""] * (2*m+n+1)
    
    M = 2e9

    for i in range(m):
        d[i] = M
        tableau[i, :n] = A[i]
        tableau[i, n+2*i] = -1
        tableau[i, n+2*i+1] = 1
        tableau[i, -1] = b[i]
        encabezado_fila[n+2*i] = "S" + str(i+1)
        encabezado_fila[n+2*i+1] = "A" + str(i+1)
        encabezado_columna[i+1] = "A" + str(i+1)
        zeta[n+2*i+1] = str(0)
        zeta[n+2*i+2] = "M"
        
    for j in range(n):
        encabezado_fila[j] = "X" + str(j+1)
    
    encabezado_fila[-1] = "r"
    zeta[0] = "z"
    zeta[1:n+1] = [str(v) for v in c]

    # Imprimir la matriz inicial
    print("Tabla Simplex Inicial:")
    imprimir_matriz_con_formato(tableau, zeta, encabezado_fila, encabezado_columna, d)

    # Ejecutar el Simplex
    while any([float(s) for s in zeta[1:n+1]] - np.dot(d, tableau[:, :n]) < 0):
        print("\nSiguiente paso del Simplex:")
        simplex_step(tableau, n, m, zeta, encabezado_columna, d)
        imprimir_matriz_con_formato(tableau, zeta, encabezado_fila, encabezado_columna, d)

    # Imprimir el resultado
    print("\nResultado final:")
    solucion = np.zeros(n)

    # Guardamos los valores en resultado
    for i in range(1,m+1):
        if encabezado_columna[i].startswith('X'):
            solucion[int(encabezado_columna[i][1]) - 1] = tableau[i-1, -1]
    print("Solucion:", solucion)
    print("Valor optimo:", np.dot(c, solucion))

if __name__ == "__main__":
    main()
