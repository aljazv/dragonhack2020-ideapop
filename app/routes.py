from app import app
import os
import random

import datetime
import numpy as np
import matplotlib.pyplot as plt
from sentinelhub import MimeType, CRS, BBox, SentinelHubRequest, SentinelHubDownloadClient, \
    DataCollection, bbox_to_dimensions, DownloadRequest
from sentinelhub import SHConfig
from bresenham import bresenham

from helper_functions import get_rays, seeable_points_on_ray, plot_image, get_resolution

import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict
from flask import send_from_directory, send_file
from flask import request

app.config["CLIENT_IMAGES"] = "/home/aljaz/dragonhack2020-ideapop/"




@app.route('/ping', methods=['GET'])
def ping():
    return "pong"

@app.route('/coordinates', methods=['POST'])
def add_coordinates():
    filename="picture.png"
    data = request.json
    #print(data)
    """
    leftBottomLat: 46.09728117681059
    leftBottomLng: 14.524612426757812
    rightTopLat: 46.12728117681059
    rightTopLng: 14.554612426757812
    """
    # PLS do not abuse
    CLIENT_ID = 'ec4f50ed-33c6-4e8d-806c-f6ca435c18bd'
    CLIENT_SECRET = '&E}d~KiDvRmIUmZ>fd+h_TF*mg#:g~[<bPI<ix<E'
    config = SHConfig()

    if CLIENT_ID and CLIENT_SECRET:
        config.sh_client_id = CLIENT_ID
        config.sh_client_secret = CLIENT_SECRET

    betsiboka_coords_wgs84 = [data_json["leftBottomLng"],data_json["leftBottomLat"],data_json["rightTopLng"],data_json["rightTopLat"]]
    #betsiboka_coords_wgs84 = [13.430786,45.565987,15.548401,46.464349]
    #filename = #f"hi{str(sum(betsiboka_coords_wgs84))}.png" 

    # GET DEM DATA
    resolution, betsiboka_bbox, betsiboka_size = get_resolution(betsiboka_coords_wgs84)
    dem_data = get_dem_data(betsiboka_bbox, betsiboka_size)

    
    rays = get_rays(center_point, dem_data)

    evalscript_true_color = """
        //VERSION=3

        function setup() {
            return {
                input: [{
                    bands: ["B02", "B03", "B04"]
                }],
                output: {
                    bands: 3
                }
            };
        }

        function evaluatePixel(sample) {
            return [sample.B04, sample.B03, sample.B02];
        }
    """

    request_true_color = SentinelHubRequest(
        evalscript=evalscript_true_color,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L1C,
                time_interval=('2020-04-01', '2020-08-30'),
                mosaicking_order='leastCC'
            )
        ],
        responses=[
            SentinelHubRequest.output_response('default', MimeType.PNG)
        ],
        bbox=betsiboka_bbox,
        size=betsiboka_size,
        config=config
    )

    true_color_imgs = request_true_color.get_data()
    image = true_color_imgs[0]
    print(f'Image type: {image.dtype}')


    figsize = (12,8*n/m)
    fig, ax = plot_image(image, factor=0.017, clip_range=(0,1), figsize=figsize)

    ax.set_ylim(dem_data.shape[1]-1, 0)
    p1 = None
    for ray in rays:
        if random.random() < 0.1:
            see_ray = seeable_points_on_ray(list(ray.keys()), list(ray.values()))
            #print(see_ray)
            for p in see_ray:
                if see_ray[p] == 1:
                    p1 = p
                    #seeable.add((p[0],p[1]))
                    plt.plot(p[0],p[1],'o', color='y', alpha=1, markersize=3)
    plt.plot(p1[0],p1[1],'o', color='y', alpha=1, label="visible area")
    #x_seeable, y_seeable = list(map(lambda x : x[0], seeable)), list(map(lambda x : x[1], seeable))
    #plt.plot(x[:5],y[:5],'o', color='b')
    plt.plot(center_point[0], center_point[1], '*', color='r', label="our location")
    ax.legend()
    #plt.show()
    #seeable_points(z)
    plt.savefig(filename)
    return send_file("../"+filename, as_attachment=True)

@app.route('/fajl', methods=['POST', 'GET'])
def sen_fajl():

    filename = "fig.png"

    return send_file(filename, as_attachment=True)

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_path = app.static_folder + "/../../angular-leaflet-starter/dist/angular-leaflet-starter"
    print(os.path.exists(static_path + '/' + path))
    if path != "" and os.path.exists(static_path + '/' + path):
        return send_from_directory(static_path, path)
    else:
        print(app.static_folder)
        return send_from_directory(static_path, 'index.html')