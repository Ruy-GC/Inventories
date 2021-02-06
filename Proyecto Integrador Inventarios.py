from pathlib import Path
import prodCol
import vendCol
import ventCol

def load_file(filename):
    """Funcion que busca el archivo csv que recibe y lo carga a una matriz"""
    file = open(Path.cwd()/filename)
    items = file.readlines()[1:]
    file.close()
    
    matriz_items = []
    
    for item in items:
        item = item.strip()
        matriz_items.append(item.split(','))
        
    return matriz_items

def muestra_matriz_consulta(matriz):
    """ recibe una matriz y la imprime con tabulación entre cada
    elemento de la fila"""
    
    for i in matriz:
        for x in i:
            print(x, end = "\t")
        print()

def guardar_datos(productos, vendedores, ventas):
    """opcion del menú 7: escribe los datos de las matrices en sus archivos
    correspondientes"""

    files = ['Productos.csv', 'Vendedor.csv', 'Ventas.csv']
    for i in range(3):
        if i == 0:
            item_string =prodCol.NAMES + "\n"
            matriz_a_guardar = productos
        elif i == 1:
            item_string = vendCol.NAMES + "\n"
            matriz_a_guardar = vendedores
        else:
            item_string = ventCol.NAMES + "\n"
            matriz_a_guardar = ventas
            
        for fila in matriz_a_guardar:
            for columna in fila:
                item_string = item_string + str(columna) + ","
            item_string = item_string[:-1] + "\n"
            
            
            item_file = open(Path.cwd() / files[i], 'w')
            item_file.write(item_string)
            item_file.close()
            
def obten_atributo(archivo, columna):
    """muestra el valor que se ecuentra en una celda"""
    return archivo[columna]

def obten_todo_de_columna (archivos, columna):
    """carga en una matriz llamada "datos" toda la información que se
    encuentre en el archivo y la columna ingresado"""
    
    datos = []
    for archivo in archivos:
        if columna == prodCol.NOMBRE or columna == vendCol.NOMBRE or \
           columna == vendCol.SEXO or columna == prodCol.MARCA:
            datos.append(archivo[columna].upper())
        else:
            datos.append(archivo[columna])
    return datos

def obten_todo_con_valor (archivos, columna, valor):
    """carga en una matriz llamada "datos" toda la fila del excel
    que tenga el valor dado dentro de la columna del archivo ingresado"""
    
    datos = []
    if columna == prodCol.NOMBRE or columna == vendCol.NOMBRE or \
       columna == vendCol.SEXO or columna == prodCol.MARCA:
        valor = valor.upper()
    valores = obten_todo_de_columna (archivos, columna)
    if valor in valores:
        for idx, val in enumerate(valores):
            if val == valor:
                datos.append(archivos[idx])
    return datos

def actualizar_venta(ventas, producto_id, vendedor_id, cantidad):
    """encuentra la fila en donde se debe actualiar la cantidad de venta
    de cierto producto y vendedor"""
    
    for idx, fila in enumerate(ventas):
        if int(fila[ventCol.VENDEDOR_ID]) == vendedor_id and \
            int(fila[ventCol.PRODUCTO_ID]) == producto_id:
            ventas[idx][ventCol.CANTIDAD] = \
            int(ventas[idx][ventCol.CANTIDAD]) + cantidad
            break

def registrar_ventas (productos, vendedores, ventas):
    """opcion de menu 1: agrega ventas al vendedor indicado y reduce la 
    existencia del producto en el inventario"""
    print('Ingresa el nombre del vendedor:')
    nombre_vendedor = input()
    
    while nombre_vendedor.upper() not \
          in obten_todo_de_columna (vendedores, vendCol.NOMBRE):
        print('Lo sentimos, el vendedor ingresado no \
trabaja dentro de esta \
compañía.\nFavor de ingresar de nuevo el nombre del vendedor:')
        nombre_vendedor  = input()
    
    print('Ingresa el nombre del producto a comprar:')
    nombre_producto = input()
    
    while nombre_producto.upper() not \
          in obten_todo_de_columna (productos, prodCol.NOMBRE):
        print('Lo sentimos, el producto ingresado no se encuentra dentro del \
almacén.\n Favor de ingresar de nuevo el nombre del producto:')
        nombre_producto  = input()
        
    print('Ingrese las unidades que desea vender:')
    cantidad = int(input())
    
    while cantidad < 0:
        print('Tu cantidad es menor a cero, favor \
de ingresar un número positivo:')
        cantidad = int(input())
    
    while cantidad == 0:
        print('Tu cantidad es cero, favor \
de ingresar un número mayor a 0:')
        cantidad = int(input())
    
    producto = obten_todo_con_valor(productos, prodCol.NOMBRE,
                                    nombre_producto)[0]
    if int(obten_atributo(producto, prodCol.EXISTENCIA)) < cantidad:
        print('\nNo es posible realizar la venta')
        print(f"Solo existen {producto[prodCol.EXISTENCIA]} \
{producto[prodCol.NOMBRE]} dentro del inventario\n")
    else:
        producto_id = int(obten_atributo(producto, prodCol.ID))
        productos[producto_id][prodCol.EXISTENCIA]= (
            int(productos[producto_id][prodCol.EXISTENCIA]) - cantidad)
        vendedor = obten_todo_con_valor(vendedores, vendCol.NOMBRE,
                                        nombre_vendedor)[0]
        vendedor_id = int(obten_atributo(vendedor, vendCol.ID))
        actualizar_venta(ventas, producto_id, vendedor_id, cantidad)
        cost = int(obten_atributo(producto, prodCol.COSTO)) * cantidad
        
        print(f'\nEl precio individual de \
{obten_atributo(producto, prodCol.NOMBRE)} es \
de $ {obten_atributo(producto, prodCol.COSTO)}.00')
        print('Tu precio final al cliente es de $ %d.00'%(cost))
        print('La venta fue registrada exitosamente\n')

