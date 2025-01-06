import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "P450.settings")

django.setup()

from gene.models import Species, Gene
List = []
for line in open('./data/gene.tab', 'r', encoding='UTF-8'):
    tmp = (line.strip()).split('\t')
    id = tmp[0]
    key_name = tmp[1]
    # print(tmp[2])
    key_species = Species.objects.get(key_name = tmp[2])
    species = tmp[3]
    name = tmp[4]
    gene_id = tmp[5]
    gene_seq = tmp[6]
    item = Gene(id = id,key_name = key_name,key_species = key_species,species = species,name  = name ,gene_id = gene_id,gene_seq = gene_seq)
    List.append(item)

Gene.objects.bulk_create(List)

print('Done!')
