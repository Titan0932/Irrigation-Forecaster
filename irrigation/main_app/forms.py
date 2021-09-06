
from django import forms
from django.forms.widgets import Select
  


class getDetails(forms.Form):
    state=forms.ChoiceField(widget=forms.Select, choices=(('California','California'),('Iowa','Iowa'),('Texas','Texas'),
                                ('Nebraska','Nebraska'),('Illanois','Illanois')), required=True )

    crop=forms.ChoiceField(widget=forms.Select, choices=(('Barley/Oats/Wheat','Barley/Oats/Wheat'),
                                    ('Bean,green','Bean,green'),('Bean,dry','Bean,dry'),('Cabbage','Cabbage'),('Carrot','Carrot'),('Cotton/Flax','Cotton/Flax'),
                                    ('Cucumber/Squash','Cucumber/Squash'),('Eggplant','Eggplant'),('Grain/small','Grain/small'),
                                    ('Lentil','Lentil'),
                                    ('Lettuce','Lettuce'),('Maize,sweet','Maize,sweet'),('Maize,grain','Maize,grain'),('Melon','Melon'),
                                    ('Millet','Millet'),('Onion,green','Onion,green'),('Onion,dry','Onion,dry'),('Peanut/Groundnut','Peanut/Groundnut'),
                                    ('Pea,fresh','Pea,fresh'),('Pepper,fresh','Pepper,fresh'),('Potato','Potato'),('Radish','Radish'), ('Spinach','Spinach') ,
                                    ('Sorghum','Sorghum'),('Soybean','Soybean'),('Sugarbeet','Sugarbeet'),('Sunflower','Sunflower'),('Tobacco','Tobacco'),(('Tomato','Tomato') )    
                                    ), required=True)

    """  Month= forms.DateField(label='Plantation Month:') """

    planted_Month=forms.ChoiceField(widget=forms.Select, choices=(('Jan','January'),('Feb','February'),
                            ('Mar','March'),('Apr','April'), ('May','May'),
                            ('June','June'),('July','July'), ('Aug','August'),
                            ('Sept','September'),('Oct','October'), ('Nov','November'), ('Dec','December')
                            ), required=True)

    green_or_Fresh=forms.ChoiceField(widget=forms.RadioSelect,choices=(('Fresh','Fresh'),('Green','Green')), required=True)

    crop_Sown_or_Transplanted=forms.ChoiceField(widget=forms.RadioSelect,choices=(('Sown','Sown'),('Transplanted','Transplanted')), required=True)

    expected_harvest_days= forms.IntegerField(label='Expected Harvest Days: ',min_value=35, max_value=230, error_messages={'max_value':'INVALID. Refer to the harvest Table','min_value':'INVALID. Refer to the harvest Table'})

