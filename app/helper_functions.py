def plot_image(image, factor=1.0, clip_range = None, figsize=None, **kwargs):
    """
    Utility function for plotting RGB images.
    """
    if figsize:
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)
    else:
        fig, ax = plt.subplots(nrows=1, ncols=1)
    if clip_range is not None:
        ax.imshow(np.clip(image * factor, *clip_range), **kwargs)
        return fig, ax
    else:
        ax.imshow(image * factor, **kwargs)
        return fig, ax
    #ax.set_xticks([])
    #ax.set_yticks([])

def is_left(p1, p2, p3):
    p1, p2, p3 = list(map(np.array, [p1, p2, p3]))
    #print(p1)
    return np.cross(p3 - p1, p2 - p1) <= 0

def seeable_points_on_ray(ray, altitudes):
    start = (0,altitudes[0])
    middle = (1,altitudes[1])
    
    final_ray = {}
    # našo in prvo točko, ki ni naša, vedno vidimo
    final_ray[ray[0]] = 1
    final_ray[ray[1]] = 1
    
    for i in range(2,len(ray)):
        #print(start,middle,(ray[i],i))
        if is_left(start,middle,(i,altitudes[i])):
            middle = (i,altitudes[i])
            final_ray[ray[i]] = 1
        else:
            final_ray[ray[i]] = 0
    
    return final_ray

def get_rays(center_point, data):
    # m vrstic (y), n stolpcev (x)
    m, n = dem_data.shape[1], dem_data.shape[0]
    center_point = (n//2,m//2)
    
    edge_points = list(zip([0 for _ in range(m)], list(range(m)))) + list(zip([n-1 for _ in range(m)], list(range(m)))) + list(zip(list(range(1,n-1)), [0 for _ in range(n-2)])) + list(zip(list(range(1,n-1)), [m-1 for _ in range(n-1)]))

    x,y = list(map(lambda x : x[0], edge_points)), list(map(lambda x : x[1], edge_points))
    #plt.plot(x,y,'o')

    rays = []

    for p in edge_points:
        temp_ray = list(bresenham(center_point[0], center_point[1], p[0], p[1]))
        # dodamo podatek o višini
        ray = OrderedDict()
        for t in temp_ray[:-1]:
            ray[t] = (data[t[0],t[1]])
        rays.append(ray)

    #print(len(rays))
    '''for i in range(0,len(rays),30):
        ray = rays[i].keys()
        x,y = list(map(lambda x : x[0], ray)), list(map(lambda x : x[1], ray))
        plt.plot(x,y,color='y')

    plt.show()'''
    return rays

def get_resolution(betsiboka_coords_wgs84):
    resolution = 10

    betsiboka_bbox = BBox(bbox=betsiboka_coords_wgs84, crs=CRS.WGS84)
    betsiboka_size = bbox_to_dimensions(betsiboka_bbox, resolution=resolution)

    max_pixel = 1000*1000
    while betsiboka_size[0]*betsiboka_size[1] > max_pixel:
        resolution += 10
        betsiboka_bbox = BBox(bbox=betsiboka_coords_wgs84, crs=CRS.WGS84)
        betsiboka_size = bbox_to_dimensions(betsiboka_bbox, resolution=resolution)
    return resolution, betsiboka_bbox, betsiboka_size

def get_dem_data(betsiboka_bbox, betsiboka_size):
    get_dem_data_string = """
    //VERSION=3
    function setup() {
    return {
        input: ["DEM"],

        output:{
        id: "default",
        bands: 1,
        sampleType: SampleType.FLOAT32
        }
    }
    }

    function evaluatePixel(sample) {
    return [sample.DEM]
    }
    """

    dem_request = SentinelHubRequest(
        evalscript=get_dem_data_string,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.DEM,
                time_interval=('2020-06-12', '2020-08-13'),
        )
        ],
        responses=[
            SentinelHubRequest.output_response('default', MimeType.TIFF)
        ],
        bbox=betsiboka_bbox,
        size=betsiboka_size,
        config=config
    )
    return dem_request.get_data()[0].T