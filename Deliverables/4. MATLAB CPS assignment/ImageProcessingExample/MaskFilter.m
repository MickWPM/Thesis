function [output] = MaskFilter(image, xMin, xMax, yMin, yMax)
% Helper function to mask out all elements of an image outside a provided
% rectangle bounds.
    output = zeros(size(image));
    output(yMin:yMax, xMin:xMax) = image(yMin:yMax, xMin:xMax);    
end

