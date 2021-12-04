from django.http.response import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
# from LOGIN.models import Person as FarmingPerson
# from LOGIN.models import Feed, Booking, Workshop, Group, Member 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
# from .forms import CreateInDiscussion, PersonForm, UserUpdateForm
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.db.models.signals import post_save
from django.dispatch import receiver
from cryptography.fernet import Fernet
from .models import Feed, Comment
from group.models import Group
from member.models import Person, SoilTag, PlantTag
from sharing.models import FeedSoilTagging, FeedPlantTagging

# Create your views here.


#sharing
def mainSharing(request):
    try:
        feed=Feed.objects.all()
        soilTags = SoilTag.objects.all()
        return render(request,'MainSharing.html',{'feed':feed ,'soilTags':soilTags})
    except Feed.DoesNotExist:
        raise Http404('Data does not exist')



def sharingGroup(request, pk):
    
    group_forum = Group.objects.get(id=pk)
    creator=Person.objects.get(Email=request.session['Email'])
    soilTagList=SoilTag.objects.all()
    plantTagList=PlantTag.objects.all()

    if request.method=='POST':
        taggingSoil=SoilTag.objects.all()
        Title=request.POST.get('Title')
        Message=request.POST.get('Message')
        Photo=request.POST.get('Photo')
        Video=request.POST.get('Video')
        # Graph=request.POST.get('Graph')
        feed_id = Feed(Title=Title,Message=Message,Photo=Photo,Video=Video,Group=group_forum,Creator=creator).save()
        feed = Feed.objects.get(id=feed_id)

        soilTagsID = request.POST.getlist('SoilTag')
        plantTagsID = request.POST.getlist('PlantTag')

        for soilTagsID in soilTagsID:
            soilTag = SoilTag.objects.get(id=soilTagsID)
            FeedSoilTagging(FeedSoilTag = feed, soilTag=soilTag).save()

        for plantTagsID in plantTagsID:
            plantTag = PlantTag.objects.get(id=plantTagsID)
            FeedPlantTagging(FeedPlantTag = feed, plantTag=plantTag).save()

        messages.success(request,'The new feed is save succesfully..!')
        return render(request,'sharing.html')

    else :
        # taggingSoil=SoilTag.objects.all()
        return render(request,'sharing.html', {'SoilTag':soilTagList, 'PlantTag':plantTagList})

  

def updateSharing(request, pk):
    # feed = Feed.objects.filter(id=pk)
    feed = Feed.objects.get(id=pk)
    soilTag=FeedSoilTagging.objects.filter(FeedSoilTag=feed)
    farming_soilTag=FeedSoilTagging.objects.filter(FeedSoilTag=feed)
    soilTagList=SoilTag.objects.all()
    plantTag=FeedPlantTagging.objects.filter(FeedPlantTag=feed)
    plantTagList=PlantTag.objects.all()
    
    if request.method=='POST':
        feed.Title=request.POST['Title']
        feed.Message=request.POST.get('Message')
        feed.Photo=request.POST.get('Photo')
        feed.Video=request.POST.get('Video')

        newSoilTags = request.POST.getlist('SoilTag')
        newPlantTags = request.POST.getlist('PlantTag')

        currentSoilTag=FeedSoilTagging.objects.filter(FeedSoilTag=feed)
        farmingSoilTag2=FeedSoilTagging.objects.filter(FeedSoilTag=feed)
        currentPlantTag=FeedPlantTagging.objects.filter(FeedPlantTag=feed)
        farmingPlantTag2=FeedPlantTagging.objects.filter(FeedPlantTag=feed)
        

        if soilTag:
            for currentSoilTag in currentSoilTag:
                currentSoilTag.deleteRecordFarming()
            for farmingSoilTag2 in farmingSoilTag2:
                farmingSoilTag2.deleteRecordIgrow()

        for newSoilTag in newSoilTags:
            new_soilTag = SoilTag.objects.get(id=newSoilTag)
            FeedSoilTagging(FeedSoilTag = feed, soilTag=new_soilTag).save()

        if plantTag:
            for currentPlantTag in currentPlantTag:
                currentPlantTag.deleteRecordFarming()
            for farmingPlantTag2 in farmingPlantTag2:
                farmingPlantTag2.deleteRecordIgrow()

        for newPlantTag in newPlantTags:
            new_plantTag = PlantTag.objects.get(id=newPlantTag)
            FeedPlantTagging(FeedPlantTag = feed, plantTag=new_plantTag).save()

        feed.save()

        messages.success(request,'The post of ' + request.POST['Title'] + " is updated succesfully..!")
        return render(request,'ViewSharing.html')
    else:
        return render(request, 'ViewSharing.html', {'feed': feed, 'SoilTag':soilTagList, 'currentSoilTag':soilTag, 'PlantTag':plantTagList, 'currentPlantTag':plantTag})


