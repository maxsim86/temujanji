from django import forms

from temujanji.models import SettingTempahan


class TukarInputStyle(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, kwargs)
        # add common css classes to all widgets
        for field in iter(self.fields):
            # get current classes from Meta
            input_type = self.fields[field].widget.input_type
            classes = self.fields[field].widget.attrs.get("class")
            if classes is not None:
                classes += (
                    "form-check-input"
                    if input_type == "checkbox"
                    else "form control flatpickr-input"
                )
            else:
                classes = (
                    "form-check -input"
                    if input_type == "checkbox"
                    else "form contrl flatpickr-input"
                )
                self.fields[field].widget.attrs.update({"class": classes})


class TempahanTarikhForm(TukarInputStyle):
    tarikh = forms.DateField(
        required=True,
    )


class TempahanMasaForm(TukarInputStyle):
    masa = forms.TimeField(widget=forms.HiddenInput())


class TempahanPlangganForm(TukarInputStyle):
    nama_pengguna = forms.CharField(max_length=250)
    email_pengguna = forms.EmailField()
    telefon_pengguna = forms.CharField(required=False, max_length=10)


class TempahanSettingsForm(TukarInputStyle, forms.ModelForm):
    masa_mula = forms.TimeField(widget=forms.TimeInput(format="%H:%M"))
    masa_tamat = forms.TimeField(widget=forms.TimeInput(format="%H:%M"))

    def clean(self):
        if "masa_tamat" in self.cleaned_data and "masa_mula" in self.cleaned_data:
            if self.cleaned_data["masa_tamat"] <= self.cleaned_data["masa_mula"]:
                raise forms.ValidationError(
                    "Masa tamat hendaklah selepas dari masa mula."
                )
            return self.cleaned_data

        class Meta:
            model = SettingTempahan
            fields = "__all__"
            exclude = [
                # TODO : tambah fields ni ke admin dan fix the functions
                "max_tempahan_per_masa",
                "max_tempahan_per_hari",
            ]
