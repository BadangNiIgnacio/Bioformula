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
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from math import ceil

def index(request):
    page = 'Organic'
    return render(request, 'app/organic.html', {'page': page})

def fertilizer(request):
    page = 'Organic'
    form = FertilizerSearchForm()
    search_query = request.POST.get("search", "")

    try:
        result = FertilizersIngredients.objects.filter(
            Q(fertilizer__name__icontains=search_query) |
            Q(fertilizer__description__icontains=search_query) |
            Q(description__icontains=search_query)
        ).values('fertilizer_id', 'fertilizer__name', 'fertilizer__description').annotate(count=Count('fertilizer_id')).distinct()

        if not result.exists():
            messages.error(request, "No fertilizers found matching your search.")
            return render(request, 'app/fertilizer.html', {
                'page': page,
                'form': form,
                'list_': None,
                'fertilizer': None,
            })

        ratings = []
        for i in result:
            fertilizer_feedback = FertilizerFeedback.objects.filter(fertilizer_id=i['fertilizer_id'])
            fertilizer_obj = FertilizersIngredients.objects.filter(fertilizer_id=i['fertilizer_id']).first()
            rating = 0
            total_reviews = fertilizer_feedback.count()
            if total_reviews > 0:
                rating = sum(f.rating for f in fertilizer_feedback) / total_reviews
            ratings.append({
                'fertilizer_id': i['fertilizer_id'],
                'fertilizer_name': i['fertilizer__name'],
                'rating': round(rating, 1),
                'total_reviews': total_reviews,
                'image': fertilizer_obj.fertilizer.image.url if fertilizer_obj and fertilizer_obj.fertilizer.image else None
            })

        ratings.sort(key=lambda x: x['rating'], reverse=True)

        recommendations_per_page = 4
        ratings_per_page = 6
        paginator_result = Paginator(result, recommendations_per_page)
        paginator_ratings = Paginator(ratings, ratings_per_page)
        page_number = int(request.GET.get('page', 1))

        try:
            page_obj_result = paginator_result.page(page_number)
        except (PageNotAnInteger, EmptyPage):
            page_obj_result = paginator_result.page(1)

        try:
            page_obj_ratings = paginator_ratings.page(page_number)
        except (PageNotAnInteger, EmptyPage):
            page_obj_ratings = paginator_ratings.page(1)

        total_pages = max(
            ceil(len(result) / recommendations_per_page),
            ceil(len(ratings) / ratings_per_page)
        )

        return render(request, 'app/fertilizer.html', {
            'page': page,
            'form': form,
            'list_': page_obj_result,
            'fertilizer': page_obj_ratings,
            'total_pages': total_pages,
            'current_page': page_number,
        })

    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
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

    # Paginate feedbacks
    paginator = Paginator(feedback, 4)  # Show 5 feedbacks per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Add user profile image to each feedback
    for i in page_obj:
        profile = Profile.objects.filter(user_id=i.user_id)
        for x in profile:
            if x.image:
                i.image = x.image
            else:
                i.image = settings.MEDIA_URL + "dp/default.jpeg"

    form = FertilizerConversionForm(instance=instance)
    return render(request, 'app/fertilizer-details.html', {
        'page': page, 'details': details, 'ing': ing, 'proc': proc,
        'feedback': page_obj, 'id': id, 'form': form,
        'source': source, 'benefits': benefits, 'notes': notes
    })

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
    form = PesticideSearchForm()
    search_query = request.POST.get("search", "")
    
    try:
        # Fetch results based on the search query
        result = PesticideIngredients.objects.filter(
            Q(pesticide__name__icontains=search_query) |
            Q(pesticide__description__icontains=search_query) |
            Q(description__icontains=search_query)
        ).values('pesticide_id', 'pesticide__name', 'pesticide__description').annotate(count=Count('pesticide_id')).distinct()

        # Check if no results were found
        if not result.exists():
            messages.error(request, "No pesticides found matching your search.")
            return render(request, 'app/pesticide.html', {
                'page': page,
                'form': form,
                'list_': None,
                'pesticide': None,
            })

        # Generate pesticide ratings and total reviews
        ratings = []
        for i in result:
            pesticide_feedback = PesticideFeedback.objects.filter(pesticide_id=i['pesticide_id'])
            pesticide_obj = PesticideIngredients.objects.filter(pesticide_id=i['pesticide_id']).first()
            
            # Calculate the average rating and total reviews
            rating = 0
            total_reviews = pesticide_feedback.count()
            if total_reviews > 0:
                rating = sum(f.rating for f in pesticide_feedback) / total_reviews
            
            ratings.append({
                'pesticide_id': i['pesticide_id'],
                'pesticide_name': i['pesticide__name'],
                'rating': round(rating, 1),
                'total_reviews': total_reviews,
                'image': pesticide_obj.pesticide.image.url if pesticide_obj and pesticide_obj.pesticide.image else None
            })

        # Sort ratings by highest to lowest
        ratings.sort(key=lambda x: x['rating'], reverse=True)

        # Pagination settings
        recommendations_per_page = 4
        ratings_per_page = 6

        # Calculate pages for recommendations and ratings
        paginator_result = Paginator(result, recommendations_per_page)
        paginator_ratings = Paginator(ratings, ratings_per_page)

        # Get page numbers
        page_number = int(request.GET.get('page', 1))

        # Determine which page of each to display
        try:
            page_obj_result = paginator_result.page(page_number)
        except (PageNotAnInteger, EmptyPage):
            page_obj_result = paginator_result.page(1)

        try:
            page_obj_ratings = paginator_ratings.page(page_number)
        except (PageNotAnInteger, EmptyPage):
            page_obj_ratings = paginator_ratings.page(1)

        # Calculate total number of pages to synchronize pagination
        total_pages = max(
            ceil(len(result) / recommendations_per_page),
            ceil(len(ratings) / ratings_per_page)
        )

        return render(request, 'app/pesticide.html', {
            'page': page,
            'form': form,
            'list_': page_obj_result,
            'pesticide': page_obj_ratings,
            'total_pages': total_pages,
            'current_page': page_number,
        })

    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return render(request, 'app/pesticide.html', {'page': page, 'form': form})

