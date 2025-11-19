from django.contrib import admin
from .models import Evento, Inscripcion, Cuori

# Configuraciones personalizadas para el Admin

class InscripcionInline(admin.TabularInline):
    model = Inscripcion
    extra = 1 # Cuántos campos de inscripción mostrar por defecto
    fields = ['cuori', 'fecha_inscripcion'] # Mostrar solo los campos relevantes
    readonly_fields = ('fecha_inscripcion',)
    # Permitir buscar y agregar Cuoris directamente desde el evento
    autocomplete_fields = ['cuori']

class EventoAdmin(admin.ModelAdmin):
    class Media:
        js = ('admin/js/evento_ofrenda.js',)

    list_display = ('titulo', 'fecha', 'hora_fin', 'lugar', 'direccion', 'ciudad', 'departamento', 'coordenadas_mapa', 'cupos', 'tipo_asistencia', 'dirigido_a', 'requiere_ofrenda', 'valor_ofrenda', 'requiere_inscripcion')
    list_filter = ('fecha', 'lugar', 'ciudad', 'departamento', 'tipo_asistencia', 'dirigido_a', 'requiere_ofrenda', 'requiere_inscripcion')
    search_fields = ('titulo', 'descripcion', 'ciudad', 'departamento', 'direccion', 'coordenadas_mapa')
    inlines = [InscripcionInline]
    fieldsets = (
        (None, {
            'fields': ('titulo', 'descripcion', 'fecha', 'hora_fin', 'lugar', 'direccion', 'ciudad', 'departamento', 'coordenadas_mapa', 'imagen', 'slug')
        }),
        ('Configuración de Asistencia y Público', {
            'fields': ('tipo_asistencia', 'cupos', 'dirigido_a')
        }),
        ('Configuración de Ofrenda', {
            'fields': ('requiere_inscripcion', 'requiere_ofrenda', 'valor_ofrenda'),
        }),
    )

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        # Convertir a lista para poder modificar
        fieldsets = list(fieldsets)

        # Lógica para ocultar/mostrar cupos
        if obj and obj.tipo_asistencia == 'ABIERTO':
            for i, (name, field_options) in enumerate(fieldsets):
                if name == 'Configuración de Asistencia y Público':
                    fields_list = list(field_options['fields'])
                    if 'cupos' in fields_list:
                        fields_list.remove('cupos')
                    field_options['fields'] = tuple(fields_list)
                    fieldsets[i] = (name, field_options)
                    break

        return tuple(fieldsets)

class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('id', 'evento', 'get_evento_fecha', 'get_cuori_nombre_completo', 'get_cuori_numero_contacto_1', 'get_cuori_numero_contacto_2', 'fecha_inscripcion')
    list_filter = ('evento__fecha', 'evento')
    search_fields = ('cuori__nombre_completo', 'cuori__cedula', 'evento__titulo')
    readonly_fields = ('fecha_inscripcion',)
    autocomplete_fields = ['cuori', 'evento']

    def get_evento_fecha(self, obj):
        return obj.evento.fecha
    get_evento_fecha.admin_order_field = 'evento__fecha'  # Permite ordenar por fecha del evento
    get_evento_fecha.short_description = 'Fecha del Evento'  # Nombre de la columna

    def get_cuori_nombre_completo(self, obj):
        return obj.cuori.nombre_completo if obj.cuori else 'N/A'
    get_cuori_nombre_completo.admin_order_field = 'cuori__nombre_completo'
    get_cuori_nombre_completo.short_description = 'Nombre Cuori'

    def get_cuori_numero_contacto_1(self, obj):
        return obj.cuori.numero_contacto if obj.cuori else 'N/A'
    get_cuori_numero_contacto_1.admin_order_field = 'cuori__numero_contacto'
    get_cuori_numero_contacto_1.short_description = 'Contacto 1'

    def get_cuori_numero_contacto_2(self, obj):
        return obj.cuori.numero_contacto_2 if obj.cuori else 'N/A'
    get_cuori_numero_contacto_2.admin_order_field = 'cuori__numero_contacto_2'
    get_cuori_numero_contacto_2.short_description = 'Contacto 2'

class InscripcionInlineForCuori(admin.TabularInline):
    model = Inscripcion
    extra = 0 # No mostrar campos vacíos por defecto
    fields = ['evento', 'fecha_inscripcion']
    readonly_fields = ['evento', 'fecha_inscripcion'] # Hacerlos de solo lectura
    can_delete = False # No permitir eliminar inscripciones desde aquí

class CuoriAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'cedula', 'email_contacto', 'numero_contacto', 'numero_contacto_2', 'ciudad', 'departamento')
    search_fields = ('nombre_completo', 'cedula', 'email_contacto', 'numero_contacto', 'numero_contacto_2')
    inlines = [InscripcionInlineForCuori]

# Registro de los modelos
admin.site.register(Evento, EventoAdmin)
admin.site.register(Inscripcion, InscripcionAdmin)
admin.site.register(Cuori, CuoriAdmin)
