from django import forms
from .models import Post,Comment,UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm



class PostForm(forms.ModelForm):

	        title = forms.CharField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))
	        '''
	        slug = forms.SlugField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))

	        	'''
	        text =  forms.CharField(widget=forms.Textarea(
	        	attrs={
	        			'class':'form-control',


	        	}))
	        author =  forms.CharField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))
	        class Meta:
	        	model = Post
	        	exclude = ['created_on','user','favourite','likes']

class CommentForm(forms.ModelForm):
	
	text =  forms.CharField(widget=forms.Textarea(
	        	attrs={
	        			'class':'form-control',


	        	}))
	class Meta: 
 		model = Comment 
 		fields = ['text']

class RegistrationForm(UserCreationForm):
	email = forms.EmailField(required=True,widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))

	class Meta:
		model = User
		fields = (
			'username',
			'first_name',
			'last_name',
			'email',
			'password1',
			'password2'
			) 
	def save(self,commit = True):
		user = super(RegistrationForm,self).save(commit = False)
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.email = self.cleaned_data['email']

		if commit:
			user.save()
class EditProfileForm(forms.ModelForm):
	 email = forms.CharField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))
	   
	 first_name = forms.SlugField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))
	        
	 last_name =  forms.CharField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))
	 class Meta:
	 	model = User
	 	fields = [
					'email',
					'first_name',
					'last_name',
					
					'password'
					]
class UserUpdateForm(forms.ModelForm):
	description =  forms.CharField(widget=forms.Textarea(
	        	attrs={
	        			'class':'form-control',


	        	}))
	city =  forms.CharField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))
	age =  forms.CharField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))
	website =  forms.CharField(widget=forms.TextInput(
	        	attrs={
	        			'class':'form-control',


	        	}))
	


	        	

	class Meta:
		model = UserProfile
		fields = [
			'description',
			'gender',
			'age',
			'city',
			'website',
			'image'
	]
				