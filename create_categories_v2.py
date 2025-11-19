from products.models import Category

# Eliminar categorías existentes si es necesario
categorias_existentes = Category.objects.all()
print(f"Se encontraron {categorias_existentes.count()} categorías existentes")
for cat in categorias_existentes:
    print(f"- Eliminando: {cat.name}")
    cat.delete()

# Crear la categoría principal "Productos"
productos_categoria = Category.objects.create(name="Productos", slug="productos")

# Crear las subcategorías bajo "Productos"
libros_categoria = Category.objects.create(name="Libros", slug="libros", parent=productos_categoria)
serie_categoria = Category.objects.create(name="Serie", slug="serie", parent=productos_categoria)
otros_productos_categoria = Category.objects.create(name="Otros Productos", slug="otros-productos", parent=productos_categoria)

print("Categorías creadas exitosamente:")
print(f"- {productos_categoria.name}")
print(f"  - {libros_categoria.name}")
print(f"  - {serie_categoria.name}")
print(f"  - {otros_productos_categoria.name}")

# Mostrar todas las categorías creadas
print("\nTodas las categorías en la base de datos:")
for cat in Category.objects.all():
    parent_name = f" (hijo de {cat.parent.name})" if cat.parent else " (categoría principal)"
    print(f"- {cat.name}{parent_name}")