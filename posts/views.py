# -*- coding: utf-8 -*-
from urllib import quote_plus

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone

from .models import Post
from .forms import PostForm
from comments.models import Comment
from comments.forms import CommentForm

# Create your views here.


def post_list(request):
	queryset_list = Post.objects.active().order_by('-timestamp')
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all().order_by('-timestamp') 
	
	query = request.GET.get("q")
	if query:
		queryset_list = Post.objects.filter(
			Q(title__icontains=query)|
			Q(content__icontains=query)
			# Q(author__name__icontains=query)
			).distinct()
		
	paginator = Paginator(queryset_list, 5)
	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)



	context = {
		"title": "R酱的小站",
		"object_list": queryset,
	}
	return render(request, "post_list.html", context)



 


def post_create(request):
	if not request.user.is_authenticated():
		raise Http404

	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		# message success
		messages.success(request, "Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())
	# else:
	# 	messages.error(request, "Fail Created")

	# to see how the post method works
	# if request.method == "POST":
	# 	print request.POST.get("content")
	# 	print request.POST.get("title")
	
	context = {
		"title": "Form",
		"form": form,
	}

	return render(request, "post_create.html", context)



def post_detail(request, slug = None): # retrieve
	# instance = Post.objects.get(id = 1) #not include exception
	instance = get_object_or_404(Post, slug=slug)
	share_string = quote_plus(instance.slug)


	initial_data = {
			"content_type": instance.get_content_type,
		"object_id": instance.id
	}
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():

		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()

		new_comment, created = Comment.objects.get_or_create(
			user = request.user,
			content_type = content_type,
			object_id = obj_id,
			content = content_data,
			parent = parent_obj,
			)
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	comments = instance.comments
	
	context = {
		"title": instance.title,
		"instance": instance,
		"share_string": share_string,
		"comments": comments,
		"comment_form": form,
		
	}

	return render(request, "post_detail.html", context)


# def post_list(request): # list items

# 	return HttpResponse("<h1>Hello</h1>")


def post_update(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	form = PostForm(request.POST or None, request.FILES or None, instance = instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		# message success
		messages.success(request, "Saved", extra_tags = "some_tag")
		return HttpResponseRedirect(instance.get_absolute_url())
	# else:
	# 	messages.error(request, "Fail Saved")

	context = {
		"title": instance.title,
		"instance": instance,
		"form": form,
	}

	return render(request, "post_create.html", context)


def post_delete(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	instance.delete()
	messages.success(request, "Successfully Deleted")
	return redirect("posts:list")	
