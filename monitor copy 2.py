# peso pagina descargada y los tipos de archivo
# tipo html o pdf (is pdf)
# e_nav

# (c) vicente b. lopez plaza
# vinxenxo@protonmail.com

import csv
import re
import json
import textstat
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from datetime import datetime
import time
import string
from PIL import Image
from io import BytesIO
import os
import imghdr
import subprocess
from collections import Counter
from lxml import etree
from urllib.parse import urlparse, urljoin
import aspell
import string
import langid
from sqlalchemy import Boolean, distinct, func, create_engine, Column, Integer, String, Text, DateTime, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import secrets
from sqlalchemy import desc
import re
import logging
#from langdetect import detect

# Definir el modelo de la tabla "resultados"
Base = declarative_base()

class Resultado(Base):
    __tablename__ = 'resultados'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_escaneo = Column(DateTime, default=datetime.now)
    dominio = Column(String(255))
    codigo_respuesta = Column(Integer)
    tiempo_respuesta = Column(Float)  #Column(Integer)
    tipo_documento = Column(String(255))
    pagina = Column(String(1383))
    parent_url = Column(String(1383))
    meta_tags = Column(JSON)
    heading_tags = Column(JSON)
    imagenes = Column(JSON)
    enlaces_totales = Column(Integer)
    enlaces_inseguros = Column(Integer)
    enlaces_internos = Column(Integer)
    enlaces_internos_unicos = Column(Integer)
    enlaces_js_unicos = Column(Integer)
    enlaces_salientes = Column(Integer)
    enlaces_salientes_unicos = Column(Integer)
    enlaces_salientes_js_unicos = Column(Integer)
    enlaces_salientes_externos = Column(Integer)
    enlaces_salientes_externos_unicos = Column(Integer)
    enlaces_salientes_js_externos_unicos = Column(Integer)
    tipos_archivos = Column(JSON)
    errores_ortograficos = Column(JSON)
    num_errores_ortograficos = Column(Integer)
    num_redirecciones = Column(Integer)
    alt_vacias = Column(Integer)
    num_palabras = Column(Integer)
    frases = Column(Integer)
    media_palabras_frase = Column(Integer)
    flesh_score = Column(Float)
    e_title = Column(Integer)
    e_head = Column(Integer)
    e_body = Column(Integer)
    e_html = Column(Integer)
    e_robots = Column(Integer)
    e_description = Column(Integer)
    e_keywords = Column(Integer)
    e_viewport = Column(Integer)
    e_charset = Column(Integer)
    c_title = Column(Text)
    c_robots = Column(Text)
    c_description = Column(Text)
    c_keywords = Column(Text)
    c_charset = Column(Text)
    html_valid = Column(Integer)
    content_valid = Column(Integer)
    responsive_valid = Column(Integer)
    image_types = Column(JSON)
    wcagaaa = Column(JSON)
    valid_aaa = Column(Integer)
    lang = Column(String(10))
    title_long = Column(String(1383))
    title_short = Column(String(1383))
    title_duplicate = Column(String(1383))
    desc_long = Column(String(1383))
    desc_short = Column(String(1383))
    h1_duplicate = Column(Integer)
    images_1MB = Column(Integer)
    imagenes_rotas = Column(Integer)
    html_copy = Column(Text)
    html_copy_dos = Column(Text)
    html_copy_tres = Column(Text)
    html_copy_cuatro = Column(Text)
    html_copy_cinco = Column(Text)
    html_copy_seis = Column(Text)
    html_copy_siete = Column(Text)
    html_copy_ocho = Column(Text)
    html_copy_nueve = Column(Text)
    html_copy_diez = Column(Text)
    id_escaneo = Column(String(255), nullable=False)
    peso_total_pagina = Column(Integer)
    is_pdf = Column(Integer)
    meta_description_mas_155_caracteres = Column(Integer)
    meta_description_duplicado = Column(Integer)
    canonicals_falta = Column(Integer)
    directivas_noindex = Column(Integer)
    falta_encabezado_x_content_type_options = Column(Integer)
    falta_encabezado_secure_referrer_policy = Column(Integer)
    falta_encabezado_content_security_policy = Column(Integer)
    falta_encabezado_x_frame_options = Column(Integer)
    titulos_pagina_menos_30_caracteres = Column(Integer)
    meta_description_menos_70_caracteres = Column(Integer)
    titulos_pagina_mas_60_caracteres = Column(Integer)
    titulos_pagina_igual_h1 = Column(Integer)
    titulos_pagina_duplicado = Column(Integer)
    meta_description_falta = Column(Integer)
    version_http = Column(String(50))
    ultima_modificacion = Column(String(50))
    meta_og_card = Column(String(255))
    meta_og_title = Column(String(1383))
    meta_og_image = Column(String(1383))
    h2_duplicado = Column(Integer)
    h2_mas_70_caracteres = Column(Integer)
    h2_multiple = Column(Integer)
    h2_falta = Column(Integer)
    h2_no_secuencial = Column(Integer)


class Diccionario(Base):
    __tablename__ = 'diccionario'
    id = Column(Integer, primary_key=True, autoincrement=True)
    palabra = Column(String(255))
    idioma = Column(String(50))

class Diccionario_usuario(Base):
    __tablename__ = 'diccionario_usuario'
    id = Column(Integer, primary_key=True, autoincrement=True)
    palabra = Column(String(255))
    idioma = Column(String(50))


class Configuracion(Base):
    __tablename__ = 'configuracion'
    id = Column(Integer, primary_key=True)
    is_running = Column(Boolean)
    dominios_analizar = Column(JSON)
    frecuencia_dias = Column(Integer)
    w3c_validator = Column(String(255))
    url_Excluidas = Column(JSON)
    extensiones_Excluidas = Column(JSON)
    keywords_analizar = Column(JSON)


# Definir el modelo de la tabla "sumario"
class Sumario(Base):
    __tablename__ = 'sumario'
    id = Column(Integer, primary_key=True, autoincrement=True)
    dominio = Column(String(255))
    total_paginas = Column(Float)
    duracion_total = Column(Integer)
    codigos_respuesta = Column(JSON)
    hora_inicio = Column(String(20))
    hora_fin = Column(String(20))
    fecha = Column(String(10))
    html_valid_count = Column(Integer)
    content_valid_count = Column(Integer)
    responsive_valid_count = Column(Integer)
    valid_aaaa_pages = Column(Integer)
    idiomas = Column(JSON)
    paginas_inseguras = Column(Integer)  # Nuevo campo
    total_404 = Column(Integer)  # Nuevo campo
    enlaces_inseguros = Column(Integer)
    pages_title_long = Column(Integer)  # Nuevos campos
    pages_title_short = Column(Integer)
    pages_title_dup = Column(Integer)
    pages_desc_long = Column(Integer)
    pages_desc_short = Column(Integer)
    pages_h1_dup = Column(Integer)
    pages_img_1mb = Column(Integer)
    id_escaneo = Column(String(255), nullable=False)
    #id_escaneo = Column(Integer, ForeignKey('escaneo.id'))
    tiempo_medio = Column(Float)
    pages_err_orto = Column(Integer)
    pages_alt_vacias = Column(Integer)
    peso_total_paginas = Column(Integer)
    pdf_count = Column(Integer)
    html_count = Column(Integer)
    others_count = Column(Integer)
    media_frases = Column(Integer)
    total_media_palabras_frase = Column(Integer)
    media_flesh_score = Column(Integer)
    total_meta_description_mas_155_caracteres = Column(Integer)
    total_meta_description_duplicado = Column(Integer)
    total_canonicals_falta = Column(Integer)
    total_directivas_noindex = Column(Integer)
    total_falta_encabezado_x_content_type_options = Column(Integer)
    total_falta_encabezado_secure_referrer_policy = Column(Integer)
    total_falta_encabezado_content_security_policy = Column(Integer)
    total_falta_encabezado_x_frame_options = Column(Integer)
    total_titulos_pagina_menos_30_caracteres = Column(Integer)
    total_meta_description_menos_70_caracteres = Column(Integer)
    total_titulos_pagina_mas_60_caracteres = Column(Integer)
    total_titulos_pagina_igual_h1 = Column(Integer)
    total_titulos_pagina_duplicado = Column(Integer)
    total_meta_description_falta = Column(Integer)
    total_h2_duplicado = Column(Integer)
    total_h2_mas_70_caracteres = Column(Integer)
    total_h2_multiple = Column(Integer)
    total_h2_falta = Column(Integer)
    total_h2_no_secuencial = Column(Integer)


def crear_lock(session):
    try:
        # Obtener la ruta actual del directorio
        directorio_actual = os.getcwd()
        # Comprobar si ya existe el archivo .lock
        if os.path.exists(os.path.join(directorio_actual, '.lock')):
            print("El archivo .lock ya existe. El script no se ejecutará.")
            return False
        else:
            # Crear el archivo .lock
            with open(os.path.join(directorio_actual, '.lock'), 'w'):
                pass  # No necesitamos escribir contenido en el archivo
            print("Archivo .lock creado. El script se ejecutará.")
            # Actualizar el campo is_running a False en la tabla de configuración
            session.query(Configuracion).update({Configuracion.is_running: False})
            session.commit()  # Confirmar la transacción
            return True
    except Exception as e:
        print("Error al crear el archivo .lock:", e)
        return False


def eliminar_lock(session):
    try:
        # Obtener la ruta actual del directorio
        directorio_actual = os.getcwd()
        # Eliminar el archivo .lock si existe
        if os.path.exists(os.path.join(directorio_actual, '.lock')):
            os.remove(os.path.join(directorio_actual, '.lock'))
            print("Archivo .lock eliminado.")
            # Actualizar el campo is_running a True en la tabla de configuración
            session.query(Configuracion).update({Configuracion.is_running: True})
            session.commit()  # Confirmar la transacción
        else:
            print("No se encontró el archivo .lock.")
    except Exception as e:
        print("Error al eliminar el archivo .lock:", e)


def guardar_en_resultados(session, resultado):

    try:
        session.add(resultado)
        session.commit()
    except OperationalError as e:
        print(f"Error de conexión: {e}")
        session.rollback()
        session = Session()
        guardar_en_resultados(session, resultado)
    finally:
        session.flush()


# FunciÃ³n para guardar un sumario en la tabla "sumario"
def guardar_en_sumario(session, sumario):
    try:
        #session = Session()
        session.add(sumario)
        session.commit()
    except OperationalError as e:
        print(f"Error de conexión: {e}")
        # Realizar reconexión y volver a intentar
        session.rollback()
        session = Session(
        )  # Asegúrate de configurar la sesión según tus necesidades
        guardar_en_sumario(session, sumario)
    finally:
        #print("Guardado sumario")
        session.flush()



def extraer_texto_visible(response_text):
    soup = BeautifulSoup(response_text, 'html.parser')
    #soup = BeautifulSoup(response_text, 'html.parser', markup_type='html')
    visible_text = ' '.join(soup.stripped_strings)
    return visible_text



def obtener_idioma_desde_url(url):
    try:
        # Realiza la solicitud GET para obtener el contenido HTML de la URL
        response = requests.get(url)
        response.raise_for_status()  # Lanza una excepción si la solicitud no tiene éxito

        # Parsea el HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encuentra la etiqueta meta con el atributo property="og:locale"
        etiqueta_meta = soup.find('meta', property='og:locale')

        # Si se encuentra la etiqueta meta, extrae el valor del atributo content
        if etiqueta_meta:
            idioma_meta = etiqueta_meta.get('content', None)
            if idioma_meta:
                # Elimina las comillas escapadas usando expresiones regulares
                codigo_idioma = re.sub(r'^\\"|\\"$', '', idioma_meta).split('_')[0]
                #print("idioma:")
                #print(codigo_idioma)
                return codigo_idioma
            else:
                print("No se encontró el atributo content en la etiqueta meta con property='og:locale'.")
        else:
            print("No se encontró la etiqueta meta con property='og:locale'.")

            # Encuentra la etiqueta <html> y extrae el valor del atributo lang
            idioma_html = soup.html.get('lang', None)

            # Si se encuentra el atributo lang, extrae los dos primeros caracteres (código del idioma)
            if idioma_html:
                # Elimina las comillas escapadas usando expresiones regulares
                codigo_idioma = re.sub(r'^\\"|\\"$', '', idioma_html).split('-')[0]
                #print("idioma:")
                #print(codigo_idioma)
                return codigo_idioma
            else:
                print("No se encontró el atributo lang en la etiqueta <html>.")

                # Si no se encuentra el idioma en ninguna de las etiquetas, utiliza la función detectar_idioma
                texto_pagina = soup.get_text()
                codigo_idioma_detectado = detectar_idioma(texto_pagina)
                if codigo_idioma_detectado:
                    print("Idioma detectado mediante texto de la página:", codigo_idioma_detectado)
                    return codigo_idioma_detectado

    except Exception as e:
        print(f"Error al obtener el idioma del HTML de la URL {url}: {e}")

    return "es"  # Idioma predeterminado



