class foodType:
    #foodType is a class defining a type of food in the american diet 
    #
    # Properties 
    #   - species               - Name of animal species that produces this food
    #   - sufferingYearsPerKg   - Distribution of years of suffering per kg of this food
    #   - sufferingLevel        - Distribution of level of suffering during production (-0.5 to 0.5)
    #   - annaulConsumptionKg   - Distribution of average American annual consumption of this food (kg)
    #   - welfareRange          - Welfare range of this species (relative to humans)
    #   - co2ekgPerkg           - kg of CO2e per kg of this food
    #   - welfareImpact         - Distribution of total welfare impact of this food (human-equivalent WELLBYs)
    #   - welfareImpact         - Distribution of total climate impact of this food (kg CO2e)
    #
    # Methods 
    #   - __init__              - Constructs an instance of this class
    #   - __str__               - Formats a string describing an instance of this class
    #
    
    import numpy as np
    import squigglepy as sq

    def __init__(self, species, sufferingYearsPerKg,sufferingLevel,annaulConsumptionKg,welfareRange,co2ekgPerkg):
        #__init__ constructs an instance of this class
        # Inputs: 
        #  - self (implicit)
        #  - Species (string)
        #  - Years of suffering per kg of this food (squigglepy distribution)
        #  - Level of suffering during production(squigglepy distribution)
        #  - Average American annual consumption of this food in kg (squigglepy distribution)
        #  - Welfare range of this food's species relative to humans (squigglepy distribution)
        #  - kg of CO2e emissions per kg of this food (squigglepy distribution)
        # Outputs: 
        #  - An instance of this class
        #
        
        self.species              = species
        self.sufferingYearsPerKg  = sufferingYearsPerKg
        self.sufferingLevel       = sufferingLevel
        self.annualConsumptionKg  = annaulConsumptionKg
        self.welfareRange         = welfareRange 
        self.co2ekgPerkg          = co2ekgPerkg
        
        #Welfare impact in human-equivalent WELLBYs is the product of annual
        #consumption in kg, years of suffering per kg, suffering level, and
        #welfare range
        self.welfareImpact = self.annualConsumptionKg*self.sufferingYearsPerKg*\
                             self.sufferingLevel*self.welfareRange  
                             
        #Climate impact in kg CO2e is the product of annual consumption in kg 
        #and kg CO2e per kg
        self.climateImpact = self.annualConsumptionKg*self.co2ekgPerkg
        
    def __str__(self):
        #__str__ formats a string describing an instance of this class
        # Inputs: 
        #  - self (implicit)        
        # Outputs: 
        #  - Formatted string describing the object 
        #

        strList = [f"Species:                 {self.species}\n",\
                   f"Suffering Years per kg:  {self.sufferingYearsPerKg}\n",
                   f"Suffering Level:         {self.sufferingLevel}\n",
                   f"Annual Consumption (kg): {self.annualConsumptionKg}\n",
                   f"CO2e per kg (kg):        {self.co2ekgPerkg}\n",                   
                   f"Welfare Range:           {self.welfareRange}"]
        return ''.join(strList) 
    


