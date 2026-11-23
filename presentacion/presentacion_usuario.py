from prettytable import PrettyTable
from rutificador import Rut

import re
from datetime import datetime

from negocio.negocio_usuario import lista_usuarios,crear_usuario,actualizar_usuario
from negocio.negocio_pais import buscar_paises
from datos.repositorios.repositorio_paises import obtener_pais_nombre
from datos.modelos.usuario import Usuario
from auxiliares.mensajes import mensaje_error
from auxiliares.validaciones import validar_correo, validar_fecha_nacimiento,validar_genero,validar_contrasenia

def mostrar_usuario():
    try:
        tabla_usuarios = PrettyTable()
        tabla_usuarios = lista_usuarios(tabla_usuarios)
        print(tabla_usuarios)
    except Exception as error:
        print(f'Ha ocurrido un error: {error}')
    

def solicitar_datos_usuario():
    rut_in = nombre = apellido = correo = pais = id_pais = fecha_nacimiento = genero = contrasenia = ''
    tabla_paises = PrettyTable()
    print('Ingrese Datos de Usuario')
    try:
        while rut_in == '':
            rut_in = input('RUT (12.345.678-5): ')
            rut = Rut(rut_in)
            if not rut:
                print('RUT Inválido, ingrese nuevamente...')
                rut_in = ''

        while nombre == '':
            nombre = input('Nombre: ')

        while apellido == '':
            apellido = input('Apellido: ')

        while correo == '':
            correo = input('Correo: ')
            correo, mensaje = validar_correo(correo)
            print(mensaje)

        while pais == '':
            pais = input('País: ')
            tabla_paises = buscar_paises(tabla_paises, pais)
            print(tabla_paises)
            id_pais = input('ID País:')

        while fecha_nacimiento == '':
            fecha_nacimiento = input('Fecha Nacimiento (dd/mm/yyyy): ')
            fecha_nacimiento, mensaje = validar_fecha_nacimiento(fecha_nacimiento)
            print(mensaje)

        while genero == '':
            print('Género: \n[1] Masculino \n[2] Femenino \n[3]Otro')
            genero = input('Seleccione Género [1-3]: ')
            genero, mensaje = validar_genero(genero)
            print(mensaje)

        while contrasenia == '':
            contrasenia = input('Contraseña: ')
            contrasenia, mensaje = validar_contrasenia(contrasenia)
            if len(mensaje) > 0:
                print('Contraseña inválida, revise los siguientes errores:')
                for error in mensaje:
                    print(error)
        
        crear_usuario(rut.formatear(separador_miles=True), nombre.title(), apellido.title(), correo, id_pais, fecha_nacimiento, genero, contrasenia)
    except Exception as mensaje:
        print(f'{mensaje_error} {mensaje}')

def modificar_pais():
    pais_encontrado = Usuario()
    try:
        nombre_pais = ''
        while nombre_pais == '':
            nombre_pais = input('Ingrese nombre país a modificar: ')
            pais_encontrado = obtener_pais_nombre(nombre_pais)
            if pais_encontrado:
                print(f'\nID: {pais_encontrado.id_pais} - Nombre: {pais_encontrado.usuario}')
                print(f'Nacionalidad: {pais_encontrado.nacionalidad} - ISO 2: {pais_encontrado.iso2} - ISO 3: {pais_encontrado.iso3}\n')

                usuario = input('Ingrese nombre país (o ENTER para conservar): ')
                nacionalidad = input('Ingrese nacionalida país (o ENTER para conservar): ')
                iso2 = input('Ingrese ISO 2 país (o ENTER para conservar): ')
                iso3 = input('Ingrese ISO 3 país (o ENTER para conservar): ')
                actualizar_pais(usuario,nacionalidad,iso2,iso3,True,pais_encontrado)
            else:
                nombre_pais = ''
    except Exception as error:
        print(f'{mensaje_error} {error}')

def eliminar_pais():
    pais_encontrado = Usuario()
    try:
        nombre_pais = ''
        while nombre_pais == '':
            nombre_pais = input('Ingrese nombre país a eliminar: ')
            pais_encontrado = obtener_pais_nombre(nombre_pais)
            if pais_encontrado:
                print('Se eliminará el siguiente país:')
                print(f'\nID: {pais_encontrado.id_pais} - Nombre: {pais_encontrado.usuario}')
                print(f'Nacionalidad: {pais_encontrado.nacionalidad} - ISO 2: {pais_encontrado.iso2} - ISO 3: {pais_encontrado.iso3}\n')
                habilitado = False
                actualizar_pais(
                    pais_encontrado.usuario,
                    pais_encontrado.nacionalidad,
                    pais_encontrado.iso2,
                    pais_encontrado.iso3,
                    habilitado,
                    pais_encontrado)
            else:
                nombre_pais = ''
    except Exception as error:
        print(f'{mensaje_error} {error}')