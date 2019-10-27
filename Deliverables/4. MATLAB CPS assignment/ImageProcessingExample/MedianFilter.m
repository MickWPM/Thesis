function [output] = MedianFilter(image, xSize,ySize)
%Apply a median filter to an image. Median filter sets the new pixel value
%to the median value over the filter size about the point. This is very
%usefeul for the removal of 'salt and pepper' noise.

   imgX = size(image,2);
   imgY = size(image,1);
   output = zeros(imgY, imgX);
   
    for x = 1:imgX 
        for y = 1:imgY
            output(y,x) = MedianFromCoord(image, x, y, xSize,ySize);
        end
    end
    
end

