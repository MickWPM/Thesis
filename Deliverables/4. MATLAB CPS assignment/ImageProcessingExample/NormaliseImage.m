function [output] = NormaliseImage(image)
%Helper function to normalise an image from 8 bit to floating point between
%0 and 1

    maxVal = max(max(image));
    minVal = min(min(image));
    
    output = 255*(image - minVal)/maxVal;
    
end

