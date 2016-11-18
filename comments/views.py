from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required

from .models import Comment
from .forms import CommentForm

# Create your views here.

def comment_thread(request, id):
	obj = get_object_or_404(Comment, id = id)
	content_object = obj.content_object
	content_id = obj.content_object.id

	initial_data = {
		"content_type":obj.content_type,
		"object_id": obj.object_id
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

	context={
		"comment": obj,
		"comment_form": form,
	}

	return render(request, "comment_thread.html", context)


@login_required
def comment_delete(request, id):
	obj = get_object_or_404(Comment, id=id)
	if obj.user != request.user:
		# messages.error(request, "You do not have the permission!")
		# raise Http404
		response = HttpResponse("You do not have the permission!")
		response.status_code = 403
		return response
		
	if request.method == "POST":
		parent_obj_url = obj.content_object.get_absolute_url()
		obj.delete()
		messages.success(request, "This has been deleted!")
		return HttpResponseRedirect(parent_obj_url)
	context = {
		"object": obj
	}

	return render(request, "comment_delete.html", context)


















































