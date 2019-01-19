from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic.edit import CreateView,UpdateView
from .models import Post,Category,Comment,UserProfile,Friend
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView 
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from .forms import PostForm,CommentForm
from django.contrib.auth.models import User
from .forms import RegistrationForm,EditProfileForm, UserUpdateForm
from django.contrib.auth.forms import UserChangeForm
from django.views.generic import TemplateView
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.http import HttpResponseRedirect
import requests


# Create your views here.
'''
@login_required(login_url="login/")
def add_post(request):
 form = PostForm(request.POST or None)
 if form.is_valid():
  	post = form.save() 
  	return redirect('booklibrary:book_paste_list') 
 return render(request, 'booklibrary/post_form.html',{ 'form': form })
''' 
def index(request):
	r = requests.get('http://httpbin.org/status/418')
	print(r.text)
	return HttpResponse('<pre>' + r.text + '</pre>')





@login_required(login_url="/login/")
def	add_post(request):
	if request.method =='POST':
		a_form = PostForm(request.POST,request.FILES)
		if a_form.is_valid:
			#save to db
			post= a_form.save(commit=False)
			post.user = request.user
			post.save()
			return redirect('booklibrary:book_paste_list')
	else:
		a_form =  PostForm()		
		return render(request, 'booklibrary/post_form.html',{ 'a_form': a_form })


#@login_required(login_url="login/")
'''
def view_comment(request, slug):
 		post = get_object_or_404(Post,slug=slug)
 		if request.method == 'POST':
 			form = 	CommentForm(request.POST)
 			if form.is_valid():
 				comment = form.save(commit=False)
 				comment.post = post
 				comment.save()
 				return redirect('booklibrary:bookcomment', slug=post.slug)
 		else:
 				form = CommentForm()
 				return render(request, 'booklibrary/bookcomment.html',{ 'form': form })
		
'''
# class Comment(ListView):
# 	model= Comment
# 	template_name = 'booklibrary/bookcomment.html'
# 	queryset =  Comment.objects.filter('post_id')
# 	context_object_name = 'queryset'

def display_comment(request, post_id):
	text = Comment.objects.filter(post_id= post_id).order_by('-created_on')
	
			
	context =    {'text':text}
	return render(request, 'booklibrary/bookcomment.html', context)



@login_required(login_url="/login/")
def add_comment(request,id):
	post = get_object_or_404(Post,id=id)
	
	if request.method == 'POST':
			p_form = CommentForm(request.POST)
			if p_form.is_valid()  :
				comment=p_form.save(commit=False)
				comment.post = post
				comment.name = request.user
				comment.save()
				
				#return redirect(request.path) 
				return redirect('booklibrary:book_paste_detail',pk=id)
	else:
			p_form = CommentForm()
			context = {'p_form':p_form}
			return render(request, 'booklibrary/addcomment.html', context)



		
'''
		if request.method == 'POST':
			form = 	CommentForm(request.POST)
			if form.is_valid():
				comment = form.save(commit=False)
				comment.post = post
				comment.save()
				return redirect('booklibrary:bookcomment')

		else: CommentForm
			form = CommentForm()
			'''
		
		#post = get_object_or_404(Post)

		
		# post = get_object_or_404(Post)
		# if request.method == 'POST':
		# 	form = 	CommentForm(request.POST)
		# 	if form.is_valid():
		# 		comment = form.save(commit=False)
		# 		comment.post = post
		# 		comment.save()
		# 		return redirect('booklibrary:bookcomment')

		# else:
		# 	form = CommentForm()
		# 	return render(request,'booklibrary/bookcomment.html', context, {'form':form})

def display_category(request,category_id):
	text = Post.objects.filter(category_id=category_id)
	
	query = request.GET.get('q')
	if query:
		text = text.filter(Q(title__icontains=query)|
						   Q(text__icontains=query)|
						   Q(author__icontains=query)
						   
						   )

		
	paginator = Paginator(text,24)		
	page = request.GET.get('page')
	text = paginator.get_page(page)
	try:
		text = paginator.page(page)
	except PageNotAnInteger:
			text = paginator.page(1)
	except EmptyPage:
			text = paginator.page(paginator.num_page)
 


	context = {'text': text}
	return render(request, 'booklibrary/displaycategory.html', context)

