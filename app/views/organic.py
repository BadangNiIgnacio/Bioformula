from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User, Group
from datetime import date, datetime, timedelta, timezone
from django.db import transaction
from django.contrib.sessions.models import Session
from django.core.paginator import Paginator
from ..forms import *
from ..models import *
from django.db.models import Q, Avg, Count
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max
from django.views.decorators.http import require_GET
from django.db.models import Count

def index(request):
    page = 'Organic'
    return render(request, 'app/organic.html', {'page': page})

def fertilizer(request):
    page = 'Organic'
    if request.method == "POST":
        try:
            search = request.POST.get("search")
            result = FertilizersIngredients.objects.filter(
                Q(fertilizer__name__icontains=search) | Q(fertilizer__description__icontains=search) | Q(description__icontains=search)
            ).values('fertilizer_id', 'fertilizer__name', 'fertilizer__description').annotate(count=Count('fertilizer_id')).distinct()
            #feedback
            #fertilizer = FertilizerFeedback.objects.filter(fertilizer__status=True).annotate(max_rating=Max('rating')).order_by('-max_rating')
            """ fertilizer = FertilizerFeedback.objects.filter(
                Q(fertilizer__name__icontains=search) | Q(fertilizer__description__icontains=search)
            ).values('fertilizer_id').annotate(avg_rating=Avg('rating')).order_by('-rating') """
            ratings = []
            if result:
                for i in result:
                    fertilizer = FertilizerFeedback.objects.filter(fertilizer_id=i['fertilizer_id'])
                    rating = 0
                    count = 0
                    for j in fertilizer:
                        rating += j.rating
                        count += 1
                        rating = rating / count
                    ave = {
                        'fertilizer_id'     : i['fertilizer_id'],
                        'fertilizer_name'   : i['fertilizer__name'],
                        'rating'            : rating
                    }
                    ratings.append(ave)
            paginator = Paginator(result, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            form = FertilizerSearchForm()
            return render(request, 'app/fertilizer.html', {'page': page, 'form': form, 'list_': page_obj, 'fertilizer': ratings})
        except Exception as e:
            messages.error(request, str(e))
    form = FertilizerSearchForm()
    return render(request, 'app/fertilizer.html', {'page': page, 'form': form})

def fertilizer_details(request, id):
    page = 'Organic'
    instance = get_object_or_404(Fertilizers, pk=id)
    details = Fertilizers.objects.filter(fertilizer_id=id)
    ing = FertilizersIngredients.objects.filter(fertilizer_id=id)
    proc = FertilizersProcedure.objects.filter(fertilizer_id=id)
    feedback = FertilizerFeedback.objects.filter(fertilizer_id=id)
    source = FertilizerSource.objects.filter(fertilizer_id=id)
    benefits = FertilizerBenefits.objects.filter(fertilizer_id=id)
    notes = FertilizerNotes.objects.filter(fertilizer_id=id)

    for i in feedback:
        profile = Profile.objects.filter(user_id=i.user_id)
        for x in profile:
            if x.image:
                i.image = x.image
            else:
                i.image = settings.MEDIA_URL + "dp/default.jpeg"
    form = FertilizerConversionForm(instance=instance)
    return render(request, 'app/fertilizer-details.html', {'page': page, 'details': details, 'ing': ing, 'proc': proc, 'feedback': feedback, 'id': id, 'form': form, 'source': source, 'benefits': benefits, 'notes': notes})

def post_fertilizer_feedback(request, id):
    try:
        if request.method == "POST":
            feedbacks = request.POST.get('feedback')
            rating = request.POST.get('rating')
            with transaction.atomic():
                add_feedback = FertilizerFeedback(user_id=request.session['userid'], fertilizer_id=id, rating=rating, feedback=feedbacks, datetime_posted=timezone.now())
                add_feedback.save()
                if add_feedback.feedback_id:
                    messages.success(request, 'Your feedback is posted successfully')
            return HttpResponseRedirect("/fertilizer-details/" + str(id) + "#comment")
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect("/fertilizer-details/" + str(id) + "#comment")
    

def pesticide(request):
    page = 'Organic'
    if request.method == "POST":
        try:
            form = PesticideSearchForm(request.POST)
            search = request.POST.get("search")
            result = PesticideIngredients.objects.filter(
                Q(pesticide__name__icontains=search) | Q(pesticide__description__icontains=search) | Q(description__icontains=search)
            ).values('pesticide_id', 'pesticide__name', 'pesticide__description').annotate(count=Count('pesticide_id')).distinct()

            #feedback
            # pesticide = PesticideFeedback.objects.filter(pesticide__status=True).annotate(max_rating=Max('rating')).order_by('-max_rating')
            ratings = []
            if result:
                for i in result:
                    pesticide = PesticideFeedback.objects.filter(pesticide_id=i['pesticide_id'])
                    rating = 0
                    count = 0
                    for j in pesticide:
                        rating += j.rating
                        count += 1
                        rating = rating / count
                    ave = {
                        'pesticide_id'     : i['pesticide_id'],
                        'pesticide_name'   : i['pesticide__name'],
                        'rating'           : rating
                    }
                    ratings.append(ave)
            paginator = Paginator(result, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            form = PesticideSearchForm()
            return render(request, 'app/pesticide.html', {'page': page, 'form': form, 'list_': page_obj, 'pesticide': ratings})
        except Exception as e:
            messages.error(request, str(e))
    form = PesticideSearchForm()
    return render(request, 'app/pesticide.html', {'page': page, 'form': form})

def pesticide_details(request, id):
    page = 'Organic'
    instance = get_object_or_404(Pesticides, pk=id)
    details = Pesticides.objects.filter(pesticide_id=id)
    ing = PesticideIngredients.objects.filter(pesticide_id=id)
    proc = PesticideProcedure.objects.filter(pesticide_id=id)
    feedback = PesticideFeedback.objects.filter(pesticide_id=id)
    source = PesticideSource.objects.filter(pesticide_id=id)
    pest = PesticideTargetPest.objects.filter(pesticide_id=id)
    usage = PesticideUsage.objects.filter(pesticide_id=id)
    benefit = PesticideBenefit.objects.filter(pesticide_id=id)
    notes = PesticideNotes.objects.filter(pesticide_id=id)
    for i in feedback:
        profile = Profile.objects.filter(user_id=i.user_id)
        for x in profile:
            if x.image:
                i.image = x.image
            else:
                i.image = settings.MEDIA_URL + "dp/default.jpeg"
    form = PesticideConversionForm(instance=instance)
    return render(request, 'app/pesticide-details.html', {'page': page, 'details': details, 'ing': ing, 'proc': proc, 'feedback': feedback, 'id': id, 'form': form, 'source': source, 'pest': pest, 'usage': usage, 'benefits': benefit, 'notes': notes})


def post_pesticide_feedback(request, id):
    try:
        if request.method == "POST":
            feedbacks = request.POST.get('feedback')
            rating = request.POST.get('rating')
            with transaction.atomic():
                add_feedback = PesticideFeedback(user_id=request.session['userid'], pesticide_id=id, rating=rating, feedback=feedbacks, datetime_posted=timezone.now())
                add_feedback.save()
                if add_feedback.feedback_id:
                    messages.success(request, 'Your feedback is posted successfully')
            return HttpResponseRedirect("/pesticide-details/" + str(id) + "#comment")
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect("/pesticide-details/" + str(id) + "#comment")

@csrf_exempt
def pesticide_conversion(request):
    if request.method == 'POST':
        try:
            uom_qty = request.POST.get('uom_qty') or 0
            uom = request.POST.get('uom')
            land_qty = request.POST.get('land_qty') or 0
            land = request.POST.get('land')
            define = request.POST.get('define')
            id = request.POST.get("id")
            db_uom_qty = 0
            db_land_qty = 0
            data = PesticideConversion.objects.filter(pesticide_id=id, uom_id=uom, land_id=land)
            if data:
                for i in data:
                    db_uom_qty = i.uom_qty
                    db_land_qty = i.land_qty
                if define == 'UOM':
                    result = (float(uom_qty) * float(db_land_qty))/float(db_uom_qty)
                if define == "LAND":
                    result = (float(db_uom_qty) * float(land_qty))/float(db_land_qty)
                response = {
                    'status': 'success',
                    'result':  result,
                }
            else:
                response = {
                    'status': 'success',
                    'result':  0,
                }
        except:
            response = {
                'status': 'error',
            }
        return JsonResponse(response)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def fertilizer_conversion(request):
    if request.method == 'POST':
        try:
            uom_qty = request.POST.get('uom_qty') or 0
            uom = request.POST.get('uom')
            land_qty = request.POST.get('land_qty') or 0
            land = request.POST.get('land')
            define = request.POST.get('define')
            id = request.POST.get("id")
            db_uom_qty = 0
            db_land_qty = 0
            data = FertilizerConversion.objects.filter(fertilizer_id=id, uom_id=uom, land_id=land)
            if data:
                for i in data:
                    db_uom_qty = i.uom_qty
                    db_land_qty = i.land_qty
                if define == 'UOM':
                    result = (float(uom_qty) * float(db_land_qty))/float(db_uom_qty)
                if define == "LAND":
                    result = (float(db_uom_qty) * float(land_qty))/float(db_land_qty)
                response = {
                    'status': 'success',
                    'result':  result,
                }
            else:
                response = {
                    'status': 'success',
                    'result':  0,
                }
        except Exception as e:
            response = {
                'status': 'error',
            }
        return JsonResponse(response)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@require_GET
def search_suggestions(request):
    query = request.GET.get('q', '')  # Get the search term from the query parameter
    if query:
        suggestions = FertilizersIngredients.objects.filter(
                    Q(fertilizer__name__icontains=query) | Q(fertilizer__description__icontains=query) | Q(description__icontains=query)
                ).distinct()
        suggestions_list = list(suggestions.values('description')[:10])  # Convert QuerySet to list
        fertilizers = Fertilizers.objects.filter(Q(name__icontains=query)).distinct()
        fertilizers_list = list(fertilizers.values('name')[:10])
    else:
        suggestions_list = []
        fertilizers_list = []
    
    results = {
        'suggestion': suggestions_list,
        'fertilizers': fertilizers_list,
    }
    return JsonResponse(results, safe=False)

@require_GET
def search_suggestions_pest(request):
    query = request.GET.get('q', '')  # Get the search term from the query parameter
    if query:
        suggestions = PesticideIngredients.objects.filter(
                    Q(pesticide__name__icontains=query) | Q(pesticide__description__icontains=query) | Q(description__icontains=query)
                ).distinct()
        suggestions_list = list(suggestions.values('description')[:10])  # Convert QuerySet to list
        pesticides = Pesticides.objects.filter(Q(name__icontains=query)).distinct()
        pesticide_list = list(pesticides.values('name')[:10])
    else:
        suggestions_list = []
        pesticide_list = []
    
    results = {
        'suggestion': suggestions_list,
        'pesticides': pesticide_list,
    }
    return JsonResponse(results, safe=False)