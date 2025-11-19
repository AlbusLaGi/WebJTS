"""
Funcionalidad de importación de productos desde Google Sheets (sin API directa)
"""
import pandas as pd
import io
import csv
import requests
from urllib.parse import urlparse, parse_qs
from io import StringIO
from .models import Product

def extract_sheet_id_from_url(sheet_url):
    """
    Extrae el ID del documento de Google Sheets de la URL
    """
    try:
        # Soportar diferentes formatos de URL de Google Sheets
        parsed = urlparse(sheet_url)
        if 'docs.google.com' in parsed.netloc:
            # Formato: https://docs.google.com/spreadsheets/d/ID_DEL_SHEET/edit
            path_parts = parsed.path.split('/')
            if 'd' in path_parts:
                sheet_id_index = path_parts.index('d') + 1
                if sheet_id_index < len(path_parts):
                    return path_parts[sheet_id_index]
        
        # Si no se encuentra en el path, intentar con query parameters
        query_params = parse_qs(parsed.query)
        if 'key' in query_params:
            return query_params['key'][0]
            
        raise ValueError("No se pudo extraer el ID del Google Sheet")
    except:
        raise ValueError("URL de Google Sheets inválida")

def import_products_with_gspread(sheet_url, delete_existing=False):
    """
    Importa productos desde un Google Sheet exportando como CSV.
    Esta función permite al usuario copiar y pegar el contenido o descargar como CSV.
    """
    errors = []
    imported_count = 0
    
    try:
        if delete_existing:
            Product.objects.all().delete()

        # Extraer ID del sheet y construir URL para exportar como CSV
        try:
            sheet_id = extract_sheet_id_from_url(sheet_url)

            # Construir URL para exportar como CSV
            csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

            # Intentar descargar y leer el CSV
            try:
                # Intentar leer directamente desde la URL
                response = requests.get(csv_url)
                
                if response.status_code == 200:
                    # Decodificar el contenido CSV
                    csv_content = response.content.decode('utf-8')
                    csv_data = csv_content
                    
                    # Usar pandas para leer el CSV
                    df = pd.read_csv(StringIO(csv_data))
                    
                    # Procesar cada fila del CSV
                    for idx, row in df.iterrows():
                        # Asegurarse de que los datos requeridos existan
                        name = str(row.get('name', '')).strip()
                        if not name:
                            name = str(row.get('Name', '')).strip()  # También intentar variaciones
                            if not name:
                                name = str(row.get('producto', '')).strip()
                                if not name:
                                    name = str(row.get('Producto', '')).strip()
                        
                        if not name:
                            errors.append(f"Fila {idx+1}: No se encontró un nombre de producto válido")
                            continue
                        
                        # Extraer otros campos con posibles variaciones
                        description = str(row.get('description', ''))
                        if not description or description == 'nan':
                            description = str(row.get('Description', ''))
                            if not description or description == 'nan':
                                description = str(row.get('descripción', ''))
                                if not description or description == 'nan':
                                    description = str(row.get('Descripción', ''))
                        
                        try:
                            price_value = row.get('price', row.get('Price', row.get('precio', row.get('Precio', 0))))
                            if pd.isna(price_value) or str(price_value).lower() == 'nan' or str(price_value).strip() == '':
                                price = 0.0
                            else:
                                price = float(price_value)
                        except (ValueError, TypeError):
                            price = 0.0
                        
                        # Obtener y procesar el valor de categoría
                        raw_category = row.get('categories', row.get('category', row.get('Category', row.get('categoría', row.get('Categoría', 'otro_producto')))))
                        
                        if pd.isna(raw_category) or str(raw_category).lower() == 'nan' or str(raw_category).strip() == '':
                            category = 'otro_producto'
                        else:
                            category = str(raw_category).strip().lower()
                            
                            # Validar que la categoría sea una de las válidas
                            valid_categories = ['paquete', 'serie', 'libro', 'otro_producto']
                            
                            # Manejar variantes comunes de nombres de categorías
                            if category in ['producto', 'productos', 'product', 'prod']:
                                # Determinar si debería ser 'otro_producto' basado en el campo book_type
                                book_type_raw = str(row.get('book_type', row.get('bookType', row.get('booktype', '')))).lower()
                                
                                # Si el tipo de libro indica serie o bolsillo, usar categoría serie
                                if book_type_raw in ['serie_bolsillo', 'serie bolsillo', 'bolsillo', 'pocket', 'series']:
                                    category = 'serie'
                                else:
                                    category = 'otro_producto'  # Valor por defecto para 'producto'
                            elif category in ['libro', 'libros', 'book', 'books']:
                                category = 'libro'
                            elif category in ['serie', 'series', 'bolsillo', 'pocket', 'collection', 'bolsillos']:
                                category = 'serie'
                            elif category in ['paquete', 'packages', 'package', 'pack']:
                                category = 'paquete'
                            elif category in ['otro producto', 'otro_producto', 'otros productos', 'other product', 'other products']:
                                category = 'otro_producto'
                            else:
                                # Si aún no es válida después de la transformación, usar valor por defecto
                                book_type_raw = str(row.get('book_type', row.get('bookType', row.get('booktype', '')))).lower()
                                
                                # Si el tipo de libro indica serie o bolsillo, usar categoría serie
                                if book_type_raw in ['serie_bolsillo', 'serie bolsillo', 'bolsillo', 'pocket', 'series']:
                                    category = 'serie'
                                # Si la categoría original es 'libro', asignar como libro
                                elif category in ['libro']:
                                    category = 'libro'
                                else:
                                    category = 'otro_producto'  # Valor por defecto si no se puede determinar
                        
                        try:
                            is_available_value = str(row.get('is_available', row.get('available', row.get('disponible', 'True')))).lower()
                            is_available = is_available_value in ['true', '1', 'yes', 'sí', 'si', 't', 'y'] or is_available_value not in ['false', '0', 'no', 'n', 'f']
                        except:
                            is_available = True

                        measures = str(row.get('measures', row.get('Measures', row.get('medidas', row.get('Medidas', row.get('measurements', ''))))))
                        if pd.isna(measures) or str(measures).lower() == 'nan' or str(measures).strip() == '' or str(measures).lower() == 'none':
                            measures = ''

                        try:
                            pages_value = row.get('pages', row.get('Pages', row.get('páginas', row.get('Páginas', row.get('page_count', 0)))))
                            if pd.isna(pages_value) or str(pages_value).lower() == 'nan' or str(pages_value).strip() == '' or str(pages_value).lower() == 'none':
                                pages = None
                            else:
                                pages = int(pages_value)
                        except (ValueError, TypeError):
                            pages = None

                        # El campo ISBN ya no se utiliza, simplemente asignamos cadena vacía
                        isbn = ''
                        
                        # Extraer información de autores u otros campos adicionales
                        authors = str(row.get('authors', row.get('author', row.get('Authors', row.get('Autor', row.get('autores', ''))))))
                        if pd.isna(authors) or str(authors).lower() == 'nan' or str(authors).strip() == '' or str(authors).lower() == 'none':
                            authors = ''

                        # Crear o actualizar producto (sin product_type ni isbn)
                        product, created = Product.objects.get_or_create(
                            name=name,
                            defaults={
                                'description': description if (description != 'nan' and description.lower() != 'none') else '',
                                'price': price,
                                'category': category,
                                'is_available': is_available,
                                'measures': measures if (measures != 'nan' and measures.lower() != 'none') else '',
                                'pages': pages,
                                'authors': authors if (authors != 'nan' and authors.lower() != 'none') else '',
                            }
                        )

                        if not created:
                            # Si el producto ya existía, actualizar los campos
                            product.description = description if (description != 'nan' and description.lower() != 'none') else ''
                            product.price = price
                            product.category = category
                            product.is_available = is_available
                            product.measures = measures if (measures != 'nan' and measures.lower() != 'none') else ''
                            product.pages = pages
                            product.authors = authors if (authors != 'nan' and authors.lower() != 'none') else ''
                            product.save()

                        if created:
                            imported_count += 1
                else:
                    errors.append(f"No se pudo acceder al Google Sheet. Código de estado: {response.status_code}")
                    errors.append("Asegúrate de que el documento esté compartido con permisos de lectura.")
            except requests.RequestException as e:
                errors.append(f"Error al descargar el archivo: {str(e)}")
                errors.append("Verifica que la URL sea correcta y esté accesible.")
        except ValueError as e:
            errors.append(f"Error al procesar la URL: {str(e)}")
    
    except Exception as e:
        errors.append(f"Error general en la importación: {str(e)}")
    
    # Eliminar las líneas de diagnóstico para que no aparezcan en la interfaz
    filtered_errors = [error for error in errors if not str(error).startswith("DEBUG:")]
    return imported_count, filtered_errors