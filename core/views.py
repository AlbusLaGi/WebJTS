from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import IntegrityError
from django.http import JsonResponse
from .models import Evento, Inscripcion, Cuori
from .forms import InscripcionPublicaForm, CuoriForm
from django.utils import timezone
import random

# Create your views here.
def home(request):
    """
    Esta es la vista para la página de inicio.
    Incluye una sección de contenido recomendado basado en los eventos del mes.
    """
    now = timezone.now()

    # 1. Encontrar el tema del mes basado en el próximo evento
    upcoming_event = Evento.objects.filter(fecha__year=now.year, fecha__month=now.month, fecha__gte=now).order_by('fecha').first()

    # 2. Obtener contenido recomendado para la sección de blog
    try:
        from blog.models import BlogPost
        recommended_items = BlogPost.objects.filter(
            esta_publicado=True
        ).order_by('-fecha_publicacion')[:6]  # últimos 6 posts
    except:
        # Si la app blog no está completamente configurada aún
        recommended_items = []

    context = {
        'upcoming_event': upcoming_event,
        'recommended_items': recommended_items
    }
    return render(request, 'core/home.html', context)

def about(request):
    """
    Esta es la vista para la página "Quiénes Somos".
    """
    return render(request, 'core/about.html')

def eventos_list(request):
    eventos = Evento.objects.all().order_by('fecha')
    return render(request, 'core/eventos.html', {'eventos': eventos})

def evento_detalle(request, evento_slug):
    evento = get_object_or_404(Evento, slug=evento_slug)
    # Ya no se verifica si el usuario está inscrito usando request.user
    # La lógica de inscripción es ahora completamente pública
    esta_inscrito = False # Opcional: si quieres mantener la variable pero siempre en False
    context = {
        'evento': evento,
        'esta_inscrito': esta_inscrito,
    }
    return render(request, 'core/evento_detalle.html', context)

def events(request):
    """
    Esta es la vista para la página "Eventos".
    """
    return render(request, 'core/eventos.html')

def get_inscripcion_data_by_cedula(request):
    cedula = request.GET.get('cedula', None)
    evento_slug = request.GET.get('evento_slug', None)
    data = {'is_inscribed': False}
    if cedula:
        cuori = Cuori.objects.filter(cedula=cedula).first()
        if cuori:
            data = {
                'nombre_completo': cuori.nombre_completo,
                'numero_contacto': cuori.numero_contacto,
                'numero_contacto_2': cuori.numero_contacto_2,
                'email_contacto': cuori.email_contacto,
                'pais': cuori.pais,
                'departamento': cuori.departamento,
                'ciudad': cuori.ciudad,
            }
            if evento_slug:
                evento = Evento.objects.filter(slug=evento_slug).first()
                if evento and Inscripcion.objects.filter(evento=evento, cuori=cuori).exists():
                    data['is_inscribed'] = True
    return JsonResponse(data)

