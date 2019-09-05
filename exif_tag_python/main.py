# import io
# from PIL import Image
# import piexif
# # import pyexiv2
#
#
# # src_file = '/Users/abhishek/Desktop/logo.jpeg'
# # dest_file = '/Users/abhishek/Desktop/logo2.jpeg'
#
# #
# # def to_deg(value, loc):
# #     if value < 0:
# #         loc_value = loc[0]
# #     elif value > 0:
# #         loc_value = loc[1]
# #     else:
# #         loc_value = ""
# #     abs_value = abs(value)
# #     deg = int(abs_value)
# #     t1 = (abs_value - deg) * 60
# #     min = int(t1)
# #     sec = round((t1 - min) * 60, 5)
# #     return (deg, min, sec, loc_value)
# #
# #
# # def write_data(src_file, data, dest_file=None):
# #     dest_file = dest_file if dest_file else src_file
# #     o = io.BytesIO()
# #     thumb_im = Image.open(src_file)
# #     thumb_im.thumbnail((50, 50), Image.ANTIALIAS)
# #     thumb_im = thumb_im.convert("RGB")
# #     thumb_im.save(o, "jpeg")
# #     thumbnail = o.getvalue()
# #
# #     exiv_image = pyexiv2.Image(file_path)
# #     exiv_image.readMetadata()
# #     exif_keys = exiv_image.exifKeys()
# #
# #     lat_deg = to_deg(lat, ["S", "N"])
# #     lng_deg = to_deg(lng, ["W", "E"])
# #
# #     # convert decimal coordinates into degrees, munutes and seconds
# #     exiv_lat = (pyexiv2.Rational(lat_deg[0] * 60 + lat_deg[1], 60), pyexiv2.Rational(lat_deg[2] * 100, 6000),
# #                 pyexiv2.Rational(0, 1))
# #     exiv_lng = (pyexiv2.Rational(lng_deg[0] * 60 + lng_deg[1], 60), pyexiv2.Rational(lng_deg[2] * 100, 6000),
# #                 pyexiv2.Rational(0, 1))
# #
# #     gps_ifd = {piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),
# #                piexif.GPSIFD.GPSAltitudeRef: 1,
# #                piexif.GPSIFD.GPSDateStamp: u"1999:99:99 99:99:99",
# #                }
# #
# #     exif_dict = {"Exif":gps_ifd}
# #     exif_bytes = piexif.dump(exif_dict)
# #     im = Image.open(dest_file)
# #     im.thumbnail((100, 100), Image.ANTIALIAS)
# #     im = im.convert("RGB")
# #     im.save(dest_file, exif=exif_bytes)
#
#
# def read_data(file_path):
#     exif_dict = piexif.load(file_path)
#     thumbnail = exif_dict.pop("thumbnail")
#     if thumbnail is not None:
#         with open("thumbnail.jpg", "wb+") as f:
#             f.write(thumbnail)
#
#     print(exif_dict)
#     for ifd_name in exif_dict:
#         print("\n{0} IFD:".format(ifd_name))
#         for key in exif_dict[ifd_name]:
#             try:
#                 print(key, exif_dict[ifd_name][key][:10])
#             except:
#                 print(key, exif_dict[ifd_name][key])
#
# #
# # def write_location(file_path, lat, lng):
# #     exiv_image["Exif.GPSInfo.GPSLatitude"] = exiv_lat
# #     exiv_image["Exif.GPSInfo.GPSLatitudeRef"] = lat_deg[3]
# #     exiv_image["Exif.GPSInfo.GPSLongitude"] = exiv_lng
# #     exiv_image["Exif.GPSInfo.GPSLongitudeRef"] = lng_deg[3]
# #     exiv_image["Exif.Image.GPSTag"] = 654
# #     exiv_image["Exif.GPSInfo.GPSMapDatum"] = "WGS-84"
# #     exiv_image["Exif.GPSInfo.GPSVersionID"] = '2 0 0 0'
# #
# #     exiv_image.writeMetadata()
# # # write_data(src_file, {}, dest_file)
# read_data('/Users/abhishek/Downloads/LS-Camera-(16_Oct_18-4_36_10_PM).jpeg')
# # write_location(src_file, lat=32.122332, lng=23.23222)
