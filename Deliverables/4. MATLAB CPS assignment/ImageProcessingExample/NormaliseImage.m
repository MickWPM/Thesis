function [output] = NormaliseImage(image)
    
    maxVal = max(max(image));
    minVal = min(min(image));
    
    output = 255*(image - minVal)/maxVal;
    
end

