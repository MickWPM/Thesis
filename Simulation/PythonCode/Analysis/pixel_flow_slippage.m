miny = 120;
maxy = 174;
deltaY = maxy - miny;


estFlow = [23.7645 3.7510 22.9775 32.0686 15.5520 24.9122 25.6496 40.8375 37.0613];
pixelSlip = [10 4 12 18 10 11 21 42 33];
steps = [8 2 4 9 8 16 9 8 12];

predictedFlow = estFlow ./ steps;
correctedFlow = (estFlow + pixelSlip) ./ steps;
frameSlip = pixelSlip ./ steps;

figure;
stem(correctedFlow, frameSlip)
title('Optical flow pixel slippage')
xlabel('Pixel flow per frame (pixels)')
ylabel('Pixel flow error per frame (pixels)')

correctedFlowPct = correctedFlow * 100 / deltaY;
frameSlipPct = pixelSlip ./ steps ./ deltaY * 100;

figure;
stem(correctedFlowPct, frameSlipPct)
title('Optical flow slippage (Related to area of interest size)')
xlabel('Pixel flow per frame (percent of region of interest)')
ylabel('Pixel flow error per frame (percent of region of interest)')
xlim([0 20])