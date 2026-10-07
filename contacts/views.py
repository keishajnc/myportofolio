from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, QueryDict
from django.views.decorators.http import require_http_methods
from .models import Contact

def contact_list(request):
    contacts = Contact.objects.all()
    return render(request, "contacts/index.html", {"contacts": contacts})

def contact_add(request):
    if request.method == "POST":
        Contact.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone")
        )
        contacts = Contact.objects.all()
        # Returning only the newly added row and inserting it using out-of-band swap for feedback as per Latihan 2 & 3
        # Latihan 2: kembalikan hanya baris baru dan sisipkan baris tersebut dengan hx-swap="beforeend"
        # Since contact_add uses hx-swap="beforeend" to `#contact-rows`, we can return just `_contact_row.html` with the new contact.
        # But wait, HTMX will swap the response into `tbody`. If we use hx-swap="beforeend", returning one row is correct.
        
        # Let's get the latest contact (the one we just created)
        contact = Contact.objects.last()
        return render(request, "contacts/_contact_row.html", {"contact": contact, "show_feedback": True})

@require_http_methods(["DELETE"])
def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    contact.delete()
    return HttpResponse("")

def contact_search(request):
    query = request.GET.get("q", "")
    contacts = Contact.objects.filter(name__icontains=query) if query else Contact.objects.all()
    return render(request, "contacts/_contact_rows.html", {"contacts": contacts})

def contact_edit(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    return render(request, "contacts/_contact_edit_row.html", {"contact": contact})

def contact_row(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    return render(request, "contacts/_contact_row.html", {"contact": contact})

@require_http_methods(["PUT"])
def contact_update(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    data = QueryDict(request.body)
    contact.name = data.get("name", contact.name)
    contact.email = data.get("email", contact.email)
    contact.phone = data.get("phone", contact.phone)
    contact.save()
    return render(request, "contacts/_contact_row.html", {"contact": contact})