def pesticide_details(request, id):
    page = 'Organic'
    instance = get_object_or_404(Pesticides, pk=id)
    details = Pesticides.objects.filter(pesticide_id=id)
    ing = PesticideIngredients.objects.filter(pesticide_id=id)
    proc = PesticideProcedure.objects.filter(pesticide_id=id)
    feedback = PesticideFeedback.objects.filter(pesticide_id=id)
    source = PesticideSource.objects.filter(pesticide_id=id)
    benefits = PesticideBenefit.objects.filter(pesticide_id=id)
    notes = PesticideNotes.objects.filter(pesticide_id=id)

    # Paginate feedbacks
    paginator = Paginator(feedback, 4)  # Show 5 feedbacks per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Add user profile image to each feedback
    for i in page_obj:
        profile = Profile.objects.filter(user_id=i.user_id)
        for x in profile:
            if x.image:
                i.image = x.image
            else:
                i.image = settings.MEDIA_URL + "dp/default.jpeg"

    form = PesticideConversionForm(instance=instance)
    return render(request, 'app/pesticide-details.html', {
        'page': page, 'details': details, 'ing': ing, 'proc': proc,
        'feedback': page_obj, 'id': id, 'form': form,
        'source': source, 'benefits': benefits, 'notes': notes
    })

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
        fertilizers_list = list(fertilizers.values('name')[:5])
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
        pesticide_list = list(pesticides.values('name')[:5])
    else:
        suggestions_list = []
        pesticide_list = []
    
    results = {
        'suggestion': suggestions_list,
        'pesticides': pesticide_list,
    }
    return JsonResponse(results, safe=False)