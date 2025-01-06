from django.shortcuts import render, redirect
from .models import Gene, Species, Compound, Reference, GeneCompoundRelationship
from django.db.models import Q
import os, datetime, random
from django.http import JsonResponse, HttpResponse

# Create your views here.
def home(request):
    return render(request, 'home.html')

def search(request):
    query = request.GET.get('q')  # 获取搜索关键词
    s_order = request.GET.get('s_order')
    flag=False
    results = []
    
    if query:
        genes = Gene.objects.filter(
            Q(name__icontains=query) | Q(key_name__icontains=query)
        )

        if s_order == 'all':
            results=genes
            flag=True
        else:
            for x in genes:
                Species=x.key_species
                if Species.order == s_order:
                    results.append(x)
                    flag=True
        
        for x in genes:
            gene_compound=GeneCompoundRelationship.objects.filter(gene=x)
            x.gene_compound = gene_compound
    
    return render(request, 'Search.html', {'results': results, 'query': query,'s_order':s_order, 'flag':flag})

def blast(request):
    return render(request, 'blast.html')

def get_ran_dom():
    nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前时间
    randomNum = random.randint(0, 100)  # 生成的随机整数n，其中0<=n<=100
    if randomNum <= 10:
        randomNum = str(0)+str(randomNum)
    uniqueNum = str(nowTime)+str(randomNum)
    return uniqueNum

class blastGene:
    def __init__(self, query_name, search_name, gene_id, gene, evalue, score):
        self.query_name = query_name
        self.search_name = search_name
        self.gene_id = gene_id
        self.gene = gene
        self.evalue = evalue
        self.score = score

def blastResult(request):
    results = {}
    blast_type=request.POST.get('type')
    evalue=request.POST.get('evalue')
    file_name=get_ran_dom()+'.fasta'
    out_name=get_ran_dom()+'.out'
    context=request.POST.get('q')
    save_path = os.path.join('upload/', file_name)
    with open(save_path, 'w') as f:
        if '>' not in context:
            f.write('>tmp\n'+context)
        else:
            f.write(context)
    
    if blast_type == 'blastp' or blast_type == 'blastx':
        db='/home/jau/database/01_eP450/django/db/prot.fa'
    else:
        db='/home/jau/database/01_eP450/django/db/nucl.fa'
    cmd='/home/jau/software/ncbi-blast-2.16.0+/bin/'+blast_type+' -query /home/jau/database/01_eP450/django/'+save_path+' -db '+db+' -outfmt 6 -num_threads 8 -evalue '+evalue+' -out /home/jau/database/01_eP450/django/result/'+out_name
    os.system(cmd)
    
    with open('/home/jau/database/01_eP450/django/result/'+out_name) as f:
        context = f.readlines()
        if context == []:
            results['error']='Yes'
        else:
            results['error']='No'
            results['result'] = []
            results['download'] = 'result|'+out_name
            for line in f.readlines()[20:]:
                line = line.strip().split('\t')
                query_name = line[0]
                search_name = line[1].split('_')[0]
                gene_id = line[1].split('_')[1]
                gene = Gene.objects.get(id=gene_id)
                evalue = line[10]
                score = line[11]
                results['result'].append(blastGene(query_name, search_name, gene_id, gene, evalue, score))
    
    return render(request, 'blastResult.html', results)


def insect(request,id):
    insect = Species.objects.get(id=id)
    gene = insect.genes.all()
    gene_compound = GeneCompoundRelationship.objects.filter(gene__in=gene)
    result={}
    result['insect']=insect
    result['gene']=gene
    result['gene_compound']=gene_compound
    return render(request, 'insect.html', result)

def compound(request, id):
    compound = Compound.objects.get(id=id)
    gene_compound = GeneCompoundRelationship.objects.filter(compound=compound)
    compound.cmpdsynonym =  compound.cmpdsynonym.split('|')
    compound.annotationlist =  compound.annotation.split('>')
    result={}
    result['compound']=compound
    result['gene_compound']=gene_compound
    return render(request, 'compound.html', result)

def gene(request, id):
    gene = Gene.objects.get(id=id)
    gene_compound = GeneCompoundRelationship.objects.filter(gene=gene)
    if os.path.exists('data/nucl/'+gene.key_name+'.fa'):
        gene.nucl='data|nucl|'+gene.key_name+'.fa'
    else:
        gene.nucl='none'
    
    if os.path.exists('data/prot/'+gene.key_name+'.fa'):
        gene.prot='data|prot|'+gene.key_name+'.fa'
    else:
        gene.prot='none'
    
    if os.path.exists('data/cif/'+gene.key_name.lower()+'.cif'):
        gene.cif='data|cif|'+gene.key_name.lower()+'.cif'
        gene.cifname=gene.key_name.lower()+'.cif'
    else:
        gene.cif='none'

    if gene.gene_id != 'none':
        if 'gene' in gene.gene_id:
            gene.id_tag = 'gene'
        elif 'prot' in gene.gene_id:
            gene.id_tag = 'protein'
        elif 'nucl' in gene.gene_id:
            gene.id_tag = 'nucleotide'
        gene.idname = gene.gene_id.split('|')[1]
    else:
        gene.id_tag = 'none'

    result={}
    result['gene']=gene
    result['gene_compound']=gene_compound
    return render(request, 'gene.html', result)

def compoundlist(request):
    compounds = Compound.objects.all()
    result={}
    result['compounds']=compounds
    return render(request, 'compoundlist.html', result)

def insectlist(request):
    insects = Species.objects.all()
    default_insect = Species.objects.get(id=17)
    result={}
    result['insects']=insects
    result['default_insect']=default_insect
    return render(request, 'insectlist.html', result)

def get_insect_content(request, id):
    insect = Species.objects.get(id=id)
    return JsonResponse({
        'name': insect.name,
        'order': insect.order,
        'family': insect.family,
        'genus': insect.genus,
        'description': insect.description,
        'id': insect.id
    })

def download(request):
    return render(request, 'download.html')

def download_file(request, file_path):
    with open(file_path.replace('|', '/'), 'rb') as f:
        file_name=file_path.split('|')[-1]
        response = HttpResponse(f.read(), content_type="application/octet-stream")
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response

def tree(request):
    return render(request, 'tree.html')

def help(request):
    return render(request, 'help.html')