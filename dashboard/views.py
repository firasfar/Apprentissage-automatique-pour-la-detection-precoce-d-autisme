from time import sleep
from django.shortcuts import render
from .models import Profile
from .models import User
from .models import Data
from .camera import VideoCamera,gen,Video
from django.http import StreamingHttpResponse
def index(res):
    return render(res,'profile/profile.html')

def home(res):
    per = Profile.objects.all()
    le = range(len(per))
    totale = zip(per,le)
    return render(res,'dashboard/dashboard.html',{'profile':totale}) 

def create(res):
    nom = res.POST.get('nom')
    prenom = res.POST.get('prenom')
    sexe = res.POST.get('sexe')
    date = res.POST.get('date')  
    email = res.POST.get('email')
    ville = res.POST.get('ville')
    contact = res.POST.get('contact')
    return render(res,'profile/profile_fixed.html',{'nom':nom,'prenom':prenom,'sexe':sexe,'date':date,'email':email,'ville':ville,'contact':contact})
def edit(res):
    nom = res.POST.get('nom')
    prenom = res.POST.get('prenom')
    sexe = res.POST.get('sexe')
    date = res.POST.get('date')  
    email = res.POST.get('email')
    ville = res.POST.get('ville')
    contact = res.POST.get('contact')
    return render(res,'profile/profile_edit.html',{'nom':nom,'prenom':prenom,'sexe':sexe,'date':date,'email':email,'ville':ville,'contact':contact})
def choix(res,nom,prenom,sexe,date,email,ville,contact):
    profile = Profile(nom=nom,prenom=prenom,sexe=sexe,date=date,email=email,ville=ville,contact=contact) 
    profile.save()
    
    print("id=")
    print(profile)
    id = profile.id
    return render(res,'video/choix_analyse.html',{'id':id})
def conecte(res):
    user = User.objects.filter(user=res.POST.get('user'))
    if(user.filter(password=res.POST.get('password'))):
        per = Profile.objects.all()
        le = range(len(per))
        totale = zip(per,le)
        return render(res,'dashboard/dashboard.html',{'profile':totale}) 
    else:
        return render(res,'login/login.html') 


def opencam(res,id):
    return StreamingHttpResponse(gen(VideoCamera(id)), content_type='multipart/x-mixed-replace; boundary=frame')

def closecam(res,id):
    return StreamingHttpResponse(gen(VideoCamera(id).__del__), content_type='multipart/x-mixed-replace; boundary=frame')    

def video(res,file,id):
    return StreamingHttpResponse(gen(Video("C:/Users/Firas Farjallah/"+file,id)), content_type='multipart/x-mixed-replace; boundary=frame')    

def streaming(res,id):
    
    return render(res,'video/video_streaming.html',{"id":id})

def analyse(res,id):
    file = res.POST.get("file")
    
    return render(res,'video/video_inporte.html',{"file":file,"id":id})        

def profile_show(res,id):
    profilee = Profile.objects.get(id=id)
    
    data = Data.objects.filter(profile=profilee)
    le = range(len(data))
    autism =0 
    no_autism =0 
    for i in data:
        if i.classe=='Autism':
            autism=autism+1
        else : 
            no_autism=no_autism+1  
    autism=autism/len(data)*100
    no_autism=no_autism/len(data)*100         
    totale = zip(data,le)
    return render(res,'profile/profile_show.html',{'Data':totale,'profile':profilee,'autism':f'{autism:.2f}','no_autism':f'{no_autism:.2f}'}) 
# Create your views here.
