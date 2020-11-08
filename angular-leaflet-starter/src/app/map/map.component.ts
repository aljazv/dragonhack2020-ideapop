import { Component, OnInit } from '@angular/core';
import { icon, latLng, latLngBounds, MapOptions, Marker, rectangle, tileLayer } from 'leaflet';
import { AppService } from "../app.service";

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.scss']
})
export class MapComponent implements OnInit {

  map: any;
  mapOptions: MapOptions;

  constructor(private _service: AppService) { }

  ngOnInit() {
    this.initializeMapOptions();
  }

  onMapReady(map: any) {
    this.map = map;
    this.addSampleMarker(46.0569, 14.5058);
  }

  onMapClick(event) {
    const coordinateLat = event.latlng.lat;
    const coordinateLng = event.latlng.lng;
    const corner1 = latLng(coordinateLat, coordinateLng);
    const corner2 = latLng(coordinateLat + 0.03, coordinateLng + 0.03);
    const bounds = latLngBounds(corner1, corner2);
    rectangle(bounds, {color: '#800000'}).addTo(this.map);
    this.map.fitBounds(bounds);

    this.addSampleMarker((coordinateLat + coordinateLat + 0.03)/2, (coordinateLng + coordinateLng + 0.03)/2)

    const data = {
      leftBottomLat: coordinateLat,
      leftBottomLng: coordinateLng,
      rightTopLat: coordinateLat + 0.03,
      rightTopLng: coordinateLng + 0.03
    }
    this._service.sendCoordinates(data);
  }

  private initializeMapOptions() {
    this.mapOptions = {
      center: latLng(46.0569, 14.5058),
      zoom: 12,
      layers: [
        tileLayer(
          'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
          {
            maxZoom: 18,
            attribution: 'Map data © OpenStreetMap contributors'
          })
      ],
    };
  }

  private addSampleMarker(coordinateX, coordinateY) {
    const marker = new Marker([coordinateX, coordinateY])
      .setIcon(
        icon({
          iconSize: [25, 41],
          iconAnchor: [13, 41],
          iconUrl: 'assets/marker-icon.png'
        }));
    marker.addTo(this.map);
  }
}