def inscribir_evento(request, evento_slug):
    evento = get_object_or_404(Evento, slug=evento_slug)

    if request.method == 'POST':
        cuori_form = CuoriForm(request.POST)
        inscripcion_form = InscripcionPublicaForm(request.POST, request.FILES)

        if cuori_form.is_valid() and inscripcion_form.is_valid():
            cedula = cuori_form.cleaned_data['cedula']

            # Obtener o crear el Cuori
            cuori, created = Cuori.objects.get_or_create(
                cedula=cedula,
                defaults={
                    'nombre_completo': cuori_form.cleaned_data['nombre_completo'],
                    'numero_contacto': cuori_form.cleaned_data['numero_contacto'],
                    'numero_contacto_2': cuori_form.cleaned_data['numero_contacto_2'],
                    'email_contacto': cuori_form.cleaned_data['email_contacto'],
                    'pais': cuori_form.cleaned_data['pais'],
                    'departamento': cuori_form.cleaned_data['departamento'],
                    'ciudad': cuori_form.cleaned_data['ciudad'],
                }
            )

            # Si el Cuori ya existía, actualizar sus datos con la información del formulario
            if not created:
                cuori.nombre_completo = cuori_form.cleaned_data['nombre_completo']
                cuori.numero_contacto = cuori_form.cleaned_data['numero_contacto']
                cuori.numero_contacto_2 = cuori_form.cleaned_data['numero_contacto_2']
                cuori.email_contacto = cuori_form.cleaned_data['email_contacto']
                cuori.pais = cuori_form.cleaned_data['pais']
                cuori.departamento = cuori_form.cleaned_data['departamento']
                cuori.ciudad = cuori_form.cleaned_data['ciudad']
                cuori.save()
                # No usar messages.info aquí, se manejará en el frontend

            # Verificar si ya existe una inscripción para este evento con este Cuori
            if Inscripcion.objects.filter(evento=evento, cuori=cuori).exists():
                # Si es una solicitud AJAX, devolver JSON
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'message': f'Ya estás inscrito(a) en {evento.titulo}. Tus datos de contacto han sido actualizados.'})
                # Si no es AJAX, usar messages y redireccionar
                messages.warning(request, f'Ya estás inscrito(a) en {evento.titulo}. Tus datos de contacto han sido actualizados.')
                return redirect('inscripcion_confirmacion', evento_slug=evento.slug)

            if evento.cupos_disponibles <= 0 and evento.tipo_asistencia == 'LIMITADO':
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'message': 'Lo sentimos, ya no hay cupos disponibles para este evento.'})
                messages.error(request, 'Lo sentimos, ya no hay cupos disponibles para este evento.')
                return redirect('evento_detalle', evento_slug=evento.slug)

            try:
                inscripcion = inscripcion_form.save(commit=False)
                inscripcion.evento = evento
                inscripcion.cuori = cuori # Asignar el Cuori a la inscripción
                inscripcion.save()

                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': True, 'message': f'¡Te has pre-inscrito exitosamente en {evento.titulo}! Por favor, espera la confirmación.'})
                messages.success(request, f'¡Te has pre-inscrito exitosamente en {evento.titulo}! Por favor, espera la confirmación.')
                return redirect('inscripcion_confirmacion', evento_slug=evento.slug)
            except IntegrityError:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'message': 'Hubo un error al procesar tu inscripción. Por favor, inténtalo de nuevo.'})
                messages.error(request, 'Hubo un error al procesar tu inscripción. Por favor, inténtalo de nuevo.')
                # Esto podría ocurrir si hay una condición de carrera y se intenta crear una inscripción duplicada
                # aunque ya se haya verificado antes. Es una capa extra de seguridad.
        else:
            # Si la validación del formulario falla, devolver errores en JSON para AJAX
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                errors = {}
                if cuori_form.errors:
                    errors.update(cuori_form.errors.get_json_data())
                if inscripcion_form.errors:
                    errors.update(inscripcion_form.errors.get_json_data())
                return JsonResponse({'success': False, 'message': 'Por favor, corrige los errores en el formulario.', 'errors': errors}, status=400)
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else: # GET request
        initial_cuori_data = {}
        cedula_param = request.GET.get('cedula')
        if cedula_param:
            # Buscar un Cuori existente para pre-llenar el formulario de Cuori
            cuori_existente = Cuori.objects.filter(cedula=cedula_param).first()
            if cuori_existente:
                initial_cuori_data = {
                    'nombre_completo': cuori_existente.nombre_completo,
                    'cedula': cuori_existente.cedula,
                    'numero_contacto': cuori_existente.numero_contacto,
                    'numero_contacto_2': cuori_existente.numero_contacto_2,
                    'email_contacto': cuori_existente.email_contacto,
                    'pais': cuori_existente.pais,
                    'departamento': cuori_existente.departamento,
                    'ciudad': cuori_existente.ciudad,
                }
        cuori_form = CuoriForm(initial=initial_cuori_data)
        inscripcion_form = InscripcionPublicaForm()

    context = {
        'evento': evento,
        'cuori_form': cuori_form,
        'inscripcion_form': inscripcion_form,
    }
    return render(request, 'core/inscripcion_publica_form.html', context)

