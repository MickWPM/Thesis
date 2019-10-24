function [value] = GetValueOrZero(array2d, x, y)
    value = 0;
    
    maxX = size(array2d,2);
    maxY = size(array2d,1);
    
    if x > 0 & y > 0 & x <= maxX & y <= maxY
        value = array2d(y, x);
    end
    
end

