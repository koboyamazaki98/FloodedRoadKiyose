import logging
from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic import TemplateView

from ac01.forms import Sc0101Form, Sc0102Form, Sc0104Form
from ac01.query import get_photo_nextcode

# 一般会員 - index View
class IndexView(TemplateView):
    template_name: str = "index.html"


# 一般会員 - メニュー View
class Sc0101View(View):
    def get(self, request, *args, **kwargs):
        form = Sc0101Form()
        if request:
            form.function_cd = request.GET.get("function_cd") if request.GET.get("function_cd") else '00'
        return render(request, 'sc0101.html', {'form': form})

    def post(self, request, *args, **kwargs):
        logging.debug("Sc0101View" + " - request:" + str(type(request)))
        print(request)
        print(request.POST)
        form = Sc0101Form(request.POST)
        if request:
            form.function_cd = request.POST.get("function_cd") if request.POST.get("function_cd") else '00'
            logging.debug("Sc0101View.POST" + " - function_cd:" + form.function_cd)

        if form.is_valid():
            if form.function_cd == '02':
                return redirect('ac01:sc0102')
            elif form.function_cd == '04':
                return redirect('ac01:sc0104')
        return render(request, 'sc0101.html', {'form': form})


# 一般会員 - 写真投稿 View
class Sc0102View(View):
    def get(self, request, *args, **kwargs):
        form = Sc0102Form()
        logging.debug("Sc0102View.get" + " - op_time=" + form.op_time)
        if request:
            form.function_cd = request.GET.get("function_cd") if request.GET.get("function_cd") else '99'
        return render(request, 'sc0102.html', {'form': form})

    def post(self, request, *args, **kwargs):
        print(request.POST)
        if request:
            form = Sc0102Form(data=request.POST, files=request.FILES)
            form.function_cd = request.POST.get("function_cd") if request.POST.get("function_cd") else '99'
            logging.debug("Sc0102View.POST" + " - function_cd:" + form.function_cd)
        else:
            form = Sc0102Form()
        if form.function_cd == '02':
            print('is_valid 前')
            if form.is_valid():
                print('is_valid 通過')

                # プライマリーキーの設定
                dtime = form.cleaned_data['dtime']
                #dtime = 201910121800
                logging.debug("Sc0102View.POST" + " - dtime:" + str(dtime))
                yyyymm = dtime // 1000000
                nextcode = get_photo_nextcode(yyyymm)
                logging.debug("Sc0102View.POST" + " - nextid:" + str(nextcode))
                form.cleaned_data['code'] = nextcode

                print("Sc0102View.POST - form.cleaned_data:", form.cleaned_data)
                form.save()
                return redirect('ac01:sc0102')
            else:
                print(form.errors)
        else:
            return redirect('ac01:sc0101')
        return render(request, 'sc0102.html', {'form': form})

# 一般会員 - 写真一覧 View
class Sc0104View(View):
    def get(self, request, *args, **kwargs):
        print(request.GET)
        form = Sc0104Form(request.GET)
        if request:
            form.function_cd = request.GET.get("function_cd") if request.GET.get("function_cd") else '00'
            form.category_cd = request.GET.get("category") if request.GET.get("category") else ''
        logging.debug("Sc0104View.GET" + " - function_cd:" + form.function_cd)
        photos = form.get_photos() if form.is_valid() else []
        return render(request, 'sc0104.html', {'form': form, 'photos': photos})

    def post(self, request, *args, **kwargs):
        form = Sc0104Form(request.POST)
        if request:
            form.function_cd = request.POST.get("function_cd") if request.POST.get("function_cd") else '00'
            logging.debug("Sc0104View.POST" + " - function_cd:" + form.function_cd)
        if form.function_cd == '99':
            return redirect('ac01:sc0101')
        return render(request, 'sc0104.html', {'form': form, 'photos': []})
