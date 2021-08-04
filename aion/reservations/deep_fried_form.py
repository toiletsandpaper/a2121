# aion/reservations/deep_fried_forms.py
from crispy_forms.layout import LayoutObject, Layout, ButtonHolder, Submit, HTML, Field
from crispy_forms.utils import TEMPLATE_PACK
from django import forms
from captcha.fields import CaptchaField    

class DeepFriedForm(LayoutObject):
    '''Custom crispy layout object. 
    This object:
     1) Replaces all placeholder text with the label text.
     2) Removes the help text and labels.
     3) Sets the submit button text
     4) Sets the cancel url and text (if available)
     
    Example::
    
        DeepFriedForm(submit_text="Save", cancel_url="/home/", cancel_text="Cancel")
        
    '''
    def __init__(self, *fields, **kwargs):
        # kwargs.pop verifies valid parameters, and specifies a default value
        self.render_buttons = kwargs.pop('render_buttons', True)
        self.submit_text = kwargs.pop('submit_text', 'Submit')
        self.cancel_url = kwargs.pop('cancel_url', None)
        self.cancel_text = kwargs.pop('cancel_text', None)
        self.render_delete_buttons = kwargs.pop('render_delete_buttons', False)
        self.delete_text = kwargs.pop('delete_text', None)
        self.layout_object = Layout()

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK):
        # layout_object = Layout()
        for field_name, field in form.fields.items():
            if(field_name=='sequence'):
                '''Add helper text for sequence field in blocks
                '''
                self.layout_object.append(
                    Field(
                        HTML(
                            '''<small class="helper-text helper-text-block">
                            You may specify a sequence for your block. If left
                            blank, Aion will order blocks in alpha-numeric 
                            order based on the block name.
                            </small>'''
                        )
                    )
                )
            
            if(isinstance(field, forms.DateField)):
                
                self.layout_object.append(
                    Field(
                        field_name, template="reservations/deep_fried/deep_fried_date.html")
                )
                
            elif(isinstance(field, forms.BooleanField)):
                if field_name == 'enabled':
                    self.layout_object.append(
                        Field(
                            field_name, 
                            template="reservations/deep_fried/deep_fried_switch_enable.html"
                        )
                    )
                else:
                    self.layout_object.append(
                        Field(
                            field_name, 
                            template="reservations/deep_fried/deep_fried_switch.html"
                        )
                    )
            elif(isinstance(field, forms.MultipleChoiceField)):
                self.layout_object.append(
                    Field(
                        field_name, 
                        template="reservations/deep_fried/deep_fried_multi_switch.html"
                    )
                )
            else:
                self.layout_object.append(
                    Field(
                        field_name,
                        placeholder=field.label, # Set placeholder to label
                        aria_label=field.label
                    )
                )
            
            field.help_text = None # surpress help_text
        
        if self.render_buttons:
        
            if self.cancel_url is None or self.cancel_text is None:
                self.layout_object.append( ButtonHolder(
                    Submit('submit', self.submit_text, css_class='btn-dark-gray'),
                    css_class="btn-group d-flex"
                ))
            else:
                self.layout_object.append(
                    ButtonHolder(
                        Submit('submit', self.submit_text, css_class='btn-dark-gray'),
                        HTML(f"""<a class="btn btn-secondary" href="{self.cancel_url}">{self.cancel_text}</a>"""),
                        css_class="btn-group d-flex"
                    )
                )
                
        if self.render_delete_buttons:
            # todo: Fix this button so the text isn't always "RESOURCE"
            self.layout_object.append( 
                ButtonHolder(
                    HTML(f'''<button type="submit" value="submit" class="btn btn-primary">
                    <i class="fas fa-exclamation-triangle"></i>&nbsp;{self.delete_text}&nbsp;<i class="fas fa-exclamation-triangle"></i>
                    </button>'''),
                    css_class = "btn-group d-flex"
                )
            )
        
        return self.layout_object.render(form, form_style, context)
        