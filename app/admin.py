from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import *

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


class PesticideIngredientsStacked(admin.StackedInline):
    model = PesticideIngredients
    initial_num = 1
    list_display = ("description")

    def get_extra(self, request, obj=None, **kwargs):
        if obj is not None:
            try:
                return max(self.initial_num - obj.answers.count(), 1)
            except:
                pass
        return self.initial_num
    
class PesticideProcedureStacked(admin.StackedInline):
    model = PesticideProcedure
    initial_num = 1
    list_display = ("procedure")

    def get_extra(self, request, obj=None, **kwargs):
        if obj is not None:
            try:
                return max(self.initial_num - obj.answers.count(), 1)
            except:
                pass
        return self.initial_num
    
class PesticideConversionStacked(admin.StackedInline):
    model = PesticideConversion
    initial_num = 1
    list_display = ("pesticide", "uom_qty", "uom", "land_qty", "land", "status")

    def get_extra(self, request, obj=None, **kwargs):
        if obj is not None:
            try:
                return max(self.initial_num - obj.answers.count(), 1)
            except:
                pass
        return self.initial_num

class PesticideSourceStacked(admin.StackedInline):
    model = PesticideSource
    initial_num = 1
    list_display = ("pesticide", "source", "link", "status")

    def get_extra(self, request, obj=None, **kwargs):
        if obj is not None:
            try:
                return max(self.initial_num - obj.answers.count(), 1)
            except:
                pass
        return self.initial_num

class PesticideBenefitStacked(admin.StackedInline):
    model = PesticideBenefit
    initial_num = 1
    list_display = ("pesticide", "benefit", "status")

    def get_extra(self, request, obj=None, **kwargs):
        if obj is not None:
            try:
                return max(self.initial_num - obj.answers.count(), 1)
            except:
                pass
        return self.initial_num

class PesticideNotesStacked(admin.StackedInline):
    model = PesticideNotes
    initial_num = 1
    list_display = ("pesticide", "notes", "status")

    def get_extra(self, request, obj=None, **kwargs):
        if obj is not None:
            try:
                return max(self.initial_num - obj.answers.count(), 1)
            except:
                pass
        return self.initial_num

class PesticideUsageStacked(admin.StackedInline):
    model = PesticideUsage
    initial_num = 1
    list_display = ("pesticide", "usage", "status")

    def get_extra(self, request, obj=None, **kwargs):
        if obj is not None:
            try:
                return max(self.initial_num - obj.answers.count(), 1)
            except:
                pass
        return self.initial_num
    
class FertilizerIngredientsStacked(admin.StackedInline):
    model = FertilizersIngredients
    initial_num = 1
    list_display = ("description")

    def get_extra(self, request, obj=None, **kwargs):
        if obj is not None:
            try:
                return max(self.initial_num - obj.answers.count(), 1)
            except:
                pass
        return self.initial_num
    
class FertilizerProcedureStacked(admin.StackedInline):
    model = FertilizersProcedure
    initial_num = 1
    list_display = ("procedure")

    def get_extra(self, request, obj=None, **kwargs):
        if obj is not None:
            try:
                return max(self.initial_num - obj.answers.count(), 1)
            except:
                pass
        return self.initial_num
    
class FertilizerConversionStacked(admin.StackedInline):
    model = FertilizerConversion
    initial_num = 1
    list_display = ("fertilizer", "uom_qty", "uom", "land_qty", "land", "status")

    def get_extra(self, request, obj=None, **kwargs):
        if obj is not None:
            try:
                return max(self.initial_num - obj.answers.count(), 1)
            except:
                pass
        return self.initial_num

class FertilizerSourceStacked(admin.StackedInline):
    model = FertilizerSource
    initial_num = 1
    list_display = ("fertilizer", "benefit", "status")

    def get_extra(self, request, obj=None, **kwargs):
        if obj is not None:
            try:
                return max(self.initial_num - obj.answers.count(), 1)
            except:
                pass
        return self.initial_num

class FertilizerNotesStacked(admin.StackedInline):
    model = FertilizerNotes
    initial_num = 1
    list_display = ("fertilizer", "notes", "status")

    def get_extra(self, request, obj=None, **kwargs):
        if obj is not None:
            try:
                return max(self.initial_num - obj.answers.count(), 1)
            except:
                pass
        return self.initial_num

class FertilizerBenefitStacked(admin.StackedInline):
    model = FertilizerBenefits
    initial_num = 1
    list_display = ("fertilizer", "be", "link", "status")

    def get_extra(self, request, obj=None, **kwargs):
        if obj is not None:
            try:
                return max(self.initial_num - obj.answers.count(), 1)
            except:
                pass
        return self.initial_num

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Pesticides)
class PesticideAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "status")
    search_fields = ['name']
    inlines = [
        PesticideIngredientsStacked,
        PesticideProcedureStacked,
        PesticideConversionStacked,
        PesticideSourceStacked,
        PesticideBenefitStacked,
        PesticideNotesStacked,
        PesticideUsageStacked,
    ]

@admin.register(Fertilizers)
class FertilizerAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "status")
    search_fields = ['name']
    inlines = [
        FertilizerIngredientsStacked,
        FertilizerProcedureStacked,
        FertilizerConversionStacked,
        FertilizerSourceStacked,
        FertilizerBenefitStacked,
        FertilizerNotesStacked,
    ]

@admin.register(Appointments)
class AppointmentsAdmin(admin.ModelAdmin):
    list_display = ("user__first_name", "user__last_name", "user__email", "event_type", "start", "end", "duration")

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("subject", "sent_datetime", "created_by")

    exclude = ('created_by', 'sent_datetime',)

    def has_change_permission(self, request, obj=None):
        # Prevent editing: Allow editing only for superusers, or based on conditions
        if request.user.is_superuser:
            return True
        return False  # Regular users cannot edit

    def has_delete_permission(self, request, obj=None):
        # Prevent deleting: Allow deleting only for superusers, or based on conditions
        if request.user.is_superuser:
            return True
        return False  # Regular users cannot delete

    def save_model(self, request, obj, form, change):
        # Automatically set the user who is creating or updating the model
        if not change:  # If creating a new object
            obj.created_by = request.user
        obj.save()

admin.site.register(UOM)
admin.site.register(LandMeasure)
