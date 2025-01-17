from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django import forms



class UserInfoForm(forms.ModelForm):
	phone = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'SĐT'}), required=False)
	address1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Địa chỉ'}), required=False)
	address2 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Số nhà'}), required=False)
	city = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Thành phố'}), required=False)
	

	class Meta:
		model = Profile
		fields = ('phone', 'address1', 'address2', 'city',)


class ChangePasswordForm(SetPasswordForm):
	class Meta:
		model = User
		fields = ['new_password1', 'new_password2']

	def __init__(self, *args, **kwargs):
		super(ChangePasswordForm, self).__init__(*args, **kwargs)

		self.fields['new_password1'].widget.attrs['class'] = 'form-control'
		self.fields['new_password1'].widget.attrs['placeholder'] = 'Mật khẩu'
		self.fields['new_password1'].label = ''
		self.fields['new_password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['new_password2'].widget.attrs['class'] = 'form-control'
		self.fields['new_password2'].widget.attrs['placeholder'] = 'Nhập lại mật khẩu'
		self.fields['new_password2'].label = ''
		self.fields['new_password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'


class UpdateUserForm(UserChangeForm):
	password = None
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Địa chỉ email'}), required=False)
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Tên người dùng'}), required=False)
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Họ và tên đệm'}), required=False)

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email')

	def __init__(self, *args, **kwargs):
		super(UpdateUserForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'Tên người dùng'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		
class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Địa chỉ email'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Tên người dùng'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Họ và tên đệm'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'Tên người dùng'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Mật khẩu'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Nhập lại mật khẩu'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'