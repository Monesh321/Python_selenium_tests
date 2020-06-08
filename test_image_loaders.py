from urllib.parse import urlparse

import pytest

from Tests.test_image_scraper import get_all_images, download


def get_data():
    # Retrieve values from CSV
    urlist = []
    with open("urls.csv") as urlsfile:
        ignore = urlsfile.readline()
        for url in urlsfile.readlines():
            print(url)
            urlist.append(url.strip())
    return urlist


class TestCase():
    def img_downloader(self, url, path):
        # get all images
        imgs = get_all_images(url)
        flag = True
        for img in imgs:
            # for each img, download it
            if download(img, path) == False:
                flag = False
        return flag

    # @pytest.mark.parametrize("number", get_data())
    # def test_foo(self, number):
    #     print(number)

    @pytest.mark.parametrize("url", get_data())
    def test_verify_all_images_loaded_correctly(self, url):
        print(url)
        flag = True
        path = urlparse(url).netloc
        if not self.img_downloader(url=url, path=path):
            flag = False

        if flag == False:
            pytest.fail("FAILED", pytrace=False)
        print("Completed")


if __name__ == '__main__':
    pytest.main()