def postbyuser(request,user_id):
	user =	 Post.objects.filter(user_id=user_id)

	paginator = Paginator(user,24)		
	page = request.GET.get('page')
	user = paginator.get_page(page)
	try:
		user = paginator.page(page)
	except PageNotAnInteger:
			user = paginator.page(1)
	except EmptyPage:
			user = paginator.page(paginator.num_page)
	context = {'user': user}
	return render(request, 'booklibrary/userprofile_form.html', context)
	











def like_post(request):
	obj = get_object_or_404(Post,id=request.POST.get('obj_id'))
	is_liked = False
	if obj.likes.filter(id=request.user.id).exists():
		obj.likes.remove(request.user)
		is_liked = False
	else:	
			obj.likes.add(request.user)
			is_liked = True
	return HttpResponseRedirect(obj.get_absolute_url())


'''
class createinfouser(CreateView):
	model = UserProfile
	fields =  ['description','city','website','image']
	'''


'''
class Bookcomment(DetailView):
   model = Comment
   template_name = 'booklibrary/bookcomment.html'	
   queryset = Comment.objects.all() 
   context_object_name = 'queryset'
   
class Comment(CreateView):
	 model = Comment

	 fields = ['name','text']

'''

class BookList(ListView):
	
	 template_name = 'booklibrary/booklist.html'
	 def get(self,request):
	  	 model = Post
	  	 queryset = Post.objects.all().order_by('-created_on')
	  	 query = request.GET.get("q")
	  	 if query:
	  	 	queryset =  queryset.filter(
	  	 			Q(title__icontains=query)|
					Q(text__icontains=query)|
					Q(author__icontains=query)
	  	 			
	  	 									)

	  	 									



	  	 paginator = Paginator( queryset,24)
	  	 page = request.GET.get('page')
	  	 queryset = paginator.get_page(page)
	  	 try:
	  	 	 queryset = paginator.page(page)
	  	 except PageNotAnInteger:
	  	 	 queryset = paginator.page(1)
	  	 except EmptyPage:
	  	 	 queryset = paginator.page(paginator.num_page)
 



	  	 args = {'queryset':queryset }
	  	 return render(request,self.template_name,args)




class BookDetail(DetailView):
	
	template_name = 'booklibrary/bookdetail.html'
	def get(self,request,pk):
		text = Comment.objects.filter(post_id= pk).order_by('-created_on')
		model = Post
		obj = Post.objects.get(pk=pk)
		is_liked = False
		is_favourite =False
		if obj.likes.filter(id=request.user.id).exists():
			is_liked =True
		if obj.favourite.filter(id=request.user.id).exists():
			is_favourite =True

	
			
		context =    {'text':text,'obj':obj,'is_liked':is_liked,'total_likes':obj.total_likes(),'is_favourite':is_favourite}
		return render(request, self.template_name, context)


def userfavourite_book(request):
	user = request.user
	favourite_posts = user.favourite.all()
	
	query = request.GET.get('q')
	if query:
	  	 	favourite_posts =favourite_posts.filter(Q(title__icontains=query)|
						   Q(text__icontains=query)|
						   Q(author__icontains=query)
						  
						   )
	paginator = Paginator( favourite_posts,24)
	page = request.GET.get('page')
	favourite_posts = paginator.get_page(page)
	try:
	  	 	 favourite_posts = paginator.page(page)
	except PageNotAnInteger:
	  	 	 favourite_posts = paginator.page(1)
	except EmptyPage:
		favourite_posts = paginator.page(paginator.num_page)
 
	context ={'favourite_posts':favourite_posts}
	return render(request,'booklibrary/userfavourite_book.html',context)



def favourite_book(request,id):
	obj = get_object_or_404(Post,id=id)
	if obj.favourite.filter(id=request.user.id).exists():
		obj.favourite.remove(request.user)
	else:
			obj.favourite.add(request.user)
	return HttpResponseRedirect(obj.get_absolute_url())			