def registrar_llegada_de_articulos(matriz):
    """opcion de menu 2: añade articulos de un producto al inventario"""
    
    print('Ingrese el nombre del producto:')
    nombre_producto = input()
    
    while nombre_producto.upper() not \
          in obten_todo_de_columna (matriz, prodCol.NOMBRE):
        print('Lo sentimos, el producto ingresado no se encuentra dentro del \
almacén.\nFavor de ingresar de nuevo el nombre del producto:')
        nombre_producto  = input()
    
    print('Ingrese la cantidad que ha llegado al almacén:')
    cantidad_a_almacen = int(input())
    
    while cantidad_a_almacen < 0:
        print('Tu cantidad es menor a cero, favor \
de ingresar un número positivo:')
        cantidad_a_almacen = int(input())
        
    while cantidad_a_almacen == 0:
        print('Tu cantidad es cero, favor \
de ingresar un número mayor a 0:')
        cantidad_a_almacen = int(input())
    
    producto= obten_todo_con_valor(matriz, prodCol.NOMBRE, nombre_producto)[0]
    producto_id=int(obten_atributo(producto, prodCol.ID))
    
    matriz[producto_id][prodCol.EXISTENCIA] = (
        int(matriz[producto_id][prodCol.EXISTENCIA]) + cantidad_a_almacen)
    print('El inventario ha sido actualizado exitosamente\n')

def consultar_inventario_por_nombre(matriz):
    """opcione de menu 3: muestra los datos del producto dentro del 
    inventario"""
    print('Ingrese el nombre del producto que desea consultar:')
    nombre_producto = input()
    
    while nombre_producto.upper() not \
          in obten_todo_de_columna (matriz, prodCol.NOMBRE):
        print('Lo sentimos, el producto ingresado no se encuentra dentro del \
almacén.\nFavor de ingresar de nuevo el nombre del producto:')
        nombre_producto  = input()
        
    producto = obten_todo_con_valor(matriz, prodCol.NOMBRE, nombre_producto)[0]
    for elemento in producto:
        if elemento == obten_atributo(producto, prodCol.COSTO):
            print('$ %d.00'%(int(elemento)), end="     ")
        else:
            print(elemento, end="     ")

def consultar_vendedores(matriz):
    """opción de menu 4: muestra los datos de todos los vendedores"""

    bigger_size = []
    biggest = 0
    for columna in range(len(matriz[0])):
        for fila in range(len(matriz)):
            if len(matriz[fila][columna]) > biggest:
                biggest = len(matriz[fila][columna])
        bigger_size.append(biggest)
        biggest = 0
        
    for fila in matriz:
        for columna, value in enumerate(fila):
            print(value.ljust(bigger_size[columna] + 3), end = "")
        print()

