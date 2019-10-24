originalImage = countryside;
testImage = rgb2gray(originalImage);

%Initial smoothing filter
filter = ones(3,3) / 9;
newImg = RunFilter(testImage, filter);

%Harden edges by subtracting smoothed edges
k = 1.5;
newImg = testImage - k*newImg;
newImg = RunFilter(newImg, filter);

%Remove 'salt and pepper noise' effect using median and thresholds to 
newImg = MedianFilter(newImg, 25, 20);
newImg = NormaliseImage(newImg);
newImg = Threshold(newImg, 0, true);
newImg = MedianFilter(newImg, 20, 20);

%Mask to remove 'far/middle ground'
%Use full width and bottom 30%
newImg = MaskFilter(newImg, 1, size(newImg,2), size(newImg,1)*0.7, size(newImg,1));
filter = ones(5,5) / 25;
mask = newImg / 255;

%Combine developed mask with original image for final masked lane detected
%output


finalImg = uint8(times(double(originalImage),mask));
imshow(finalImg);