class BookListdemo(ListView):
	 model = Category
	 template_name = 'booklibrary/booklistdemo.html'
	 queryset = Category.objects.all()
	 context_object_name = 'queryset'


#
#@login_required(login_url="/login/")
class Usersview(TemplateView):
	 template_name = 'booklibrary/community.html'
	 def get(self,request):

		 users = User.objects.exclude(id=request.user.id).order_by('?')
		 #friend = Friend.objects.get(current_user=request.user)
		 #friends = Friend.objects.all()
		 #ends = Friend.objects.all()
		 query = request.GET.get('q')
		 if query:
		 	#friends  = friends .filter(username__icontains=query)
		 	users = users .filter(username__icontains=query)
								   
		 args = {'users':users }
		 return render(request,self.template_name,args)



class Friendview(TemplateView):
	 template_name = 'booklibrary/notification.html'
	 def get(self,request):

		
		 
		 friend = Friend.objects.get(current_user=request.user)
		 friends = friend.users.all().order_by('username')
		 #ends = Friend.objects.all()
		 query = request.GET.get('q')
		 if query:
		 	friends  = friends .filter(username__icontains=query)
		 	
								   
		 args = {'friends':friends}
		 return render(request,self.template_name,args)


#class BookDelete(DeleteView):
	#model = Post
	#success_url = reverse_lazy('booklibrary:book_paste_edit')

def signup_view(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			 form.save()
			 

			 return redirect('booklibrary:login')
	else:
		form = RegistrationForm()
		
	return render(request,'booklibrary/signup.html',{'form':form})

def login_view(request):
	if request.method =='POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			#Log user in
			user = form.get_user()
			login(request,user)
			if 'next' in request.POST:
				return redirect(request.POST.get('next'))
			else:	

				return redirect('booklibrary:book_paste_list')



	else:
		form = AuthenticationForm()
	return render(request,'booklibrary/login.html',{'form':form})
	
def logout_view(request):
	if request.method =='POST':
		logout(request)
		return redirect('booklibrary:login')

		
#@login_required(login_url="login/")
@login_required(login_url="/login/")
def profile(request,pk=None):
	if pk:
		user = User.objects.get(pk=pk)
	else:
		user = request.user

	args = {'user':user}
	return render(request,'booklibrary/profile.html',args)


def otherprofile(request,pk):
	
		user = User.objects.get(pk=pk)
		args = {'user':user}
		return render(request,'booklibrary/notificationalert.html',args)	

@login_required(login_url="/login/")
def edit_profile(request):
		if request.method == 'POST':
				
				p_form = EditProfileForm(request.POST, instance=request.user)
				u_form = UserUpdateForm(request.POST,request.FILES,instance=request.user.userprofile)
				

				if p_form.is_valid() and u_form.is_valid()  :
						p_form.save()
						u_form.save()
						
						return redirect('booklibrary:userprofile')
		else:
			
			p_form =  EditProfileForm( instance=request.user)
			u_form =UserUpdateForm(instance=request.user.userprofile)
			context = {'p_form':p_form,'u_form':u_form}
			return render(request,'booklibrary/editprofile.html',context)
'''
def add_comment(request,id):
	if request.method == 'POST':
				
				p_form = CommentForm(request.POST)
				
				if p_form.is_valid()  :
						p_form.save()
						return redirect('booklibrary:bookcomment')
	else:
			
			p_form = CommentForm( )
			
			context = {'p_form':p_form}
			return render(request,'booklibrary/addcomment.html',context)
			

'''

def change_friends(request,operation,pk):
	
	new_friend = User.objects.get(pk=pk)
	if operation == 'add':

			Friend.make_friend(request.user,new_friend)
	elif operation == 'remove':
		Friend.lose_friend(request.user,new_friend)
	return redirect('booklibrary:friendview')	

'''
def userupdateform(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST,request.FILES,instance=request.user)
		if u_form.is_valid():
			u_form.save()
			return redirect('booklibrary:userprofile')
	else:
		u_form = UserUpdateForm(instance=request.user)	
	context = {'u_form':u_form}
	return render(request,'booklibrary/userprofile_form.html',context)
	'''