def consultar_ventas(matriz_ventas, matriz_vendedores,\
                     matriz_inventario):
    
    """opción de menu 5: muestra las ventas de un producto realizadas 
    por un vendededor"""
    
    id_vendedor = None
    id_producto = None
    vendedor = input("Nombre del vendedor: ").upper()
    producto = input("Nombre del Articulo: ").upper()
    
    for i in range(len(matriz_vendedores)):
        if vendedor == matriz_vendedores[i][vendCol.NOMBRE].upper():
            id_vendedor = int(matriz_vendedores[i][vendCol.ID])
    
    for i in range(len(matriz_inventario)):
        if producto == matriz_inventario[i][prodCol.NOMBRE].upper():
            id_producto = int(matriz_inventario[i][prodCol.ID])
    
    if id_vendedor == None and id_producto == None:
        print("El producto y el vendedor no existen")
    elif  id_vendedor == None: 
        print("El vendedor no existe")
    elif id_producto == None:
        print("El producto no existe")
    else:
        for i in matriz_ventas:
            if id_vendedor == int(i[ventCol.VENDEDOR_ID]) and \
            id_producto == int(i[ventCol.PRODUCTO_ID]):
                print(f"Ventas de {producto} por {vendedor}: ",
                      i[ventCol.CANTIDAD],"\n")

def reporte_ventas(opcion, matriz_ventas, matriz_vendedores, \
                   matriz_inventario):
    """opción de menu 6: muestra el dinero total generado por un vendedor
    o el total de todas las ventas de un producto"""
    
    id_vendedor = None
    id_producto = None
    consulta_vendedor = [["Articulo","Cantidad","Total $"]]
    consulta_articulo = [["Vendedor","Cantidad","Venta $"]]
    cantidades = []
    total = 0

    if opcion == 1:
        vendedor = input("Nombre del vendedor: ").upper()
        
        for i in range(len(matriz_vendedores)):
            if vendedor == matriz_vendedores[i][vendCol.NOMBRE].upper():
                id_vendedor = matriz_vendedores[i][vendCol.ID]
        
        if id_vendedor == None:
            print("El vendedor no existe")
        else:  
            for i in matriz_ventas:
                if id_vendedor == i[ventCol.VENDEDOR_ID]:
                    cantidades.append(int(i[ventCol.CANTIDAD]))

                
            for i in range(len(matriz_inventario)):
                dinero_venta = int(matriz_inventario[i][prodCol.COSTO]) * \
                               int(cantidades[i])
                
                if dinero_venta != 0:
                    total += dinero_venta
                    consulta_vendedor.append([\
                        matriz_inventario[i][prodCol.NOMBRE],\
                        cantidades[i],f"\t${dinero_venta}"])
        
            muestra_matriz_consulta(consulta_vendedor)
            print("total: $"+str(total))
                
    elif opcion == 2:
        articulo = input("Nombre del Articulo: ").upper()
        
        for i in matriz_inventario:
            if articulo == i[prodCol.NOMBRE].upper():
                id_producto = i[prodCol.ID]
                precio = int(i[prodCol.COSTO])
        
        if id_producto == None:
            print("El producto no existe")
        else:
            
            for i in matriz_ventas:
                if id_producto == i[ventCol.PRODUCTO_ID]:
                    cantidades.append(int(i[ventCol.CANTIDAD]))
                    
                    
            for i in range(len(matriz_vendedores)):
                dinero_venta = cantidades[i] * precio
                
                if dinero_venta != 0:
                    total += dinero_venta
                    consulta_articulo.append([\
                        matriz_vendedores[i][vendCol.NOMBRE],\
                        cantidades[i],f"\t${dinero_venta}"])
            
            muestra_matriz_consulta(consulta_articulo)
            print("total: $"+str(total))

    
def main():
    #Cargar los archivos
    productos = load_file("Productos.csv")
    vendedores = load_file("Vendedor.csv")
    ventas = load_file("Ventas.csv")
    
    #Opciones de menú
    opcion = "--"
    reporte = 0
    
    while opcion != '7':
        print('\n')
        print('Eliga del menú que función desea realizar\
(ingrese solo el número)\n')
        print('1. Registrar una venta')
        print('2. Registrar llegada de artículos al almacén')
        print('3. Consultar datos de inventario')
        print('4. Consultar datos de vendedor -es')
        print('5. Consultar datos de ventas')
        print('6. Generar reportes de ventas')
        print('7. Guardar y salir')
        
        opcion=input()
        
        if opcion == '1':
            registrar_ventas(productos, vendedores, ventas)
        elif opcion == '2':
            registrar_llegada_de_articulos(productos)
        elif opcion == '3':
            consultar_inventario_por_nombre(productos)
        elif opcion == '4':
            consultar_vendedores(vendedores)
        elif opcion == '5':
            consultar_ventas(ventas,vendedores, productos)
        elif opcion == '6':
            print("\nReporte de ventas:\n\t1.Por vendedor\n\t2.Por Articulo")
            reporte = int(input())
            reporte_ventas(reporte, ventas,vendedores, productos)
        elif opcion != '7':
            print('\nLa opción ingresada no existe en el menú')
            
    guardar_datos(productos, vendedores, ventas)
    print('\nTus datos han sido guardados, que tenga buen día')

main()