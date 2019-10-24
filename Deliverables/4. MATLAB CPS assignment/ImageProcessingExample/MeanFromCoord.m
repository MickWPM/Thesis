function [value] = MeanFromCoord(image, x, y, filterXSize,filterYSize)


    filterXOffset = floor(filterXSize/2);
    filterYOffset = floor(filterYSize/2);
    
    values = zeros(1,filterXSize*filterYSize);
    for fX = 1:filterXSize
        for fY = 1:filterYSize
            index = filterYSize*(fX-1) + fY;
            imgX = x - filterXOffset + fX;
            imgY = y - filterYOffset + fY;
            values(index) = GetValueOrZero(image, imgX, imgY);
        end
    end
    value = median(values);
end

