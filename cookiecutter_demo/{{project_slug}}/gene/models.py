from django.db import models

# Create your models here.
class Species(models.Model):
    id = models.IntegerField(primary_key=True)
    key_name = models.CharField(max_length=100, unique=True, null=True)
    name = models.CharField(max_length=100, unique=True, null=True)  
    order = models.CharField(max_length=100, blank=True, null=True)  
    family = models.CharField(max_length=100, blank=True, null=True)  
    genus = models.CharField(max_length=100, blank=True, null=True)  
    taxonomy = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)  

    def __str__(self):
        return self.key_name

class Gene(models.Model):
    id = models.IntegerField(primary_key=True)
    key_name = models.CharField(max_length=100, unique=True, null=True)
    key_species = models.ForeignKey(Species, on_delete=models.CASCADE, related_name='genes', null=True)
    species = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, null=True) 
    gene_id = models.CharField(max_length=100, blank=True, null=True)
    gene_seq = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.key_name

class Compound(models.Model):
    id = models.IntegerField(primary_key=True)
    pubchem_id = models.CharField(max_length=100, blank=True, null=True) 
    name = models.CharField(max_length=100, unique=True, null=True)
    cmpdsynonym = models.TextField(blank=True, null=True)
    mw = models.CharField(max_length=100, blank=True, null=True)
    mf = models.CharField(max_length=100, blank=True, null=True)
    polararea = models.CharField(max_length=100, blank=True, null=True)
    complexity = models.CharField(max_length=100, blank=True, null=True)
    xlogp = models.CharField(max_length=100, blank=True, null=True)
    heavycnt = models.CharField(max_length=100, blank=True, null=True)
    hbonddonor = models.CharField(max_length=100, blank=True, null=True)
    hbondacc = models.CharField(max_length=100, blank=True, null=True)
    rotbonds = models.CharField(max_length=100, blank=True, null=True)
    inchi = models.CharField(max_length=1000, blank=True, null=True)
    isosmiles = models.CharField(max_length=1000, blank=True, null=True)
    canonicalsmiles = models.CharField(max_length=1000, blank=True, null=True)
    inchikey = models.CharField(max_length=1000, blank=True, null=True)
    iupacname = models.CharField(max_length=1000, blank=True, null=True)
    exactmass = models.CharField(max_length=100, blank=True, null=True)
    monoisotopicmass = models.CharField(max_length=100, blank=True, null=True)
    charge = models.CharField(max_length=100, blank=True, null=True)
    covalentunitcnt = models.CharField(max_length=100, blank=True, null=True)
    isotopeatomcnt = models.CharField(max_length=100, blank=True, null=True)
    totalatomstereocnt = models.CharField(max_length=100, blank=True, null=True)
    definedatomstereocnt = models.CharField(max_length=100, blank=True, null=True)
    undefinedatomstereocnt = models.CharField(max_length=100, blank=True, null=True)
    totalbondstereocnt = models.CharField(max_length=100, blank=True, null=True)
    definedbondstereocnt = models.CharField(max_length=100, blank=True, null=True)
    undefinedbondstereocnt = models.CharField(max_length=100, blank=True, null=True)
    annotation = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.pubchem_id

# 文献模型
class Reference(models.Model):
    id = models.IntegerField(primary_key=True)
    wos = models.CharField(max_length=1000, blank=True, null=True) 
    title = models.CharField(max_length=1000, null=True) 
    journal = models.CharField(max_length=255, null=True) 
    doi = models.CharField(max_length=100, blank=True, null=True) 
    year = models.CharField(max_length=100, blank=True, null=True) 
    pubmed_id = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.title} ({self.year})"

# 基因-化合物关系模型
class GeneCompoundRelationship(models.Model):
    id = models.IntegerField(primary_key=True)
    gene = models.ForeignKey(Gene, on_delete=models.CASCADE, null=True) 
    compound = models.ForeignKey(Compound, on_delete=models.CASCADE, null=True) 
    validation_method = models.CharField(max_length=200, blank=True, null=True) 
    references = models.ForeignKey(Reference, on_delete=models.CASCADE, null=True)
    note = models.CharField(max_length=1000, blank=True, null=True)
    

    def __str__(self):
        return f"{self.gene.key_name} - {self.compound.pubchem_id}"