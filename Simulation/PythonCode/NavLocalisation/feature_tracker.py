"""
Handle road feature management
Includes generating a feature mask based off an input feature
and testing against this mask
Feature uses meters as scale
"""

#TODO: Add distance scaling based off ipm image total distance
#eg. here the IPM is 20m from top to bottom
def get_feature_masks(feature, mask_resolution, ipm_distance_range=20):
    """
    Get the raw feature masks for the approach. 
    Sets feature at 60% of ipm distance
    """
    pass

def update_feature_masks(distance_from_feature, feature, mask_resolution, ipm_distance_range=20):
    """
    As per get_feature_masks however feature distance is less than the initial tracking distance
    """
    pass

def check_feature(feature_mask, road_surface, probability_threshold=0.7):
    """
    Considers features elementwise
    """
    #return lowestProbability>0.7, individualProbabilities
    pass