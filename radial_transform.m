function radial_transform( path_in, path_out )
%RADIAL_TRANSFORM
%IMAGE AUGMENTATION USING RADIAL TRANSFORM
%   input:
%       original image(224 * 224) and polar coodinate
%   output:
%       new image

img_in = imresize(imread(path_in), [224, 224]);
img_out = uint8(zeros(224, 224, 3));
for i = 1:10
    for j = 1:10
        img_out = img_out * 0;
        u = 22 * (i - 1) + 1;
        v = 22 * (j - 1) + 1;
        for m = 1:224
            for r = 1:224
                theta = 2 * pi * m / 224;
                x = u + round(r * cos(theta));
                y = v + round(r * sin(theta));
        %         disp([x, y]);
                if x >= 1 && x <= 224 && y >= 1 && y <= 224
                    img_out(m, r, :) = img_in(x, y, :);
                end
            end
        end
        path = [path_out(1:end-4) '_radial_' num2str(10*(i-1)+j-1) '.jpg'];
        imwrite(img_out, path);
    end
end

end

