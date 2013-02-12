# coding:utf-8

from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from random import choice
from string import lowercase, digits
import markdown
import exceptions as exc

try:
    from django.core.urlresolvers import reverse_lazy
except ImportError:
    from django.utils.functional import lazy
    reverse_lazy = lazy(reverse, str)

import logging
logger = logging.getLogger(__name__)


def generate_random_password(max_length=5):
    return "".join([choice(lowercase+digits) for i in range(max_length)])


def paginate(objlist, numitems, pagenum, count=None):
    paginator = Paginator(objlist, numitems)
    if count is not None:
        ''' raw querylerde count'u disardan sagliyoruz. aksi halde len falan ile almak gerek ki
        bu da bellek dertleri yaratabilir.
        '''
        paginator._count = count
    return paginator.page(pagenum)


def t_int(_str, default=0):
    ''' degeri integer'a cevir, ya da default degeri don'''
    try:
        return int(_str)
    except (exc.ValueError, exc.TypeError):
        pass
    return default


def one_or_none(klass, *args, **kwargs):
    ''' osrgudan sonuc donerse ilk sonucu al, hata veya sifir sonuc durumunda None don''' 
    try:
        if not hasattr(klass, 'objects'):
            return klass.filter(*args, **kwargs)[0]
        return klass.objects.get(*args, **kwargs)
    except:
        return None


def chunks(l, n):
    ''' listeyi n elemanli alt gruplara boluyoruz. 
        orn: [1,2,3,4,5,6,7,8,9,0] -> [[1,2,3], [4,5,6], [7,8,9], [0]] 
    '''
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


def get_int(request, param_name):
    try:
        return int(request.REQUEST[param_name])
    except:
        return None


def markdown_to_html(content): 
    return markdown.markdown(content, extensions=["extra", "footnotes"])


import difflib
def show_diff(t1, t2):
    seqm= difflib.SequenceMatcher(None, t1, t2)
    output= []
    for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
        if opcode == 'equal':
            output.append(seqm.a[a0:a1])
        elif opcode == 'insert':
            output.append("<ins>" + seqm.b[b0:b1] + "</ins>")
        elif opcode == 'delete':
            output.append("<del>" + seqm.a[a0:a1] + "</del>")
        elif opcode == 'replace':
            output.append("<del>" + seqm.a[a0:a1] + "</del><ins>" + seqm.b[b0:b1] + "</ins>")
        else:
            raise RuntimeError, "unexpected opcode"
    return ''.join(output)


