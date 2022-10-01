import os

# TODO delete this

#google clouf credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "####"

from os import listdir
from os.path import isfile, join

from google.cloud import vision
import io


def detect_text(path: str) -> list[str]:
    """
    function that uses google visionApi to extract reaction times from a table in PGE ekstraliga app,
    table is passed as a screenshot from a mobile app

    :param path:path to an image containing table with reaction times
    :return: list of reaction times in each race of a racer
    """

    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    reaction_times = response.text_annotations
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    return [time.description for time in reaction_times][1::]


def parse_all_images(dir_path: str, output_file_name: str) -> None:
    """
    function that applies extract_reaction_times to every image in the directory and saves the result to a output_file
    :param dir_path: path to directory containig all the images
    :param output_file_name: name of file with extracted data
    :return: None
    """
    # get list of all files in the folder
    files = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]

    with open(output_file_name, "a") as output_file:
        for file in files:
            filename = file[:-4]  # skip .png to get age of the rider in days
            reaction_times = detect_text(os.path.join(dir_path, file))

            # each file in the dir_path is named with the value of age of racer in days at the day of a match
            for reaction_time in reaction_times:
                output_file.write(f'{filename},{reaction_time}\n')


if __name__ == '__main__':
    parse_all_images('images', 'data.txt')
