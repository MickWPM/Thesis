
function [output] = MaskFilter(image, xMin, xMax, yMin, yMax)
    output = zeros(size(image));
    output(yMin:yMax, xMin:xMax) = image(yMin:yMax, xMin:xMax);    
end

