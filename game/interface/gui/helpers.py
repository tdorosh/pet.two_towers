import pygame


# https://www.pygame.org/wiki/TextWrap
# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
def wrap_text(text, color, rect, font, additional_delimiter=None):
    images = []
    rect = pygame.Rect(rect)
    y = rect.top
    line_spacing = -2

    # get the height of the font
    font_height = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + font_height > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            if additional_delimiter and additional_delimiter in text:
                i = text.rfind(additional_delimiter, 0, i) + 1
            else:
                i = text.rfind(" ", 0, i) + 1

        # render the line
        image = font.render(text[:i], True, color)
        images.append(image)

        y += font_height + line_spacing

        # remove the text we just blitted
        text = text[i:]

    return images
