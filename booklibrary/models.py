from django.db import models

# Create your models here.
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings



class Category(models.Model):
	name = models.CharField(max_length=250)
	slug = models.SlugField(unique=True,max_length=250)


	def __str__(self):
		return self.name

	

	def get_absolute_url(self):
		return reverse('booklibrary:post_by_category', args=[self.slug])



	class Meta:
		ordering = ('name',)
		verbose_name = 'category'
		verbose_name_plural = 'categories'    


class Post(models.Model):

	        category = models.ForeignKey(Category, on_delete=models.CASCADE)
	        title = models.CharField(max_length=100)
	        #slug = models.SlugField(unique=True)
	        book_cover = models.ImageField(default='default.png', blank =True)
	        text = models.TextField()
	        upload_book = models.FileField(blank =True)
	        created_on = models.DateTimeField(auto_now_add=True)
	        author = models.CharField(max_length=100)
	        user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default=1)
	        likes = models.ManyToManyField(User,related_name='likes',blank=True)
	        favourite = models.ManyToManyField(User,related_name='favourite',blank=True)


	        # comments = models.TextField()


	        def get_absolute_url(self):
	        	return reverse('booklibrary:book_paste_detail',kwargs={'pk': self.pk})



	        def __str__(self):
	        	return "%s by %s, %s"  %(self.title,self.author,self.created_on)


	        def total_likes(self):
	        		return self.likes.count()	
'''




	        
def save(self, *args, **kwargs):
	if not self.slug:
		self.slug = slugify(self.title)



	super(Post, self).save(*args, **kwargs)

'''



class Comment(models.Model): 

	name = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default=1)
	email = models.EmailField(max_length=75) 
	website = models.URLField(max_length=200, null=True, blank=True) 
	text = models.TextField() 
	post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments') 
	created_on = models.DateTimeField(auto_now_add=True)
	# approved = models.BooleanField(default=False)

	# def approved(self):
	# 	self.approved= True
	# 	self.save()

	
	def __str__(self):
		return "%s said %s for %s"  %(self.name,self.text,self.post)

    
class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	gender = models.CharField(max_length=6,choices=(('Male','Male'),('Female','Female')),blank=True)
	age = models.PositiveIntegerField(blank=True,null=True)
	description = models.CharField(max_length=2000,default='')
	city = models.CharField(max_length=100,default='')
	website = models.URLField(default='')
	image = models.ImageField(upload_to='profile_image',blank=True)
	def __str__(self):
		return self.user.username


	class Meta:
		verbose_name = 'Profile'
		verbose_name_plural = 'Profiles'	








def create_profile(sender,**kwargs):
	if kwargs ['created']:
		user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile,sender=User)



class Friend(models.Model):
	users= models.ManyToManyField(User)
	current_user = models.ForeignKey(User,related_name='owner',null=True,on_delete=models.CASCADE)

	@classmethod
	def make_friend(cls, current_user,new_friend):
		friend, created = cls.objects.get_or_create(
			current_user=current_user
			)
		friend.users.add(new_friend)


	@classmethod
	def lose_friend(cls, current_user,new_friend):
		friend, created = cls.objects.get_or_create(
			current_user=current_user
			)
		friend.users.remove(new_friend)

