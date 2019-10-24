function [output] = RunFilter(image,filter)

   filterX = size(filter,2);
   filterY = size(filter,1);
   imgX = size(image,2);
   imgY = size(image,1);
   output = zeros(imgY, imgX);
   im = double(image);
    
    for x = 1:imgX 
        for y = 1:imgY
            output(y,x) = ValueFromFilterCoord(im, filter, x, y);
        end
    end
    maxVal = max(max(output));
    minVal = min(min(output));
    output = output / maxVal * 255;
    output = uint8(output);
end