def detectar_idioma(texto):
    try:
        idioma, _ = langid.classify(texto)
        return idioma
    except Exception as e:
        print(f"Error al detectar el idioma: {e}")
        return None


def analizar_ortografia(url, texto,
                        idiomas=[
                            'es', 'fr', 'en', 'ca', 'eu', 'ca_general', 'ca_valencia'
                        ]):
    errores_ortograficos = None  # Inicializa como None en lugar de una lista vacía
    palabras = set()  # Usamos un conjunto para almacenar las palabras únicas

    idioma_detectado = obtener_idioma_desde_url(url)  #detectar_idioma(texto)
    try:
        speller = aspell.Speller('lang', idioma_detectado)

        # Eliminar números y símbolos de moneda, así como exclamaciones, interrogaciones y caracteres similares
        translator = str.maketrans(
             '', '', string.digits + string.punctuation + '“”$€£»«¿?¡!.“')
        #    '', '', string.digits + string.punctuation + '¡!¿?“”»«¡!¿?$€£@#%^&*()_-+=[]{}|;:,.<>/–“"')


        texto_limpio = texto.translate(translator)



        #print("revisando pagina ortografia")
        #print(PALABRAS_DICCIONARIO)
        # Agrega palabras personalizadas excluidas
        #palabras = {
        #    palabra
        #    for palabra in texto_limpio.split()
        #    if palabra.lower() not in PALABRAS_DICCIONARIO
        #    and len(palabra) >= 4
        #}

        # Filtra palabras que tengan TODOS los signos de puntuación, interrogación, exclamación, caracteres especiales o símbolos de moneda
        #caracteres_especiales = string.punctuation + '“”»«¡!¿?$€£@#%^&*()_-+=[]{}|;:,.<>/–“"'
        caracteres_especiales = string.punctuation + '»«'
        palabras = {
            palabra
            for palabra in texto_limpio.split()
            if not all(c in caracteres_especiales for c in palabra)
            if palabra not in PALABRAS_DICCIONARIO
            and len(palabra) >= 4
        }

        # Errores ortográficos solo para palabras que no están en la lista excluida y no cumplen con el chequeo del speller
        errores_ortograficos = [
            palabra for palabra in palabras if not speller.check(palabra) and palabra.lower() not in PALABRAS_DICCIONARIO and palabra.upper() not in PALABRAS_DICCIONARIO and palabra.capitalize() not in PALABRAS_DICCIONARIO
        ]

    except Exception as e:
        print(f"Error al procesar el idioma {idioma_detectado}: {e}")

    return list(errores_ortograficos)


def analizar_heading_tags(response_text):
    soup = BeautifulSoup(response_text, 'html.parser')
    heading_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    heading_tags_count = {tag: len(soup.find_all(tag)) for tag in heading_tags}

    # Contar las veces que aparece la etiqueta h1 específicamente
    h1_duplicate = heading_tags_count.get('h1', 0)

    # Nuevas métricas para h2
    h2_mas_70_caracteres = sum(
        len(tag.text) > 70 for tag in soup.find_all('h2'))
    h2_duplicado = any(count > 1 for count in heading_tags_count.values())
    h2_multiple = any(count > 1 for count in heading_tags_count.values())
    h2_falta = heading_tags_count.get('h2', 0) == 0
    h2_no_secuencial = heading_tags_count.get(
        'h1', 0) > 0 and heading_tags_count.get(
            'h2', 0) > 0 and soup.find_all('h1')[0].find_next('h2') is None

    # Nuevas métricas para h1 y h2
    #h1_longitud = max(len(tag.text) for tag in soup.find_all('h1'))
    #h2_longitud = max(len(tag.text) for tag in soup.find_all('h2'))

    return heading_tags_count, h1_duplicate, h2_mas_70_caracteres, h2_duplicado, h2_multiple, h2_falta, h2_no_secuencial


