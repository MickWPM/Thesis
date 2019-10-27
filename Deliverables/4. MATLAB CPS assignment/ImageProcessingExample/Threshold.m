function [output] = Threshold(image, threshold, invert)
% Simple thresholding function implemented as nested loops with conditionals

    if(nargin<3)
        invert = false;
    end

   imgX = size(image,2);
   imgY = size(image,1);
   output = zeros(imgY, imgX);
   
    for x = 1:imgX 
        for y = 1:imgY
            if image(y,x) > threshold
                if (invert)
                    output(y,x) = 0;
                else
                    output(y,x) = 255;
                end
            else
                if (invert)
                    output(y,x) = 255;
                else
                    output(y,x) = 0;
                end
                
            end
        end
    end

end

