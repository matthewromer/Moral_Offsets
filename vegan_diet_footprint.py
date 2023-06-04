## SET-UP
import squigglepy as sq


def make_distribution(dist_type, lower, upper, lclip='', rclip=''):
    if dist_type != sq.uniform:
        if lclip != '' and rclip != '': 
            dist = dist_type(lower, upper, lclip, rclip)
        elif lclip != '' and rclip == '':
            dist = dist_type(lower, upper, lclip)
        elif lclip == '' and rclip != '':
            dist = dist_type(lower, upper, rclip)
        else:
            dist = dist_type(lower, upper)
    else:
        dist = dist_type(lower, upper)

    return dist

def make_mixture_distribution(dist_list, weights):
    for dist_info in dist_list:
        dist_type = dist_info['dist_type']
        lower = dist_info['lower']
        upper = dist_info['upper']
        lclip = dist_info['lclip']
        rclip = dist_info['rclip']
        dist_i = make_distribution(dist_type, lower, upper, lclip, rclip)
        dist_list.append(dist_i)
    mixture_dist = sq.mixture(dist_list, weights)
    return mixture_dist

class ProteinSource: 

    def __init__(self, ) -> None:
        pass


## Foods

other_pulses_dict = {
        'Land Use': {'distributions': [{'dist_type': sq.lognorm, 'lower': 4.1, 'upper': 41.9, 'lclip' : 0, 'rclip': ''}], 
                     'weights': [1]},
        'GHGs': {'distributions': [{'dist_type': sq.lognorm, 'lower': 0.9, 'upper': 4, 'lclip': '', 'rclip': ''}],
                 'weights': [1]},
        'Freshwater Use': {'distributions': [{'dist_type': sq.uniform, 'lower': 0, 'upper': 0}, \
                                                  {'dist_type': sq.lognorm, 'lower': 200, 'upper': 2500}], 
                            'weights': [0.5, 0.5]},
        }

peas_dict = {
        'Land Use': {'distributions': [{'dist_type': sq.norm, 'lower': 2.3, 'upper': 20.5, 'lclip' : 0, 'rclip': ''}], 
                     'weights': [1]},
        'GHGs': {'distributions': [{'dist_type': sq.lognorm, 'lower': 0.5, 'upper': 1.9, 'lclip': '', 'rclip': ''}],
                 'weights': [1]},
        'Freshwater Use': {'distributions': [{'dist_type': sq.uniform, 'lower': 0, 'upper': 0}, \
                                                  {'dist_type': sq.lognorm, 'lower': 50, 'upper': 200}, \
                                                  {'dist_type': sq.lognorm, 'lower': 450, 'upper': 3500}], 
                            'weights': [0.5, 0.25, 0.25]},
        }

nuts_dict = {
        'Land Use': {'distributions': [{'dist_type': sq.lognorm, 'lower': 4.2, 'upper': 26.6, 'lclip': '', 'rclip': ''}],
                     'weights': [1]},
        'GHGs': {'distributions': [{'dist_type': -1*sq.lognorm, 'lower': 1, 'upper': 4, 'lclip': '', 'rclip': ''}, \
                                   {'dist_type': sq.uniform, 'lower': -1, 'upper': 0}, \
                                   {'dist_type': sq.lognorm, 'lower': 2, 'upper': 12, 'lclip': '', 'rclip': ''}],
                 'weights': [0.5, 0.2, 0.3]},
        'Freshwater Use': {'distributions': [{'dist_type': sq.uniform, 'lower': 0, 'upper': 0}, \
                                             {'dist_type': sq.lognorm, 'lower': 1500, 'upper': 3500}],
                            'weights': [0.25, 0.75]},                            
        }

groundnuts_dict = {
        'Land Use': {'distributions': [{'dist_type': sq.lognorm, 'lower': 4.2, 'upper': 15.4, 'lclip': '', 'rclip': ''}],
                     'weights': [1]},
        'GHGs': {'distributions': [{'dist_type': sq.norm, 'lower': 1.4, 'upper': 6.2, 'lclip': 0, 'rclip': ''}],
                 'weights': [1]},
        'Freshwater Use': {'distributions': [{'dist_type': sq.lognorm, 'lower': 54, 'upper': 6525}],
                            'weights': [1]},
        }   

soymilk_dict = {
        'Land Use': {'distributions': [{'dist_type': sq.norm, 'lower': 0.3, 'upper': 1.1, 'lclip': 0, 'rclip': ''}],
                     'weights': [1]},
        'GHGs': {'distributions': [{'dist_type': sq.norm, 'lower': 0.5, 'upper': 1.7, 'lclip': 0, 'rclip': ''}],
                 'weights': [1]},
        'Freshwater Use': {'distributions': [{'dist_type': sq.uniform, 'lower': 1, 'upper': 1}, \
                                             {'dist_type': sq.lognorm, 'lower': 10, 'upper': 180}], 
                                'weights': [0.5, 0.5]},
        }

tofu_dict = {
        'Land Use': {'distributions': [{'dist_type': sq.norm, 'lower': 1.6, 'upper': 5.9, 'lclip': 0, 'rclip': ''}],
                     'weights': [1]},
        'GHGs': {'distributions': [{'dist_type': sq.lognorm, 'lower': 1.4, 'upper': 7.3, 'lclip': '', 'rclip': ''}],
                 'weights': [1]},
        'Freshwater Use': {'distributions': [{'dist_type': sq.uniform, 'lower': 6, 'upper': 7}, \
                                             {'dist_type': sq.lognorm, 'lower': 30, 'upper': 1000}],
                            'weights': [0.5, 0.5]},
        }