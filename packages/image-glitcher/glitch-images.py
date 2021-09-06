import datetime
import os

from glitch_this import ImageGlitcher


def glitch_scrapes_directory():
    todays_date_string = str(datetime.date.today())
    dirname = os.path.dirname(__file__)

    # path to scraped images
    images_directory = os.path.join(dirname, '../image-scraper/scrapes', todays_date_string)

    # create directory to store today's glitched images
    todays_directory = os.path.join(dirname, 'glitched', todays_date_string)
    os.makedirs(todays_directory, exist_ok=True)
    print(os.listdir(images_directory))

    glitcher = ImageGlitcher()

    for filename in os.listdir(images_directory):
        if filename == '.gitkeep':
            continue

        print(f'glitching {filename}')
        glitched_img = glitcher.glitch_image(
            f"{images_directory}/{filename}",
            2,
            color_offset=True)
        glitched_img.save(f"{todays_directory}/glitched-{filename}")


if __name__ == '__main__':
    glitch_scrapes_directory()
