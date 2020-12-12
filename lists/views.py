from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, render
from lists.models import Item

def home_page(request):
    return render(request, 'home.html')
    
def new_list(request):
    list_ = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': list_})

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_)
    return render(request, 'list.html', {'items': items})

def add_item(request, list_id):    
    list_ = List.objects.get(id=list_id)    
    Item.objects.create(text=request.POST['item_text'], list=list_)    
    return redirect(f'/lists/{list_.id}/')

#def home_page(request):
#    item = Item()
#    item.text = request.POST.get('item_text', '')
#    item.save()
#    
#    return render(request, 'home.html', {        
#        #'new_item_text': request.POST.get('item_text', ''),    
#        'new_item_text': item.text
#    })
    #if request.method == 'POST':        
    #    return HttpResponse(request.POST['item_text'])
    #return render(request, 'home.html')
    #return HttpResponse('<html><title>To-Do lists</title></html>')

#    def home_page(request):
#        if request.method == 'POST':
#            new_item_text = request.POST['item_text']
#            Item.objects.create(text=new_item_text)
#        else:
#            new_item_text = '' 
#
#        return render(request, 'home.html', {
#            'new_item_text': new_item_text, 
#        })