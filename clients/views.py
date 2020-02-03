from django.contrib.auth.mixins import LoginRequiredMixin #New
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic import ListView, DetailView


from .forms import CommentForm
from .models import models
from .models import Client
from django.urls import reverse_lazy

class ClientListView(LoginRequiredMixin,ListView):
    model = Client
    template_name = 'client_list.html'

class ClientDetailView(LoginRequiredMixin,DetailView):
    model = Client
    template_name = 'client_detail.html'
    login_url = 'login'

class ClientUpdateView(LoginRequiredMixin,UpdateView):
    model = Client
    fields = ('name', 'notes', 'address', 'city', 'state', 'zipcode', 'email', 'cell_phone', 'acct_number')
    template_name = 'client_edit.html'

class ClientDeleteView(LoginRequiredMixin,DeleteView):
    model = Client
    template_name = 'client_delete.html'
    success_url = reverse_lazy('client_list')

class ClientCreateView(LoginRequiredMixin,CreateView):
    model = Client
    template_name = 'client_new.html'
    fields = ('name', 'notes', 'address', 'city', 'state', 'zipcode', 'email', 'cell_phone', 'acct_number')
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

def comment(request,pk):
    post = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.client = post
            comment.author = request.user
            comment.comment = comment.comment
            comment.save()
            return redirect('client_detail', pk=post.pk)
    else:
        comment_form = CommentForm()
    new_content = {'comment_form': comment_form}

    return render(request, 'comment.html', new_content)