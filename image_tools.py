import numpy, random, math
from PIL import Image, ImageDraw


def get_components_of_triangle(slope: float, hypotenuse: float):
    x = hypotenuse / math.sqrt(math.pow(slope, 2) + 1)
    y = x * slope
    return x, y


def slice_offset(image: Image, slope: float = None, offset: int = 10):
    """
    :param image: Image in numpy array form
    :param slope: The slope of the line to slice the image
    :param offset: The amount to push the sub-images perpendicular to the slice
    :return: An image that has been 'cut' along a line and spread apart by the offset
    """
    if slope is None:
        slope = random.random() - .5
        while slope == 0:
            slope = random.random() - .5

    assert (slope != 0)
    print(slope)
    perpendicular_slope = (-1) / slope
    # Slope Formula y = m(x+c) + b
    # c is left offset, b is up offset
    width_offset = image.width / 2
    height_offset = image.height / 2

    width = image.width
    height = image.height
    x_offset, y_offset = get_components_of_triangle(perpendicular_slope, offset)
    y_offset = math.fabs(y_offset)
    left_intersection = (0, int((slope * (0 - width_offset)) + height_offset))
    right_intersection = (width, int((slope * (width - width_offset)) + height_offset))

    # top_left = (0+x_offset/2, 0)
    # top_right = (width+x_offset/2, 0)
    print(image.height)

    top_left = (0, 0)
    top_right = (width, 0)

    bottom_left = (0, height)
    bottom_right = (width, height)

    # top_half_bbox = (top_left,
    #                  top_right,
    #                  (width+x_offset/2, int((slope * (width - width_offset)) + height_offset)),
    #                  (0+x_offset/2, int((slope * (0 - width_offset)) + height_offset)))
    top_half_bbox = (top_left,
                     top_right,
                     (width, int((slope * (width - width_offset)) + height_offset)),
                     (0, int((slope * (0 - width_offset)) + height_offset)))


    bottom_half_bbox = ((0, int((slope * (0 - width_offset)) + height_offset)),
                        (width, int((slope * (width - width_offset)) + height_offset)),
                        bottom_right,
                        bottom_left)



    new_image = Image.new(mode=image.mode, size=(int(width + x_offset), int(height + y_offset)),color=(255,255,255,255))

    top_half = Image.new("L", size=new_image.size)
    top_half_draw = ImageDraw.Draw(top_half)
    top_half_draw.polygon(top_half_bbox, fill=255)
    # top_half_draw.polygon(bottom_half_bbox, fill=255)

    print(top_half_bbox)
    print(bottom_half_bbox)

    bottom_half = Image.new("L", size=new_image.size)
    bottom_half_draw = ImageDraw.Draw(bottom_half)
    bottom_half_draw.polygon(bottom_half_bbox, fill=255)

    # top_half.show()
    # bottom_half.show()
    # image.show()
    print(image.size)
    print(new_image.size)

    temp_image = Image.new(new_image.mode, new_image.size, color=(255,255,255,255))
    temp_image.paste(image)
    image = temp_image
    # image = image.resize((width+1000, height+1000))
    # image.show()

    if perpendicular_slope > 0:
        new_image.paste(image, box=(0, 0), mask=top_half)
        new_image.paste(image, box=(int(x_offset), int(y_offset)), mask=bottom_half)
    elif perpendicular_slope < 0:
        new_image.paste(image, box=(int(x_offset), 0), mask=top_half)
        new_image.paste(image, box=(0, int(y_offset)), mask=bottom_half)
    return new_image


class ToolsImage:
    def __init__(self, image: Image):
        self.image = image

    @classmethod
    def from_image_path(cls, path: str):
        image = Image.open(path)
        return cls(image)

    @classmethod
    def from_pill_image(cls, image: Image):
        return cls(image)

    def show(self):
        self.image.show()

    def slice_offset(self, slope: float = None, offset: int = 10, preview: bool=False):
        self.image = slice_offset(self.image, slope, offset)
        if preview:
            self.image.show()
