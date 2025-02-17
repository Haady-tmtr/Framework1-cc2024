from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,  HttpResponseRedirect, Http404
from collec_management.models import Collec
from collec_management.forms import *
from django.utils import timezone

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

#from django.contrib.auth.decorators import login_required


# Create your views here.

def about(request):
    return render(request, "about.html",{})


def d_collection(request,id):
    collection= Collec.objects.get(id=id)
    elements = collection.elements.all()
    context = {"collection":collection, "elements":elements}

    if collection.created_by != request.user:
        return render(request, 'errors/403.html', status=403)
    
    return render ( request , "details_collection.html", context )

def liste_collections(request):
    collections = Collec.objects.all()
    return render(request, 'liste_collections.html', {'collections': collections})

   
def new_collection(request) :
    if request.method == "POST":
        form = CollecForm(request. POST)
        if form.is_valid():
            collection = form.save (commit=False) 
            collection.date = timezone.now()

            collection.created_by = request.user # on rattache une collection à son createur
            
            collection.save () 
            return HttpResponseRedirect(f"/collection/{collection.id}")
        return HttpResponseRedirect(f"/all")
        
    else:
        form = CollecForm ()
        context = {"form": form}
        return render(request, "collection_form.html",context)



def delete_collection_confirmation(request, id):
    collection = Collec.objects.get(id=id)

    if collection.created_by != request.user:
        return render(request, 'errors/403.html', status=403)
    
    else:
        if request.method == "POST":
            collection.delete()
            return redirect('liste_collections')

        else:
            return render(request, "delete_confirmation.html", {'collection':collection})



def edit_collection(request, id):
    collection = get_object_or_404(Collec, pk=id)

    if collection.created_by != request.user:
        return render(request, 'errors/403.html', status=403)
    
    else:
        if request.method == "POST":
            collec = CollecForm(request.POST, instance=collection)
            if collec.is_valid():
                collection = collec.save()
                return redirect('liste_collections')
        else:
            collec = CollecForm(instance=collection)

        return render(
            request,
            "modifier_collection.html",{"form": collec}
        )
    

def add_element(request, id_collection):
    collection = get_object_or_404(Collec, id=id_collection)
    

    if request.method == "POST":
        form = ElementForm(request.POST)
        if form.is_valid():
            element = form.save(commit=False)
            element.collection = collection

            element.created_by = request.user # on rattache un élément à son créateur

            element.save()
            #return HttpResponse(f"L'element '{element.title}' a bien ete ajoute a la collection '{collection.title}'.", content_type="text/plain")
            return redirect(f"/collection/{collection.id}")
    else:
        form = ElementForm()

    return render(request, 'form_element.html', {'form': form, 'collection': collection})



def delete_element(request, element_id):
    element = get_object_or_404(Element, id=element_id)
    collection = element.collection 

    if element.created_by != request.user:
        return render(request, 'errors/403.html', status=403)
    
    else :
        if request.method == "POST":
            element.delete()  
            return redirect(f"/collection/{collection.id}")  

        return render(request, "delete_element.html", {
            "element": element,
            "collection": collection,
        }) 


def d_element(request,id):
    element= Element.objects.get(id=id)
    context = {"element":element}
    if element.created_by != request.user:
        return render(request, 'errors/403.html', status=403)
        
    return render ( request , "detail_element.html", context )



def edit_element(request, id):
    element = get_object_or_404(Element, id=id)

    if element.created_by != request.user:
        return render(request, 'errors/403.html', status=403)
    else :
        if request.method == "POST":
            elmt_form = ElementForm(request.POST, instance=element)
            if elmt_form.is_valid():
                element = elmt_form.save()
                return redirect(f"/collection/{element.collection.id}")
        else:
            elmt_form = ElementForm(instance=element)
        return render(request, "modifier_element.html", {"element":element, "form":elmt_form})


def main(request):
    return render(request,"main.html",{})


def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("liste_collections")
            else:
                messages.error(request,"Identifiant ou mot de passe incorrect")
        else:
            messages.error(request, "Erreur dans le formulaire de connexion")
    else:
        # Pas de données POST, afficher un formulaire vide
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form":form})


def logout_user(request):
    logout(request)
    return redirect("liste_collections")


def custom_403_view(request, exception=None):
    return render(request, 'errors/403.html', status=403)
