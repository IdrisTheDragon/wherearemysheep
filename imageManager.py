from tifffile import TiffFile, TiffWriter, TiffTag
import cv2
import numpy as np
import tifffile as tif

from finders import Finder
from location import Location


class ImageManager:
    """
    Loads image and finds runs a finder in the image data and allows you to save the results.
    """

    def __init__(self, filepath: str):
        """
            initialses Mammal Finder

            filepath - filepath of the image to process
        """
        self.filetype: str = filepath[len(filepath) - 3:].upper()
        self.tags = None
        self.locations: [Location] = None
        self.intermediaryImage = None
        self.outlined = None
        if self.filetype == 'TIF':
            print('found tif')
            with TiffFile(filepath) as tif:
                # fileInfo(tif)
                self.tags = metadataGeoTags(tif)
                self.image = tif.asarray()
        elif self.filetype == 'PNG' or self.filetype == 'JPG':
            print('found png')
            self.image = cv2.imread(filepath, cv2.IMREAD_UNCHANGED)
        else:
            print('invalid file type:', self.filetype)

    def singleLayerFind(self, method: Finder, layer: int = 0):
        """
        find the the mammel in the Image

        method - the finder to find the mammal
        layer -  the layer or sample of the image to use.
        """
        prepared_image = None
        if len(self.image.shape) > 2:  # atleast 3 dimesions in array e.g 100,100,5
            if self.image.shape[0] > self.image.shape[2]:  # one image array with multi samples e.g 100,100,5
                if self.image.shape[2] > layer:  # check sample that exists
                    prepared_image = self.image[:, :, layer]
                else:
                    print('sample:', layer, ' out of bounds:', self.image.shape[2],
                          'from the following multi sample image', self.image.shape)
                    return
            elif self.image.shape[0] < self.image.shape[2]:  # image with more than one layer e.g 5,100,100
                if self.image.shape[0] > layer:  # check layer exisits
                    prepared_image = self.image[layer]
                else:
                    print('layer:', layer, ' out of bounds:', self.image.shape[0],
                          'from the following multi layer image', self.image.shape)
                    return
            else:
                print('Unrecognised dimesnsions:', self.image.shape)
        elif len(self.image.shape) == 2:  # basic 2 dimesional array
            prepared_image = self.image
        else:
            print('invalid dimensions in image', self.image.shape)
            return

        if prepared_image is None:
            print('something went wrong')

        self.locations, self.intermediaryImage = method.findInImage(prepared_image)
        return self.locations, self.intermediaryImage

    def combineToSingleLayer(self,layers=[1.]):
        prepared_image = None
        if self.image.shape[0] < len(layers) or self.image.shape[2] < len(
                layers):  # check number of layers provided is less than or equal to the number of layers in image
            print("too many layers given")
            return -1
        count = 0.
        for l in layers:
            count = count + l
        if 1. < count < 0.9999:
            print("layers do not sum to one:", layers, "sum:", count)
            return -1
        for c, l in enumerate(layers):
            if self.image.shape[0] > self.image.shape[2]:
                if prepared_image is None:
                    prepared_image = l * self.image[:, :, c]
                else:
                    prepared_image = prepared_image + l * self.image[:, :, c]
            else:
                if prepared_image is None:
                    prepared_image = l * self.image[c]
                else:
                    prepared_image = prepared_image + l * self.image[c]
        return prepared_image

    def combinedSingleLayerFind(self, method: Finder, layers=[1.]):
        prepared_image = None
        if len(self.image.shape) > 2:  # check number of dimensions in image
            prepared_image = self.combineToSingleLayer(layers)
            if prepared_image == -1:
                return
        else:
            prepared_image = self.image

        self.locations, self.intermediaryImage = method.findInImage(prepared_image)
        return self.locations, self.intermediaryImage

    def multiLayerFind(self, method: Finder):
        variance = 10
        if len(self.image.shape) > 2:
            results = []
            for i in range(0, min(self.image.shape[0], self.image.shape[2])):
                if self.image.shape[0] > self.image.shape[2]:
                    prepared_image = self.image[:, :, i]
                else:
                    prepared_image = self.image[i]
                locations, self.intermediaryImage = method.findInImage(
                    prepared_image)  # only store last intermediaryImage
                print(locations)
                for l in locations:
                    found_pair = False
                    for r in results:
                        if r.coords[0] + variance > l.coords[0] > r.coords[0] - variance and r.coords[1] + variance > \
                                l.coords[1] > r.coords[1] - variance:
                            r.detected = r.detected + 1
                            found_pair = True
                            break
                    if not found_pair:
                        results.append(l)

            self.locations = filter(lambda x: x.detected > 1, results)
        else:
            self.locations, self.intermediaryImage = method.findInImage(self.image)

        return self.locations, self.intermediaryImage

    def outline_mammal(self, baseImage: str = 'blank', padding=30):
        """
        based on coordinates provided outline the sheep in the image

        baseImage - one of {'blank','original','rgb'}
        padding - default 30px padding around a mammal when outlined

        returns - numpy array of base image with rectangles highlighting the mammals found mammels.

        """
        if self.locations is None:
            print('no locations yet please run find first')
            return

        if baseImage == 'blank':
            outlined = np.zeros(self.intermediaryImage.shape)
        elif baseImage == 'original':
            outlined = self.image
        elif baseImage == 'rgb':
            if len(self.image.shape) > 2 and self.image.shape[0] > self.image.shape[2] >= 3:
                r = self.image[:, :, 0]
                g = self.image[:, :, 1]
                b = self.image[:, :, 2]
                outlined = cv2.merge((r,g,b))
            else:
                print('probably already rgb')
                return
        else:
            print('not a valid baseImage type:', baseImage, '. one of {\'blank\',\'original\'}')
            return

        if outlined is None:
            print("errror")
            return
        print(outlined.shape)

        for location in self.locations:
            center = location.coords
            size = location.size
            if size is None:
                size = (25, 25)

            outlined = cv2.rectangle(
                outlined,
                (center[1] - round(size[1] / 2) - padding, center[0] - round(size[0] / 2) - padding),
                (center[1] + round(size[1] / 2) + padding, center[0] + round(size[0] / 2) + padding),
                255,
                3
            )
        self.outlined = outlined
        return outlined

    def saveIntermidiary(self, filepath: str):
        """
        saves the intermidiary file to system

        filepath -  the location to save the image to.
        """
        if self.intermediaryImage is None:
            print('No intermidiary image, try run find first')
            return
        self.save(filepath, self.intermediaryImage)

    def saveOutlined(self, filepath: str):
        """
        saves the outlined sheep image file to system

        filepath -  the location to save the image to.
        """

        if self.outlined is None:
            print('No intermidiary image, try run find first')
            return
        self.save(filepath, self.outlined)

    def save(self, filepath: str, image):
        if image is None:
            print('No image to save')
        if filepath is None:
            print('No file specified')

        saveType = filepath[len(filepath) - 3:].upper()
        if saveType == 'TIF':
            with TiffWriter(filepath, bigtiff=True) as tifw:
                if self.tags is None:
                    print('btw there\'s no tif tags being saved to this image')
                    tifw.save(image)
                else:
                    tifw.save(image, extratags=self.tags)
        elif saveType == 'PNG' or saveType == 'JPG':
            cv2.imwrite(filepath, image)
            print('saved', filepath)
        else:
            print('file type not handled:', saveType,
                  '. try one of {\'.tif\',\'.png\',\'.jpg\'} at end of the filepath')

    def extract_sheep(self, folder: str):
        size = 10
        if self.locations is None:
            print("No locations")
            return
        for location in self.locations:
            sheep = self.image[location.coords[0] - int(location.size[0]) - size:location.coords[0] + size,
                    location.coords[1] - int(location.size[1]) - size:location.coords[1] + size
            , :]

            tif.imwrite(folder + "/sheep_" + str(location.coords) + ".tif", sheep, photometric='rgb')


def fileInfo(tif: TiffFile):
    """
    prints out useful tiff info
    """
    print(tif.flags)
    print(tif.geotiff_metadata)
    for page in tif.pages:
        print(page.tags)
        print(page.geotiff_tags)
        print(page.shape)
        print(page.dtype)
        print(page.flags)


def metadataGeoTags(tif: TiffFile):
    """
    extracts the useful geo tags from the tiff file
    """
    geoTag: TiffTag = tif.pages[0].tags.get('GeoKeyDirectoryTag')
    if geoTag is not None:
        g: TiffTag = tif.pages[0].tags.get(34737)
        g2: TiffTag = tif.pages[0].tags.get(34736)
        g3: TiffTag = tif.pages[0].tags.get(33922)
        g4: TiffTag = tif.pages[0].tags.get(33550)

        tags = [(geoTag.code, 'H', geoTag.count, geoTag.value),
                (g.code, 's', g.count, g.value),
                (g2.code, 'd', g2.count, g2.value),
                (g3.code, 'd', g3.count, g3.value),
                (g4.code, 'd', g4.count, g4.value)]
        return tags
    else:
        print('no geo tags in file')
