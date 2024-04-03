from django import forms


class CheckboxSelectMultipleWOA(forms.CheckboxSelectMultiple):
    """
    CheckboxSelectMultiple with option attributes
    """

    def create_option(
            self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        option_dict = super(CheckboxSelectMultipleWOA, self).create_option(name, value, label.label, selected, index,
                                                                           subindex, attrs)
        for key, val in label.kwargs.items():
            option_dict["attrs"][key] = val
        return option_dict
