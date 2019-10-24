function [output] = MedianFilter(image, xSize,ySize)
    
   imgX = size(image,2);
   imgY = size(image,1);
   output = zeros(imgY, imgX);
   
    for x = 1:imgX 
        for y = 1:imgY
            output(y,x) = MeanFromCoord(image, x, y, xSize,ySize);
        end
    end
    
end

