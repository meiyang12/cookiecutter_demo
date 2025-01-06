from django.contrib import admin
from .models import Gene, Species, Compound, Reference, GeneCompoundRelationship

# Register your models here.

class GeneAdmin(admin.ModelAdmin):
    list_display = ('id', 'key_name')

admin.site.register(Gene, GeneAdmin)

class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('id', 'key_name')

admin.site.register(Species, SpeciesAdmin)

class CompoundAdmin(admin.ModelAdmin):
    list_display = ('id', 'pubchem_id')

admin.site.register(Compound, CompoundAdmin)

class ReferenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'wos')

admin.site.register(Reference, ReferenceAdmin)

class GeneCompoundRelationshipAdmin(admin.ModelAdmin):
    list_display = ('id', 'gene', 'compound')

admin.site.register(GeneCompoundRelationship, GeneCompoundRelationshipAdmin)