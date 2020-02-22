from django.shortcuts import render, redirect
from money.forms import PiroMoneyForm


def check_money(request):
    if request.method == 'POST':
        form = PiroMoneyForm(request.POST)
        if form.is_valid():
            checked = form.save(commit=False)

            checked.save()
            if checked.type == 'late':
                checked.user.left_over -= 10000
            else:
                checked.user.left_over -= 20000
            checked.user.save()
            return redirect("intranet:mainscreen")
        else:
            return redirect("intranet:mainscreen")
    else:
        form = PiroMoneyForm()
        return render(request, 'money/check_money.html', {'form': form})
