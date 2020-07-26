import logging
from datetime import datetime
from django import forms
from ac01.models import *
from ac01.query import has_member_no

dTimeFormatter = "{0:%Y/%m/%d} {0:%H:%M:%S}"

# 時刻プルダウンリスト選択肢
class SelTime:
	pass


# メニュー画面フォーム
class Sc0101Form(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.function_cd = "00"
        self.op_time = dTimeFormatter.format(datetime.now())

    def clean(self):
        #logging.debug("Sc0101Form" + " - clean=" + self.cleaned_data['function_cd'])
        #function_cd = self.cleaned_data['function_cd']
        #if function_cd != "01" and function_cd != "02":
        #    raise forms.ValidationError('メニューを選択して下さい。')
        return self.cleaned_data


# 画像登録フォーム
class Sc0102Form(forms.ModelForm):
    entryTime = forms.DateTimeInput()

    class Meta:
        model = Photo
        fields = ['code', 'dtime', 'chome', 'detail', 'member_no', 'photo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.function_cd = "99"
        self.op_time = dTimeFormatter.format(datetime.now())
        #print(self.op_time)
        self.data_time = self.op_time.replace("/", "").replace(" ", "").replace(":", "")[0:11] + "0"
        self.sel_time_list = list()
        for hh in range(0, 24):
            for mm in range(0, 60, 10):
                sel_time = SelTime()
                sel_time.txt : str = '{:02d}:{:02d}'.format(hh, mm)
                sel_time.val = '{:02d}{:02d}'.format(hh, mm)
                self.sel_time_list.append(sel_time)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        try:
            photo = self.cleaned_data['photo']
            if photo:
                pass
            else:
                self.add_error('photo', '画像が選択されていません。')
        except (KeyError, ValueError):
            self.add_error('photo', '画像が選択されていません。')
        return self.cleaned_data

    def clean_member_no(self):
        member_no = self.cleaned_data['member_no']

        if has_member_no(int(member_no)):
            pass
        else:
            raise forms.ValidationError('会員番号が不適切です。')

        return member_no

    def save(self, commit=False):
        state = super().save(commit)
        state.code = str(self.cleaned_data['code'])
        print("Sc0102Form.save - state:", state)
        state.save()


# 画像一覧フォーム
class Sc0104Form(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.exclude(category_cd=0), required=False)

    def __init__(self, *args, **kwargs):
        print(kwargs)
        super().__init__(*args, **kwargs)
        self.function_cd = "00"
        self.op_time = dTimeFormatter.format(datetime.now())
        self.category_cd = ""
        #print(self.op_time)
        logging.debug("Sc0104Form" + " - op_time=" + self.op_time)

    def clean(self):
        if self.cleaned_data['category'] is None:
            raise forms.ValidationError('')
        print("Sc0104Form.clean - category", self.cleaned_data['category'])
        return self.cleaned_data

    @property
    def filter_params(self):
        result = {}

        value = self.category_cd
        print("Sc0104Form.filter_params - value", value)
        result["category_cd"] = value

        return result

    def get_photos(self):
        photos = Photo.objects.filter(**self.filter_params).order_by('dtime', 'chome')
        return photos
