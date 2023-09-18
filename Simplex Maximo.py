import numpy as np

def imprimir_matriz_con_formato(matriz, encabezado_fila, encabezado_columna):
    # Redondear los valores
    matriz = np.around(matriz, 3)

    # Obtener las dimensiones de la matriz
    filas = len(matriz)
    columnas = len(matriz[0]) if filas > 0 else 0

    # Imprimir el encabezado de columna
    encabezado = f"{str(encabezado_columna[0]):^8} | "  # Añade la línea vertical
    for i in range(columnas):
        encabezado += f"{str(encabezado_fila[i]):^8}"  # Ajusta el encabezado al centro
    print(encabezado)
    
    # Imprimir la línea separadora del encabezado
    linea_separadora = "-" * (8 * columnas + 2 * (columnas - 1))  # Ajusta la longitud
    print(linea_separadora)
    
    # Imprimir la matriz con formato
    for i in range(filas):
        fila = f"{str(encabezado_columna[i + 1]):^8} | "  # Añade la línea vertical
        for j in range(columnas):
            fila += f"{matriz[i][j]:^8}"  # Ajusta el valor al centro
        print(fila)
        
        # Imprimir línea separadora si no es la última fila
        if i == filas - 2:
            print("-" * (8 * columnas + 2 * (columnas - 1)))  # Ajusta la longitud

def simplex_step(tableau, n, m, encabezado_fila, encabezado_columna):
        # Encontrar la columna pivote
        j = np.argmin(tableau[-1, 1:1+n]) + 1
        
        # Encontrar la fila pivote
        ratios = np.divide(tableau[:-1, -1], tableau[:-1, j], out=np.full_like(tableau[:-1, -1], np.inf), where=(tableau[:-1, j] != 0))
        indices_positivos = np.where(ratios > 0)[0]
        i = indices_positivos[np.argmin(ratios[indices_positivos])]
        
        # Reemplazar Xi por S
        encabezado_columna[i+1] = "X" + str(j)
        
        # Hacer la fila pivote igual a 1
        tableau[i, :] /= tableau[i, j]

        # Hacer las demás filas igual a 0
        for k in range(m+1):
            if k != i:
                tableau[k, :] -= tableau[k, j] * tableau[i, :]

def main():
    print("Método Simplex - Resolucion de Problemas de Programación Lineal")
#     m = int(input("Número de restricciones: "))
#     n = int(input("Número de variables: "))
    # m = 3
    # n = 3
    m = 2
    n = 2
    
    A = np.zeros((m, n))
    b = np.zeros(m)
    c = np.zeros(n)

#     print("Ingrese los coeficientes de la matriz de coeficientes A:")
#     for i in range(m):
#         A[i] = [float(x) for x in input().split()]
    # A = [[2, 1, 1],
    #      [1, 2, 3],
    #      [2, 2, 1]]
    # b = [2, 5, 6]
    # c = [3, 1, 3]
    # c = np.array(c)

    A = [[-1, 3],
         [7, 1]]
    b = [6, 35]
    c = [7, 9]
    c = np.array(c)

#     print("Ingrese los coeficientes del vector b:")
#     b = [float(x) for x in input().split()]

#     print("Ingrese los coeficientes del vector c (función objetivo):")
#     c = [float(x) for x in input().split()]

    tableau = np.zeros((m + 1, m + n + 2))
    encabezado_fila = [""] * (m+n+2)
    encabezado_columna = [""] * (m+2) 
    
    for i in range(m):
        tableau[i, 1:n+1] = A[i]
        tableau[i, n+1+i] = 1
        tableau[i, -1] = b[i]
        encabezado_columna[i+1] = "S" + str(i+1)
        
    for j in range(n):
        encabezado_fila[1+j] = "X" + str(j+1)
        encabezado_fila[1+n+j] = "S" + str(j+1)
    
    encabezado_fila[0] = "z"
    encabezado_fila[-1] = "r"
    encabezado_columna[-1] = "z"
    tableau[-1, 1:n+1] = -c
    tableau[-1, 0] = 1

    # Imprimir la matriz inicial
    print("\n.:Tabla Simplex Inicial:.\n")
    imprimir_matriz_con_formato(tableau, encabezado_fila, encabezado_columna)

    # Ejecutar el Simplex
    while any(tableau[-1, :-1] < 0):
        print("\n.:Siguiente paso del Simplex:.\n")
        simplex_step(tableau, n, m, encabezado_fila, encabezado_columna)
        imprimir_matriz_con_formato(tableau, encabezado_fila, encabezado_columna)

    # Imprimir el resultado
    print("\n.:Resultado final:.\n")
    solucion = np.zeros(n)

    # Guardamos los valores en resultado
    for i in range(1,m+1):
        if encabezado_columna[i].startswith('X'):
            solucion[int(encabezado_columna[i][1]) - 1] = tableau[i-1, -1]
    print("Solucion:", solucion)
    print("Valor optimo:", np.dot(c, solucion))

if __name__ == "__main__":
    main()
