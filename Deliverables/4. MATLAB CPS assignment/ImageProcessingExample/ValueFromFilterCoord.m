function [value] = ValueFromFilterCoord(image, filter, x, y)
% Return a single filtered value from an image x,y point with a convolution filter 

    filterX = size(filter,2);
    filterY = size(filter,1);    
    filterXOffset = floor(filterX/2);
    filterYOffset = floor(filterY/2);
    
    value = 0;
    for fX = 1:filterX
        for fY = 1:filterY
            imgX = x - filterXOffset + fX;
            imgY = y - filterYOffset + fY;
            value = value + filter(fY, fX) * GetValueOrZero(image, imgX, imgY);
        end
    end

end

