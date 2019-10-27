originalImage = farmroad;
testImage = rgb2gray(originalImage);

%Initial smoothing filter
filter = ones(3,3) / 9;
newImg = RunFilter(testImage, filter);

%Harden edges by subtracting smoothed edges
k = 0.8;
newImg = testImage - k*newImg;
newImg = RunFilter(newImg, filter);

%Remove 'salt and pepper noise' effect using median and thresholds
newImg = MedianFilter(newImg, 20, 20);
newImg = RunFilter(newImg, filter);
newImg = Threshold(newImg, 150);

filter = ones(10,10) / 100;
newImg = RunFilter(testImage, filter);
newImg = MedianFilter(newImg, 10, 10);
newImg = Threshold(newImg, 140);

mask = MaskFilter(newImg, 1, size(newImg,2), size(newImg,1)*0.7, size(newImg,1));
mask = mask / 255;

finalImg = uint8(times(double(originalImage),mask));
imshow(finalImg);