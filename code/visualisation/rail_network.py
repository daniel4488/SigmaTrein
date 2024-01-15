import osm2rail as orl

subarea_name = 'IHB Blue Island Yard'
download_dir = r'C:\Users\TWTNi\Documents\Programming\ah\osm'
osm_file = orl.download_osm_data_from_overpass(subarea_names=subarea_name,download_dir = download_dir,ret_download_path=True)
net=orl.get_network_from_file(filename=osm_file[0],POIs=True,check_boundary=True)
orl.show_network(net)
orl.save_network(net,output_folder='./csvfile')

# https://ruaridhw.github.io/london-tube/VisualisingData.html