def extraer_meta_tags(response_text, response):
    soup = BeautifulSoup(response_text, 'html.parser')
    meta_tags = soup.find_all('meta')
    meta_tags_info = [{
        'name': tag.get('name'),
        'content': tag.get('content')
    } for tag in meta_tags]

    # Nuevos datos de meta tags
    meta_description_mas_155_caracteres = any(
        len(tag.get('content', '')) > 155 for tag in meta_tags
        if tag.get('name') == 'description')
    meta_description_duplicado = any(
        meta_tags_info.count(tag) > 1 for tag in meta_tags_info
        if tag.get('name') == 'description')

    canonicals_falta = not soup.find('link', {'rel': 'canonical'})
    directivas_noindex = 'noindex' in [
        tag.get('content') for tag in meta_tags if tag.get('name') == 'robots'
    ]

    falta_encabezado_x_content_type_options = 'X-Content-Type-Options' not in [
        header[0] for header in response.headers
    ]
    falta_encabezado_secure_referrer_policy = 'Referrer-Policy' not in [
        header[0] for header in response.headers
    ]
    falta_encabezado_content_security_policy = 'Content-Security-Policy' not in [
        header[0] for header in response.headers
    ]
    falta_encabezado_x_frame_options = 'X-Frame-Options' not in [
        header[0] for header in response.headers
    ]

    titulos_pagina_menos_30_caracteres = any(
        len(tag.text) < 30
        for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']))
    meta_description_menos_70_caracteres = any(
        len(tag.get('content', '')) < 70 for tag in meta_tags
        if tag.get('name') == 'description')
    titulos_pagina_mas_60_caracteres = any(
        len(tag.text) > 60
        for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']))
    titulos_pagina_igual_h1 = any(
        tag.text == soup.find('h1').text
        for tag in soup.find_all(['h2', 'h3', 'h4', 'h5', 'h6']))
    titulos_pagina_duplicado = any(
        meta_tags_info.count(tag) > 1 for tag in meta_tags_info
        if tag.get('name') == 'title')

    meta_description_falta = not any(
        tag.get('name') == 'description' for tag in meta_tags)

    version_http = response.headers.get('Version')
    ultima_modificacion = response.headers.get('last-modified')

    meta_og_card = any(tag.get('property') == 'og:card' for tag in meta_tags)
    meta_og_title = any(tag.get('property') == 'og:title' for tag in meta_tags)
    meta_og_image = any(tag.get('property') == 'og:image' for tag in meta_tags)

    # Nuevos campos
    #hreflang_enlaces_vuelta_noindex = ...  # Lógica para determinar si se cumplen las condiciones
    #hreflang_falta_x_default = ...  # Lógica para determinar si se cumple la condición
    #seguridad_falta_encabezado_hsts = ...  # Lógica para determinar si se cumple la condición

    #return meta_tags_info, meta_description_mas_155_caracteres, meta_description_duplicado, canonicals_falta, directivas_noindex, \
    #       falta_encabezado_x_content_type_options, falta_encabezado_secure_referrer_policy, \
    #       falta_encabezado_content_security_policy, falta_encabezado_x_frame_options, \
    #       titulos_pagina_menos_30_caracteres, meta_description_menos_70_caracteres, titulos_pagina_mas_60_caracteres, \
    #       titulos_pagina_igual_h1, titulos_pagina_duplicado, meta_description_falta, version_http, ultima_modificacion, \
    #       meta_og_card, meta_og_title, meta_og_image, hreflang_enlaces_vuelta_noindex, hreflang_falta_x_default, seguridad_falta_encabezado_hsts


    return meta_tags_info, meta_description_mas_155_caracteres, meta_description_duplicado, canonicals_falta, directivas_noindex, \
           falta_encabezado_x_content_type_options, falta_encabezado_secure_referrer_policy, \
           falta_encabezado_content_security_policy, falta_encabezado_x_frame_options, \
           titulos_pagina_menos_30_caracteres, meta_description_menos_70_caracteres, titulos_pagina_mas_60_caracteres, \
           titulos_pagina_igual_h1, titulos_pagina_duplicado, meta_description_falta, version_http, ultima_modificacion, \
           meta_og_card, meta_og_title, meta_og_image


def extraer_informacion_imagenes(response_text, base_url):
    soup = BeautifulSoup(response_text, 'html.parser')
    img_tags = soup.find_all('img')
    info_imagenes = []
    image_types = []
    images_1MB = 0
    imagenes_rotas = 0

    for img_tag in img_tags:
        src = img_tag.get('src')
        alt = img_tag.get('alt', '')
        src_url = urljoin(base_url, src)

        try:
            response = requests.get(src_url, stream=True)
            response.raise_for_status()

            # Get the filename, size in MB, and check if the image is broken
            filename = urlparse(src_url).path.split("/")[-1]
            size_mb = len(response.content) / (1024 * 1024)
            is_broken = False

            # Nuevo campo
            if size_mb > 1:
                images_1MB += 1

            # Check if the image is broken by opening it with PIL
            try:
                Image.open(BytesIO(response.content))
            except Exception as e:
                is_broken = True
                imagenes_rotas += 1

            # Get the image type
            image_type = imghdr.what(None, h=response.content)

            info_imagen = {
                'filename': filename,
                'size_mb': size_mb,
                'url': src_url,
                'alt_text': alt,
                'broken': is_broken,
                'image_type': image_type
            }

            info_imagenes.append(info_imagen)
            image_types.append(image_type)
        except Exception as e:
            print(
                f"Error al obtener informaciÃ³n de la imagen {src_url}: {str(e)}"
            )

    return info_imagenes, image_types, images_1MB, imagenes_rotas


def contar_alt_vacias(response_text):
    soup = BeautifulSoup(response_text, 'html.parser')
    img_tags = soup.find_all('img', alt='')

    return len(img_tags)


def contar_enlaces(response_text):
    soup = BeautifulSoup(response_text, 'html.parser')

    # Enlaces totales y enlaces inseguros
    enlaces = soup.find_all('a', href=True)
    enlaces_inseguros = [
        enlace['href'] for enlace in enlaces
        if enlace['href'].startswith('http://')
    ]

    # Enlaces internos
    enlaces_internos = [
        enlace['href'] for enlace in enlaces
        if not enlace['href'].startswith(('http://', 'https://'))
    ]

    # Enlaces internos únicos
    enlaces_internos_unicos = list(set(enlaces_internos))

    # Enlaces JS únicos
    enlaces_js_unicos = [
        enlace['href'] for enlace in enlaces
        if enlace.get('href') and enlace['href'].startswith('javascript:')
    ]

    # Enlaces salientes
    enlaces_salientes = [
        enlace['href'] for enlace in enlaces
        if enlace.get('href') and enlace['href'].startswith(('http://',
                                                             'https://'))
    ]

    # Enlaces salientes únicos
    enlaces_salientes_unicos = list(set(enlaces_salientes))

    # Enlaces salientes JS únicos
    enlaces_salientes_js_unicos = [
        enlace['href'] for enlace in enlaces_salientes
        if enlace.startswith('javascript:')
    ]

    # Enlaces salientes externos
    enlaces_salientes_externos = [
        enlace for enlace in enlaces_salientes if not any(
            enlace.startswith(dominio) for dominio in DOMINIOS_ESPECIFICOS)
    ]

    # Enlaces salientes externos únicos
    enlaces_salientes_externos_unicos = list(set(enlaces_salientes_externos))

    # Enlaces salientes JS externos únicos
    enlaces_salientes_js_externos_unicos = [
        enlace for enlace in enlaces_salientes_js_unicos if not any(
            enlace.startswith(dominio) for dominio in DOMINIOS_ESPECIFICOS)
    ]

    return len(enlaces), len(enlaces_inseguros), len(enlaces_internos),\
            len(enlaces_internos_unicos), len(enlaces_js_unicos),\
            len(enlaces_salientes), len(enlaces_salientes_unicos),\
            len(enlaces_salientes_js_unicos), len(enlaces_salientes_externos),\
            len(enlaces_salientes_externos_unicos),\
            len(enlaces_salientes_js_externos_unicos), \
            enlaces, enlaces_inseguros,enlaces_internos,\
            enlaces_internos_unicos, enlaces_js_unicos,\
            enlaces_salientes, enlaces_salientes_unicos,\
            enlaces_salientes_js_unicos, enlaces_salientes_externos,\
            enlaces_salientes_externos_unicos,\
            enlaces_salientes_js_externos_unicos

def contar_tipos_archivos(response_text):
    soup = BeautifulSoup(response_text, 'html.parser')
    archivos = soup.find_all(
        ['a', 'img', 'video', 'audio', 'source', 'link', 'script'],
        href=True,
        src=True)
    tipos_archivos = {
        'pdf': 0,
        'video': 0,
        'sound': 0,
        'image': 0,
        'app': 0,
        'others': 0
    }
    peso_total = 0  # Nuevo campo

    for archivo in archivos:
        url_archivo = archivo.get('href') or archivo.get('src')
        extension = url_archivo.split('.')[-1].lower()

        if extension == 'pdf':
            tipos_archivos['pdf'] += 1
        elif extension in ['mp4', 'avi', 'mkv', 'mov']:
            tipos_archivos['video'] += 1
        elif extension in ['mp3', 'wav', 'ogg']:
            tipos_archivos['sound'] += 1
        elif extension in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
            tipos_archivos['image'] += 1
            # Obtener el peso de la imagen y sumarlo al peso total
            peso_total += obtener_peso_archivo(url_archivo)
        elif extension in ['apk', 'exe', 'msi']:
            tipos_archivos['app'] += 1
        else:
            tipos_archivos['others'] += 1

    tipos_archivos['peso_total'] = peso_total  # Nuevo campo
    return tipos_archivos


def obtener_peso_archivo(url_archivo):
    try:
        response = requests.head(url_archivo, allow_redirects=True)
        if response.status_code == 200:
            # Calcular el peso en kilobytes
            peso_kb = int(response.headers.get('content-length', 0)) / 1024
            return peso_kb
    except Exception as e:
        print(f"Error al obtener el peso del archivo {url_archivo}: {str(e)}")
    return 0


def es_html_valido(html_text):
    try:
        parser = etree.HTMLParser()
        etree.fromstring(html_text, parser)
        return True
    except Exception as e:
        return False


# es necesaria?
def contar_redirecciones(url, max_redirecciones=10):
    count = 0
    current_url = url
    redireccion_tipo = 'Desconocido'  # Valor predeterminado

    while count < max_redirecciones:
        try:
            response = requests.head(current_url, allow_redirects=True)
            if response.status_code // 100 == 3:
                redireccion_tipo = obtener_tipo_redireccion(
                    response.status_code)
                current_url = response.headers['Location']
                count += 1
            else:
                break
        except Exception as e:
            print(f"Error al contar redirecciones para {url}: {str(e)}")
            break

    return count, redireccion_tipo


# Sigue sin contarlos?
def obtener_tipo_redireccion(status_code):
    if status_code == 301:
        return 'RedirecciÃ³n permanente (301)'
    elif status_code == 302:
        return 'RedirecciÃ³n temporal (302)'
    elif status_code == 303:
        return 'RedirecciÃ³n de otro recurso (303)'
    elif status_code == 307:
        return 'RedirecciÃ³n temporal (307)'
    elif status_code == 308:
        return 'RedirecciÃ³n permanente (308)'
    else:
        return 'Desconocido'


def contar_palabras_visibles(response_text):
    texto_visible = extraer_texto_visible(response_text)
    palabras = texto_visible.split()

    # Almacenar el número de frases en resultado.frases
    frases = re.split(r'[;.|,]', texto_visible)
    
    # Calcular la media de palabras por frase y almacenarla en resultado.media_palabras_frases
    palabras_por_frase = [
        len(frase.split()) for frase in frases
        if frase.strip()
    ]
    media_palabras_frase = sum(
        palabras_por_frase) / len(
            palabras_por_frase
        ) if palabras_por_frase else 0
  
    # Calcular la prueba de legibilidad de Flesch-Kincaid y almacenarla en resultado.flesh
    try:
        total_palabras = len(
            re.findall(r'\b\w+\b', texto_visible))
        total_oraciones = len(frases)
        #total_silabas = sum([textstat.syllable(word) for word in re.findall(r'\b\w+\b', texto_visible)])
        total_silabas = sum([
            textstat.lexicon_count(word, True)
            for word in re.findall(
                r'\b\w+\b', texto_visible)
        ])
        flesh_score = 206.835 - 1.015 * (
            total_palabras / total_oraciones
        ) - 84.6 * (total_silabas / total_palabras)
        flesh_score = round(
            flesh_score, 2)
    except ZeroDivisionError:
        flesh_score = 0.0
    
    return len(palabras), len(frases), media_palabras_frase,flesh_score


# Modificaciones en analizar_meta_tags
def analizar_meta_tags(response_text):
    soup = BeautifulSoup(response_text, 'html.parser')
    meta_tags_info = {
        'e_title': False,
        'e_head': False,
        'e_body': False,
        'e_html': False,
        'e_robots': False,
        'e_description': False,
        'e_keywords': False,
        'e_viewport': False,
        'e_charset': False,
        'c_title': '',
        'c_robots': '',
        'c_description': '',
        'c_keywords': '',
        'c_charset': '',
        'title_long': False,
        'title_short': False,
        'title_duplicate': False,
        'desc_short': False,
        'desc_long': False
    }

    title_content = None
    desc_content = None

    # Obtener las etiquetas específicas
    body_tag = soup.find('body')
    title_tag = soup.find('title')
    head_tag = soup.find('head')
    html_tag = soup.find('html')
    robots_tag = soup.find('meta', attrs={'name': 'robots'})
    description_tag = soup.find('meta', attrs={'name': 'description'})
    keywords_tag = soup.find('meta', attrs={'name': 'keywords'})
    viewport_tag = soup.find('meta', attrs={'name': 'viewport'})
    charset_tag = soup.find('meta', attrs={'charset': True})

    # Verificar la existencia de las etiquetas y actualizar el diccionario
    meta_tags_info['e_title'] = 1 if title_tag else 0
    meta_tags_info['e_head'] = 1 if head_tag else 0
    meta_tags_info['e_body'] = 1 if body_tag else 0
    meta_tags_info['e_html'] = 1 if html_tag else 0
    meta_tags_info['e_robots'] = 1 if robots_tag else 0
    meta_tags_info['e_description'] = 1 if description_tag else 0
    meta_tags_info['e_keywords'] = 1 if keywords_tag else 0
    meta_tags_info['e_viewport'] = 1 if viewport_tag else 0
    meta_tags_info['e_charset'] = 1 if charset_tag else 0

    # Almacenar el contenido de las etiquetas en el diccionario
    meta_tags_info['c_title'] = title_tag.text if title_tag else ''
    meta_tags_info['c_robots'] = robots_tag.get(
        'content') if robots_tag else ''
    meta_tags_info['c_description'] = description_tag.get(
        'content') if description_tag else ''
    meta_tags_info['c_keywords'] = keywords_tag.get(
        'content') if keywords_tag else ''
    meta_tags_info[
        'c_charset'] = 'utf-8'  #charset_tag.get('charset') if charset_tag else ''

    for tag in soup.find_all('meta'):
        tag_name = tag.get('name', '').lower()
        tag_content = tag.get('content', '').lower()

        if tag_name in meta_tags_info:
            meta_tags_info[tag_name] = 1
        elif tag_content in meta_tags_info:
            meta_tags_info[tag_content] = 1

    if tag_name == 'title':
        title_content = tag_content
    elif tag_name == 'description':
        desc_content = tag_content

    # Nuevos campos
    if title_tag:
        title_content = title_tag.get_text().lower()
        if len(title_content) > 150:
            meta_tags_info['title_long'] = title_content
        elif len(title_content) < 50:
            meta_tags_info['title_short'] = title_content

        # Verificar duplicados en title
        if title_content in response_text[len(title_content):]:
            meta_tags_info['title_duplicate'] = title_content

    if description_tag:
        desc_content = description_tag.get('content', '').lower()
        if len(desc_content) > 150:
            meta_tags_info['desc_long'] = desc_content
        elif len(desc_content) < 50:
            meta_tags_info['desc_short'] = desc_content

    return meta_tags_info


def es_html_valido(response_text):
    try:
        soup = BeautifulSoup(response_text, 'html.parser')
        return bool(soup.html and soup.head and soup.title and soup.body)
    except Exception as e:
        return False


def es_contenido_valido(response_text):
    try:
        soup = BeautifulSoup(response_text, 'html.parser')
        return bool(soup.h1 and soup.h2 and soup.h3)
    except Exception as e:
        return False


def es_responsive_valid(response_text):
    try:
        soup = BeautifulSoup(response_text, 'html.parser')
        viewport_tag = soup.find('meta', attrs={'name': 'viewport'})
        return viewport_tag is not None
    except Exception as e:
        return False


def ejecutar_pa11y(url_actual):
    try:
        # Ejecuta pa11y y captura la salida directamente
        #command = f"pa11y --standard WCAG2AAA  --ignore issue-code-1 --ignore issue-code-2 --reporter csv {url_actual}"
        #command = f"pa11y --standard WCAG2AA  --reporter csv {url_actual}"
        #print("url p4lly:")
        #print(url_actual)
        #command = f"pa11y -e axe -d -T 3 --ignore issue-code-2 --ignore issue-code-1 -r json {url_actual}"
        command = f"pa11y --standard {W3C_VALIDATOR} -T 1 --ignore issue-code-2 --ignore issue-code-1 -r json {url_actual}"
        process = subprocess.run(command,
                                 shell=True,
                                 check=False,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 text=True)

        # Imprime la salida estÃ¡ndar y la salida de error de pa11y
        #print("pa11y stdout:")
        #print(process.stdout)
        #print("pa11y stderr:")
        #print(process.stderr)

        # Verifica si el cÃ³digo de salida es diferente de cero (error)
        #if process.returncode != 0:
        #    print(
        #        f"pa11y devolviÃ³ un cÃ³digo de salida no nulo {process.returncode}"
        #    )
        #    return []  # Devuelve una lista vacÃ­a en caso de error

        # Obtiene la salida del comando pa11y (sin la primera lÃ­nea que es la cabecera)
        pa11y_results_lines = process.stdout.strip().split('\n')[1:]

        #print("resultados:")
        #print(process.stdout)

        # Reformatea los resultados de pa11y en una lista de objetos
        pa11y_results_list = []
        for line in pa11y_results_lines:
            fields = line.split('","')
            if len(fields) == 5:
                pa11y_results_list.append({
                    "type": fields[0].strip('"'),
                    "code": fields[1].strip('"'),
                    "message": fields[2].strip('"'),
                    "context": fields[3].strip('"'),
                    "selector": fields[4].strip('"')
                })

        # Verifica si el resultado de pa11y contiene datos
        # return pa11y_results_list
        return process.stdout
    
    except Exception as e:  # subprocess.CalledProcessError as e:
        error_message = f"Error al ejecutar pa11y para {url_actual}: {e}"
        print(error_message)
        return []


def escanear_dominio(url_dominio, exclusiones=[], extensiones_excluidas=[]):
    resultados = []
    dominio_base = urlparse(url_dominio).netloc
    urls_por_escanear = [(url_dominio, None)]
    urls_escaneadas = set()

    pdf_count = 0  # Contador para el total de PDFs rastreados

    while urls_por_escanear:
        url_actual, parent_url = urls_por_escanear.pop()

        if url_actual in urls_escaneadas:
            continue

        # ComprobaciÃ³n de exclusiones antes de la solicitud HTTP
        if any(patron in url_actual for patron in exclusiones) or any(
                ext in url_actual for ext in extensiones_excluidas):
            urls_escaneadas.add(url_actual)
            continue

        try:
            response = requests.get(url_actual) #, timeout=180)
            tiempo_respuesta = response.elapsed.total_seconds()
            codigo_respuesta = response.status_code
            # Obtener el tipo de documento (Content-Type)
            if response.headers.get('Content-Type'):
                tipo_documento = response.headers.get('Content-Type')

            resultados_pagina = {
                'fecha_escaneo': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'dominio': dominio_base,
                'codigo_respuesta': codigo_respuesta,
                'tiempo_respuesta': tiempo_respuesta,
                'tipo_documento': tipo_documento,
                'pagina': url_actual,
                'parent_url': parent_url,
                # Python 'tuple' cannot be converted to a MySQL type
                'num_redirecciones': 0,  #contar_redirecciones(url_actual)
                'title_long': False,
                'title_short': False,
                'title_duplicate': False,
                'desc_long': False,
                'desc_short': False,
                'h1_duplicate': False,  # Nuevo campo
                'images_1MB': False,  # Nuevo campo
                'imagenes_rotas': 0,
                'id_escaneo': id_escaneo,
                'tipos_archivos': False,
                'peso_total_pagina': 0,
                'is_pdf': -1  # Nuevo campo para indicar si la página es un PDF
            }

            # Si la respuesta es una redirección, actualiza la URL actual
            if codigo_respuesta in [301, 302]:
                resultados_pagina['codigo_respuesta'] = codigo_respuesta
                resultados_pagina['tipo_documento'] = tipo_documento
            elif codigo_respuesta in [401, 402, 403, 404]:
                resultados_pagina['codigo_respuesta'] = codigo_respuesta
                resultados_pagina['tipo_documento'] = tipo_documento
            elif codigo_respuesta == 200:
                if response.headers['content-type'].startswith('text'):
                    #if codigo_respuesta == 200 and response.headers['content-type'].startswith('text/html'):
                    #    if es_html_valido(response.text):
                    if 'pdf' in url_actual.lower(
                    ):  # Comprobar si la URL contiene '%pdf%'
                        resultados_pagina['is_pdf'] = 1
                        pdf_count += 1
                        resultados.append(resultados_pagina)
                        continue  # Si es un PDF, no analizar y pasar a la siguiente URL

                    resultados_pagina['is_pdf'] = 0  # otros
                    resultados_pagina['tipo_documento'] = tipo_documento

                    if response.headers['content-type'].startswith(
                            'text'):
                        if es_html_valido(response.text):

                            print(f"Escaneando: {url_actual}")

                            resultados_pagina[
                                'enlaces_totales'] = 0  # Inicializar en 0
                            resultados_pagina[
                                'enlaces_inseguros'] = 0  # Inicializar en 0
                            resultados_pagina[
                                'enlaces_internos'] = 0  # Inicializar en 0
                            resultados_pagina[
                                'enlaces_internos_unicos'] = 0  # Inicializar en 0
                            resultados_pagina[
                                'enlaces_js_unicos'] = 0  # Inicializar en 0
                            resultados_pagina[
                                'enlaces_salientes'] = 0  # Inicializar en 0
                            resultados_pagina[
                                'enlaces_salientes_unicos'] = 0  # Inicializar en 0
                            resultados_pagina[
                                'enlaces_salientes_js_unicos'] = 0  # Inicializar en 0
                            resultados_pagina[
                                'enlaces_salientes_externos'] = 0  # Inicializar en 0
                            resultados_pagina[
                                'enlaces_salientes_externos_unicos'] = 0  # Inicializar en 0
                            resultados_pagina[
                                'enlaces_salientes_js_externos_unicos'] = 0  # Inicializar en 0

                         
                            heading_tags_count, h1_duplicate, h2_mas_70_caracteres, h2_duplicado, h2_multiple, h2_falta, h2_no_secuencial = analizar_heading_tags(
                                response.text)
                            meta_tags_info, meta_description_mas_155_caracteres, meta_description_duplicado, canonicals_falta, directivas_noindex, \
                                falta_encabezado_x_content_type_options, falta_encabezado_secure_referrer_policy, \
                                falta_encabezado_content_security_policy, falta_encabezado_x_frame_options, \
                                titulos_pagina_menos_30_caracteres, meta_description_menos_70_caracteres, titulos_pagina_mas_60_caracteres, \
                                titulos_pagina_igual_h1, titulos_pagina_duplicado, meta_description_falta, version_http, ultima_modificacion, \
                                meta_og_card, meta_og_title, meta_og_image = extraer_meta_tags(response.text, response)

                            # Asignación de los resultados a resultados_pagina
                            resultados_pagina[
                                'heading_tags'] = heading_tags_count or {}
                            resultados_pagina['h1_duplicate'] = h1_duplicate
                            resultados_pagina[
                                'h2_mas_70_caracteres'] = h2_mas_70_caracteres
                            resultados_pagina['h2_duplicado'] = h2_duplicado
                            resultados_pagina['h2_multiple'] = h2_multiple
                            resultados_pagina['h2_falta'] = h2_falta
                            resultados_pagina[
                                'h2_no_secuencial'] = h2_no_secuencial

                            resultados_pagina[
                                'meta_tags'] = meta_tags_info or {}
                            resultados_pagina[
                                'meta_description_mas_155_caracteres'] = meta_description_mas_155_caracteres
                            resultados_pagina[
                                'meta_description_duplicado'] = meta_description_duplicado
                            resultados_pagina[
                                'canonicals_falta'] = canonicals_falta
                            resultados_pagina[
                                'directivas_noindex'] = directivas_noindex
                            resultados_pagina[
                                'falta_encabezado_x_content_type_options'] = falta_encabezado_x_content_type_options
                            resultados_pagina[
                                'falta_encabezado_secure_referrer_policy'] = falta_encabezado_secure_referrer_policy
                            resultados_pagina[
                                'falta_encabezado_content_security_policy'] = falta_encabezado_content_security_policy
                            resultados_pagina[
                                'falta_encabezado_x_frame_options'] = falta_encabezado_x_frame_options
                            resultados_pagina[
                                'titulos_pagina_menos_30_caracteres'] = titulos_pagina_menos_30_caracteres
                            resultados_pagina[
                                'meta_description_menos_70_caracteres'] = meta_description_menos_70_caracteres
                            resultados_pagina[
                                'titulos_pagina_mas_60_caracteres'] = titulos_pagina_mas_60_caracteres
                            resultados_pagina[
                                'titulos_pagina_igual_h1'] = titulos_pagina_igual_h1
                            resultados_pagina[
                                'titulos_pagina_duplicado'] = titulos_pagina_duplicado
                            resultados_pagina[
                                'meta_description_falta'] = meta_description_falta
                            resultados_pagina['version_http'] = version_http
                            resultados_pagina[
                                'ultima_modificacion'] = ultima_modificacion
                            resultados_pagina['meta_og_card'] = meta_og_card
                            resultados_pagina['meta_og_title'] = meta_og_title
                            resultados_pagina['meta_og_image'] = meta_og_image

                            meta_tags_revision = analizar_meta_tags(
                                response.text)
                            resultados_pagina.update(meta_tags_revision)

                            if meta_tags_revision['title_long']:
                                resultados_pagina[
                                    'title_long'] = meta_tags_revision[
                                        'title_long']
                            if meta_tags_revision['title_short']:
                                resultados_pagina[
                                    'title_short'] = meta_tags_revision[
                                        'title_short']
                            if meta_tags_revision['title_duplicate']:
                                resultados_pagina[
                                    'title_duplicate'] = meta_tags_revision[
                                        'title_duplicate']
                            if meta_tags_revision['desc_long']:
                                resultados_pagina[
                                    'desc_long'] = meta_tags_revision[
                                        'desc_long']
                            if meta_tags_revision['desc_short']:
                                resultados_pagina[
                                    'desc_short'] = meta_tags_revision[
                                        'desc_short']

                            info_imagenes, image_types, images_1MB, imagenes_rotas = extraer_informacion_imagenes(
                                response.text, url_actual)  #images_1MB
                            resultados_pagina['imagenes'] = info_imagenes or []
                            resultados_pagina[
                                'alt_vacias'] = contar_alt_vacias(
                                    response.text)

                            palabras, frases, media_palabras_frase,flesh_score = contar_palabras_visibles(response.text)

                            resultados_pagina['num_palabras'] = palabras
                            resultados_pagina['frases'] = frases
                            resultados_pagina['media_palabras_frase'] = media_palabras_frase
                            resultados_pagina['flesh_score'] = flesh_score
                                                        
                            #resultados_pagina[
                            #    'num_palabras'] = contar_palabras_visibles(
                            #        response.text)

                            enlaces_totales, enlaces_inseguros, enlaces_internos, enlaces_internos_unicos, enlaces_js_unicos, enlaces_salientes, enlaces_salientes_unicos, enlaces_salientes_js_unicos, enlaces_salientes_externos, enlaces_salientes_externos_unicos, enlaces_salientes_js_externos_unicos,\
                            j_enlaces_totales, j_enlaces_inseguros, j_enlaces_internos, j_enlaces_internos_unicos, j_enlaces_js_unicos, j_enlaces_salientes, j_enlaces_salientes_unicos, j_enlaces_salientes_js_unicos, j_enlaces_salientes_externos, j_enlaces_salientes_externos_unicos, j_enlaces_salientes_js_externos_unicos = contar_enlaces(response.text)

                            # Almacenar en la base de datos los resultados obtenidos
                            resultados_pagina[
                                'enlaces_totales'] = enlaces_totales
                            resultados_pagina[
                                'enlaces_inseguros'] = enlaces_inseguros
                            resultados_pagina[
                                'enlaces_internos'] = enlaces_internos
                            resultados_pagina[
                                'enlaces_internos_unicos'] = enlaces_internos_unicos
                            resultados_pagina[
                                'enlaces_js_unicos'] = enlaces_js_unicos
                            resultados_pagina[
                                'enlaces_salientes'] = enlaces_salientes
                            resultados_pagina[
                                'enlaces_salientes_unicos'] = enlaces_salientes_unicos
                            resultados_pagina[
                                'enlaces_salientes_js_unicos'] = enlaces_salientes_js_unicos
                            resultados_pagina[
                                'enlaces_salientes_externos'] = enlaces_salientes_externos
                            resultados_pagina[
                                'enlaces_salientes_externos_unicos'] = enlaces_salientes_externos_unicos
                            resultados_pagina[
                                'enlaces_salientes_js_externos_unicos'] = enlaces_salientes_js_externos_unicos

                            resultados_pagina['images_1MB'] = images_1MB
                            resultados_pagina[
                                'imagenes_rotas'] = imagenes_rotas

                            tipos_archivos = contar_tipos_archivos(
                                response.text)
                            resultados_pagina[
                                'tipos_archivos'] = tipos_archivos
                            resultados_pagina[
                                'peso_total_pagina'] = tipos_archivos.get(
                                    'peso_total', 0)

                            texto_visible = extraer_texto_visible(
                                response.text)
                            errores_ortograficos = analizar_ortografia(
                                url_actual, texto_visible
                            )  #analizar_ortografia(texto_visible)
                            resultados_pagina[
                                'errores_ortograficos'] = errores_ortograficos
                            resultados_pagina[
                                'num_errores_ortograficos'] = len(
                                    errores_ortograficos)

                            resultados_pagina['lang'] =obtener_idioma_desde_url(
                                url_actual)

                            # Nuevos campos de revisiÃ³n
                            #meta_tags_revision = analizar_meta_tags(response.text)
                            #resultados_pagina.update(meta_tags_revision)

                            resultados_pagina['html_valid'] = es_html_valido(
                                response.text)
                            resultados_pagina[
                                'content_valid'] = es_contenido_valido(
                                    response.text)
                            resultados_pagina[
                                'responsive_valid'] = es_responsive_valid(
                                    response.text)

                            # Actualizar los campos a True si las validaciones son exitosas
                            if resultados_pagina['html_valid']:
                                resultados_pagina['e_html'] = True
                            if resultados_pagina['content_valid']:
                                resultados_pagina['e_body'] = True
                            if resultados_pagina['responsive_valid']:
                                resultados_pagina['e_viewport'] = True

                            # Contar las veces que se repiten los diferentes tipos de formato de imagen
                            image_types_count = Counter(image_types)
                            resultados_pagina[
                                'image_types'] = image_types_count

                            # Ejecutar pa11y y obtener resultados WCAG AAA
                            pa11y_results_csv = ejecutar_pa11y(url_actual)

                            # Antes de la inserción en la base de datos
                            resultados_pagina['wcagaaa'] = pa11y_results_csv
                            #resultados_pagina['wcagaaa'] = {'pa11y_results': pa11y_results_csv}
                            #resultados_pagina['wcagaaa']['pa11y_results'] = list(pa11y_results_csv)
                            #resultados_pagina['wcagaaa'] = {'pa11y_results': pa11y_results_csv}
                            resultados_pagina[
                                'valid_aaa'] = not pa11y_results_csv  # True si no hay recomendaciones, False en caso contrario

                            resultados_pagina['is_pdf'] = 2  # es un html
                        else:
                            resultados_pagina[
                                'codigo_respuesta'] = codigo_respuesta
                            resultados_pagina[
                                'tipo_documento'] = tipo_documento

            else:
                resultados_pagina['codigo_respuesta'] = codigo_respuesta
                resultados_pagina['tipo_documento'] = tipo_documento

            resultados.append(resultados_pagina)

            soup = BeautifulSoup(response.text, 'html.parser')

            # Extraer enlaces con etiqueta 'a' (href)
            enlaces_href = [
                urljoin(url_actual, a['href'])
                for a in soup.find_all('a', href=True)
            ]

            # Extraer enlaces con etiqueta 'src'
            enlaces_src = [
                urljoin(url_actual, img['src'])
                for img in soup.find_all('img', src=True)
            ]

            # Combinar las dos listas de enlaces
            enlaces = enlaces_href + enlaces_src

            enlaces_filtrados = [
                (enlace, url_actual) for enlace in enlaces
                if urlparse(enlace).netloc == dominio_base and not any(
                    patron in enlace for patron in exclusiones) and not any(
                        enlace.endswith(ext) for ext in extensiones_excluidas)
            ]

            urls_por_escanear.extend(enlaces_filtrados)
        except Exception as e:
            print(f"Error al escanear {url_actual}: {str(e)}")

        urls_escaneadas.add(url_actual)

    return resultados


def generar_informe_resumen(resumen, nombre_archivo):
    header_present = os.path.exists(nombre_archivo)

    idiomas_encontrados = Counter()
    total_404 = Counter()
    total_enlaces_inseguros = Counter()
    paginas_inseguras = Counter()

    with open(nombre_archivo, 'a', newline='',
              encoding='utf-8') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)

        if not header_present:
            escritor_csv.writerow([
                'dominio', 'total_paginas', 'duracion_total',
                'codigos_respuesta', 'hora_inicio', 'hora_fin', 'fecha',
                'html_valid_count', 'content_valid_count',
                'responsive_valid_count', 'valid_aaaa_pages', 'idiomas',
                'paginas_inseguras', 'total_404', 'total_enlaces_inseguros',
                'pages_title_long', 'pages_title_short', 'pages_title_dup',
                'pages_desc_long', 'pages_desc_short', 'pages_h1_dup',
                'pages_img_1mb', 'id_escaneo', 'tiempo_medio',
                'pages_err_orto', 'pages_alt_vacias', 'peso_total_paginas',
                'pdf_count', 'html_count', 'others_count'
            ])  # Agregar nuevos campos

        for dominio, datos in resumen.items():
            #print(f'Dominio: {dominio}, Datos: {datos}')
            total_404 =  0
            paginas_inseguras = 0
            total_enlaces_inseguros =  0
            pages_title_long = 0
            pages_title_short =  0
            pages_title_dup = 0
            pages_desc_long =  0
            pages_desc_short =  0
            html_valid_count =  0
            content_valid_count =  0
            responsive_valid_count =  0
            valid_aaaa_pages =  0 # Contador para pÃ¡ginas con 'valid_aaa' True
            codigos_respuesta = datos['codigos_respuesta']
            total_paginas = datos['total_paginas']
            duracion_total = datos['duracion_total']
            id_escaneo = datos['id_escaneo']
            #paginas_inseguras = sum(pagina.get('enlaces_inseguros', 0) > 0 for pagina in datos.get('paginas', []))
            total_404 = datos[
                'total_404']  #sum(pagina.get('codigo_respuesta', 0) == 404 for pagina in datos.get('paginas', []))
            tiempo_medio = datos[
                'tiempo_medio']  # (sum(pagina.get('tiempo_respuesta', 0) for pagina in datos.get('paginas', []))) / (total_paginas)
            pages_err_orto = 0
            pages_alt_vacias = 0
            peso_total_paginas = 0
            pdf_count =  0
            html_count =  0
            others_count =  0

            #for pagina in datos.get('paginas', []):
            #print(resultados_dominio)
            for pagina in resultados_dominio:
                total_enlaces_inseguros += pagina.get('enlaces_inseguros')
                peso_total_paginas += pagina.get('peso_total_pagina')

                if pagina.get('is_pdf') == 1:
                    pdf_count += 1

                if pagina.get('is_pdf') == 2:
                    html_count += 1

                if pagina.get('is_pdf') == 0:
                    others_count += 1

                if pagina.get('alt_vacias') >= 1:
                    pages_alt_vacias += 1

                if pagina.get('num_errores_ortograficos') >= 1:
                    pages_err_orto += 1

                if pagina.get('codigo_respuesta') == 404:
                    total_404 += 1

                if pagina.get('enlaces_inseguros') >= 1:
                    paginas_inseguras += 1

                lang = pagina.get('lang')
                if lang:
                    idiomas_encontrados[lang] += 1

                html_valid_count += bool(pagina.get('html_valid', False))
                content_valid_count += bool(pagina.get('content_valid', False))
                responsive_valid_count += bool(
                    pagina.get('responsive_valid', False))
                valid_aaaa_pages += bool(pagina.get(
                    'valid_aaa',
                    False))  # Incrementa el contador si 'valid_aaa' es True
                #print(resultados_dominio)

            pages_title_long = sum(1 if pagina.get('title_long') else 0 for pagina in resultados_dominio)
            pages_title_short = sum(1 if pagina.get('title_short') else 0 for pagina in resultados_dominio)
            pages_title_dup = sum(1 if pagina.get('title_duplicate') else 0 for pagina in resultados_dominio)
            pages_desc_long = sum(1 if pagina.get('desc_long') else 0 for pagina in resultados_dominio)
            pages_desc_short = sum(1 if pagina.get('desc_short') else 0 for pagina in resultados_dominio)
            pages_h1_dup = sum(1 if pagina.get('h1_duplicate') else 0 for pagina in resultados_dominio)
            pages_img_1mb = sum(1 if pagina.get('images_1MB') else 0 for pagina in resultados_dominio)


            # Convert Counter to dictionary before writing to CSV
            idiomas_encontrados_dict = dict(idiomas_encontrados)

            # Imprimir para depuraciÃ³n
            logging.info(
                f'Dominio: {dominio}, Idiomas Encontrados: {idiomas_encontrados_dict}, Total 404: {total_404},Total enlaces inseguros: {total_enlaces_inseguros}, Paginas Inseguras: {paginas_inseguras}'
            )
            print(
                f'Dominio: {dominio}, Idiomas Encontrados: {idiomas_encontrados_dict}'
            )
            print(
                f'Total 404: {total_404}, Total enlaces inseguros: {total_enlaces_inseguros}, Paginas Inseguras: {paginas_inseguras}'
            )
            print(
                f'Total Paginas con errores: {pages_err_orto}, Total paginas con alt vacios: {pages_alt_vacias}, Paginas Inseguras: {paginas_inseguras}'
            )

            escritor_csv.writerow([
                dominio, total_paginas, duracion_total, codigos_respuesta,
                datos['hora_inicio'], datos['hora_fin'], datos['fecha'],
                html_valid_count, content_valid_count, responsive_valid_count,
                valid_aaaa_pages, idiomas_encontrados_dict, paginas_inseguras,
                total_404, total_enlaces_inseguros, pages_title_long,
                pages_title_short, pages_title_dup, pages_desc_long,
                pages_desc_short, pages_h1_dup, pages_img_1mb, id_escaneo,
                tiempo_medio, pages_err_orto, pages_alt_vacias,
                peso_total_paginas, pdf_count, html_count, others_count
            ])  # Actualizado con nuevos campos


def guardar_en_csv_y_json(resultados, nombre_archivo_base, modo='w'):
    campos = [
        'fecha_escaneo', 'dominio', 'codigo_respuesta', 'tipo_documento',
        'tiempo_respuesta', 'pagina', 'parent_url', 'meta_tags',
        'heading_tags', 'imagenes', 'enlaces_totales', 'enlaces_inseguros',
        'tipos_archivos', 'errores_ortograficos', 'num_errores_ortograficos',
        'num_redirecciones', 'alt_vacias', 'num_palabras', 'e_title', 'e_head',
        'e_body', 'e_html', 'e_robots', 'e_description', 'e_keywords',
        'e_viewport', 'e_charset', 'html_valid', 'content_valid',
        'responsive_valid', 'image_types', 'wcagaaa', 'valid_aaa', 'lang',
        'title_long', 'title_short', 'title_duplicate', 'desc_long',
        'desc_short', 'h1_duplicate', 'images_1MB', 'imagenes_rotas',
        'id_escaneo', 'alt_vacias', 'peso_total_pagina', 'is_pdf', 'c_title',
        'c_robots', 'c_description', 'c_keywords', 'c_charset', 'frases',
        'media_palabras_frase', 'flesh_score', 'enlaces_internos',
        'enlaces_internos_unicos', 'enlaces_js_unicos', 'enlaces_salientes',
        'enlaces_salientes_unicos', 'enlaces_salientes_js_unicos',
        'enlaces_salientes_externos', 'enlaces_salientes_externos_unicos',
        'enlaces_salientes_js_externos_unicos', 'h2_mas_70_caracteres',
        'h2_duplicado', 'h2_multiple', 'h2_falta', 'h2_no_secuencial',
        'meta_description_mas_155_caracteres', 'meta_description_duplicado',
        'canonicals_falta', 'directivas_noindex',
        'falta_encabezado_x_content_type_options',
        'falta_encabezado_secure_referrer_policy',
        'falta_encabezado_content_security_policy',
        'falta_encabezado_x_frame_options',
        'titulos_pagina_menos_30_caracteres',
        'meta_description_menos_70_caracteres',
        'titulos_pagina_mas_60_caracteres', 'titulos_pagina_igual_h1',
        'titulos_pagina_duplicado', 'meta_description_falta', 'version_http',
        'ultima_modificacion', 'meta_og_card', 'meta_og_title', 'meta_og_image'
    ]

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    nombre_archivo = f"{timestamp}-{nombre_archivo_base}"

    # Archivo CSV
    with open(f"results/{nombre_archivo}.csv",
              modo,
              newline='',
              encoding='utf-8') as archivo_csv:
        escritor_csv = csv.DictWriter(archivo_csv, fieldnames=campos)
        if modo == 'w':
            escritor_csv.writeheader()

        for resultado in resultados:
            # AsegÃºrate de que las claves que no estÃ©n presentes en el diccionario tengan un valor por defecto de False
            resultado.setdefault('meta_tags', False)
            resultado.setdefault('tipo_documento', False)
            resultado.setdefault('heading_tags', False)
            resultado.setdefault('imagenes', False)
            resultado.setdefault('enlaces_totales', 0)
            resultado.setdefault('enlaces_inseguros', 0)
            resultado.setdefault('enlaces_internos', 0)
            resultado.setdefault('enlaces_internos_unicos', 0)
            resultado.setdefault('enlaces_js_unicos', 0)
            resultado.setdefault('enlaces_salientes', 0)
            resultado.setdefault('enlaces_salientes_unicos', 0)
            resultado.setdefault('enlaces_salientes_js_unicos', 0)
            resultado.setdefault('enlaces_salientes_externos', 0)
            resultado.setdefault('enlaces_salientes_externos_unicos', 0)
            resultado.setdefault('enlaces_salientes_js_externos_unicos', 0)
            resultado.setdefault('tipos_archivos', False)
            resultado.setdefault('errores_ortograficos', False)
            resultado.setdefault('num_errores_ortograficos', 0)
            resultado.setdefault('num_redirecciones', '0')
            resultado.setdefault('alt_vacias', 0)
            resultado.setdefault('num_palabras', 0)
            resultado.setdefault('frases', 0)
            resultado.setdefault('media_palabras_frase', 0)
            resultado.setdefault('flesh_score', False)
            resultado.setdefault('e_title', False)
            resultado.setdefault('e_head', False)
            resultado.setdefault('e_body', False)
            resultado.setdefault('e_html', False)
            resultado.setdefault('e_robots', False)
            resultado.setdefault('e_description', False)
            resultado.setdefault('e_keywords', False)
            resultado.setdefault('e_viewport', False)
            resultado.setdefault('e_charset', False)
            resultado.setdefault('c_title', False)
            resultado.setdefault('c_robots', False)
            resultado.setdefault('c_description', False)
            resultado.setdefault('c_keywords', False)
            resultado.setdefault('c_charset', False)
            resultado.setdefault('html_valid', 0)
            resultado.setdefault('content_valid', 0)
            resultado.setdefault('responsive_valid', 0)
            resultado.setdefault('wcagaaa', {})
            resultado.setdefault(
                'image_types', {}
            )  # AsegÃºrate de que 'image_types' estÃ© presente con un valor por defecto
            resultado.setdefault('lang', False)
            resultado.setdefault('images_1MB', 0)
            resultado.setdefault('imagenes_rotas', 0)
            resultado.setdefault('is_pdf', -1)
            resultado.setdefault('valid_aaa', False)

            resultado.setdefault('h2_mas_70_caracteres', 0)
            resultado.setdefault('h2_duplicado', 0)
            resultado.setdefault('h2_multiple', 0)
            resultado.setdefault('h2_falta', 0)
            resultado.setdefault('h2_no_secuencial', 0)

            resultado.setdefault('meta_description_mas_155_caracteres', 0)
            resultado.setdefault('meta_description_duplicado', 0)
            resultado.setdefault('canonicals_falta', 0)
            resultado.setdefault('directivas_noindex', 0)
            resultado.setdefault('falta_encabezado_x_content_type_options', 0)
            resultado.setdefault('falta_encabezado_secure_referrer_policy', 0)
            resultado.setdefault('falta_encabezado_content_security_policy', 0)
            resultado.setdefault('falta_encabezado_x_frame_options', 0)
            resultado.setdefault('titulos_pagina_menos_30_caracteres', 0)
            resultado.setdefault('meta_description_menos_70_caracteres', 0)
            resultado.setdefault('titulos_pagina_mas_60_caracteres', 0)
            resultado.setdefault('titulos_pagina_igual_h1', 0)
            resultado.setdefault('titulos_pagina_duplicado', 0)
            resultado.setdefault('meta_description_falta', 0)
            resultado.setdefault('version_http', 0)
            resultado.setdefault('ultima_modificacion', 0)
            resultado.setdefault('meta_og_card', 0)
            resultado.setdefault('meta_og_title', 0)
            resultado.setdefault('meta_og_image', 0)

            # Reemplaza los valores None por False
            resultado = {
                k: False if v is None else v
                for k, v in resultado.items()
            }

            escritor_csv.writerow(resultado)

    # Archivo JSON
    #with open(f"results/{nombre_archivo}.json", modo, encoding='utf-8') as archivo_json:
    #    if modo == 'w':
    #        json.dump(resultados, archivo_json, ensure_ascii=False, indent=4)


from config import DOMINIOS_ESPECIFICOS, USER, PWD, HOST, DB,  IS_RUNNING, FRECUENCIA, W3C_VALIDATOR, PATRONES_EXCLUSION, EXTENSIONES_EXCLUIDAS, KEYWORDS

if __name__ == "__main__":

    print(f"{USER}@{PWD}\\{DB}@{HOST}")

    # Directorios a verificar y crear si no existen
    directorios = ['logs', 'offline', 'results']

    # Verificar y crear los directorios si no existen
    for directorio in directorios:
        if not os.path.exists(directorio):
            os.makedirs(directorio)

    log_timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    log_nombre_archivo = f"logs/{log_timestamp}-registro.log"

    # ConfiguraciÃ³n del sistema de registro
    logging.basicConfig(filename=log_nombre_archivo, level=logging.DEBUG)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    start_script_time = time.time()

    print("aqui llega")
  
    #engine = create_engine("mysql+mysqlconnector://usuario:contraseña@localhost/db?connect_timeout=300")
    engine = create_engine(
        'mysql+mysqlconnector://' + USER + ':' + PWD + '@' + HOST + '/' + DB,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        pool_recycle=3600,
        echo=False
    )  # Cambia 'echo=True' a 'False' para desactivar el modo verbose
    print("aqui llega 2")
    Base.metadata.create_all(engine)
    print("aqui llega 3")

    # InicializaciÃ³n de la sesiÃ³n de SQLAlchemy
    Session = sessionmaker(bind=engine)
    session = Session()

    #carga las configuraciones

    print("aqui llega 4")

    ultima_configuracion = session.query(Configuracion).order_by(desc(Configuracion.id)).first()

    if ultima_configuracion:
        IS_RUNNING = ultima_configuracion.is_running
        DOMINIOS_ESPECIFICOS = [dominio for dominio in ultima_configuracion.dominios_analizar.split('\r\n') if dominio.strip()] if ultima_configuracion.dominios_analizar else []
        FRECUENCIA = ultima_configuracion.frecuencia_dias
        W3C_VALIDATOR = ultima_configuracion.w3c_validator
        PATRONES_EXCLUSION = [patron for patron in ultima_configuracion.url_Excluidas.split('\r\n') if patron.strip()] if ultima_configuracion.url_Excluidas else []
        EXTENSIONES_EXCLUIDAS = [extension for extension in ultima_configuracion.extensiones_Excluidas.split('\r\n') if extension.strip()] if ultima_configuracion.extensiones_Excluidas else []
        KEYWORDS = [keyword for keyword in ultima_configuracion.keywords_analizar.split('\r\n') if keyword.strip()] if ultima_configuracion.keywords_analizar else []
    else:
        print("Error al recuperar la configuración.")

                           
    #ultima_configuracion = session.query(Configuracion).order_by(desc(Configuracion.id)).first()
    #
    #if ultima_configuracion:
    #    IS_RUNNING = ultima_configuracion.is_running
    #    DOMINIOS_ESPECIFICOS = ultima_configuracion.dominios_analizar.split('\r\n') if ultima_configuracion.dominios_analizar else []
        #DOMINIOS_ESPECIFICOS = json.dumps(ultima_configuracion.dominios_analizar) if ultima_configuracion.dominios_analizar else []
    #    FRECUENCIA = ultima_configuracion.frecuencia_dias
    #    W3C_VALIDATOR = ultima_configuracion.w3c_validator
    #    PATRONES_EXCLUSION = ultima_configuracion.url_Excluidas.split('\r\n') if ultima_configuracion.url_Excluidas else []
    #    EXTENSIONES_EXCLUIDAS = ultima_configuracion.extensiones_Excluidas.split('\r\n') if ultima_configuracion.extensiones_Excluidas else []
    #    KEYWORDS = ultima_configuracion.keywords_analizar.split('\r\n') if ultima_configuracion.keywords_analizar else []
    #else:
    #    print("error recuperando config")
        
    #print("palabras diccionario de la base de datos dos diccionarios USUARIO")
    palabras_a_revisar = [palabra.palabra for palabra in session.query(Diccionario_usuario).all()]
    #print(palabras_a_revisar)
    #print("palabras diccionario de la base de datos dos diccionarios NORMALES")
    palabras_a_revisar.extend([palabra.palabra for palabra in session.query(Diccionario).all()])
    #print(palabras_a_revisar)
    session.close()

    #lista_palabras = json.dumps(palabras_a_revisar)
    
    palabras_limpias = []
    for palabra in palabras_a_revisar:
        # Remover caracteres no deseados como retornos de carro, espacios, tabuladores, etc.
        palabra_limpia = palabra.replace('\n', '').replace('\t', '').strip()
        palabras_limpias.append(palabra_limpia)

    PALABRAS_DICCIONARIO = palabras_a_revisar

    print(ultima_configuracion.dominios_analizar)

    #print("palabras diccionario de la base de datos dos diccionarios")
    # Imprimir los valores recogidos
    print("Última Configuración:")
    print(f"Is Running: {IS_RUNNING}")
    print(f"Dominios a Analizar: {DOMINIOS_ESPECIFICOS}")
    print(f"Frecuencia de Días: {FRECUENCIA}")
    print(f"W3C Validator: {W3C_VALIDATOR}")
    print(f"URL Excluidas: {PATRONES_EXCLUSION}")
    print(f"Extensiones Excluidas: {EXTENSIONES_EXCLUIDAS}")
    print(f"Keywords a Analizar: {KEYWORDS}")
    #print(f"Diccionario: {PALABRAS_DICCIONARIO}")


    print(f"ruta pally: pa11y --standard {W3C_VALIDATOR} -T 1 --ignore issue-code-2 --ignore issue-code-1 -r json <url_actual>")

    #Session = sessionmaker(bind=engine)

    #session = Session()

    urls_a_escanear = DOMINIOS_ESPECIFICOS
    patrones_exclusion = PATRONES_EXCLUSION
    extensiones_excluidas = EXTENSIONES_EXCLUIDAS


    if crear_lock(session):
        try:
            idiomas_por_dominio = {}
            resumen_escaneo = {}

            # Extraer todas las palabras de la columna "palabra" de la tabla "diccionario"
            #PALABRAS_DICCIONARIO = [
            #    row.palabra for row in session.query(Diccionario).all()
            #]
            #print(PALABRAS_DICCIONARIO)

            for url in DOMINIOS_ESPECIFICOS:
                print(f"url a escanear: {url}")
                start_time = time.time()
                hora_inicio = datetime.now().strftime('%H:%M:%S')

                id_escaneo = secrets.token_hex(32)

                resultados_dominio = escanear_dominio(url, PATRONES_EXCLUSION,
                                                    EXTENSIONES_EXCLUIDAS)
                end_time = time.time()

                duracion_total = end_time - start_time
                codigos_respuesta = [
                    resultado['codigo_respuesta']
                    for resultado in resultados_dominio
                ]
                total_paginas = len(resultados_dominio)

                # Verificar si la URL analizada es vÃ¡lida
                parsed_url = urlparse(url)
                if parsed_url.netloc:
                    dominio = parsed_url.netloc
                    # Crear un nuevo contador para cada dominio
                    idiomas_encontrados = Counter()

                    for pagina in resultados_dominio:
                        lang = pagina.get('lang')
                        if lang:
                            idiomas_encontrados[lang] += 1

                    idiomas_por_dominio[dominio] = idiomas_encontrados.copy()

                    print("idiomas por dominio")
                    print(idiomas_por_dominio)

                    print("idiomas encontrados")
                    print(idiomas_encontrados)

                    resumen_escaneo[dominio] = {
                        'dominio':
                        dominio,
                        'total_paginas':
                        total_paginas,
                        'duracion_total':
                        duracion_total,
                        'codigos_respuesta':
                        dict(
                            zip(codigos_respuesta, [
                                codigos_respuesta.count(c)
                                for c in codigos_respuesta
                            ])),
                        'hora_inicio':
                        hora_inicio,
                        'hora_fin':
                        datetime.now().strftime('%H:%M:%S'),
                        'fecha':
                        datetime.now().strftime('%Y-%m-%d'),
                        'html_valid_count':
                        sum(1 for pagina in resultados_dominio
                            if pagina.get('html_valid')),
                        'content_valid_count':
                        sum(1 for pagina in resultados_dominio
                            if pagina.get('content_valid')),
                        'responsive_valid_count':
                        sum(1 for pagina in resultados_dominio
                            if pagina.get('responsive_valid')),
                        'valid_aaaa_pages':
                        sum(1 for pagina in resultados_dominio
                            if pagina.get('valid_aaa')),
                        'idiomas':
                        idiomas_encontrados,
                        'enlaces_inseguros':
                        sum(1 for pagina in resultados_dominio
                            if pagina.get('enlaces_inseguros')),
                        'paginas_inseguras':
                        sum(1 for pagina in resultados_dominio
                            if pagina.get('paginas_inseguras')),
                        'total_404':
                        sum(1 for pagina in resultados_dominio
                            if pagina.get('total_404')),
                        'pages_h1_dup':
                        0,  # Nuevo campo
                        'pages_img_1mb':
                        0,  # Nuevo campo
                        'id_escaneo':
                        id_escaneo,
                        'tiempo_medio':
                        None,
                        'pages_err_orto':
                        0,  # sum(1 for pagina in resultados_dominio if pagina.get('num_errores_ortograficos') >= 1),
                        'pages_alt_vacias':
                        0,  #sum(1 for pagina in resultados_dominio if pagina.get('alt_vacias') >= 1)
                        'peso_total_paginas':
                        0,
                        'pdf_count':
                        -1,
                        'html_count':
                        -1,
                        'others_count':
                        -1,
                        'media_frases':
                        0,
                        'total_media_palabras_frase':
                        0,
                        'media_flesh_score':
                        0,
                        'total_meta_description_mas_155_caracteres':
                        0,
                        'total_meta_description_duplicado':
                        0,
                        'total_canonicals_falta':
                        0,
                        'total_directivas_noindex':
                        0,
                        'total_falta_encabezado_x_content_type_options':
                        0,
                        'total_falta_encabezado_secure_referrer_policy':
                        0,
                        'total_falta_encabezado_content_security_policy':
                        0,
                        'total_falta_encabezado_x_frame_options':
                        0,
                        'total_titulos_pagina_menos_30_caracteres':
                        0,
                        'total_meta_description_menos_70_caracteres':
                        0,
                        'total_titulos_pagina_mas_60_caracteres':
                        0,
                        'total_titulos_pagina_igual_h1':
                        0,
                        'total_titulos_pagina_duplicado':
                        0,
                        'total_meta_description_falta':
                        0,
                        'total_h2_duplicado':
                        0,
                        'total_h2_mas_70_caracteres':
                        0,
                        'total_h2_multiple':
                        0,
                        'total_h2_falta':
                        0,
                        'total_h2_no_secuencial':
                        0,
                        'pages_title_long' : 0,
                        'pages_title_short' :  0,
                        'pages_title_dup' : 0,
                        'pages_desc_long' :  0,
                        'pages_desc_short' :  0,
                    }

                    guardar_en_csv_y_json(resultados_dominio,
                                        f"{dominio}_resultados")

                    with Session() as session:
                        for resultado_pagina in resultados_dominio:
                            if 'pagina' in resultado_pagina and isinstance(
                                    resultado_pagina['pagina'], str):
                                resultado_pagina['pagina'] = resultado_pagina[
                                    'pagina'].encode('utf-8')
                                resultado_pagina['id_escaneo'] = id_escaneo
                                resultado = Resultado(**resultado_pagina)
                                guardar_en_resultados(session, resultado)
                            else:
                                print(
                                    f"La URL {url} no se pudo analizar correctamente."
                                )

            with Session() as session:
                for url, resumen in resumen_escaneo.items():
                    sumario = Sumario(**resumen)
                    sumario.idiomas = str(dict(idiomas_por_dominio[url]))
                    guardar_en_sumario(session, sumario)

            with Session() as session:
                with session.no_autoflush:
                    for dominio, resumen in resumen_escaneo.items():
                        # Obtener la fecha más reciente para el dominio
                        most_recent_date = session.query(
                            func.max(Resultado.fecha_escaneo)).filter(
                                Resultado.dominio == dominio).scalar()

                        most_recent_id_escaneo = resumen['id_escaneo']

                        # Si no hay registros para el dominio, continuar con el siguiente
                        if most_recent_date is None:
                            continue

                        pages_title_long = sum(1 if pagina.get('title_long') else 0 for pagina in resultados_dominio)
                        pages_title_short = sum(1 if pagina.get('title_short') else 0 for pagina in resultados_dominio)
                        pages_title_dup = sum(1 if pagina.get('title_duplicate') else 0 for pagina in resultados_dominio)
                        pages_desc_long = sum(1 if pagina.get('desc_long') else 0 for pagina in resultados_dominio)
                        pages_desc_short = sum(1 if pagina.get('desc_short') else 0 for pagina in resultados_dominio)
                        pages_h1_dup = sum(1 if pagina.get('h1_duplicate') else 0 for pagina in resultados_dominio)
                        pages_img_1mb = sum(1 if pagina.get('images_1MB') else 0 for pagina in resultados_dominio)

                        suma_media_frases = session.query(
                            func.sum(Resultado.frases)).filter(
                                Resultado.dominio == dominio,
                                Resultado.codigo_respuesta == 200,
                                Resultado.id_escaneo == most_recent_id_escaneo,
                                Resultado.frases > 0
                                #Resultado.fecha_escaneo == most_recent_date
                            ).scalar()

                        print(total_paginas)
                        print(suma_media_frases)

                        suma_media_frases = suma_media_frases if suma_media_frases is not None else 0

                        if total_paginas is not None and suma_media_frases is not None and total_paginas != 0:
                            media_frases = suma_media_frases / total_paginas
                        else:
                            media_frases = 0

                        print(f"media_frases : {media_frases }")

                        suma_media_palabras_frase = session.query(
                            func.sum(Resultado.media_palabras_frase)).filter(
                                Resultado.dominio == dominio,
                                Resultado.codigo_respuesta == 200,
                                Resultado.id_escaneo == most_recent_id_escaneo,
                                Resultado.media_palabras_frase > 0
                                #Resultado.fecha_escaneo == most_recent_date
                            ).scalar()

                        suma_media_palabras_frase = suma_media_palabras_frase if suma_media_palabras_frase is not None else 0

                        if total_paginas is not None and suma_media_palabras_frase is not None and total_paginas != 0:
                            total_media_palabras_frase = suma_media_palabras_frase / total_paginas
                        else:
                            total_media_palabras_frase = 0

                        print(
                            f"total_media_palabras_frase : {total_media_palabras_frase}"
                        )

                        suma_flesh_scores = session.query(
                            func.sum(Resultado.flesh_score)).filter(
                                Resultado.dominio == dominio,
                                Resultado.codigo_respuesta == 200,
                                Resultado.id_escaneo == most_recent_id_escaneo,
                                Resultado.flesh_score > 0
                                #Resultado.fecha_escaneo == most_recent_date
                            ).scalar()

                        suma_flesh_scores = suma_flesh_scores if suma_flesh_scores is not None else 0

                        if total_paginas is not None and suma_flesh_scores is not None and total_paginas != 0:
                            media_flesh_score = suma_flesh_scores / total_paginas
                        else:
                            media_flesh_score = 0

                        # Imprime o utiliza la media_ponderada como sea necesario
                        print(f"Media flesh score: {media_flesh_score}")

                        resultados_tmp_20 = session.query(Resultado).filter(
                            Resultado.dominio == dominio,
                            Resultado.codigo_respuesta == 200,
                            Resultado.id_escaneo == most_recent_id_escaneo,
                            Resultado.meta_description_mas_155_caracteres > 0
                            #Resultado.fecha_escaneo == most_recent_date
                        ).all()

                        total_meta_description_mas_155_caracteres = len(
                            resultados_tmp_20)

                        print(
                            f"total_meta_description_mas_155_caracteres: {total_meta_description_mas_155_caracteres}"
                        )

                        resultados_tmp_19 = session.query(Resultado).filter(
                            Resultado.dominio == dominio,
                            Resultado.codigo_respuesta == 200,
                            Resultado.id_escaneo == most_recent_id_escaneo,
                            Resultado.meta_description_duplicado > 0
                            #Resultado.fecha_escaneo == most_recent_date
                        ).all()

                        total_meta_description_duplicado = len(resultados_tmp_19)

                        print(
                            f"total_meta_description_duplicado: {total_meta_description_duplicado}"
                        )

                        resultados_tmp_18 = session.query(Resultado).filter(
                            Resultado.dominio == dominio,
                            Resultado.codigo_respuesta == 200,
                            Resultado.id_escaneo == most_recent_id_escaneo,
                            Resultado.canonicals_falta > 0
                            #Resultado.fecha_escaneo == most_recent_date
                        ).all()

                        total_canonicals_falta = len(resultados_tmp_18)

                        print(f"total_canonicals_falta: {total_canonicals_falta}")

                        resultados_tmp_17 = session.query(Resultado).filter(
                            Resultado.dominio == dominio,
                            Resultado.codigo_respuesta == 200,
                            Resultado.id_escaneo == most_recent_id_escaneo,
                            Resultado.directivas_noindex > 0
                            #Resultado.fecha_escaneo == most_recent_date
                        ).all()

                        total_directivas_noindex = len(resultados_tmp_17)

                        print(
                            f"total_directivas_noindex: {total_directivas_noindex}"
                        )

                        resultados_tmp_16 = session.query(Resultado).filter(
                            Resultado.dominio == dominio,
                            Resultado.codigo_respuesta == 200,
                            Resultado.id_escaneo == most_recent_id_escaneo,
                            Resultado.falta_encabezado_x_content_type_options > 0
                            #Resultado.fecha_escaneo == most_recent_date
                        ).all()

                        total_falta_encabezado_x_content_type_options = len(
                            resultados_tmp_16)

                        print(
                            f"total_falta_encabezado_x_content_type_options: {total_falta_encabezado_x_content_type_options}"
                        )

                        resultados_tmp_15 = session.query(Resultado).filter(
                            Resultado.dominio == dominio,
                            Resultado.codigo_respuesta == 200,
                            Resultado.id_escaneo == most_recent_id_escaneo,
                            Resultado.falta_encabezado_secure_referrer_policy > 0
                            #Resultado.fecha_escaneo == most_recent_date
                        ).all()

                        total_falta_encabezado_secure_referrer_policy = len(
                            resultados_tmp_15)

                        print(
                            f"total_falta_encabezado_secure_referrer_policy : {total_falta_encabezado_secure_referrer_policy }"
                        )

                        resultados_tmp_14 = session.query(Resultado).filter(
                            Resultado.dominio == dominio,
                            Resultado.codigo_respuesta == 200,
                            Resultado.id_escaneo == most_recent_id_escaneo,
                            Resultado.falta_encabezado_content_security_policy > 0
                            #Resultado.fecha_escaneo == most_recent_date
                        ).all()

                        total_falta_encabezado_content_security_policy = len(
                            resultados_tmp_14)

                        print(
                            f"total_falta_encabezado_content_security_policy : {total_falta_encabezado_content_security_policy}"
                        )

                        resultados_tmp_13 = session.query(Resultado).filter(
                            Resultado.dominio == dominio,
                            Resultado.codigo_respuesta == 200,
                            Resultado.id_escaneo == most_recent_id_escaneo,
                            Resultado.falta_encabezado_x_frame_options > 0
                            #Resultado.fecha_escaneo == most_recent_date
                        ).all()

                        total_falta_encabezado_x_frame_options = len(
                            resultados_tmp_13)

                        print(
                            f"total_falta_encabezado_x_frame_options : {total_falta_encabezado_x_frame_options}"
                        )

                        resultados_tmp_12 = session.query(Resultado).filter(
                            Resultado.dominio == dominio,
                            Resultado.codigo_respuesta == 200,
                            Resultado.id_escaneo == most_recent_id_escaneo,
                            Resultado.titulos_pagina_menos_30_caracteres > 0
                            #Resultado.fecha_escaneo == most_recent_date
                        ).all()

                        total_titulos_pagina_menos_30_caracteres = len(
                            resultados_tmp_12)

                        print(
                            f"total_titulos_pagina_menos_30_caracteres : {total_titulos_pagina_menos_30_caracteres}"
                        )

                        resultados_tmp_11 = session.query(Resultado).filter(
                            Resultado.dominio == dominio,
                            Resultado.codigo_respuesta == 200,
                            Resultado.id_escaneo == most_recent_id_escaneo,
                            Resultado.meta_description_menos_70_caracteres > 0
                            #Resultado.fecha_escaneo == most_recent_date
                        ).all()

                        total_meta_description_menos_70_caracteres = len(
                            resultados_tmp_11)

                        print(
                            f"total_meta_description_menos_70_caracteres : {total_meta_description_menos_70_caracteres}"
                        )

                        resultados_tmp_10 = session.query(Resultado).filter(
                            Resultado.dominio == dominio,
                            Resultado.codigo_respuesta == 200,
                            Resultado.id_escaneo == most_recent_id_escaneo,
                            Resultado.titulos_pagina_mas_60_caracteres > 0
                            #Resultado.fecha_escaneo == most_recent_date
                        ).all()

                        total_titulos_pagina_mas_60_caracteres = len(
                            resultados_tmp_10)

                        print(
                            f"total_titulos_pagina_mas_60_caracteres  : {total_titulos_pagina_mas_60_caracteres}"
                        )

                        resultados_tmp_9 = session.query(Resultado).filter(
                            Resultado.dominio == dominio,
                            Resultado.codigo_respuesta == 200,
                            Resultado.id_escaneo == most_recent_id_escaneo,
                            Resultado.titulos_pagina_igual_h1 > 0
                            #Resultado.fecha_escaneo == most_recent_date
                        ).all()

                        total_titulos_pagina_igual_h1 = len(resultados_tmp_9)

                        print(
                            f"total_titulos_pagina_igual_h1  : {total_titulos_pagina_igual_h1}"
                        )

                        resultados_tmp_8 = session.query(Resultado).filter(
                            Resultado.dominio == dominio,
                            Resultado.codigo_respuesta == 200,
                            Resultado.id_escaneo == most_recent_id_escaneo,
                            Resultado.titulos_pagina_duplicado > 0
                            #Resultado.fecha_escaneo == most_recent_date
                        ).all()

                        total_titulos_pagina_duplicado = len(resultados_tmp_8)

                        print(
                            f"total_titulos_pagina_duplicado   : {total_titulos_pagina_duplicado }"
                        )

                        #resultados_tmp_7 = session.query(Resultado).filter(
                        #    Resultado.dominio == dominio,
                        #    Resultado.codigo_respuesta == 200,
                        #    Resultado.id_escaneo == most_recent_id_escaneo,
                        #    Resultado.titulos_pagina_duplicado > 0
                        #    #Resultado.fecha_escaneo == most_recent_date
                        #).all()

                        #total_media_palabras_frase = len(resultados_tmp_7)

                        #print(f"total_media_palabras_frase : {total_media_palabras_frase}")

                        resultados_tmp_6 = session.query(Resultado).filter(
                            Resultado.dominio == dominio,
                            Resultado.codigo_respuesta == 200,
                            Resultado.id_escaneo == most_recent_id_escaneo,
                            Resultado.meta_description_falta > 0
                            #Resultado.fecha_escaneo == most_recent_date
                        ).all()

                        total_meta_description_falta = len(resultados_tmp_6)

                        print(
                            f"total_meta_description_falta    : {total_meta_description_falta}"
                        )

                        resultados_tmp_5 = session.query(Resultado).filter(
                            Resultado.dominio == dominio,
                            Resultado.codigo_respuesta == 200,
                            Resultado.id_escaneo == most_recent_id_escaneo,
                            Resultado.h2_duplicado > 0
                            #Resultado.fecha_escaneo == most_recent_date
                        ).all()

                        total_h2_duplicado = len(resultados_tmp_5)

                        print(f"total_h2_duplicado  : {total_h2_duplicado}")

                        resultados_tmp_4 = session.query(Resultado).filter(
                            Resultado.dominio == dominio,
                            Resultado.codigo_respuesta == 200,
                            Resultado.id_escaneo == most_recent_id_escaneo,
                            Resultado.h2_mas_70_caracteres > 0
                            #Resultado.fecha_escaneo == most_recent_date
                        ).all()

                        total_h2_mas_70_caracteres = len(resultados_tmp_4)

                        print(
                            f"total_h2_mas_70_caracteres : {total_h2_mas_70_caracteres}"
                        )

                        resultados_tmp_3 = session.query(Resultado).filter(
                            Resultado.dominio == dominio,
                            Resultado.codigo_respuesta == 200,
                            Resultado.id_escaneo == most_recent_id_escaneo,
                            Resultado.h2_multiple > 0
                            #Resultado.fecha_escaneo == most_recent_date
                        ).all()

                        total_h2_multiple = len(resultados_tmp_3)

                        print(f"total_h2_multiple : {total_h2_multiple}")

                        resultados_tmp_2 = session.query(Resultado).filter(
                            Resultado.dominio == dominio,
                            Resultado.codigo_respuesta == 200,
                            Resultado.id_escaneo == most_recent_id_escaneo,
                            Resultado.h2_falta > 0
                            #Resultado.fecha_escaneo == most_recent_date
                        ).all()

                        total_h2_falta = len(resultados_tmp_2)

                        print(f"total_h2_falta: {total_h2_falta}")

                        # Seleccionar los registros de la tabla que cumplen las condiciones
                        resultados_tmp_1 = session.query(Resultado).filter(
                            Resultado.dominio == dominio,
                            Resultado.codigo_respuesta == 200,
                            Resultado.id_escaneo == most_recent_id_escaneo,
                            Resultado.h2_no_secuencial > 0
                            #Resultado.fecha_escaneo == most_recent_date
                        ).all()

                        total_h2_no_secuencial = len(resultados_tmp_1)

                        print(f"total_h2_no_secuencial: {total_h2_no_secuencial}")

                        # Seleccionar los registros de la tabla que cumplen las condiciones
                        resultados_404 = session.query(Resultado).filter(
                            Resultado.dominio == dominio,
                            Resultado.codigo_respuesta == 404,
                            Resultado.id_escaneo == most_recent_id_escaneo
                            #Resultado.fecha_escaneo == most_recent_date
                        ).all()

                        # Obtener el número total de registros resultantes de esa consulta
                        total_404 = len(resultados_404)

                        # Imprimir el número total y los IDs de escaneo
                        print(
                            f"Total de registros 404 para el dominio {dominio}: {total_404}"
                        )

                        # Seleccionar los registros de la tabla que cumplen las condiciones
                        resultados_pdf = session.query(Resultado).filter(
                            Resultado.dominio == dominio, Resultado.is_pdf == 1,
                            Resultado.id_escaneo == most_recent_id_escaneo
                            #Resultado.fecha_escaneo == most_recent_date
                        ).all()

                        pdf_count = len(resultados_pdf)

                        print(f"Total pdf: {pdf_count }")

                        # Seleccionar los registros de la tabla que cumplen las condiciones
                        resultados_html = session.query(Resultado).filter(
                            Resultado.dominio == dominio, Resultado.is_pdf == 2,
                            Resultado.id_escaneo == most_recent_id_escaneo
                            #Resultado.fecha_escaneo == most_recent_date
                        ).all()

                        html_count = len(resultados_html)
                        print(f"Total html_coun: {html_count}")

                        # Seleccionar los registros de la tabla que cumplen las condiciones
                        resultados_others = session.query(Resultado).filter(
                            Resultado.dominio == dominio, Resultado.is_pdf == 0,
                            Resultado.id_escaneo == most_recent_id_escaneo
                            #Resultado.fecha_escaneo == most_recent_date
                        ).all()

                        others_count = len(resultados_others)
                        print(f"Total others_count: {others_count}")

                        # Obtener el id_escaneo más reciente para el dominio
                        most_recent_id_escaneo = resumen['id_escaneo']

                        # Si no hay registros en el sumario para el dominio, continuar con el siguiente
                        if most_recent_id_escaneo is not None:
                            # Seleccionar los registros de la tabla que cumplen las condiciones
                            resultados_errores_ortograficos = session.query(
                                Resultado).filter(
                                    Resultado.dominio == dominio,
                                    Resultado.codigo_respuesta == 200,
                                    ~func.locate('redirect=', Resultado.pagina),
                                    Resultado.num_errores_ortograficos > 0,
                                    Resultado.id_escaneo ==
                                    most_recent_id_escaneo).all()

                            print(
                                f"Páginas con errores ortográficos para el dominio {dominio} en el último escaneo: {len(resultados_errores_ortograficos)}"
                            )

                            base_folder = "offline"
                            os.makedirs(base_folder, exist_ok=True)

                            for resultado in resultados_errores_ortograficos:
                                # Descargar la página
                                print(f"Descargando la página: {resultado.pagina}")
                                response = requests.get(resultado.pagina)

                                if response.status_code == 200:
                                    
                                    # Parsear el contenido HTML
                                    soup = BeautifulSoup(response.text, 'html.parser')

                                    # Buscar todas las etiquetas de texto (p, div, span, etc.)
                                    etiquetas_texto = soup.find_all(text=True)

                                    # Buscar palabras con errores ortográficos y resaltarlas con CSS
                                    for tag in etiquetas_texto:
                                        contenido_tag = str(tag)
                                        for error in resultado.errores_ortograficos:
                                            # Usamos expresiones regulares para encontrar todas las ocurrencias de la palabra con errores ortográficos
                                            contenido_tag = re.sub(r'\b' + re.escape(error) + r'\b', f'<span style="color:white!important;background-color:red!important">{error}</span>', contenido_tag, flags=re.IGNORECASE)
                                        tag.replace_with(BeautifulSoup(contenido_tag, 'html.parser'))  # Creamos un nuevo objeto BeautifulSoup con el contenido modificado


                                    # Generar el contenido HTML con las palabras resaltadas
                                    contenido_html = str(soup)


                                    # Guardar el contenido HTML en un archivo
                                    with open('pagina_con_errores.html', 'w', encoding='utf-8') as file:
                                        file.write(contenido_html)

                                    # Obtener el texto visible de la página
                                    texto_visible = soup.get_text()

                                    # Almacenar el número de frases en resultado.frases
                                    frases = re.split(r'[;.|,]', texto_visible)
                                    resultado.frases = len(frases)

                                    # Calcular la media de palabras por frase y almacenarla en resultado.media_palabras_frases
                                    palabras_por_frase = [
                                        len(frase.split()) for frase in frases
                                        if frase.strip()
                                    ]
                                    media_palabras_frase = sum(
                                        palabras_por_frase) / len(
                                            palabras_por_frase
                                        ) if palabras_por_frase else 0
                                    resultado.media_palabras_frase = media_palabras_frase

                                    # Calcular la prueba de legibilidad de Flesch-Kincaid y almacenarla en resultado.flesh
                                    try:
                                        total_palabras = len(
                                            re.findall(r'\b\w+\b', texto_visible))
                                        total_oraciones = resultado.frases
                                        #total_silabas = sum([textstat.syllable(word) for word in re.findall(r'\b\w+\b', texto_visible)])
                                        total_silabas = sum([
                                            textstat.lexicon_count(word, True)
                                            for word in re.findall(
                                                r'\b\w+\b', texto_visible)
                                        ])
                                        flesh_score = 206.835 - 1.015 * (
                                            total_palabras / total_oraciones
                                        ) - 84.6 * (total_silabas / total_palabras)
                                        resultado.flesh_score = round(
                                            flesh_score, 2)
                                    except ZeroDivisionError:
                                        resultado.flesh_score = 0.0

                                    modified_html = response.text
                                    #modified_html = BeautifulSoup(response.text,'html.parser')
                                    #modified_html = str(soup)


                                    modified_html = str(soup).encode(
                                        'utf-8').decode('utf-8', 'ignore')
                                    modified_html = ' '.join(
                                        modified_html.split()
                                    )  # Eliminar espacios adicionales
                                    modified_html = modified_html.replace(
                                        '\n', '').replace('\t','').replace('\r', '')

                                    for palabra in resultado.errores_ortograficos:
                                        # Encontrar la posición de la palabra en el HTML original
                                        #start_index = modified_html.find(palabra)

                                        #if start_index != -1:
                                        #    modified_html = (
                                        #        modified_html[:start_index] +
                                        #        f'<span style="background-color:red!important;color:white!important;border:2px solid #fff!important">{palabra}</span>'
                                        #        + modified_html[start_index +
                                        #                        len(palabra):])

                                        # Buscar la etiqueta <body> en el HTML
                                        start_body_index = modified_html.find('<body>')
        
                                        # Si no encuentra la etiqueta <body>, buscar en todo el documento
                                        if start_body_index == -1:
                                            start_index = modified_html.find(palabra)
                                        else:
                                            # Encontrar la posición de la palabra en el HTML original después de la etiqueta <body>
                                            start_index = modified_html.find(palabra, start_body_index)
        
                                            if start_index != -1:
                                                modified_html = (
                                                modified_html[:start_index] +
                                                f'<span style="background-color:red!important;color:white!important;border:2px solid #fff!important">***{palabra}***</span>'
                                                + modified_html[start_index +
                                                len(palabra):])

                                    # Campos a almacenar en la instancia de Resultado
                                    campos_html_copy = [
                                        'html_copy', 'html_copy_dos',
                                        'html_copy_tres', 'html_copy_cuatro',
                                        'html_copy_cinco', 'html_copy_seis',
                                        'html_copy_siete', 'html_copy_ocho',
                                        'html_copy_nueve', 'html_copy_diez'
                                    ]

                                    # Inicializar campos
                                    for campo in campos_html_copy:
                                        setattr(resultado, campo, '')

                                    # Generar la ruta del archivo
                                    domain_folder = os.path.join(
                                        base_folder, resultado.dominio)
                                    os.makedirs(domain_folder, exist_ok=True)
                                    filename = f"{resultado.id}.html"
                                    filepath = os.path.join(
                                        domain_folder, filename)

                                    # Escribir el HTML en el archivo
                                    with open(filepath, 'w',
                                            encoding='utf-8') as file:
                                        #file.write(modified_html)
                                        file.write(contenido_html)

                                    print(f"HTML guardado en: {filepath}")

                        else:
                            print(
                                f"No hay registros en el sumario para el dominio {dominio}."
                            )

                        # Obtener el objeto Sumario existente desde la base de datos
                        sumario_existente = session.query(Sumario).filter_by(
                            id_escaneo=resumen['id_escaneo']).first()

                        # Seleccionar los registros de la tabla que cumplen las condiciones
                        resultados_tiempo_respuesta = session.query(
                            Resultado
                        ).filter(
                            Resultado.dominio == dominio,
                            Resultado.codigo_respuesta == 200,
                            ~func.locate('redirect=', Resultado.pagina),
                            Resultado.tiempo_respuesta.isnot(
                                None
                            ),  # Filtrar resultados con tiempo_respuesta no nulo
                            Resultado.id_escaneo == most_recent_id_escaneo).all()

                        print(
                            f"Páginas con tiempo de respuesta para el dominio {dominio} en el último escaneo: {len(resultados_tiempo_respuesta)}"
                        )

                        # Calcular el tiempo medio de respuesta
                        tiempo_total = sum(
                            resultado.tiempo_respuesta
                            for resultado in resultados_tiempo_respuesta)
                        tiempo_medio = tiempo_total / len(
                            resultados_tiempo_respuesta) if len(
                                resultados_tiempo_respuesta) > 0 else 0

                        # Verificar si se encontró un Sumario existente
                        if sumario_existente:
                            # Actualizar los campos necesarios
                            sumario_existente.total_404 = total_404
                            sumario_existente.tiempo_medio = tiempo_medio  # Nueva columna "tiempo_medio"
                            sumario_existente.pdf_count = pdf_count
                            sumario_existente.html_count = html_count
                            sumario_existente.others_count = others_count
                            sumario_existente.pages_err_orto = len(
                                resultados_errores_ortograficos)

                            sumario_existente.media_frases = media_frases
                            sumario_existente.total_media_palabras_frase = total_media_palabras_frase
                            sumario_existente.media_flesh_score = media_flesh_score
                            sumario_existente.total_meta_description_mas_155_caracteres = total_meta_description_mas_155_caracteres
                            sumario_existente.total_meta_description_duplicado = total_meta_description_duplicado
                            sumario_existente.total_canonicals_falta = total_canonicals_falta
                            sumario_existente.total_directivas_noindex = total_directivas_noindex
                            sumario_existente.total_falta_encabezado_x_content_type_options = total_falta_encabezado_x_content_type_options
                            sumario_existente.total_falta_encabezado_secure_referrer_policy = total_falta_encabezado_secure_referrer_policy
                            sumario_existente.total_falta_encabezado_content_security_policy = total_falta_encabezado_content_security_policy
                            sumario_existente.total_falta_encabezado_x_frame_options = total_falta_encabezado_x_frame_options
                            sumario_existente.total_titulos_pagina_menos_30_caracteres = total_titulos_pagina_menos_30_caracteres
                            sumario_existente.total_meta_description_menos_70_caracteres = total_meta_description_menos_70_caracteres
                            sumario_existente.total_titulos_pagina_mas_60_caracteres = total_titulos_pagina_mas_60_caracteres
                            sumario_existente.total_titulos_pagina_igual_h1 = total_titulos_pagina_igual_h1
                            sumario_existente.total_titulos_pagina_duplicado = total_titulos_pagina_duplicado
                            sumario_existente.total_meta_description_falta = total_meta_description_falta
                            sumario_existente.total_h2_duplicado = total_h2_duplicado
                            sumario_existente.total_h2_mas_70_caracteres = total_h2_mas_70_caracteres
                            sumario_existente.total_h2_multiple = total_h2_multiple
                            sumario_existente.total_h2_falta = total_h2_falta
                            sumario_existente.total_h2_no_secuencial = total_h2_no_secuencial
                            sumario_existente.pages_title_long = pages_title_long
                            sumario_existente.pages_desc_short = pages_title_short
                            sumario_existente.pages_title_dup = pages_title_dup 
                            sumario_existente.pages_desc_long = pages_desc_long
                            sumario_existente.pages_desc_short = pages_desc_short 
                        else:
                            # Manejar el caso en que no se encontró el Sumario existente (puede imprimir un mensaje o lanzar una excepción según tus necesidades)
                            print(
                                f"¡No se encontró un Sumario existente para el id_escaneo {resumen['id_escaneo']}!"
                            )

                        # Confirmar los cambios en la base de datos
                        session.commit()
        finally:
                eliminar_lock(session)
                end_script_time = time.time()
                script_duration = end_script_time - start_script_time

                logging.info(
                    f'\nDuraciÃ³n total del script: {script_duration} segundos ({script_duration // 3600} horas y {(script_duration % 3600) // 60} minutos)'
                )

                print(
                    f'\nDuraciÃ³n total del script: {script_duration} segundos ({script_duration // 3600} horas y {(script_duration % 3600) // 60} minutos)'
                )

                generar_informe_resumen(resumen_escaneo, 'resumen_escaneo.csv')
    else:
        print("El script no se ejecutará debido a la existencia del archivo .lock.")
