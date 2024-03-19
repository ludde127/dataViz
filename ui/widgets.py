from django import forms


class CheckboxSelectMultipleWOA(forms.CheckboxSelectMultiple):
    """
    CheckboxSelectMultiple with option attributes
    """

    def create_option(
            self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        if isinstance(label, dict):
            opt_attrs = label.copy()
            label = opt_attrs.pop("label")
        else:
            opt_attrs = {}
        option_dict = super(CheckboxSelectMultipleWOA, self).create_option(name, value, label, selected, index,
                                                                           subindex, attrs)
        for key, val in opt_attrs.items():
            option_dict["attrs"][key] = val
        return option_dict