def deleteSharing(request,pk):
    try:
        feed=Feed.objects.get(id=pk)
        feed2=Feed.objects.get(id=pk)

        data=Feed.objects.all()
        if request.method=='POST':
            feed.deleteRecordIgrow()
            feed2.deleteRecordFarming()
            # messages.success(request,'The ' + feed.Title + " is deleted succesfully..!")
            return redirect('sharing:MainSharing')
        
        else:
            return render(request, 'deleteSharing.html', {'feed':feed})
        
    except Feed.DoesNotExist:
        messages.success(request,'No record of the feed!')
        return redirect('sharing:MainSharing')


def viewForum(request, pk):
    data = Group.objects.get(id=pk)
    # soilTags = FeedSoilTagging.objects.all()
    feed = Feed.objects.filter(Group = data)

    return render(request, 'Forum.html', {'feed': feed, 'data':data})


def addComment(request, pk):
    commenter=Person.objects.get(Email=request.session['Email'])
    feed = Feed.objects.get(id=pk)
    group_id = feed.Group.id
    
    if request.method=='POST':
        
        Message=request.POST.get('Message')
        Picture=request.POST.get('Pictures')
        Video=request.POST.get('Video')
        
        Comment(Message=Message,Pictures=Picture,Video=Video,Commenter=commenter,Feed=feed).save(),
        # messages.success(request,'The comment is save succesfully..!')
        # return render(request,'addComment.html')
        return redirect('sharing:Forum', group_id)
    else :
        return render(request,'addComment.html', {'feed':feed})

# def viewFeed(request, pk_feed, pk_group):

#     group = Group.objects.get(id=pk_group)
#     feed = Feed.objects.get(id=pk_feed,Group=group)
#     return render(request,'Forum.html', {'feed':feed})

def updateComment(request, pk):
   
    comment = Comment.objects.get(id=pk)
    group_id=comment.Feed.Group.id
    feed = comment.Feed
    if request.method=='POST':
       
       comment.Message=request.POST.get('Message')
       comment.Photo=request.POST.get('Picture')
       comment.Video=request.POST.get('Video')
       comment.save()
    #    messages.success(request,"The comment of is updated succesfully..!")
       return redirect('sharing:Forum', group_id)
    else:
        return render(request, 'addComment.html', {'comment': comment})

def deleteComment(request,pk):
    comment = Comment.objects.get(id=pk)
    group_id=comment.Feed.Group.id
    feed = comment.Feed
    try:
        comment=Comment.objects.get(id=pk)
        comment2=Comment.objects.get(id=pk)

        if request.method=='POST':
            comment.deleteRecordIgrow()
            comment2.deleteRecordFarming()
            # messages.success(request,'The ' + feed.Title + " is deleted succesfully..!")
            return redirect('sharing:Forum', group_id)
        
        else:
            return render(request, 'deleteComment.html', {'comment':comment})
        
    except Comment.DoesNotExist:
        messages.success(request,'No record of the comment!')
        return redirect('sharing:Forum', group_id)
